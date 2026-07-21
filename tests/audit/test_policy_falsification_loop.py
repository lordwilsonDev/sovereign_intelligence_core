from __future__ import annotations

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass
from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.storage import AuditStore
from msb_v2.api import audit as audit_api
from fastapi.testclient import TestClient


def test_falsification_loop_reflected_in_snapshot():
    store = AuditStore()
    engine = AuditEngine(store=store)
    engine.record_policy_falsification(
        policy="tool_timeout_rate",
        detected_rate=0.40,
        sample_count=40,
        blocked=True,
        checksum="loop2",
    )
    app = create_app()
    app.dependency_overrides[audit_api._engine] = lambda: engine
    set_local_bypass(True)
    client = TestClient(app)
    try:
        response = client.get("/audit/policies/falsification")
        assert response.status_code == 200
        body = response.json()
        assert body["count"] >= 1
        assert isinstance(body["records"], list)
        response = client.get("/audit/sovereignty")
        assert response.status_code == 200
        data = response.json()
        assert "falsification_records" in data
        assert isinstance(data["falsification_records"], list)
        assumption_debt = data.get("assumption_debt")
        assert assumption_debt >= 0
    finally:
        app.dependency_overrides.pop(audit_api._engine, None)
        set_local_bypass(None)
