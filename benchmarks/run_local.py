from __future__ import annotations

import json
import sys

from benchmarks.harness import BenchmarkCase, BenchmarkHarness


cases = [
    BenchmarkCase(
        name="local-tool-use",
        prompt="You are an agent. Output JSON only: {\"tool\":\"search\",\"query\":\"msb\"}",
        expected_keys=["tool", "query"],
        max_tokens=64,
        temperature=0.0,
    ),
    BenchmarkCase(
        name="reasoning-extraction",
        prompt="Extract entities from: 'Lord Wilson operates MSB v2 in Honolulu'. Output JSON only.",
        expected_keys=["entities", "location"],
        max_tokens=128,
        temperature=0.0,
    ),
    BenchmarkCase(
        name="code-generation",
        prompt="Return a python function named add(a,b) that returns a+b. Code only.",
        expected_keys=["def add(", "return"],
        max_tokens=128,
        temperature=0.0,
    ),
]


def main() -> int:
    models = ["gemma4:31b", "deepseek-v4-flash", "claude"] if len(sys.argv) < 2 else sys.argv[1:]
    harness = BenchmarkHarness(cases, provider="ollama")
    for model in models:
        print(f"--- {model} ---")
        try:
            rows = harness.run_model(model)
        except Exception as exc:
            print(f"ERROR {model}: {exc}")
            continue
        for row in rows:
            status = "PASS" if row.passed else f"FAIL missing={row.missing_keys}"
            print(f"{row.case}: {status} latency={row.latency_ms:.1f}ms tokens={row.tokens_used}")
    print("--- summary ---")
    print(json.dumps(harness.summary(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
