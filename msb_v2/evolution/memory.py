from __future__ import annotations

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

    def record(self, proposal: EvolutionProposal) -> None:
        with self._lock:
            with sqlite3.connect(self.path) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO proposals
                    (proposal_id, title, affected_modules, rationale, risk, status, created_at, simulation, approval_status, failure_reason, rollback_ref)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        proposal.proposal_id,
                        proposal.title,
                        json.dumps(proposal.affected_modules),
                        proposal.rationale,
                        proposal.risk,
                        proposal.status,
                        proposal.created_at,
                        json.dumps(proposal.simulation),
                        proposal.approval_status,
                        proposal.failure_reason,
                        proposal.rollback_ref,
                    ),
                )
                conn.execute(
                    "INSERT INTO history (proposal_id, event, ts) VALUES (?, ?, ?)",
                    (proposal.proposal_id, "recorded", datetime.now(timezone.utc).isoformat()),
                )
                conn.commit()

    def get(self, proposal_id: str) -> Optional[EvolutionProposal]:
        with self._lock:
            with sqlite3.connect(self.path) as conn:
                row = conn.execute("SELECT * FROM proposals WHERE proposal_id = ?", (proposal_id,)).fetchone()
                if not row:
                    return None
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
                    rollback_ref=row[10],
                )

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
        }
