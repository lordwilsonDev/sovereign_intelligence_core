from __future__ import annotations

from msb_v2.sn.engine import NotificationEngine
from msb_v2.sn.models import AckRequest, NotificationRequest, Priority
from msb_v2.sn.policy_engine import PolicyEngine


def test_notify_console_channel() -> None:
    engine = NotificationEngine(policy=PolicyEngine(rate_limit_per_minute=100))
    request = NotificationRequest(source="star", template="job_failed", priority=Priority.medium, template_data={"job_name": "Build", "error": "timeout"})
    record = engine.notify(request)
    assert record.status == "sent"
    assert record.channel == "console"
    assert "Build" in (record.rendered or "")


def test_policy_blocks_medium_after_rate_limit() -> None:
    engine = NotificationEngine(policy=PolicyEngine(rate_limit_per_minute=1))
    request = NotificationRequest(source="star", template="job_failed", priority=Priority.medium, template_data={"job_name": "Build", "error": "timeout"})
    engine.notify(request)
    record = engine.notify(request)
    assert record.status == "blocked"


def test_ack_flow() -> None:
    engine = NotificationEngine(policy=PolicyEngine(rate_limit_per_minute=100))
    request = NotificationRequest(source="star", template="job_failed", priority=Priority.medium, template_data={"job_name": "Build", "error": "timeout"}, require_ack=True)
    record = engine.notify(request)
    assert record.status == "awaiting_ack"
    ack = engine.ack(AckRequest(ack_id=record.id, response="yes"))
    assert ack is not None
    assert ack["response"] == "yes"
