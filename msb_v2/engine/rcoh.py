from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from msb_v2.engine.orchestrator import Task, orchestrate
from msb_v2.engine.phase_tracing import PhaseTracer
from msb_v2.engine.tool_audit import ToolAudit
from msb_v2.engine.merkle_reasoning import MerkleReasoningChain


class Phase(str, Enum):
    OBSERVE = "observe"
    CONTEXT = "context"
    GOALS = "goals"
    ASSUMPTIONS = "assumptions"
    INVERSION = "inversion"
    ALTERNATIVES = "alternatives"
    EVIDENCE = "evidence"
    CONFIDENCE = "confidence"
    BLUEPRINT = "blueprint"
    TOOLS = "tools"
    EXECUTION = "execution"
    VERIFICATION = "verification"
    LEARNING = "learning"
    QUESTIONS = "questions"
    DONE = "done"


PHASE_ORDER = [
    Phase.OBSERVE,
    Phase.CONTEXT,
    Phase.GOALS,
    Phase.ASSUMPTIONS,
    Phase.INVERSION,
    Phase.ALTERNATIVES,
    Phase.EVIDENCE,
    Phase.CONFIDENCE,
    Phase.BLUEPRINT,
    Phase.TOOLS,
    Phase.EXECUTION,
    Phase.VERIFICATION,
    Phase.LEARNING,
    Phase.QUESTIONS,
]


@dataclass
class Evidence:
    label: str
    strength: str = "unknown"
    source: str = ""
    notes: str = ""

    def weight(self) -> float:
        return {"high": 1.0, "medium": 0.7, "low": 0.4, "unknown": 0.0}.get(self.strength, 0.0)


@dataclass
class Assumption:
    statement: str
    confidence: float = 0.5
    evidence: list[Evidence] = field(default_factory=list)
    inversion: str = ""
    opportunities: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    status: str = "active"


@dataclass
class Alternative:
    name: str
    description: str
    cost: str = ""
    complexity: str = ""
    scalability: str = ""
    risk: str = ""
    maintainability: str = ""
    business_value: str = ""
    technical_value: str = ""
    learning_value: str = ""


@dataclass
class HorizonTask:
    horizon: str
    task: str
    dependencies: list[str] = field(default_factory=list)
    success_criteria: str = ""


@dataclass
class ToolPlan:
    tool: str
    priority: str = "medium"
    reason: str = ""
    expected_output: str = ""


@dataclass
class VerificationResult:
    expected: str
    actual: str
    difference: str = ""
    root_cause: str = ""
    lessons: str = ""
    confidence_delta: float = 0.0


@dataclass
class RCOHState:
    cycle_id: str
    current_phase: Phase = Phase.OBSERVE
    confidence: float = 0.0
    context_summary: str = ""
    goals: list[str] = field(default_factory=list)
    goals_priority: list[str] = field(default_factory=list)
    goals_constraints: list[str] = field(default_factory=list)
    assumptions: list[Assumption] = field(default_factory=list)
    alternatives: list[Alternative] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    blueprint: list[HorizonTask] = field(default_factory=list)
    tool_queue: list[ToolPlan] = field(default_factory=list)
    execution_plan: list[str] = field(default_factory=list)
    validation_plan: list[str] = field(default_factory=list)
    knowledge_gained: list[str] = field(default_factory=list)
    next_questions: list[str] = field(default_factory=list)
    verification_history: list[VerificationResult] = field(default_factory=list)
    iteration: int = 0
    max_iterations: int = 10
    confidence_threshold: float = 0.8
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    stop_reason: str = ""


