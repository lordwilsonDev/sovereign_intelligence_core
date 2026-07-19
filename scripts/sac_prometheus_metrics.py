#!/usr/bin/env python3
"""
Phase 2 PROMETHEUS — SAC + Ouroboros gauges + validation script.

Exposes:
- msb_sac_sas_score
- msb_sac_rnr_ratio
- msb_sac_eig_score
- msb_sac_quarantine_high_risk_count
- msb_sac_cma_mirage_flag
- msb_ouroboros_vdr_min
- msb_ouroboros_scan_timestamp
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

from prometheus_client import Gauge, REGISTRY

_metrics: Dict[str, Gauge] = {}


def _gauge(name: str, documentation: str) -> Gauge:
    if name not in _metrics:
        _metrics[name] = Gauge(name, documentation)
    return _metrics[name]


def export_sac_envelope(envelope: Dict[str, Any]) -> None:
    sac = envelope.get("sac", {})
    sas = sac.get("sas", {})
    rnr = sac.get("rnr", {})
    eig = sac.get("eig", {})

    _gauge("msb_sac_sas_score", "Current SAS sovereign alignment score").set(float(sas.get("score", 0)))
    _gauge("msb_sac_rnr_ratio", "Recursive Negation Ratio").set(float(rnr.get("ratio", 0)))
    _gauge("msb_sac_eig_score", "Epistemic Invariance Guard score").set(float(eig.get("score", 0)))

    quarantine = sac.get("quarantine", {})
    high_risk = 1 if quarantine.get("required_justification") else 0
    _gauge("msb_sac_quarantine_high_risk_count", "Quarantine events requiring justification").set(float(high_risk))

    mirage_flag = 1 if sac.get("cma", {}).get("verdict") == "mirage" else 0
    _gauge("msb_sac_cma_mirage_flag", "CM mirage detection flag").set(float(mirage_flag))


def export_ouroboros_scan(scan: Dict[str, Any]) -> None:
    scorecards = scan.get("scorecards", [])
    vdr_min = min((s.get("vdr_score", 0) for s in scorecards), default=0.0)
    _gauge("msb_ouroboros_vdr_min", "Lowest VDR across modules").set(float(vdr_min))
    _gauge("msb_ouroboros_scan_timestamp", "Last Ouroboros scan unix timestamp").set(float(time.time()))
