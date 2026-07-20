from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

logger = logging.getLogger("msb_v2.memory.honcho_router")


@dataclass
class PeerCard:
    peer_id: str
    label: str
    relation: str
    trust: float = 0.5
    last_seen: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)


@dataclass
class DiachronicEntry:
    key: str
    value: Any
    timestamp: datetime = field(default_factory=datetime.now)
    strength: float = 0.5
    ttl_days: Optional[int] = None
    expired: bool = False


class HonchoMemoryRouter:
    """
    Unified memory router with diachronic identity, peer cards, and 'dream' processing.
    Backends:
      - msb_backend: MSB v2 PersistentMemoryStore
      - hermes_backend: optional callable returning memory/search results
      - sovereign_longterm_path: path to .sovereign/memory long-term identity + dreams
    """

    def __init__(
        self,
        msb_backend: Optional[Any] = None,
        hermes_backend: Optional[Any] = None,
        sovereign_longterm_path: Optional[str] = None,
    ) -> None:
        self.msb = msb_backend
        self.hermes = hermes_backend
        self.longterm_path = Path(sovereign_longterm_path) if sovereign_longterm_path else None
        self._identity: Dict[str, Any] = {}
        self.peer_cards: Dict[str, PeerCard] = {}
        self.diachronic: Dict[str, DiachronicEntry] = {}
        self.dreams: List[Dict[str, Any]] = []
        self._load_identity()

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------
    def _load_identity(self) -> None:
        if not self.longterm_path:
            return
        for candidate in [self.longterm_path / "soul.md", self.longterm_path / "identity.md"]:
            if candidate.exists():
                try:
                    text = candidate.read_text(encoding="utf-8", errors="ignore")
                    self._identity[candidate.stem] = text
                except Exception as exc:
                    logger.warning("honcho_router.identity_read_failed path=%s err=%s", candidate, exc)

    def identity(self) -> Dict[str, Any]:
        return dict(self._identity)

    # ------------------------------------------------------------------
    # Ingest / recall
    # ------------------------------------------------------------------
    def ingest(
        self,
        *,
        source: str = "unknown",
        content: str = "",
        memory_type: str = "episodic",
        importance: float = 0.5,
        tags: Optional[Sequence[str]] = None,
        peer_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        item: Dict[str, Any] = {
            "source": source,
            "content": content,
            "kind": memory_type,
            "importance": importance,
            "tags": list(tags or []),
            "timestamp": datetime.now().isoformat(),
        }
        if peer_id:
            self._touch_peer(peer_id, label=peer_id, relation="partner", tags=list(tags or []))
        ingested_at = self.msb.ingest(item) if self.msb is not None else self._hermes_ingest(item)
        item["ingested_at"] = ingested_at if isinstance(ingested_at, str) else datetime.now().isoformat()
        return item

    def recall(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        if self.msb is not None:
            try:
                raw = self.msb.search(query, limit=limit)
                for r in raw:
                    results.append({
                        "id": getattr(r, "id", None),
                        "kind": getattr(r, "kind", None),
                        "content": getattr(r, "content", None),
                        "source": "msb",
                    })
            except Exception as exc:
                logger.warning("honcho_router.msb_search_failed: %s", exc)
        if not results and self.hermes is not None:
            results = self._hermes_recall(query, limit=limit)
        results.extend(self._longterm_recall(query, limit=max(1, limit - len(results))))
        return results[:limit]

    # ------------------------------------------------------------------
    # Diachronic / curation
    # ------------------------------------------------------------------
    def upsert_diachronic(self, key: str, value: Any, strength: float = 0.5, ttl_days: Optional[int] = None) -> DiachronicEntry:
        existing = self.diachronic.get(key)
        if existing and existing.expired:
            strength = max(existing.strength, strength)
        entry = DiachronicEntry(key=key, value=value, strength=strength, ttl_days=ttl_days)
        self.diachronic[key] = entry
        return entry

    def decay_diachronic(self, age_days: float) -> List[str]:
        expired = []
        for key, entry in list(self.diachronic.items()):
            if entry.ttl_days is not None and age_days > entry.ttl_days:
                entry.expired = True
                expired.append(key)
            else:
                entry.strength = max(0.0, entry.strength * (0.98 ** age_days))
        return expired

    def prune(self) -> Dict[str, Any]:
        expired = self.decay_diachronic(age_days=30.0)
        peers_to_remove = [k for k, v in self.peer_cards.items() if v.trust <= 0.05]
        for k in peers_to_remove:
            self.peer_cards.pop(k, None)
        return {"expired_diachronic": expired, "pruned_peers": peers_to_remove}

    def consolidate(self, kind: str, min_items: int = 3) -> List[Dict[str, Any]]:
        if self.msb is None:
            return []
        try:
            summaries = self.msb.consolidate(kind, min_items=min_items)
            return [
                {
                    "id": getattr(s, "id", None),
                    "kind": getattr(s, "kind", kind),
                    "content": getattr(s, "content", ""),
                }
                for s in summaries
            ]
        except Exception as exc:
            logger.debug("honcho_router.consolidate_failed: %s", exc)
            return []

    # ------------------------------------------------------------------
    # Dreaming / dreaming-like aggregation from long-term identity notes
    # ------------------------------------------------------------------
    def dream(self, max_insights: int = 12) -> List[Dict[str, Any]]:
        insights: List[Dict[str, Any]] = []
        for key, text in self._identity.items():
            lines = [line.strip() for line in text.splitlines() if line.strip().startswith("- ")]
            for line in lines[:max_insights]:
                insights.append({"source": key, "insight": line, "kind": "identity_dream"})
        insights.extend({"source": "dream", "insight": d, "kind": "dream"} for d in self.dreams[-max_insights:])
        self.dreams.extend(insights[:max_insights])
        return insights[:max_insights]

    def summary(self) -> Dict[str, Any]:
        return {
            "identity_keys": sorted(self._identity.keys()),
            "peer_cards": len(self.peer_cards),
            "diachronic_entries": len(self.diachronic),
            "dream_insights": len(self.dreams),
            "msb_backend": self.msb is not None,
            "hermes_backend": self.hermes is not None,
            "sovereign_longterm_path": str(self.longterm_path) if self.longterm_path else None,
        }

    # ------------------------------------------------------------------
    # Backends
    # ------------------------------------------------------------------
    def _hermes_ingest(self, item: Dict[str, Any]) -> str:
        if self.hermes is None:
            return datetime.now().isoformat()
        if hasattr(self.hermes, "add"):
            try:
                return str(self.hermes.add({**item, "id": item.get("id") or _stable_id(item)}))
            except Exception as exc:
                logger.debug("honcho_router.hermes_add_failed: %s", exc)
        return datetime.now().isoformat()

    def _hermes_recall(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        if self.hermes is None:
            return []
        if hasattr(self.hermes, "search"):
            try:
                results = self.hermes.search(query, limit=limit)
                out: List[Dict[str, Any]] = []
                for r in results:
                    if isinstance(r, dict):
                        out.append(r)
                    else:
                        out.append({"id": getattr(r, "id", None), "content": getattr(r, "content", str(r)), "source": "hermes"})
                return out
            except Exception as exc:
                logger.debug("honcho_router.hermes_search_failed: %s", exc)
        return []

    def _longterm_recall(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        if not self.longterm_path:
            return []
        q = query.casefold()
        out: List[Dict[str, Any]] = []
        for path in sorted(self.longterm_path.rglob("*.md")):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore").casefold()
            except Exception:
                continue
            if q in text:
                out.append({"id": str(path), "content": str(path.name), "source": "sovereign_longterm"})
            if len(out) >= limit:
                break
        return out

    def _touch_peer(self, peer_id: str, *, label: str, relation: str, tags: List[str]) -> PeerCard:
        card = self.peer_cards.get(peer_id)
        if card is None:
            card = PeerCard(peer_id=peer_id, label=label, relation=relation, tags=tags)
            self.peer_cards[peer_id] = card
        else:
            card.last_seen = datetime.now()
            if tags:
                card.tags = list(set(card.tags).union(tags))
        return card


def _stable_id(item: Dict[str, Any]) -> str:
    raw = f"{item.get('source','unknown')}:{item.get('content','')}:{item.get('timestamp','')}"
    import hashlib
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
