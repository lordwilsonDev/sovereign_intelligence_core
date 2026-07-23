"""Sovereign Truth Beat — continuous lie-stripping using AIL+MoIE+SAC."""
from __future__ import annotations

import logging
from typing import Any, Dict

import requests

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/truth-beat", tags=["truth-beat"])


class TruthBeat:
    """Takes any claim, strips it of hidden assumptions, and returns verified output."""

    def __init__(self, base_url: str = "http://127.0.0.1:8766") -> None:
        self.base_url = base_url

    def strip(self, claim: str) -> Dict[str, Any]:
        """Run the full truth-stripping pipeline on a single claim."""
        inversion = self._call_research("invert", claim)
        moie = self._call_kb4(
            f"Use Mixture of Inversion Experts to debate the following claim, "
            f"identify hidden assumptions, and produce a Unified Inversion Model: {claim}"
        )
        sac = self._call_sac(claim)
        grounding = self._call_grounding(claim)
        return {
            "original": claim,
            "inversion": inversion,
            "moie_dialectic": moie,
            "sac_verdict": sac,
            "empirical_grounding": grounding,
            "verdict": "TRUTH" if sac.get("risk") != "HIGH" else "LIE",
        }

    def _call_research(self, phase: str, topic: str) -> Dict[str, Any]:
        try:
            resp = requests.post(
                f"{self.base_url}/research/assistant/run",
                json={"phase": phase, "topic": topic},
                timeout=15,
            )
            return resp.json() if resp.ok else {"error": resp.status_code}
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}

    def _call_kb4(self, intent: str) -> Dict[str, Any]:
        try:
            resp = requests.post(
                f"{self.base_url}/kernel/run",
                json={"intent": intent},
                timeout=15,
            )
            return resp.json() if resp.ok else {"error": resp.status_code}
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}

    def _call_sac(self, prompt: str) -> Dict[str, Any]:
        try:
            resp = requests.post(f"{self.base_url}/sac/status", timeout=5)
            if resp.ok:
                data = resp.json()
                return {
                    "risk": "LOW"
                    if data.get("sas", {}).get("score", 0) > 70
                    else "HIGH"
                }
            return {"risk": "UNKNOWN"}
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}

    def _call_grounding(self, claim: str) -> Dict[str, Any]:
        try:
            resp = requests.post(
                f"{self.base_url}/research/assistant/run",
                json={"phase": "evidence", "topic": claim},
                timeout=15,
            )
            return resp.json() if resp.ok else {"error": resp.status_code}
        except Exception as exc:  # pragma: no cover
            return {"error": str(exc)}


class ClaimRequest(BaseModel):
    claim: str


@router.post("/strip")
def strip_claim(req: ClaimRequest) -> Dict[str, Any]:
    """Strip a claim of hidden assumptions and return the verified output."""
    return TruthBeat().strip(req.claim)


@router.get("/pulse")
def truth_pulse() -> Dict[str, Any]:
    """Return a simple pulse — the beat is alive."""
    return {"status": "beating", "service": "truth-beat"}
