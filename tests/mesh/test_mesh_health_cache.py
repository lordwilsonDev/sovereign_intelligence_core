"""Peer health cache tests."""
from __future__ import annotations

import pytest

from msb_v2.mesh.health_cache import PeerHealthCache


def test_miss_returns_none() -> None:
    cache = PeerHealthCache(ttl_seconds=60)
    assert cache.get("n1", "127.0.0.1", 8766) is None


def test_hit_returns_body() -> None:
    cache = PeerHealthCache(ttl_seconds=60)
    cache.put("n1", "127.0.0.1", 8766, {"ok": True})
    assert cache.get("n1", "127.0.0.1", 8766) == {"ok": True}


def test_expired_entry_returns_none() -> None:
    cache = PeerHealthCache(ttl_seconds=1)
    cache.put("n1", "127.0.0.1", 8766, {"ok": True})
    import time
    time.sleep(1.05)
    assert cache.get("n1", "127.0.0.1", 8766) is None
