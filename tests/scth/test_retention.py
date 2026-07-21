from __future__ import annotations

import pathlib

import pytest

from msb_v2.scth.db import TelemetryStore
from msb_v2.scth.retention import apply_retention


def test_apply_retention_deletes_old_runs(tmp_path: pathlib.Path) -> None:
    store = TelemetryStore(db_path=tmp_path / "scth_telemetry.db")
    store.append_run({"run_id": "old-run", "job_id": "j1", "status": "SUCCESS", "timestamp_start": "2026-01-01T00:00:00+00:00", "duration_ms": 1000})
    store.append_run({"run_id": "new-run", "job_id": "j1", "status": "SUCCESS", "timestamp_start": "2026-07-20T00:00:00+00:00", "duration_ms": 1000})
    result = apply_retention(store, retention_days=30)
    assert result["status"] == "ok"
    assert result["deleted_runs"] == 1
    assert store.get_run("old-run") is None
    assert store.get_run("new-run") is not None
    store.close()
