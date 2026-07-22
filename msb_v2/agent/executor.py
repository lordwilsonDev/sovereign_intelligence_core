from __future__ import annotations

import threading
from typing import Callable

from msb_v2.agent.error_handler import ErrorDecision, analyze_error, generate_fix
from msb_v2.agent.planner import Plan, Step


def _inject_context(params: dict, tool: str, step_results: dict[int, str], goal: str) -> dict:
    if tool == "web_search" and not params.get("query") and step_results:
        last = next(iter(reversed(step_results.values())), "")
        if last:
            params = dict(params)
            params["query"] = last[:200]
    return params


def _prepare_plan(goal: str, plan: Plan | None) -> Plan:
    if plan is None:
        return Plan(goal=goal, steps=[Step(step=1, tool="noop", description=goal, critical=True)])
    return plan


def _execute_step(step: Step, goal: str, step_results: dict[int, str], cancel_flag: threading.Event | None) -> str | None:
    if cancel_flag and cancel_flag.is_set():
        return "Task cancelled."

    params = _inject_context(dict(step.parameters), step.tool, step_results, goal)
    attempt = 1
    step_ok = False

    while attempt <= 2:
        try:
            result = _call_tool(step.tool, params)
            step_results[step.step] = result
            step_ok = True
            break
        except Exception as exc:
            error_msg = str(exc)
            step_dict = step.__dict__
            recovery = analyze_error(step_dict, error_msg, attempt=attempt)
            decision = recovery.decision

            if decision == ErrorDecision.RETRY:
                attempt += 1
                continue
            if decision == ErrorDecision.SKIP:
                step_ok = True
                break
            if decision == ErrorDecision.REPLAN and recovery.fix_suggestion:
                fix = generate_fix(step_dict, error_msg, recovery.fix_suggestion)
                try:
                    result = _call_tool(fix["tool"], fix.get("parameters", {}))
                    step_results[step.step] = result
                    step_ok = True
                    break
                except Exception:
                    pass
            if decision == ErrorDecision.ABORT:
                return recovery.user_message or f"Task aborted: {error_msg}"
            break

    if not step_ok:
        return f"Stopped at step {step.step}: {goal}"
    return None


def _summarize_result(goal: str, completed_steps: list[Step]) -> str:
    if not completed_steps:
        return f"No steps completed for: {goal}"
    return f"Completed {len(completed_steps)} step(s) for: {goal}"


def execute(goal: str, cancel_flag: threading.Event | None = None, plan: Plan | None = None) -> str:
    plan = _prepare_plan(goal, plan)
    completed_steps: list[Step] = []
    step_results: dict[int, str] = {}
    steps = plan.steps[:]

    for step in steps:
        terminal = _execute_step(step, goal, step_results, cancel_flag)
        if terminal is not None:
            return terminal
        completed_steps.append(step)

    return _summarize_result(goal, completed_steps)


def _call_tool(tool: str, parameters: dict) -> str:
    if tool == "noop":
        return "noop"

    if tool == "noop_command":
        return f"done:{goal}"

    if tool == "web_search":
        from msb_v2.integrations.rss import fetch_rss_articles
        query = parameters.get("query") or ""
        articles = fetch_rss_articles(query)
        return f"web_search({query}): {len(articles)} results"

    if tool == "open_app":
        return f"opened {parameters.get('app_name')}"

    if tool == "file_controller":
        return f"file({parameters.get('action')}) {parameters.get('path')}"

    raise KeyError(f"Unknown tool: {tool}")
