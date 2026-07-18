from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlanStep:
    step: int
    tool: str
    description: str
    parameters: dict[str, Any] = field(default_factory=dict)
    critical: bool = True


@dataclass
class Plan:
    goal: str
    steps: list[PlanStep]
    fallback: PlanStep | None = None


def _fallback_plan(goal: str) -> Plan:
    return Plan(
        goal=goal,
        steps=[
            PlanStep(
                step=1,
                tool="web_search",
                description=f"Search for: {goal}",
                parameters={"query": goal, "mode": "search"},
            )
        ],
    )


def create_plan(goal: str, available_tools: list[str] | None = None) -> Plan:
    # Hardcoded minimal planner contract for local-first runtime.
    # Replaces external LLM planner dependency with deterministic routing rules.
    goal_lower = (goal or "").lower()

    if any(k in goal_lower for k in ["weather"]):
        return Plan(
            goal=goal,
            steps=[PlanStep(step=1, tool="weather_report", description="Give weather report",
                            parameters={"city": ""})],
        )

    if any(k in goal_lower for k in ["open", "launch", "start"]) and any(
        k in goal_lower for k in ["app", "application", "browser", "spotify", "chrome"]
    ):
        return Plan(
            goal=goal,
            steps=[PlanStep(step=1, tool="open_app", description="Open app", parameters={"app_name": ""})],
        )

    if any(k in goal_lower for k in ["search", "look up", "find"]):
        return Plan(
            goal=goal,
            steps=[PlanStep(step=1, tool="web_search", description="Search web",
                            parameters={"query": goal, "mode": "search"})],
        )

    if any(k in goal_lower for k in ["remind", "reminder"]):
        return Plan(
            goal=goal,
            steps=[PlanStep(step=1, tool="reminder", description="Set reminder",
                            parameters={"date": "", "time": "", "message": goal})],
        )

    if any(k in goal_lower for k in ["youtube", "play", "video"]):
        return Plan(
            goal=goal,
            steps=[PlanStep(step=1, tool="youtube_video", description="Play YouTube",
                            parameters={"action": "play", "query": goal})],
        )

    if any(k in goal_lower for k in ["file", "create file", "save to file", "write"]):
        return Plan(
            goal=goal,
            steps=[
                PlanStep(step=1, tool="file_controller", description="Write file",
                         parameters={"action": "write", "path": "desktop", "name": "output.txt", "content": ""})
            ],
        )

    return _fallback_plan(goal)


def replan(goal: str, completed_steps: list[dict], failed_step: dict, error: str) -> Plan:
    if failed_step.get("tool") == "web_search":
        return Plan(
            goal=goal,
            steps=[
                PlanStep(step=1, tool="web_search", description="Retry search after failure",
                         parameters={"query": goal, "mode": "search"})
            ],
        )

    return _fallback_plan(goal)


def plan_to_json(plan: Plan) -> dict[str, Any]:
    return {
        "goal": plan.goal,
        "steps": [
            {
                "step": s.step,
                "tool": s.tool,
                "description": s.description,
                "parameters": s.parameters,
                "critical": s.critical,
            }
            for s in plan.steps
        ],
    }


def plan_from_json(data: dict[str, Any]) -> Plan:
    steps = [
        PlanStep(
            step=s.get("step", idx + 1),
            tool=s.get("tool", ""),
            description=s.get("description", ""),
            parameters=s.get("parameters", {}),
            critical=s.get("critical", True),
        )
        for idx, s in enumerate(data.get("steps", []))
    ]
    return Plan(goal=data.get("goal", ""), steps=steps)
