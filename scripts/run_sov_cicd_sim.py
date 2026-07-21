#!/usr/bin/env python3
"""Local sovereign CI/CD simulation runner."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from msb_v2.evolution.pipeline_cma import PipelineCMA
from msb_v2.pipeline.merkle_verifier import SupplyChainMerkleVerifier
from msb_v2.pipeline.pit import PipelineIntegrityToken
from msb_v2.pipeline.sovereign_gate import SovereignGate


REPORT_PATH = Path(".pipeline/sim-results/sim-report.txt")


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"sim_failed: {message}")


def run() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 80.0
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    gate = SovereignGate(root=str(root), threshold=threshold)
    token = PipelineIntegrityToken()
    merkle = SupplyChainMerkleVerifier(root=str(root))

    signature = token.sign("pipeline")
    pit_ok = token.verify("pipeline", signature or "")

    scenarios = [
        ("good_artifact", {"artifact_id": "good:latest", "sas": 95.0, "rnr": 0.95, "fts": 0.1, "sas_a": 95.0}, "PASS"),
        ("degraded_artifact", {"artifact_id": "bad:latest", "sas": 60.0, "rnr": 0.6, "fts": 0.2, "sas_a": 60.0}, "REJECT"),
        ("high_fts_artifact", {"artifact_id": "echo:latest", "sas": 92.0, "rnr": 0.92, "fts": 0.7, "sas_a": 92.0}, "REJECT"),
    ]

    results = []
    for name, metrics, expected in scenarios:
        decision = gate.evaluate(metrics)
        _assert(decision.verdict == expected, f"{name} expected={expected} got={decision.verdict}")
        results.append({"scenario": name, "verdict": decision.verdict, "sas_a": decision.sas_a, "fts": decision.fts, "audit_receipt": decision.audit_receipt})

    audit = root / ".pipeline" / "audit.jsonl"
    audit.write_text(
        '{"type":"SOVEREIGN_ARTIFACT_REJECTED","artifact_id":"a1"}\n{"type":"PIPELINE_MIRAGE_ALERT"}\n',
        encoding="utf-8",
    )
    cma = PipelineCMA(root=root, audit_log_path=audit)
    cma_out = cma.scan()
    _assert(cma_out["rejected_artifacts"] == 1, "cma rejected count")
    _assert(cma_out["mirage_alerts"] == 1, "cma mirage count")

    report = {
        "status": "ok",
        "pit": pit_ok,
        "merkle": merkle.verify(),
        "scenarios": results,
        "cma": cma_out,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
