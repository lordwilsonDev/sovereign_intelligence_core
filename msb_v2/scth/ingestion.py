from __future__ import annotations

from typing import Any, Dict

from msb_v2.scth.db import TelemetryStore


def ingest_event(event: Dict[str, Any], store: TelemetryStore | None = None) -> Dict[str, Any]:
    if store is None:
        store = TelemetryStore()
    validated = dict(event)
    status = str(validated.get("status", "")).upper()
    if status == "FAILED":
        validated["quarantine"] = 1
    return store.append_run(validated)
