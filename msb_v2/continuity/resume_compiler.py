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
    merkle_root_hash: str = ""
    policy_prediction_fts: float = 0.0
    audit_sovereignty_score: float = 0.0

    def compact_text(self) -> str:
        if None in (self.project, self.version):
            values = []
        else:
            values = [
                f"project={self.project}",
                f"version={self.version}",
                f"timestamp={self.timestamp}",
            ]
        values += [
            f"simple_assumption_score={self.simple_assumption_score}",
            f"assumption_debt_count={len(self.assumption_debt_ids)}",
            f"assumption_debt_ids={','.join(self.assumption_debt_ids) or 'none'}",
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
            f"merkle_root_hash={self.merkle_root_hash or 'none'}",
            f"policy_prediction_fts={self.policy_prediction_fts}",
            f"audit_sovereignty_score={self.audit_sovereignty_score}",
        ]
        return "\n".join(values)

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
    def _init_checkpoint_dir(self) -> Path:
        """Create and return the checkpoint directory."""
        path = Path("/private/var/folders/_0/1fjsnc_n747c32_7t8s014c40000gn/T/msb-checkpoints")
        path.mkdir(parents=True, exist_ok=True)
        return path

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
        merkle_root_hash: str = "",
        policy_prediction_fts: float = 0.0,
        audit_sovereignty_score: float = 0.0,
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
        self.merkle_root_hash = merkle_root_hash or ""
        self.policy_prediction_fts = float(policy_prediction_fts)
        self.audit_sovereignty_score = float(audit_sovereignty_score)
        self._checkpoint_dir = self._init_checkpoint_dir()

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
            merkle_root_hash=self.merkle_root_hash,
            policy_prediction_fts=self.policy_prediction_fts,
            audit_sovereignty_score=self.audit_sovereignty_score,
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
            merkle_root_hash=self.merkle_root_hash,
            policy_prediction_fts=self.policy_prediction_fts,
            audit_sovereignty_score=self.audit_sovereignty_score,
        )
        return blob.compact_text()

    @staticmethod
    def token_budget_check(prompt: str, limit: int = 2000) -> bool:
        return len(prompt.split()) <= limit

    @staticmethod
    def live_snapshot(store: AuditStore, engine: AuditEngine) -> dict[str, Any]:
        merkle_root = ""
        try:
            from msb_v2.audit.sovereign.store import SovereignAuditStore
            from msb_v2.audit.sovereign.metrics import compute_audit_sovereignty_score
            sovereign = SovereignAuditStore()
            merkle_root = str(sovereign.merkle.log_path)
            if merkle_root:
                merkle_root = merkle_root
        except Exception:
            pass
        falsification = engine.falsification_snapshot()
        fts = 0.0
        if falsification.get("count", 0) > 0:
            fts = falsification.get("falsified_count", 0) / falsification["count"]
        assumption_debt = engine.assumption_debt_count()
        try:
            from msb_v2.audit.business_metrics import BusinessMetrics
            snap = BusinessMetrics(audit=engine).snapshot()
            imm = snap.get("immutable_record", {})
            if imm.get("root_hash"):
                merkle_root = imm["root_hash"]
        except Exception:
            pass
        return {
            "merkle_root_hash": merkle_root,
            "policy_prediction_fts": fts,
            "audit_sovereignty_score": compute_audit_sovereignty_score(
                merkle_ok=bool(merkle_root),
                fts=fts,
                assumption_debt=assumption_debt,
                veto_active=True,
            ),
        }
