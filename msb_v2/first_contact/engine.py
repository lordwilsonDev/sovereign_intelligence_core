"""First Contact Protocol — guided axiom inversion onboarding."""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


_SESSION_PATH = Path(os.environ.get("MSB_FIRST_CONTACT_PATH", "./runtime/first_contact_sessions.jsonl"))


@dataclass(frozen=True)
class AxiomProposal:
    text: str
    inverted: str = ""


@dataclass
class FirstContactSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    current_step: str = "welcome"
    participant_assumption: str = ""
    proposals: List[AxiomProposal] = field(default_factory=list)
    inverted: bool = False
    revealed_assumption: str = ""
    completed: bool = False

    def to_dict(self) -> Dict[str, object]:
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "current_step": self.current_step,
            "participant_assumption": self.participant_assumption,
            "proposals": [{"text": p.text, "inverted": p.inverted} for p in self.proposals],
            "inverted": self.inverted,
            "revealed_assumption": self.revealed_assumption,
            "completed": self.completed,
        }


class FirstContactEngine:
    """Guides a first-time user through axiom inversion."""

    STEPS = ["welcome", "assumption", "invert", "reveal", "complete"]

    def __init__(self) -> None:
        self.sessions: Dict[str, FirstContactSession] = {}

    def start(self) -> Dict[str, object]:
        session = FirstContactSession()
        self.sessions[session.session_id] = session
        return self._persist(session).to_dict()

    def advance(self, session_id: str, payload: Dict[str, Any]) -> Dict[str, object]:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError("session_not_found")
        step = str(payload.get("step") or session.current_step).strip().lower()
        if step not in self.STEPS:
            step = session.current_step
        text = str(payload.get("text", "")).strip()
        if step == "assumption":
            session.participant_assumption = text
            session.current_step = "invert"
        elif step == "invert":
            if text:
                session.proposals.append(AxiomProposal(text=text))
            session.inverted = True
            session.current_step = "reveal"
        elif step == "reveal":
            session.revealed_assumption = text
            session.completed = True
            session.current_step = "complete"
        return self._persist(session).to_dict()

    def status(self, session_id: str) -> Dict[str, object]:
        session = self.sessions.get(session_id)
        if session is None:
            raise KeyError("session_not_found")
        return session.to_dict()

    def _persist(self, session: FirstContactSession) -> FirstContactSession:
        try:
            _SESSION_PATH.parent.mkdir(parents=True, exist_ok=True)
            with _SESSION_PATH.open("a", encoding="utf-8") as f:
                f.write(json.dumps(session.to_dict()) + "\n")
        except Exception:
            pass
        return session
