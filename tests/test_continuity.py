from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.continuity.resume_loader import ResumePromptLoader
from msb_v2.continuity.resume_compiler import ResumePromptCompiler


def test_compiler_emits_magic_header() -> None:
    compiler = ResumePromptCompiler(
        project="MSB v2",
        version="v2",
        active_task="retarget Grafana",
        topic="observability",
        last_turn_summary="metrics aligned",
    )
    prompt = compiler.compile(recent_tool_calls=["curl /metrics"])
    assert prompt.startswith("### MSB_SESSION_CONTINUITY_V1 ###")
    assert ResumePromptCompiler.token_budget_check(prompt, limit=2000)
    assert "active_task=retarget Grafana" in prompt


def test_resume_loader_parses_state() -> None:
    text = "\n".join(
        [
            "### MSB_SESSION_CONTINUITY_V1 ###",
            "project=MSB v2",
            "version=v2",
            "active_task=write docs",
            "",
            "You are resuming an MSB session.",
        ]
    )
    assert ResumePromptLoader.is_resume_prompt(text)
    state = ResumePromptLoader.load(text)
    assert state["project"] == "MSB v2"
    assert state["version"] == "v2"
    assert state["active_task"] == "write docs"


def test_resume_loader_rejects_non_resume() -> None:
    assert not ResumePromptLoader.is_resume_prompt("hello")
    assert ResumePromptLoader.load("hello") == {}


def test_resume_header_returns_prompt() -> None:
    client = TestClient(create_app())
    response = client.get(
        "/continuity/resume-prompt",
        params={
            "active_task": "build contract coverage",
            "topic": "verification",
            "last_turn_summary": "added tests",
            "simple_assumption_score": 0.9,
        },
        headers={"X-OpenAI-Consumer-Org-Unit-Id": "test"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "prompt" in body
    assert body["prompt"].startswith("### MSB_SESSION_CONTINUITY_V1 ###")
    state = ResumePromptLoader.load(body["prompt"])
    assert state["project"] == "MSB v2"
    assert state["version"] == "v2"
    assert state["active_task"] == "build contract coverage"