class RCOH:
    def __init__(self, state: RCOHState | None = None) -> None:
        self.state = state or RCOHState(cycle_id=self._new_cycle_id())
        self.trace = PhaseTracer()
        self.audit = ToolAudit()
        self.chain = MerkleReasoningChain()

    def plan_tasks(self) -> list[Task]:
        ready = []
        if self.state.current_phase == Phase.OBSERVE:
            ready.append(self._observe())
        elif self.state.current_phase == Phase.CONTEXT:
            ready.append(self._context())
        elif self.state.current_phase == Phase.GOALS:
            ready.append(self._goals())
        elif self.state.current_phase == Phase.ASSUMPTIONS:
            ready.append(self._assumptions())
        elif self.state.current_phase == Phase.INVERSION:
            ready.append(self._inversion())
        elif self.state.current_phase == Phase.ALTERNATIVES:
            ready.append(self._alternatives())
        elif self.state.current_phase == Phase.EVIDENCE:
            ready.append(self._evidence())
        elif self.state.current_phase == Phase.CONFIDENCE:
            ready.append(self._confidence())
        elif self.state.current_phase == Phase.BLUEPRINT:
            ready.append(self._blueprint())
        elif self.state.current_phase == Phase.TOOLS:
            ready.append(self._tools())
        elif self.state.current_phase == Phase.EXECUTION:
            ready.append(self._execution())
        elif self.state.current_phase == Phase.VERIFICATION:
            ready.append(self._verification())
        elif self.state.current_phase == Phase.LEARNING:
            ready.append(self._learning())
        elif self.state.current_phase == Phase.QUESTIONS:
            ready.append(self._questions())
        return ready

    def run(self, max_iterations: int = 10) -> RCOHState:
        self.state.max_iterations = max_iterations
        while self.state.current_phase != Phase.DONE and self.state.iteration < max_iterations:
            tasks = self.plan_tasks()
            if not tasks:
                self._transition(Phase.DONE)
                break
            self.chain.append(self.state.current_phase.value, {"iteration": self.state.iteration})
            orchestrate(tasks)
            self._advance()
            self.state.iteration += 1
            self.state.updated_at = datetime.now(timezone.utc).isoformat()
        return self.state

    def _new_cycle_id(self) -> str:
        return f"rcoh-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    def _transition(self, next_phase: Phase) -> None:
        self.state.current_phase = next_phase

    def _advance(self) -> None:
        idx = PHASE_ORDER.index(self.state.current_phase)
        if idx + 1 < len(PHASE_ORDER):
            self._transition(PHASE_ORDER[idx + 1])
        else:
            self._transition(Phase.DONE)

    def _stop_condition(self) -> bool:
        if self.state.confidence >= self.state.confidence_threshold:
            return True
        if self.state.current_phase == Phase.DONE:
            return True
        if self.state.iteration >= self.state.max_iterations:
            return True
        return False

    def _record(self, name: str, output: Any) -> Task:
        return Task(id=name, action=lambda n=name, o=output: None, result=output)

    def _observe(self) -> Task:
        self.state.context_summary = self.state.context_summary or "observed initial state"
        return self._record("observe", self.state.context_summary)

    def _context(self) -> Task:
        self.state.context_summary = self.state.context_summary or "(no context)"
        return self._record("context", self.state.context_summary)

    def _goals(self) -> Task:
        self.state.goals = self.state.goals or ["primary goal"]
        self.state.goals_priority = self.state.goals_priority or ["primary"]
        self.state.goals_constraints = self.state.goals_constraints or []
        return self._record("goals", self.state.goals)

    def _assumptions(self) -> Task:
        return self._record("assumptions", self.state.assumptions or [])

    def _inversion(self) -> Task:
        for a in self.state.assumptions:
            if not a.inversion:
                a.inversion = f"not({a.statement})"
        return self._record("inversion", self.state.assumptions)

    def _alternatives(self) -> Task:
        return self._record("alternatives", self.state.alternatives or [])

    def _evidence(self) -> Task:
        self.state.evidence = self.state.evidence or []
        return self._record("evidence", self.state.evidence)

    def _confidence(self) -> Task:
        total = 0.0
        count = 0
        for a in self.state.assumptions:
            total += a.confidence
            count += 1
        if count > 0:
            self.state.confidence = total / count
        return self._record("confidence", self.state.confidence)

    def _blueprint(self) -> Task:
        return self._record("blueprint", self.state.blueprint or [])

    def _tools(self) -> Task:
        return self._record("tools", self.state.tool_queue or [])

    def _execution(self) -> Task:
        return self._record("execution", self.state.execution_plan or [])

    def _verification(self) -> Task:
        return self._record("verification", self.state.verification_history or [])

    def _learning(self) -> Task:
        return self._record("learning", self.state.knowledge_gained or [])

    def _questions(self) -> Task:
        return self._record("questions", self.state.next_questions or [])
