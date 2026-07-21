from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from msb_v2.scth.db import TelemetryStore


def apply_retention(store: TelemetryStore | None = None, retention_days: int = 90) -> Dict[str, Any]:
    if store is None:
        store = TelemetryStore()
    try:
        threshold = datetime.now(timezone.utc) - timedelta(days=retention_days)
    except Exception:
        return {"status": "error", "detail": "invalid retention_days"}
    threshold_str = threshold.isoformat()
    try:
        deleted = store.delete_runs_before(threshold_str)
        return {"status": "ok", "deleted_runs": deleted, "before": threshold_str}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)[:120]}
