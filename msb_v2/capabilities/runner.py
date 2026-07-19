from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def _client() -> TestClient:
    return TestClient(create_app())


def _run_capability_test(test: Dict[str, Any]) -> Dict[str, Any]:
    client = _client()
    test_id = test.get("test_id", "unknown")
    input_text = test.get("input", "")
    expected_properties = test.get("expected_properties", [])
    min_score = float(test.get("minimum_score", 0.0))
    expected_status = test.get("expected_status")

    r = client.post(
        "/demo/query",
        json={"query": input_text, "trace_id": f"cap-{test_id}", "accepted": True},
    )
    response_payload = r.json()
    status = r.status_code

    last_status = status
    repeat = int(test.get("repeat", 1))
    if repeat > 1:
        for _ in range(repeat - 1):
            last_r = client.post(
                "/demo/query",
                json={"query": input_text, "trace_id": f"cap-{test_id}", "accepted": True},
            )
            last_status = last_r.status_code

    expected_last_call_status = test.get("expected_last_call_status")
    last_call_bonus = 0.0
    last_call_flag = None
    if expected_last_call_status is not None:
        try:
            if int(last_status) == int(expected_last_call_status):
                last_call_bonus = 0.5
                last_call_flag = "expected_last_call_status"
        except (TypeError, ValueError):
            last_call_flag = None

    score = last_call_bonus
    found: List[str] = []
    if last_call_flag:
        found.append(last_call_flag)

    if expected_status is not None:
        if status == expected_status:
            score += 0.5
            found.append("expected_status")
    else:
        if status == 200:
            score += 0.5
            found.append("status_200")

    body_text = json.dumps(response_payload).lower()
    for prop in expected_properties:
        if prop.lower() in body_text:
            score += 0.5 / max(len(expected_properties), 1)
            found.append(prop)

    passed = score >= min_score
    if expected_status is not None and int(repeat) <= 1:
        passed = passed and status == expected_status
    if expected_last_call_status is not None:
        passed = passed and int(last_status) == int(expected_last_call_status)
    return {
        "test_id": test_id,
        "status": status,
        "score": round(score, 4),
        "passed": passed,
        "found": found,
        "expected_properties": expected_properties,
    }


def load_tests(tests_dir: Path) -> Dict[str, List[Dict[str, Any]]]:
    all_tests: Dict[str, List[Dict[str, Any]]] = {}
    for json_file in tests_dir.glob("*.json"):
        try:
            data = json.loads(json_file.read_text())
        except json.JSONDecodeError:
            continue
        category = json_file.stem
        all_tests[category] = data if isinstance(data, list) else [data]
    return all_tests


def run_all(tests_dir: Path) -> Dict[str, Any]:
    tests_by_category = load_tests(tests_dir)
    overall: Dict[str, Any] = {"summary": {}, "details": {}}
    for category, tests in tests_by_category.items():
        category_results = []
        for test in tests:
            category_results.append(_run_capability_test(test))
        scores = [r["score"] for r in category_results]
        passed = [r["passed"] for r in category_results]
        avg_score = round(sum(scores) / len(scores), 4) if scores else 0.0
        overall["summary"][category] = {
            "average_score": avg_score,
            "pass_rate": round(sum(passed) / len(passed), 4) if passed else 0.0,
            "total": len(tests),
        }
        overall["details"][category] = category_results
    return overall


def compare_to_baseline(current_results: Dict[str, Any], baseline: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    comparison: Dict[str, Any] = {}
    for category, summary in current_results["summary"].items():
        baseline_info = baseline.get(category)
        if baseline_info:
            expected = float(baseline_info["expected"])
            tolerance = float(baseline_info["tolerance"])
            current = float(summary["average_score"])
            comparison[category] = {
                "expected": expected,
                "current": current,
                "tolerance": tolerance,
                "within_tolerance": abs(current - expected) <= tolerance,
                "delta": round(current - expected, 4),
            }
        else:
            comparison[category] = {"status": "no_baseline"}
    return comparison


def update_baseline(results: Dict[str, Any], memory: Any) -> None:
    for category, summary in results["summary"].items():
        memory.set_capability_baseline(category, float(summary["average_score"]), tolerance=0.05)


def main(argv: List[str]) -> int:
    tests_dir = Path(__file__).resolve().parent / "tests"
    results_path = Path("capability_results.json")

    results = run_all(tests_dir)
    results_path.write_text(json.dumps(results, indent=2))

    if "--json" in argv:
        print(json.dumps(results, indent=2))
    else:
        print(json.dumps(results, indent=2))

    if "--update-baseline" in argv:
        try:
            from msb_v2.core.evolution_memory import EvolutionMemory
            memory = EvolutionMemory()
            update_baseline(results, memory)
            print("Baseline updated.")
        except Exception as exc:
            print(f"Baseline update failed: {exc}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
