"""Evolution memory with causal skip guard."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from msb_v2.evolution.proposal import EvolutionProposal


class EvolutionMemory:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS proposals (
                  proposal_id TEXT PRIMARY KEY,
                  title TEXT,
                  affected_modules TEXT,
                  rationale TEXT,
                  risk TEXT,
                  status TEXT,
                  created_at TEXT,
                  simulation TEXT,
                  approval_status TEXT,
                  failure_reason TEXT,
                  rollback_ref TEXT
                )
                """
            )
            try:
                conn.execute("ALTER TABLE proposals ADD COLUMN fingerprint TEXT")
            except Exception:
                pass
            try:
                conn.execute("ALTER TABLE proposals ADD COLUMN target TEXT")
            except Exception:
                pass
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS history (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  proposal_id TEXT,
                  event TEXT,
                  ts TEXT
                )
                """
            )
            conn.commit()

    def record(self, proposal: EvolutionProposal, fingerprint: str = "", target: str = "") -> None:
        with self._lock:
            with sqlite3.connect(self.path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO proposals
                    (proposal_id, title, affected_modules, rationale, risk, status, created_at, simulation, approval_status, failure_reason, rollback_ref, fingerprint, target)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        proposal.proposal_id,
                        proposal.title,
                        json.dumps(proposal.affected_modules),
                        proposal.rationale,
                        proposal.risk,
                        proposal.status,
                        proposal.created_at,
                        json.dumps(getattr(proposal, "simulation", None)),
                        proposal.approval_status,
                        proposal.failure_reason,
                        proposal.rollback_ref,
                        fingerprint or getattr(proposal, "fingerprint", None) or self._fingerprint(proposal),
                        target or getattr(proposal, "target", None) or (proposal.affected_modules[0] if proposal.affected_modules else ""),
                    ),
                )
                conn.execute("INSERT INTO history (proposal_id, event, ts) VALUES (?, ?, ?)", (proposal.proposal_id, "recorded", datetime.now(timezone.utc).isoformat()))
                conn.commit()

    def get(self, proposal_id: str) -> Optional[EvolutionProposal]:
        with self._lock:
            with sqlite3.connect(self.path) as conn:
                row = conn.execute("SELECT * FROM proposals WHERE proposal_id = ?", (proposal_id,)).fetchone()
                if not row:
                    return None
        return self._row_to_proposal(row)

    def history(self, proposal_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            with sqlite3.connect(self.path) as conn:
                rows = conn.execute("SELECT event, ts FROM history WHERE proposal_id = ? ORDER BY id DESC", (proposal_id,)).fetchall()
                return [{"event": r[0], "ts": r[1]} for r in rows]

    def all(self) -> List[Dict[str, Any]]:
        with self._lock:
            with sqlite3.connect(self.path) as conn:
                rows = conn.execute("SELECT * FROM proposals ORDER BY created_at DESC").fetchall()
                return [self._row_to_dict(r) for r in rows]

    def latest(self, count: int = 1) -> List[Dict[str, Any]]:
        with self._lock:
            with sqlite3.connect(self.path) as conn:
                rows = conn.execute("SELECT * FROM proposals ORDER BY created_at DESC LIMIT ?", (count,)).fetchall()
                return [self._row_to_dict(r) for r in rows]

    def _row_to_dict(self, row: Any) -> Dict[str, Any]:
        return {
            "proposal_id": row[0],
            "title": row[1],
            "affected_modules": json.loads(row[2]),
            "rationale": row[3],
            "risk": row[4],
            "status": row[5],
            "created_at": row[6],
            "simulation": json.loads(row[7]) if row[7] else None,
            "approval_status": row[8],
            "failure_reason": row[9],
            "rollback_ref": row[10],
            "fingerprint": row[11] if len(row) > 11 else None,
            "target": row[12] if len(row) > 12 else None,
        }

    def should_skip(self, target: str, fingerprint: str) -> bool:
        if not fingerprint or not target:
            return False
        with self._lock:
            with sqlite3.connect(self.path) as conn:
                row = conn.execute(
                    "SELECT COUNT(*) FROM proposals WHERE target = ? AND fingerprint = ? AND status IN ('failed','rolled_back')",
                    (target, fingerprint),
                ).fetchone()
        return bool(row and row[0])

    @staticmethod
    def _fingerprint(proposal: EvolutionProposal) -> str:
        basis = "|".join(
            [
                proposal.title or "",
                json.dumps(proposal.affected_modules),
                proposal.rationale or "",
                proposal.risk or "",
                proposal.approval_status or "",
                proposal.failure_reason or "",
                proposal.rollback_ref or "",
            ]
        )
        return hashlib.sha256(basis.encode("utf-8")).hexdigest()

    def _row_to_proposal(self, row: Any) -> EvolutionProposal:
        return EvolutionProposal(
            proposal_id=row[0],
            title=row[1],
            affected_modules=json.loads(row[2]),
            rationale=row[3],
            risk=row[4],
            status=row[5],
            created_at=row[6],
            simulation=json.loads(row[7]) if row[7] else None,
            approval_status=row[8],
            failure_reason=row[9],
            rollback_ref=row[10] if len(row) > 10 else None,
        )
