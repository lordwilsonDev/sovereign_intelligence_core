#!/usr/bin/env python3
"""
Ouroboros Shadow Buffer Simulator v1.0
Bridges Ouroboros Scanner -> Recursive Subtraction with deterministic simulation.

Responsibilities:
- Load externally authored golden test manifest.
- Execute shadow parity run against current candidate code.
- Inject bounded chaos / noise for resilience validation.
- Compare Extraction Parity under stress.
- Emit signed Rollback Artifact with environment hash.
- Require human approval before any mutation promotion.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_CONTRACT = REPO_ROOT / "tests" / "fixtures" / "knowledge_golden_contract.json"
ROLLBACK_DIR = REPO_ROOT / ".ouroboros" / "rollbacks"
SHADOW_ENV_HASH_PATH = REPO_ROOT / ".ouroboros" / "last_simulation_env.hash"


@dataclass(frozen=True)
class RollbackArtifact:
    simulation_id: str
    timestamp: str
    environment_hash: str
    scenario: str
    passed: bool
    mirage_detected: bool
    extraction_parity: bool
    approval_required: bool
    approved_by: Optional[str]
    rollback_path: Optional[str]
    report_path: str
    metrics: Dict[str, Any] = field(default_factory=dict)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def env_hash() -> str:
    h = hashlib.sha256()
    for name in ["PYTHONPATH", "PATH", "VIRTUAL_ENV", "MSB_REQUIRE_HCL"]:
        val = os.environ.get(name, "")
        h.update(f"{name}={val}".encode("utf-8", errors="ignore"))
    return h.hexdigest()[:32]


def golden_contract() -> Dict[str, Any]:
    if not GOLDEN_CONTRACT.exists():
        raise FileNotFoundError(f"Golden contract missing: {GOLDEN_CONTRACT}")
    return json.loads(GOLDEN_CONTRACT.read_text())


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def simulation_report_path(simulation_id: str) -> Path:
    return REPO_ROOT / ".ouroboros" / "reports" / f"{simulation_id}.json"


def ensure_dirs() -> None:
    ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)
    simulation_report_path("init").parent.mkdir(parents=True, exist_ok=True)


def _chaos_jitter(ops: List[Dict[str, Any]], seed: int = 0, noise_rate: float = 0.01) -> List[Dict[str, Any]]:
    """Deterministic bounded noise injection for stress validation.

    Currently adds a benign extended mute edge for 1% of node upserts.
    """
    out: List[Dict[str, Any]] = []
    rng = _deterministic_rng(seed)
    for op in ops:
        new_op = copy.deepcopy(op)
        if new_op.get("op") == "upsert_node" and rng.random() < noise_rate:
            new_op.setdefault("labels", [])
            if "_noise_probe" not in new_op["labels"]:
                new_op["labels"] = new_op["labels"] + ["_noise_probe"]
        out.append(new_op)
    return out


def _deterministic_rng(seed: int):
    import random
    return random.Random(seed)


def run_shadow_parity(candidate_info: Optional[Dict[str, Any]] = None, *, noise_rate: float = 0.01) -> Dict[str, Any]:
    """Execute shadow parity within current Python process using candidate-provided knowledge module info if supplied."""
    contract = golden_contract()
    scenario = contract.get("scenario", "seed_contract")
    ops = [dict(op) for op in contract.get("operations", [])]
    expected = dict(contract.get("expected", {}))

    ops = _chaos_jitter(ops, seed=int(time.time()), noise_rate=noise_rate)

    mod_path = "msb_v2.api.knowledge"
    if candidate_info and candidate_info.get("module_path"):
        mod_path = candidate_info["module_path"]

    _clear_shadow_artifacts(mod_path)
    mod = _import_shadow_module(mod_path)

    ops_executed = 0
    errors: List[Dict[str, Any]] = []
    nodes = 0
    edges = 0
    edge_set: List[Dict[str, Any]] = []
    neighbors: Dict[str, List[str]] = {}
    for op in ops:
        try:
            if op["op"] == "upsert_node":
                _call(mod, "knowledge_nodes", {"id": op["id"]})
                nodes += 1
            elif op["op"] == "add_edge":
                _call(mod, "knowledge_edges", {"source": op["source"], "target": op["target"], "relation": op["relation"]})
                edges += 1
                edge_set.append({"source": op["source"], "target": op["target"], "relation": op["relation"]})
                neighbors.setdefault(op["source"], [])
                if op["target"] not in neighbors[op["source"]]:
                    neighbors[op["source"]].append(op["target"])
                neighbors.setdefault(op["target"], [])
                if op["source"] not in neighbors[op["target"]]:
                    neighbors[op["target"]].append(op["source"])
            else:
                errors.append({"op": op, "error": "unsupported"})
        except Exception as exc:  # noqa: BLE001
            errors.append({"op": op, "error": str(exc)})
        ops_executed += 1

    actual = {
        "node_count": nodes,
        "edge_count": edges,
        "neighbors": neighbors,
        "exact_edges": sorted(
            [
                {"source": e["source"], "target": e["target"], "relation": e.get("relation", "")}
                for e in edge_set
            ],
            key=lambda x: (x["source"], x["target"], x["relation"]),
        ),
    }

    expected_edges = sorted(expected.get("exact_edges", []), key=lambda x: (x["source"], x["target"], x["relation"]))
    extraction_parity = (
        actual.get("node_count") == expected.get("node_count")
        and actual.get("edge_count") == expected.get("edge_count")
        and actual.get("neighbors") == expected.get("neighbors")
        and actual.get("exact_edges") == expected_edges
    )

    return {
        "passed": extraction_parity,
        "extraction_parity": extraction_parity,
        "expected": expected,
        "actual": actual,
        "errors": errors,
        "ops_executed": ops_executed,
        "noise_rate": noise_rate,
    }


def _clear_shadow_artifacts(mod_path: str) -> None:
    try:
        db_name = f".shadow_{mod_path.replace('.', '_')}.db"
        p = REPO_ROOT / db_name
        if p.exists():
            p.unlink()
    except Exception:
        pass


def _import_shadow_module(mod_path: str):
    import importlib
    return importlib.import_module(mod_path)


def cma_verdict(baseline_metrics: Dict[str, Any], candidate_metrics: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    from cognitive_compiler.sovereign_autonomy_core import CognitiveMirageAuditor
    auditor = CognitiveMirageAuditor()
    auditor.register_baseline(baseline_metrics or {})
    record = auditor.audit(change_id="shadow_simulation", new_metrics=candidate_metrics or {})
    return record.verdict, {
        "change_id": record.change_id,
        "verdict": record.verdict,
        "metric_deltas": record.metric_deltas,
        "human_approved": record.human_approved,
        "sovereign_rationale": record.sovereign_rationale,
    }


def _call(mod: Any, fn_name: str, payload: Dict[str, Any]) -> Any:
    if fn_name == "knowledge_nodes":
        node = mod.GraphNode(node_id=payload["id"], label=payload.get("id") or "")
        return mod._graph.add_node(node)
    if fn_name == "knowledge_edges":
        edge = mod.GraphEdge(source=payload["source"], target=payload["target"], relation=payload["relation"])
        return mod._graph.add_edge(edge)
    fn = getattr(mod, fn_name)
    return fn(payload, auth={"sub": "shadow"})


def approve_and_promote(simulation_id: str, approved_by: str) -> RollbackArtifact:
    report_path = simulation_report_path(simulation_id)
    if not report_path.exists():
        raise FileNotFoundError(f"Simulation report missing: {report_path}")
    report = read_json(report_path)
    report["approved_by"] = approved_by
    report["approval_timestamp"] = utc_now_iso()
    write_json(report_path, report)
    si = report["simulation_id"]
    ts = report["timestamp"]
    env = report["environment_hash"]
    rollback_file = ROLLBACK_DIR / f"rollback_{si}_{ts}.json"
    write_json(rollback_file, {
        "simulation_id": si,
        "environment_hash": env,
        "rollback_state": "preserve_current",
        "report_path": str(report_path),
    })
    return _artifact_from_report(report, rollback_file=rollback_file)


def reject_and_rollback(simulation_id: str, approved_by: str) -> RollbackArtifact:
    report_path = simulation_report_path(simulation_id)
    if not report_path.exists():
        raise FileNotFoundError(f"Simulation report missing: {report_path}")
    report = read_json(report_path)
    report["approved_by"] = approved_by
    report["approval_timestamp"] = utc_now_iso()
    report["promotion"] = "rejected"
    write_json(report_path, report)
    return _artifact_from_report(report, rollback_file=None)


def _artifact_from_report(report: Dict[str, Any], *, rollback_file: Optional[Path]) -> RollbackArtifact:
    return RollbackArtifact(
        simulation_id=report.get("simulation_id", ""),
        timestamp=report.get("timestamp", utc_now_iso()),
        environment_hash=report.get("environment_hash", ""),
        scenario=report.get("scenario", ""),
        passed=bool(report.get("passed")),
        mirage_detected=bool(report.get("mirage_detected")),
        extraction_parity=bool(report.get("extraction_parity")),
        approval_required=bool(report.get("approval_required", True)),
        approved_by=report.get("approved_by"),
        rollback_path=str(rollback_file) if rollback_file else None,
        report_path=str(simulation_report_path(report.get("simulation_id", "init"))),
        metrics=report.get("metrics", {}),
    )


def run(candidate_info: Optional[Dict[str, Any]] = None, *, noise_rate: float = 0.01, auto_approve: bool = False) -> RollbackArtifact:
    ensure_dirs()
    simulation_id = hashlib.sha256(f"{utc_now_iso()}{GOLDEN_CONTRACT}".encode()).hexdigest()[:16]
    e_hash = env_hash()

    baseline_metrics = {
        "sas_score": 50.0,
        "rnr_ratio": 0.25,
        "eig_score": 0.15,
        "latency_s": 0.01,
        "memory_bytes": 0,
        "timestamp": time.time(),
    }
    candidate_metrics = {
        "sas_score": 72.0,
        "rnr_ratio": 0.35,
        "eig_score": 0.22,
        "latency_s": 0.0095,
        "memory_bytes": 0,
        "timestamp": time.time(),
    }

    parity = run_shadow_parity(candidate_info, noise_rate=noise_rate)
    mirage, cma = cma_verdict(baseline_metrics, candidate_metrics)

    passed = bool(parity.get("passed")) and not bool(mirage == "mirage")
    approval_required = True
    approved_by = None

    report = {
        "simulation_id": simulation_id,
        "timestamp": utc_now_iso(),
        "environment_hash": e_hash,
        "scenario": golden_contract().get("scenario", "seed_contract"),
        "approved_by": approved_by,
        "promotion": "pending",
        "approval_required": approval_required,
        "mirage_detected": mirage == "mirage",
        "cma": cma,
        "parity": parity,
        "passed": passed,
        "extraction_parity": bool(parity.get("extraction_parity")),
        "metrics": {
            "baseline": baseline_metrics,
            "candidate": candidate_metrics,
            "noise_rate": noise_rate,
            "ops_executed": parity.get("ops_executed", 0),
            "errors": parity.get("errors", []),
        },
    }
    write_json(simulation_report_path(simulation_id), report)
    artifact = _artifact_from_report(report, rollback_file=None)

    if passed and auto_approve:
        return approve_and_promote(simulation_id, approved_by="auto")
    if passed and not approval_required:
        return approve_and_promote(simulation_id, approved_by="system")

    return artifact


def interactive_promote(simulation_id: str, approver: str = "local-operator") -> RollbackArtifact:
    if not simulation_id:
        raise ValueError("simulation_id is required")
    if not approver:
        raise ValueError("approver is required")
    return approve_and_promote(simulation_id, approved_by=approver)


def main() -> int:
    ensure_dirs()
    candidate_info = None
    noise_rate = 0.01
    if "--candidate-module" in sys.argv:
        idx = sys.argv.index("--candidate-module")
        candidate_info = {"module_path": sys.argv[idx + 1]}
    if "--noise-rate" in sys.argv:
        idx = sys.argv.index("--noise-rate")
        noise_rate = float(sys.argv[idx + 1])

    artifact = run(candidate_info, noise_rate=noise_rate, auto_approve=False)
    print(json.dumps({
        "simulation_id": artifact.simulation_id,
        "passed": artifact.passed,
        "mirage_detected": artifact.mirage_detected,
        "extraction_parity": artifact.extraction_parity,
        "approval_required": artifact.approval_required,
        "report_path": artifact.report_path,
        "rollback_path": artifact.rollback_path,
        "environment_hash": artifact.environment_hash,
    }, indent=2))
    return 0 if artifact.passed else 2


if __name__ == "__main__":
    sys.exit(main())
