from __future__ import annotations

from collections import Counter
from typing import Any, Dict

from fastapi import APIRouter, Depends

from msb_v2.api.middleware import require_bearer_token
from msb_v2.engine.rcoh_persistence import RCOHPersistence

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter()
_PERSISTENCE = RCOHPersistence()


@router.post("/events", dependencies=[Depends(require_bearer_token)])
def torsion_events(limit: int = 50) -> Dict[str, Any]:
    recent = _PERSISTENCE.recent(limit=limit)
    events: list[Dict[str, Any]] = []
    anomaly_scores = []
    for cycle in recent:
        state = cycle.get("state", {})
        anomaly = float(state.get("anomaly_score", 0.0))
        anomaly_scores.append(anomaly)
        votes = state.get("votes", [])
        high_anomaly = anomaly >= 0.75
        c = Counter(vote.get("stance") for vote in votes)
        dominant = c.most_common(1)[0][0] if c else "unknown"
        events.append({
            "cycle_id": cycle.get("cycle_id"),
            "anomaly_score": anomaly,
            "dominant_stance": dominant,
            "high_anomaly": high_anomaly,
        })
    average_anomaly = sum(anomaly_scores) / len(anomaly_scores) if anomaly_scores else 0.0
    finite = [score for score in anomaly_scores if score > 0.0]
    median_anomaly = sorted(finite)[len(finite) // 2] if finite else 0.0
    deception_signals = [e for e in events if e["high_anomaly"]]
    return {
        "status": "ok",
        "events": events[-limit:],
        "deception_signals": deception_signals,
        "average_anomaly": average_anomaly,
        "median_anomaly": median_anomaly,
        "threshold": 0.75,
    }
# HCL contract registration
_register_contract(HarnessContract(route="/monitor/torsion/events", method="post", allow_anonymous=False))
