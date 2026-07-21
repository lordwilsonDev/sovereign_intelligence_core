from __future__ import annotations

from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.storage import AuditStore
from msb_v2.api import audit as audit_api


def test_falsification_loop_endpoint_reflects_live_state():
    store = AuditStore()
    engine = AuditEngine(store=store)
    engine.record_policy_falsification(
        policy="tool_timeout_rate",
        detected_rate=0.40,
        sample_count=40,
        blocked=True,
        checksum="loop-1",
    )
    engine.record_assumption_debt(1)
    engine.record_policy_falsification(
        policy="cache_miss_rate",
        detected_rate=0.10,
        sample_count=40,
        blocked=False,
        checksum="loop-2",
    )

    body = audit_api.audit_policies_falsification(engine=engine)
    assert isinstance(body, dict)
    assert body["count"] >= 2
    assert isinstance(body["records"], list)
    assert engine.assumption_debt_count() == 1

    sovereignty = audit_api.audit_sovereignty(engine=engine)
    assert isinstance(sovereignty, dict)
    assert "falsification" in sovereignty
    assert isinstance(sovereignty["falsification"], dict)
    assert sovereignty["falsification"]["count"] >= 2
    assert sovereignty["assumption_debt"] >= 0
