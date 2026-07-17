from __future__ import annotations

from typing import Any, Dict

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_agent_run_response_contains_contract_fields() -> None:
    client = TestClient(create_app())
    response = client.post("/agent/run", json={
        "run_id": "contract-1",
        "tasks": [
            {
                "task_id": "t1",
                "name": "echo",
                "callable": "msb_v2.agent.runtime:_agent_echo",
                "payload": {"payload": {"key": "value"}},
            }
        ],
    })
    assert response.status_code == 200
    body = response.json()
    assert body["run_id"] == "contract-1"
    assert "contract" in body
    assert "citation" in body["contract"]
    assert "version" in body["contract"]


def test_agent_run_bad_callable_still_reports_error_with_contract_metadata() -> None:
    client = TestClient(create_app())
    response = client.post("/agent/run", json={
        "run_id": "contract-2",
        "tasks": [
            {
                "task_id": "t2",
                "name": "noop",
                "callable": "not.a.real.callable",
                "payload": {},
            }
        ],
    })
    assert response.status_code == 200
    body = response.json()
    assert body["tasks"][0]["status"] == "failed"
    assert body["tasks"][0]["error"] is not None
    assert "contract" in body
    assert body["contract"]["citation"] is not None


def test_prompt_contract_render_contains_expected_sections() -> None:
    from msb_v2.agent.prompt_contract import build_hermes_phase5_contract
    rendered = build_hermes_phase5_contract().render()
    assert "<tool_calling>" in rendered
    assert "<memory_rules>" in rendered
    assert "<output_rules>" in rendered
    assert "PYTHONPATH=/Users/lordwilson/msb-v2" in rendered
