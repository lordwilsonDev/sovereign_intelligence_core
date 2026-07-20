from __future__ import annotations

from msb_v2.continuity.resume_compiler import ResumePromptCompiler
from msb_v2.continuity.resume_loader import ResumePromptLoader


def test_compiler_emits_magic_header_and_budget() -> None:
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
    assert state["active_task"] == "write docs"


def test_resume_loader_rejects_non_resume() -> None:
    assert not ResumePromptLoader.is_resume_prompt("hello")
    assert ResumePromptLoader.load("hello") == {}
