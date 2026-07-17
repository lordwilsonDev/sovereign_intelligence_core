from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from msb_v2.engine.rcoh import RCOHState, Phase, Alternative, Assumption, Evidence, HorizonTask, ToolPlan


@dataclass
class CycleRecord:
    cycle_id: str
    state_json: str
    created_at: str = ""


class RCOHPersistence:
    def __init__(self, db_path: str = "/tmp/_msb_cortex/rcoh_cycles.sqlite") -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self._init()

    def _init(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rcoh_cycles (
                  cycle_id TEXT PRIMARY KEY,
                  state_json TEXT NOT NULL,
                  created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS artifacts (
                  category TEXT,
                  path TEXT,
                  blob TEXT NOT NULL,
                  created_at TEXT NOT NULL,
                  PRIMARY KEY (category, path)
                )
                """
            )

    def save(self, state: RCOHState) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO rcoh_cycles (cycle_id, state_json, created_at) VALUES (?, ?, ?)",
                (state.cycle_id, json.dumps(self._serialize(state)), state.started_at),
            )

    def save_artifact(self, category: str, path: str, blob: dict[str, Any]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO artifacts (category, path, blob, created_at) VALUES (?, ?, ?, ?)",
                (category, path, json.dumps(blob), datetime.now(timezone.utc).isoformat()),
            )

    def load(self, cycle_id: str) -> RCOHState | None:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT state_json FROM rcoh_cycles WHERE cycle_id = ?", (cycle_id,)
            ).fetchone()
        if row is None:
            return None
        return self._deserialize(json.loads(row[0]))

    def recent(self, limit: int = 20) -> list[dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT cycle_id, created_at, state_json FROM rcoh_cycles ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [
            {"cycle_id": r[0], "created_at": r[1], "state": json.loads(r[2])} for r in rows
        ]

    def _serialize(self, state: RCOHState) -> dict[str, Any]:
        return {
            "cycle_id": state.cycle_id,
            "current_phase": state.current_phase.value,
            "confidence": state.confidence,
            "context_summary": state.context_summary,
            "goals": state.goals,
            "goals_priority": state.goals_priority,
            "goals_constraints": state.goals_constraints,
            "assumptions": [
                {
                    "statement": a.statement,
                    "confidence": a.confidence,
                    "evidence": [
                        {
                            "label": e.label,
                            "strength": e.strength,
                            "source": e.source,
                            "notes": e.notes,
                        }
                        for e in a.evidence
                    ],
                    "inversion": a.inversion,
                    "opportunities": a.opportunities,
                    "risks": a.risks,
                    "status": a.status,
                }
                for a in state.assumptions
            ],
            "alternatives": [
                {
                    "name": a.name,
                    "description": a.description,
                    "cost": a.cost,
                    "complexity": a.complexity,
                    "scalability": a.scalability,
                    "risk": a.risk,
                    "maintainability": a.maintainability,
                    "business_value": a.business_value,
                    "technical_value": a.technical_value,
                    "learning_value": a.learning_value,
                }
                for a in state.alternatives
            ],
            "evidence": [
                {
                    "label": e.label,
                    "strength": e.strength,
                    "source": e.source,
                    "notes": e.notes,
                }
                for e in state.evidence
            ],
            "blueprint": [
                {
                    "horizon": h.horizon,
                    "task": h.task,
                    "dependencies": h.dependencies,
                    "success_criteria": h.success_criteria,
                }
                for h in state.blueprint
            ],
            "tool_queue": [
                {
                    "tool": t.tool,
                    "priority": t.priority,
                    "reason": t.reason,
                    "expected_output": t.expected_output,
                }
                for t in state.tool_queue
            ],
            "execution_plan": state.execution_plan,
            "validation_plan": state.validation_plan,
            "knowledge_gained": state.knowledge_gained,
            "next_questions": state.next_questions,
            "iteration": state.iteration,
            "max_iterations": state.max_iterations,
            "confidence_threshold": state.confidence_threshold,
            "stop_reason": state.stop_reason,
            "started_at": state.started_at,
            "updated_at": state.updated_at,
        }

    def _deserialize(self, data: dict[str, Any]) -> RCOHState:
        state = RCOHState(
            cycle_id=data["cycle_id"],
            current_phase=Phase(data["current_phase"]),
            confidence=float(data.get("confidence", 0.0)),
            context_summary=data.get("context_summary", ""),
            goals=data.get("goals", []),
            goals_priority=data.get("goals_priority", []),
            goals_constraints=data.get("goals_constraints", []),
            assumptions=[
                Assumption(
                    statement=a["statement"],
                    confidence=float(a.get("confidence", 0.5)),
                    evidence=[
                        Evidence(
                            label=e.get("label", ""),
                            strength=e.get("strength", "unknown"),
                            source=e.get("source", ""),
                            notes=e.get("notes", ""),
                        )
                        for e in a.get("evidence", [])
                    ],
                    inversion=a.get("inversion", ""),
                    opportunities=a.get("opportunities", []),
                    risks=a.get("risks", []),
                    status=a.get("status", "active"),
                )
                for a in data.get("assumptions", [])
            ],
            alternatives=[
                Alternative(
                    name=a["name"],
                    description=a.get("description", ""),
                    cost=a.get("cost", ""),
                    complexity=a.get("complexity", ""),
                    scalability=a.get("scalability", ""),
                    risk=a.get("risk", ""),
                    maintainability=a.get("maintainability", ""),
                    business_value=a.get("business_value", ""),
                    technical_value=a.get("technical_value", ""),
                    learning_value=a.get("learning_value", ""),
                )
                for a in data.get("alternatives", [])
            ],
            evidence=[
                Evidence(
                    label=e.get("label", ""),
                    strength=e.get("strength", "unknown"),
                    source=e.get("source", ""),
                    notes=e.get("notes", ""),
                )
                for e in data.get("evidence", [])
            ],
            blueprint=[
                HorizonTask(
                    horizon=h.get("horizon", "now"),
                    task=h.get("task", ""),
                    dependencies=h.get("dependencies", []),
                    success_criteria=h.get("success_criteria", ""),
                )
                for h in data.get("blueprint", [])
            ],
            tool_queue=[
                ToolPlan(
                    tool=t.get("tool", ""),
                    priority=t.get("priority", "medium"),
                    reason=t.get("reason", ""),
                    expected_output=t.get("expected_output", ""),
                )
                for t in data.get("tool_queue", [])
            ],
            execution_plan=data.get("execution_plan", []),
            validation_plan=data.get("validation_plan", []),
            knowledge_gained=data.get("knowledge_gained", []),
            next_questions=data.get("next_questions", []),
            iteration=int(data.get("iteration", 0)),
            max_iterations=int(data.get("max_iterations", 10)),
            confidence_threshold=float(data.get("confidence_threshold", 0.8)),
            stop_reason=data.get("stop_reason", ""),
            started_at=data.get("started_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat()),
        )
        return state
