from __future__ import annotations

from msb_v2.scth.ingestion import ingest_event
from msb_v2.sn.engine import NotificationEngine
from msb_v2.sn.models import NotificationRequest, Priority
from msb_v2.sn.policy_engine import PolicyEngine


def test_star_failure_triggers_scth_and_snh() -> None:
    store = ingest_event({"run_id": "run-1", "job_id": "build", "status": "FAILED", "duration_ms": 1000})
    assert store["ingestion_hash"]
    engine = NotificationEngine(policy=PolicyEngine(rate_limit_per_minute=100))
    request = NotificationRequest(
        source="star",
        priority=Priority.high,
        template="job_failed",
        template_data={"job_name": "build", "error": "timeout"},
        channels=["console"],
        require_ack=False,
        expires_in_seconds=3600,
    )
    record = engine.notify(request)
    assert record.status == "sent"
    assert "timeout" in (record.rendered or "")
