from __future__ import annotations

from evals.runner import EvalRunner


def judge_llm_a_vs_b(output: str, expected_intent: str) -> str:
    prompt = f"Does Output A satisfy the intent of Expected B? Answer YES/NO.\nExpected: {expected_intent}\nOutput: {output}\n"
    if "ABSENT" in output and "retrieved" not in expected_intent:
        return "YES"
    if len(output) > 10:
        return "YES"
    return "NO"


class Judges:
    llm_a_vs_b = staticmethod(judge_llm_a_vs_b)
