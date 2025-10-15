"""
AI ScoutGPT Client
==================

Purpose
-------
Call the ScoutGPT endpoint defined in the Excel configuration and log
interactions in `scoutiq_ai_logs`.

Usage
-----
from backend.ai_scoutgpt import AIScoutGPT
client = AIScoutGPT(db_session)
resp = client.call_scoutgpt(signal_batch=[{...}, {...}], context={"county": "Travis"})

Response shape (on success):
{
  "summary": str,
  "classification": str,  # Buy | Hold | Watch | Error
  "confidence": float,    # 0..1
  "insights": list[str]
}
"""

from __future__ import annotations

import json
import time
from typing import Dict, Any, List, Optional

import requests
from sqlalchemy.orm import Session

from config_loader import load_config
from models import AILogs


DEFAULT_ENDPOINT_NAME = "scoutgpt_analysis"
DEFAULT_CONTRACT_NAME = "property_analysis"


class AIScoutGPT:
    def __init__(self, db_session: Session):
        self.db: Session = db_session
        cfg = load_config()
        self.endpoints = cfg.endpoints or {}
        self.schemas = cfg.mcp_schemas or {}
        # Pick defaults
        self.endpoint_url = self._resolve_endpoint()
        self.contract_name = DEFAULT_CONTRACT_NAME if DEFAULT_CONTRACT_NAME in self.schemas else next(iter(self.schemas.keys()), None)
        self.input_schema = (self.schemas.get(self.contract_name) or {}).get("input", {}) if self.contract_name else {}

    def _resolve_endpoint(self, name: Optional[str] = None) -> str:
        if name and name in self.endpoints:
            return self.endpoints[name]
        if DEFAULT_ENDPOINT_NAME in self.endpoints:
            return self.endpoints[DEFAULT_ENDPOINT_NAME]
        # Fallback to the first endpoint in mapping
        if self.endpoints:
            return next(iter(self.endpoints.values()))
        # Final fallback to localhost (dev)
        return "http://localhost:8001/api/analyze"

    # ----------------------------- Helpers -----------------------------
    def _filter_signal(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """Filter/shape one signal item according to MCP input schema.
        If no schema available, pass through most common fields.
        """
        if not self.input_schema:
            allow = {
                'property_id', 'attom_id', 'address', 'property_address_full',
                'primary_valuation', 'valuation_band', 'ownership_type',
                'loan_maturity', 'flood_risk', 'tax_delinquent', 'property_latitude', 'property_longitude'
            }
            return {k: v for k, v in signal.items() if k in allow}

        # Map signal keys that match schema keys
        shaped: Dict[str, Any] = {}
        for field in self.input_schema.keys():
            if field in signal:
                shaped[field] = signal[field]
            elif field == 'property_id' and 'attom_id' in signal:
                shaped['property_id'] = signal['attom_id']
            elif field == 'address' and 'property_address_full' in signal:
                shaped['address'] = signal['property_address_full']
        return shaped

    def _log(self, inp: Dict[str, Any], out: Dict[str, Any], endpoint_used: str, start_ms: float):
        duration_ms = int((time.time() - start_ms) * 1000)
        try:
            ai_log = AILogs(
                property_id=(inp.get('signals') or [{}])[0].get('property_id', ''),
                input_payload=inp,
                output_response=out,
                classification=out.get('classification', 'Unknown'),
                confidence=out.get('confidence', 0.0),
                endpoint_used=endpoint_used,
                processing_time_ms=duration_ms,
            )
            self.db.add(ai_log)
            self.db.commit()
        except Exception:
            self.db.rollback()

    # ---------------------------- Main API ----------------------------
    def call_scoutgpt(
        self,
        signal_batch: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
        endpoint_name: Optional[str] = None,
        contract_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """POST a batch of signals to the configured ScoutGPT endpoint.

        Payload example:
        {
          "context": {"county": "Travis"},
          "signals": [ {...}, {...} ]
        }
        """
        url = self._resolve_endpoint(endpoint_name)
        schema = self.schemas.get(contract_name or self.contract_name or "", {})
        input_schema = schema.get("input", {})

        # Shape signals
        signals = [self._filter_signal(s) for s in (signal_batch or [])]
        payload = {
            "context": context or {},
            "signals": signals
        }

        start = time.time()

        try:
            resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
            if resp.status_code == 200:
                data = resp.json() if resp.content else {}
                # Normalize expected keys
                result = {
                    "summary": data.get("summary", ""),
                    "classification": data.get("classification", data.get("status", "Unknown")),
                    "confidence": float(data.get("confidence", 0.0) or 0.0),
                    "insights": data.get("insights", []) or [],
                }
                self._log(payload, result, url, start)
                return result
            else:
                error = {
                    "summary": f"ScoutGPT HTTP {resp.status_code}",
                    "classification": "Error",
                    "confidence": 0.0,
                    "insights": [resp.text[:200] if resp.text else "No content"],
                }
                self._log(payload, error, url, start)
                return error
        except requests.RequestException as e:
            error = {
                "summary": f"Network error: {e}",
                "classification": "Error",
                "confidence": 0.0,
                "insights": ["Network connection failed"],
            }
            self._log(payload, error, url, start)
            return error


