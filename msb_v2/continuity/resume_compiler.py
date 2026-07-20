from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


MAGIC_HEADER = "### MSB_SESSION_CONTINUITY_V1 ###"


@dataclass(frozen=True)
class ResumeBlob:
    project: str = "MSB v2"
    version: str = "v2"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    topic: str = ""
    last_turn_summary: str = ""
    active_task: str = ""
    simple_assumption_score: float = 0.0
    assumption_debt_ids: list[str] = field(default_factory=list)
    recent_decisions: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    reliable_findings: list[str] = field(default_factory=list)
    code_references: list[str] = field(default_factory=list)
    pending_actions: list[str] = field(default_factory=list)
    recent_tool_calls: list[str] = field(default_factory=list)
    active_harness: str = ""
    memory_pointer: str = ""

    def compact_text(self) -> str:
        return "\n".join(
            [
                f"project={self.project} version={self.version} timestamp={self.timestamp}",
                f"simple_assumption_score={self.simple_assumption_score} assumption_debt={len(self.assumption_debt_ids)}",
                f"active_task={self.active_task or 'none'}",
                f"topic={self.topic or 'none'}",
                f"last_turn_summary={self.last_turn_summary}",
                f"recent_decisions={';'.join(self.recent_decisions) or 'none'}",
                f"open_questions={';'.join(self.open_questions) or 'none'}",
                f"reliable_findings={';'.join(self.reliable_findings) or 'none'}",
                f"code_references={';'.join(self.code_references) or 'none'}",
                f"pending_actions={';'.join(self.pending_actions) or 'none'}",
                f"recent_tool_calls={';'.join(self.recent_tool_calls) or 'none'}",
                f"memory_pointer={self.memory_pointer or 'none'}",
                f"active_harness={self.active_harness or 'none'}",
            ]
        )

    def to_prompt(self) -> str:
        return "\n".join(
            [
                MAGIC_HEADER,
                self.compact_text(),
                "",
                "You are resuming an MSB session.",
                "Use the state above. Do not restart.",
                "Continue reasoning with the same assumptions, objectives, and stance.",
            ]
        )

    def to_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False, indent=None, default=str)


class ResumePromptCompiler:
    def __init__(
        self,
        project: str = "",
        version: str = "",
        active_task: str = "",
        topic: str = "",
        last_turn_summary: str = "",
        simple_assumption_score: float = 0.0,
        assumption_debt_ids: Optional[list[str]] = None,
        recent_decisions: Optional[list[str]] = None,
        open_questions: Optional[list[str]] = None,
        reliable_findings: Optional[list[str]] = None,
        code_references: Optional[list[str]] = None,
        pending_actions: Optional[list[str]] = None,
        recent_tool_calls: Optional[list[str]] = None,
        active_harness: str = "",
        memory_pointer: str = "",
    ) -> None:
        self.project = project or "MSB v2"
        self.version = version or "v2"
        self.active_task = active_task or ""
        self.topic = topic or ""
        self.last_turn_summary = last_turn_summary or ""
        self.simple_assumption_score = float(simple_assumption_score)
        self.assumption_debt_ids = list(assumption_debt_ids or [])
        self.recent_decisions = list(recent_decisions or [])
        self.open_questions = list(open_questions or [])
        self.reliable_findings = list(reliable_findings or [])
        self.code_references = list(code_references or [])
        self.pending_actions = list(pending_actions or [])
        self.recent_tool_calls = list(recent_tool_calls or [])
        self.active_harness = active_harness or ""
        self.memory_pointer = memory_pointer or ""
        self._checkpoint_dir = Path("/private/var/folders/_0/1fjsnc_n747c32_7t8s014c40000gn/T/msb-checkpoints")
        self._checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def compile(self, recent_tool_calls: Optional[list[str]] = None) -> str:
        if recent_tool_calls is not None:
            self.recent_tool_calls = list(recent_tool_calls)[-8:]
        blob = ResumeBlob(
            project=self.project,
            version=self.version,
            topic=self.topic,
            last_turn_summary=self.last_turn_summary,
            active_task=self.active_task,
            simple_assumption_score=self.simple_assumption_score,
            assumption_debt_ids=self.assumption_debt_ids,
            recent_decisions=self.recent_decisions,
            open_questions=self.open_questions,
            reliable_findings=self.reliable_findings,
            code_references=self.code_references,
            pending_actions=self.pending_actions,
            recent_tool_calls=self.recent_tool_calls,
            active_harness=self.active_harness,
            memory_pointer=self.memory_pointer,
        )
        prompt = blob.to_prompt()
        try:
            path = self._checkpoint_dir / "latest_resume.txt"
            path.write_text(prompt, encoding="utf-8")
        except Exception:
            pass
        return prompt

    def save(self, path: str) -> None:
        Path(path).write_text(self.compile(), encoding="utf-8")

    def compact_text(self) -> str:
        blob = ResumeBlob(
            project=self.project,
            version=self.version,
            topic=self.topic,
            last_turn_summary=self.last_turn_summary,
            active_task=self.active_task,
            simple_assumption_score=self.simple_assumption_score,
            assumption_debt_ids=self.assumption_debt_ids,
            recent_decisions=self.recent_decisions,
            open_questions=self.open_questions,
            reliable_findings=self.reliable_findings,
            code_references=self.code_references,
            pending_actions=self.pending_actions,
            recent_tool_calls=self.recent_tool_calls,
            active_harness=self.active_harness,
            memory_pointer=self.memory_pointer,
        )
        return blob.compact_text()

    @staticmethod
    def token_budget_check(prompt: str, limit: int = 2000) -> bool:
        return len(prompt.split()) <= limit
