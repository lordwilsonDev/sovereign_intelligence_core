from __future__ import annotations

from typing import Any, Dict

from msb_v2.governor.engine import GovernorEngine
from msb_v2.governor.orchestrator import WorkflowOrchestrator
from msb_v2.governor.policy_engine import PolicyEngine


def test_register_and_list_harnesses() -> None:
    governor = GovernorEngine()
    governor.register_harness("local_ai", "http://127.0.0.1:8767", "/local-ai/models")
    items = governor.harnesses()
    assert [h["name"] for h in items] == ["local_ai"]


def test_health_check_reachable() -> None:
    governor = GovernorEngine()
    governor.register_harness("local_ai", "http://127.0.0.1:8767", "/local-ai/models")
    snapshot = governor.check_all_harnesses()
    assert any(h["name"] == "local_ai" for h in snapshot)


def test_enable_disable_harness() -> None:
    governor = GovernorEngine()
    governor.register_harness("github", "http://example.invalid", "/health")
    assert governor.enable_harness("github")["status"] == "enabled"
    assert governor.disable_harness("github")["status"] == "disabled"
    snap = governor.check_harness("github")
    assert snap["status"] == "disabled"


def test_workflow_orchestrator_end_to_end() -> None:
    governor = GovernorEngine()
    governor.register_harness("local_ai", "http://127.0.0.1:8767", "/local-ai/models")

    class FakeOrchestrator(WorkflowOrchestrator):
        def _http_call(self, harness_name: str, action: str) -> Dict[str, Any]:
            return {"harness": harness_name, "action": action, "status": "success"}

    orchestrator = FakeOrchestrator(governor)
    orchestrator.register_workflow({
        "name": "post_push_pipeline",
        "steps": [
            {"harness": "local_ai", "action": "status"},
            {"harness": "local_ai", "action": "models"},
        ],
    })
    result = orchestrator.execute_workflow("post_push_pipeline")
    assert result["status"] == "success"
    assert len(result.get("results", [])) == 2


def test_policy_engine_block() -> None:
    engine = PolicyEngine()
    violation = engine.evaluate({"event": "force_push", "branch": "main"})
    assert violation["status"] == "violation"
    assert any(v["rule_id"] == "block_force_push_main" for v in violation["violations"])
