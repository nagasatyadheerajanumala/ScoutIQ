"""
Signal Processor
================

Compute derived property signals using multi-table inputs (TaxAssessor,
Recorder, AVM). Designed to be robust to heterogeneous column names coming
from CSV imports or ORM-to-DataFrame extractions.

Inputs
------
- df (pandas.DataFrame): Rows that may include columns from TaxAssessor,
  Recorder, and AVM joins.
- dataset_mapping (dict): Mapping from config that may hint which datasets
  are available; not strictly required but accepted for future routing.

Outputs
-------
Returns a pandas.DataFrame with original columns plus derived signals:
- primary_valuation (float)
- valuation_band (Low/Mid/High)
- ownership_type (Individual/LLC)
- loan_maturity (datetime or None)
- flood_risk (Low/Medium/High/Unknown)

Valuation bands (requested thresholds):
- Low      < 250,000
- Mid      250,000–750,000
- High     > 750,000
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Dict, Any

import numpy as np
import pandas as pd


CORP_KEYWORDS = ("LLC", "L.L.C", "INC", "CORP", "LP", "LLP", "CO.", "COMPANY", "ENTERPRISES", "HOLDINGS")


def _coalesce_numeric(row: pd.Series, candidates: list[str]) -> float:
    for c in candidates:
        if c in row and pd.notna(row[c]):
            try:
                return float(str(row[c]).replace(",", "").strip())
            except Exception:
                continue
    return 0.0


def _primary_valuation(row: pd.Series) -> float:
    # Common valuation fields across AVM/TaxAssessor
    return _coalesce_numeric(
        row,
        [
            "estimated_value",
            "EstimatedValue",
            "TaxMarketValueTotal",
            "tax_market_value_total",
            "valuation",
        ],
    )


def _valuation_band(val: float) -> str:
    if val <= 0:
        return "Unknown"
    if val < 250_000:
        return "Low"
    if val <= 750_000:
        return "Mid"
    return "High"


def _ownership_type_from_names(row: pd.Series) -> str:
    owner_cols = [
        "party_owner1_name_full",
        "party_owner2_name_full",
        "OwnerName",
        "OwnerName1",
    ]
    for col in owner_cols:
        if col in row and pd.notna(row[col]):
            name = str(row[col]).upper()
            if any(k in name for k in CORP_KEYWORDS):
                return "LLC"
    return "Individual"


def _parse_date(value: Any) -> datetime | None:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    s = str(value).strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    # Try pandas parser
    try:
        dt = pd.to_datetime(value, errors="coerce")
        return None if pd.isna(dt) else dt.to_pydatetime()
    except Exception:
        return None


def _loan_maturity(row: pd.Series) -> datetime | None:
    """Compute loan maturity from available recorder/loan fields if present.

    Attempts, in order:
      1) direct maturity date field e.g. Mortgage1TermDate
      2) Instrument/loan date + term years
    """
    # 1) Direct maturity field
    for col in ("Mortgage1TermDate", "mortgage1_term_date", "loan_maturity"):
        if col in row and pd.notna(row[col]):
            return _parse_date(row[col])

    # 2) Start date + term years
    start = None
    for c in ("InstrumentDate", "instrument_date", "loan_date", "RecordingDate", "recording_date"):
        if c in row and pd.notna(row[c]):
            start = _parse_date(row[c])
            if start:
                break

    term_years = None
    for c in ("Mortgage1Term", "mortgage1_term", "loan_term_years"):
        if c in row and pd.notna(row[c]):
            try:
                term_years = float(str(row[c]).strip())
                break
            except Exception:
                continue

    if start and term_years and term_years > 0:
        return start + timedelta(days=int(term_years * 365))
    return None


def _flood_risk(row: pd.Series) -> str:
    """Assess flood risk from available columns.

    Heuristics: if a flood zone/ FEMA code present, map to Low/Medium/High; else Unknown.
    """
    candidates = [
        "flood_zone",
        "FloodZone",
        "fema_zone",
        "FEMAZone",
        "fema_floodplain",
    ]
    zone_val = None
    for c in candidates:
        if c in row and pd.notna(row[c]):
            zone_val = str(row[c]).upper()
            break
    if not zone_val:
        return "Unknown"

    # Simple mapping by FEMA-like codes
    if any(k in zone_val for k in ("X", "MINIMAL")):
        return "Low"
    if any(k in zone_val for k in ("AE", "A", "0.2%", "500")):
        return "Medium"
    if any(k in zone_val for k in ("FLOODWAY", "VE", "HIGH")):
        return "High"
    return "Unknown"


def _property_age(row: pd.Series) -> int | None:
    """Calculate property age from year built."""
    year_cols = ["YearBuilt", "year_built", "YEAR_BUILT", "built_year"]
    for col in year_cols:
        if col in row and pd.notna(row[col]):
            try:
                year_val = int(str(row[col]).strip())
                current_year = datetime.now().year
                if 1800 < year_val <= current_year:
                    return current_year - year_val
            except (ValueError, TypeError):
                continue
    return None


def _classification_hint(row: pd.Series) -> str:
    """Provide a simple Buy/Hold/Watch classification based on basic rules."""
    val = row.get('primary_valuation', 0)
    age = row.get('property_age')
    ownership = row.get('ownership_type', 'Unknown')
    
    # Simple scoring
    score = 50
    if val > 0:
        if val < 250000:
            score += 15
        elif val > 750000:
            score -= 10
        else:
            score += 5
    
    if age is not None:
        if 5 <= age <= 20:
            score += 20
        elif age < 5:
            score += 10
        elif age > 40:
            score -= 15
    
    if ownership in ['LLC', 'Corporation']:
        score += 10
    
    if score >= 70:
        return 'Buy'
    elif score >= 50:
        return 'Hold'
    else:
        return 'Watch'


def compute_signals(df: pd.DataFrame, dataset_mapping: Dict[str, str] | None = None) -> pd.DataFrame:
    """Return a copy of df with derived signals added.

    Parameters
    ----------
    df : DataFrame
        Rows containing columns from TaxAssessor/Recorder/AVM joins.
    dataset_mapping : Dict[str, str]
        Optional mapping from config; currently unused but accepted for future logic.
    """
    if df is None or df.empty:
        return df if df is not None else pd.DataFrame()

    out = df.copy()

    # Primary valuation
    out["primary_valuation"] = out.apply(_primary_valuation, axis=1)
    out["valuation_band"] = out["primary_valuation"].apply(_valuation_band)

    # Ownership type
    out["ownership_type"] = out.apply(_ownership_type_from_names, axis=1)

    # Loan maturity
    out["loan_maturity"] = out.apply(_loan_maturity, axis=1)

    # Flood risk
    out["flood_risk"] = out.apply(_flood_risk, axis=1)
    
    # Property age
    out["property_age"] = out.apply(_property_age, axis=1)
    
    # Classification hint (Buy/Hold/Watch)
    out["classification_hint"] = out.apply(_classification_hint, axis=1)

    return out


