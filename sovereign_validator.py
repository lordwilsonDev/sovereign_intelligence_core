#!/usr/bin/env python3
"""
sovereign_validator.py
End-to-end validation pipeline:
  MoIE Brain -> Cognitive Compiler (AIE) -> Ouroboros -> Panopticon -> Nano Memory
"""
from __future__ import annotations

import json, sys
from pathlib import Path
from typing import Any
from cognitive_compiler.cognitive_compiler_Aie import AxiomEvaluator, Violation

_ROOT = Path(__file__).resolve().parent

def _load(path: str | Path) -> Any:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_artifact(artifact: dict[str, Any], *, auto_repair: bool = False) -> dict[str, Any]:
    evaluator = AxiomEvaluator()
    context = artifact.get('context', {})
    asg = artifact.get('asg', {})

    violations = evaluator.evaluate(asg, context)

    decision = _decide(violations)

    report = {
        'artifact_id': artifact.get('id'),
        'violations': [_v_to_dict(v) for v in violations],
        'decision': decision,
        'repair_directives': evaluator.render_repair_directives(violations),
    }

    if decision == 'BLOCK':
        report['result'] = 'blocked'

    elif decision == 'REVIEW':
        report['result'] = 'review_required'

    elif decision == 'ALLOW':
        report['result'] = 'allowed'

    return report

def _decide(violations: list[Violation]) -> str:
    if not violations:
        return 'ALLOW'

    max_sev = max((v.severity for v in violations), key=lambda s: ['LOW','MEDIUM','HIGH','CRITICAL'].index(s))

    threshold = {
        'CRITICAL': 0.70,
        'HIGH': 0.50,
        'MEDIUM': 0.30,
        'LOW': 0.00,
    }.get(max_sev, 0.00)

    if threshold >= 0.70:
        return 'BLOCK'
    if threshold >= 0.20:
        return 'REVIEW'
    return 'ALLOW'

def _v_to_dict(v: Violation) -> dict[str, Any]:
    return {
        'axiom_id': v.axiom_id,
        'severity': v.severity,
        'message': v.message,
        'offending_node': v.offending_node,
        'repair_hint': v.repair_hint,
        'context': v.context,
    }

def main() -> None:
    paths = sys.argv[1:]
    if len(paths) != 1:
        print('Usage: sovereign_validator.py <artifact.json>', file=sys.stderr)
        raise SystemExit(1)

    artifact = _load(paths[0])
    report = validate_artifact(artifact)
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
