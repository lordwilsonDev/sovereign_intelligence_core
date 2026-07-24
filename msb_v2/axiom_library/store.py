"""Axiom Library store — SQLite + JSONL Merkle chain."""
from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


DB_FILENAME = "axiom_library.sqlite"
JSONL_FILENAME = "axiom_chain.jsonl"


@dataclass
class AxiomRecord:
    source: str
    axiom: str
    inversion: str
    predictions: List[str] = field(default_factory=list)
    falsified_count: int = 0
    claim_count: int = 0
    claims_supported: int = 0
    topic: Optional[str] = None
    slug: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    merkle_root: Optional[str] = None
    merkle_parent: Optional[str] = None
    id: Optional[str] = None

    def generated_id(self) -> str:
        payload = json.dumps({
            "source": self.source,
            "axiom": self.axiom,
            "inversion": self.inversion,
            "created_at": self.created_at or datetime.now(timezone.utc).isoformat(),
        }, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


class AxiomLibraryStore:
    def __init__(self, dir: str | Path = Path.home() / "msb-memory"):
        self.dir = Path(dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.dir / DB_FILENAME
        self.jsonl_path = self.dir / JSONL_FILENAME
        self.last_root: Optional[str] = None
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.conn.executescript(
            """
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS axioms (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                axiom TEXT NOT NULL,
                inversion TEXT NOT NULL,
                predictions TEXT DEFAULT '[]',
                falsified_count INTEGER DEFAULT 0,
                claim_count INTEGER DEFAULT 0,
                claims_supported INTEGER DEFAULT 0,
                topic TEXT,
                slug TEXT,
                metadata TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                merkle_root TEXT NOT NULL,
                merkle_parent TEXT
            );
            CREATE TABLE IF NOT EXISTS chains (
                merkle_root TEXT PRIMARY KEY,
                parent TEXT,
                leaf_count INTEGER DEFAULT 1,
                leaf_hash TEXT,
                artifacts TEXT DEFAULT '[]'
            );
            CREATE INDEX IF NOT EXISTS idx_axioms_topic ON axioms(topic);
            CREATE INDEX IF NOT EXISTS idx_axioms_created ON axioms(created_at);
            CREATE VIRTUAL TABLE IF NOT EXISTS axioms_fts USING fts5(source, axiom, inversion, predictions, topic, content=axioms, content_rowid=rowid);
            CREATE TRIGGER IF NOT EXISTS axioms_ai AFTER INSERT ON axioms BEGIN
              INSERT INTO axioms_fts(rowid, source, axiom, inversion, predictions, topic)
              VALUES (new.rowid, new.source, new.axiom, new.inversion, new.predictions, new.topic);
            END;
            CREATE TRIGGER IF NOT EXISTS axioms_ad AFTER DELETE ON axioms BEGIN
              INSERT INTO axioms_fts(axioms_fts, rowid, source, axiom, inversion, predictions, topic)
              VALUES ('delete', old.rowid, old.source, old.axiom, old.inversion, old.predictions, old.topic);
            END;
            CREATE TRIGGER IF NOT EXISTS axioms_au AFTER UPDATE ON axioms BEGIN
              INSERT INTO axioms_fts(axioms_fts, rowid, source, axiom, inversion, predictions, topic)
              VALUES ('delete', old.rowid, old.source, old.axiom, old.inversion, old.predictions, old.topic);
              INSERT INTO axioms_fts(rowid, source, axiom, inversion, predictions, topic)
              VALUES (new.rowid, new.source, new.axiom, new.inversion, new.predictions, new.topic);
            END;
            """
        )
        self.conn.commit()
        row = self.conn.execute("SELECT merkle_root FROM chains ORDER BY rowid DESC LIMIT 1").fetchone()
        self.last_root = row["merkle_root"] if row else None

    def close(self):
        self.conn.close()

    def _next_root(self, record: Dict[str, Any]) -> str:
        payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        leaf_hash = hashlib.sha256(payload).hexdigest()
        if self.last_root:
            combined = hashlib.sha256((self.last_root + leaf_hash).encode()).hexdigest()
            root = combined
        else:
            root = leaf_hash
        return root

    def ingest(self, record: AxiomRecord) -> Dict[str, Any]:
        created_at = record.created_at or datetime.now(timezone.utc).isoformat()
        record.created_at = created_at
        record.id = record.generated_id()
        rec = asdict(record)
        merkle_root = self._next_root(rec)
        record.merkle_root = merkle_root
        record.merkle_parent = self.last_root

        self.conn.execute(
            "INSERT INTO axioms (id, source, axiom, inversion, predictions, falsified_count, claim_count, claims_supported, topic, slug, metadata, created_at, merkle_root, merkle_parent) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                record.id, record.source, record.axiom, record.inversion,
                json.dumps(record.predictions), record.falsified_count,
                record.claim_count, record.claims_supported,
                record.topic, record.slug, json.dumps(record.metadata),
                record.created_at, record.merkle_root, record.merkle_parent,
            ),
        )
        self.conn.execute(
            "INSERT OR REPLACE INTO chains (merkle_root, parent, leaf_count, leaf_hash, artifacts) VALUES (?,?,?,?,?)",
            (merkle_root, record.merkle_parent, 1, record.id, json.dumps([record.id])),
        )
        self.conn.commit()
        self.last_root = merkle_root
        chain_entry = {
            "merkle_root": merkle_root,
            "merkle_parent": record.merkle_parent,
            "leaf_hash": record.id,
            "created_at": created_at,
        }
        self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(chain_entry, sort_keys=True, separators=(",", ":")) + "\n")
        return {"id": record.id, "merkle_root": merkle_root, "status": "ingested"}

    def get(self, axiom_id: str) -> Optional[Dict[str, Any]]:
        row = self.conn.execute("SELECT * FROM axioms WHERE id = ?", (axiom_id,)).fetchone()
        return dict(row) if row else None

    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        safe = query.replace('"', '""').strip()
        if not safe:
            return []
        rows = self.conn.execute(
            "SELECT a.* FROM axioms a JOIN axioms_fts f ON f.rowid = a.rowid WHERE axioms_fts MATCH ? ORDER BY a.created_at DESC LIMIT ?",
            (safe, limit),
        ).fetchall()
        return [dict(r) for r in rows]

    def recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM axioms ORDER BY datetime(created_at) DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]

    def random(self) -> Dict[str, Any]:
        row = self.conn.execute("SELECT * FROM axioms ORDER BY RANDOM() LIMIT 1").fetchone()
        return dict(row) if row else {}

    def count(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) AS c FROM axioms").fetchone()
        return int(row["c"])
