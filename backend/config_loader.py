"""
Config Loader for ScoutIQ
-------------------------
Parses backend/config/ScoutGPT_Data_Links.xlsx and produces structured Python
objects usable by the backend:

- endpoint_mapping: Dict[str, str]           # endpoint_name -> URL
- dataset_mapping: Dict[str, str]            # postgres_table -> domain/purpose
- schema_mapping: Dict[str, Dict[str, dict]] # contract_name -> {input, output}

This module is intentionally self‑contained and tolerant of column variations
in the Excel sheets. It prefers columns named like:
  Endpoints: endpoint_name, url, method
  DatasetMappings: postgres_table, domain, description
  MCPContracts: contract_name, input_schema, output_schema (JSON or "field:type;...")

If the Excel file can't be found, an informative error is raised.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Tuple

import pandas as pd


DEFAULT_EXCEL_RELATIVE = "backend/config/ScoutGPT_Data_Links.xlsx"


@dataclass
class ConfigData:
    endpoints: Dict[str, str]
    dataset_mappings: Dict[str, str]
    mcp_schemas: Dict[str, Dict[str, dict]]


def _resolve_excel_path(explicit_path: str | None = None) -> Path:
    """Resolve an Excel path robustly relative to repository layout.

    Checks several common locations so that running from different CWDs works.
    """
    candidates = []
    if explicit_path:
        p = Path(explicit_path)
        candidates.append(p if p.is_absolute() else Path.cwd() / explicit_path)

    here = Path(__file__).resolve().parent
    candidates.extend([
        here / "config" / "ScoutGPT_Data_Links.xlsx",
        here.parent / "backend" / "config" / "ScoutGPT_Data_Links.xlsx",
        Path.cwd() / DEFAULT_EXCEL_RELATIVE,
    ])

    for c in candidates:
        if c.exists():
            return c
    # Last resort: default
    return Path(DEFAULT_EXCEL_RELATIVE)


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df


def _parse_endpoints(df: pd.DataFrame) -> Dict[str, str]:
    df = _normalize_columns(df)
    # Try to find name/url columns
    name_col = next((c for c in df.columns if c in ("endpoint_name", "name", "endpoint")), None)
    url_col = next((c for c in df.columns if c in ("url", "endpoint_url", "path")), None)
    if not name_col or not url_col:
        return {}
    mapping: Dict[str, str] = {}
    for _, row in df.iterrows():
        name = str(row.get(name_col, "")).strip()
        url = str(row.get(url_col, "")).strip()
        if name and url:
            mapping[name] = url
    return mapping


def _parse_dataset_mappings(df: pd.DataFrame) -> Dict[str, str]:
    df = _normalize_columns(df)
    table_col = next((c for c in df.columns if c in ("postgres_table", "table", "tablename")), None)
    purpose_col = next((c for c in df.columns if c in ("domain", "purpose", "description")), None)
    if not table_col or not purpose_col:
        return {}
    mapping: Dict[str, str] = {}
    for _, row in df.iterrows():
        tbl = str(row.get(table_col, "")).strip()
        purpose = str(row.get(purpose_col, "")).strip()
        if tbl:
            mapping[tbl] = purpose
    return mapping


def _parse_schema_cell(cell: Any) -> dict:
    """Parse an input/output schema cell which may be JSON or "field:type;...".
    Returns a dict mapping field -> type/descriptor.
    """
    if cell is None or (isinstance(cell, float) and pd.isna(cell)):
        return {}
    if isinstance(cell, dict):
        return cell
    text = str(cell).strip()
    if not text:
        return {}
    # Try JSON first
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass
    # Fallback: semicolon-delimited key:type pairs
    schema: Dict[str, str] = {}
    parts = [p for p in text.split(";") if p.strip()]
    for part in parts:
        if ":" in part:
            k, v = part.split(":", 1)
            schema[k.strip()] = v.strip()
        else:
            schema[part.strip()] = "string"
    return schema


def _parse_mcp_contracts(df: pd.DataFrame) -> Dict[str, Dict[str, dict]]:
    df = _normalize_columns(df)
    name_col = next((c for c in df.columns if c in ("contract_name", "name", "contract")), None)
    in_col = next((c for c in df.columns if c in ("input_schema", "input", "request_schema")), None)
    out_col = next((c for c in df.columns if c in ("output_schema", "output", "response_schema")), None)
    if not name_col:
        return {}
    mapping: Dict[str, Dict[str, dict]] = {}
    for _, row in df.iterrows():
        name = str(row.get(name_col, "")).strip()
        if not name:
            continue
        inp = _parse_schema_cell(row.get(in_col)) if in_col else {}
        out = _parse_schema_cell(row.get(out_col)) if out_col else {}
        mapping[name] = {"input": inp, "output": out}
    return mapping


def load_config(excel_path: str | None = None) -> ConfigData:
    """Load the Excel and return structured dictionaries.

    Raises FileNotFoundError if the Excel cannot be found.
    """
    path = _resolve_excel_path(excel_path)
    if not path.exists():
        raise FileNotFoundError(f"Config Excel not found: {path}")

    xls = pd.ExcelFile(path)
    sheet_names = {s.lower(): s for s in xls.sheet_names}

    def get_sheet(name_alias: str) -> pd.DataFrame:
        # Look up case-insensitively
        for key, val in sheet_names.items():
            if key == name_alias.lower():
                return xls.parse(val)
        # Fallback: first sheet
        return xls.parse(xls.sheet_names[0])

    endpoints_df = get_sheet("Endpoints")
    datasets_df = get_sheet("DatasetMappings")
    contracts_df = get_sheet("MCPContracts")

    endpoints = _parse_endpoints(endpoints_df)
    datasets = _parse_dataset_mappings(datasets_df)
    schemas = _parse_mcp_contracts(contracts_df)

    return ConfigData(endpoints=endpoints, dataset_mappings=datasets, mcp_schemas=schemas)


def export_json(out_path: str | Path, config: ConfigData) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "endpoints": config.endpoints,
        "dataset_mappings": config.dataset_mappings,
        "mcp_schemas": config.mcp_schemas,
    }
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path


if __name__ == "__main__":
    try:
        cfg = load_config()
        print("Loaded configuration:\n")
        print("Endpoints:")
        for k, v in cfg.endpoints.items():
            print(f"  - {k}: {v}")
        print("\nDataset Mappings:")
        for k, v in cfg.dataset_mappings.items():
            print(f"  - {k} -> {v}")
        print("\nMCP Contracts:")
        for k, v in cfg.mcp_schemas.items():
            print(f"  - {k}: input={len(v.get('input', {}))} fields, output={len(v.get('output', {}))} fields")

        out = export_json(Path(__file__).resolve().parent / "config_export.json", cfg)
        print(f"\nExported JSON to: {out}")
    except Exception as e:
        print(f"Failed to load config: {e}")


