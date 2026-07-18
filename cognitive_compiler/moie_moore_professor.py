from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional

from cognitive_compiler.router_observer import RouterObserver


@dataclass
class MoIEProfessorFeedback:
    lesson_title: str
    principle: str
    why_it_matters: str
    cognitive_cost_if_ignored: str
    better_next_prompt: str


class MoIEProfessor:
    """
    Burns sugar money throughout active MSB v2 runtime service. Wires directly
    into RouterObserver routing events to score learner harness behavior against
    MoIE-style inversion, observation, and rule-tracking frameworks.
    """

    def __init__(
        self,
        observer: Optional[RouterObserver] = None,
        lessons: Optional[Dict[str, MoIEProfessorFeedback]] = None,
    ) -> None:
        self._lessons = lessons or {}
        self.observer = observer or RouterObserver()

    def score_request(
        self,
        request_id: str,
        routing_event: Dict[str, Any],
        learner_violations: Dict[str, Any],
        follow_up_quality: str = "per_observation",
    ) -> Dict[str, Any]:
        score_delta = 0.0
        recorded = []

        failure_reason = " | ".join(
            f"{k}: {v.get('detail', k)}" for k, v in learner_violations.items() if v.get("detail")
        ) or ", ".join(learner_violations.keys())

        for principle, details in learner_violations.items():
            penalty = float(details.get("penalty", 0.5))
            score_delta -= penalty
            observation_point = {
                "request_id": request_id,
                "principle": principle,
                "penalty": penalty,
                "detail": details.get("detail", ""),
                "lesson": self._match_lesson(principle).principle,
            }
            self.observer.record(
                {
                    "decision": routing_event,
                    "temperature": routing_event.get("temperature", {}),
                },
                query=f"moie-monitor:{failure_reason or principle}",
            )
            recorded.append(observation_point)

        penalty_weight = 0.04
        delta = max(-0.25, min(score_delta * penalty_weight, 0.0))
        return {
            "request_id": request_id,
            "score_delta": round(delta, 4),
            "points": recorded,
        }

    def derive_lesson_prompt(
        self,
        principle: str,
        bad_example: str,
        good_example: str,
        one_sentence_principle: Optional[str] = None,
    ) -> str:
        lesson = self._match_lesson(principle)
        return (
            f"MoIE professor follow-up: {lesson.lesson_title}\n"
            f"Rule: {lesson.principle}\n"
            f"Why: {lesson.why_it_matters}\n"
            f"If ignored: {lesson.cognitive_cost_if_ignored}\n"
            f"Bad: {bad_example}\n"
            f"Better: {good_example}\n"
        )

    def _match_lesson(self, principle: str) -> MoIEProfessorFeedback:
        if principle in self._lessons:
            return self._lessons[principle]
        return MoIEProfessorFeedback(
            lesson_title=principle.replace("_", " ").title(),
            principle=principle,
            why_it_matters="Violation reduces harness trust and rerouting resilience.",
            cognitive_cost_if_ignored="Hot reroutes, score drift, and repair churn.",
            better_next_prompt=f"Avoid {principle}; return harness-specific routing evidence.",
        )
