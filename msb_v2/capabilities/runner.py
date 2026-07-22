from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def _client() -> TestClient:
    return TestClient(create_app())


def _post_capability_query(client: TestClient, test_id: str, input_text: str) -> tuple[int, dict[str, Any]]:
    last_r = client.post(
        "/demo/query",
        json={"query": input_text, "trace_id": f"cap-{test_id}", "accepted": True},
    )
    return last_r.status_code, last_r.json()


def _run_capability_query_sequence(client: TestClient, test_id: str, input_text: str, repeat: int) -> tuple[int, int]:
    last_status = -1
    status = -1
    for _ in range(repeat):
        status, _ = _post_capability_query(client, test_id, input_text)
        last_status = status
    return last_status, status


def _score_last_call(last_status: int, expected_last_call_status: str | None) -> tuple[float, str | None]:
    last_call_flag = None
    last_call_bonus = 0.0
    if expected_last_call_status is not None:
        try:
            if int(last_status) == int(expected_last_call_status):
                last_call_bonus = 0.5
                last_call_flag = "expected_last_call_status"
        except (TypeError, ValueError):
            last_call_flag = None
    return last_call_bonus, last_call_flag


def _score_expected_status(status: int, expected_status: str | None) -> tuple[float, str | None]:
    if expected_status is not None:
        if status == int(expected_status):
            return 0.5, "expected_status"
        return 0.0, None
    if status == 200:
        return 0.5, "status_200"
    return 0.0, None


def _score_property_matches(response_payload: dict[str, Any], expected_properties: list[str]) -> tuple[float, list[str]]:
    found: list[str] = []
    prop_bonus = 0.0
    if expected_properties:
        body_text = json.dumps(response_payload).lower()
        for prop in expected_properties:
            if prop.lower() in body_text:
                prop_bonus += 0.5 / max(len(expected_properties), 1)
                found.append(prop)
    return prop_bonus, found


def _evaluate_passed(
    score: float,
    status: int,
    last_status: int,
    min_score: float,
    expected_status: str | None,
    expected_last_call_status: str | None,
    repeat: int,
) -> bool:
    passed = score >= min_score
    if expected_status is not None and int(repeat) <= 1:
        passed = passed and status == int(expected_status)
    if expected_last_call_status is not None:
        passed = passed and int(last_status) == int(expected_last_call_status)
    return passed


def _run_capability_test(test: Dict[str, Any]) -> Dict[str, Any]:
    client = _client()
    test_id = test.get("test_id", "unknown")
    input_text = test.get("input", "")
    expected_properties = test.get("expected_properties", [])
    min_score = float(test.get("minimum_score", 0.0))
    expected_status = test.get("expected_status")

    last_status, status = _run_capability_query_sequence(
        client, test_id, input_text, int(test.get("repeat", 1))
    )
    response_payload = _post_capability_query(client, test_id, input_text)[1]

    expected_last_call_status = test.get("expected_last_call_status")
    last_call_bonus, last_call_flag = _score_last_call(last_status, expected_last_call_status)

    score = last_call_bonus
    found: List[str] = []
    if last_call_flag:
        found.append(last_call_flag)

    expected_status_bonus, expected_status_flag = _score_expected_status(status, expected_status)
    score += expected_status_bonus
    if expected_status_flag:
        found.append(expected_status_flag)

    prop_bonus, prop_found = _score_property_matches(response_payload, expected_properties)
    score += prop_bonus
    found.extend(prop_found)

    passed = _evaluate_passed(
        score=score,
        status=status,
        last_status=last_status,
        min_score=min_score,
        expected_status=expected_status,
        expected_last_call_status=expected_last_call_status,
        repeat=int(test.get("repeat", 1)),
    )
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
