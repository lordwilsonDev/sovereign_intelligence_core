#!/usr/bin/env python3
"""
Phase 2 PROMETHEUS — validation script.

Verifies that all SAC + Ouroboros gauges are registered in the
prometheus_client default REGISTRY after exercising export helpers.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from cognitive_compiler.sovereign_autonomy_core import SovereignAutonomyCore

REQUIRED = {
    "msb_sac_sas_score",
    "msb_sac_rnr_ratio",
    "msb_sac_eig_score",
    "msb_sac_quarantine_high_risk_count",
    "msb_sac_cma_mirage_flag",
    "msb_ouroboros_vdr_min",
    "msb_ouroboros_scan_timestamp",
}


def _load_export():
    path = str(Path(__file__).resolve().parent / "sac_prometheus_metrics.py")
    spec = importlib.util.spec_from_file_location("sac_prometheus_metrics", path)
    if spec is None:
        raise RuntimeError(f"Missing module spec: {path}")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    mod = _load_export()
    envelope = SovereignAutonomyCore.to_dict(
        SovereignAutonomyCore().run_dispatch_gate(
            query="validate", context={"high_stakes": False}, model_source="local"
        )
    )
    mod.export_sac_envelope(envelope)
    mod.export_ouroboros_scan({"scorecards": [{"vdr_score": 0.3}, {"vdr_score": 0.9}]})

    prom = __import__("prometheus_client")
    names = {m.name for m in prom.REGISTRY.collect()}
    missing = sorted(REQUIRED - names)
    if missing:
        print(f"MISSING metrics: {missing}")
        return 1
    print(f"Prometheus metrics OK: {sorted(REQUIRED)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
