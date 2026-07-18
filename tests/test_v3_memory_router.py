from __future__ import annotations

from msb_v2.v3.memory_router import MemoryKind, MemoryRouter, MemoryTier


def test_route_by_kind():
    router = MemoryRouter()
    route = router.route(MemoryKind.WORKING)
    assert route.tier is MemoryTier.RAM
    assert route.max_entries == 200


def test_route_by_access_pattern():
    router = MemoryRouter()
    recent = router.route_by_access_pattern("what happened recently")
    assert recent.kind is MemoryKind.WORKING

    how = router.route_by_access_pattern("how do I restart the server")
    assert how.kind is MemoryKind.PROCEDURAL

    failure = router.route_by_access_pattern("logs from the last failure")
    assert failure.kind is MemoryKind.FAILURE

    generic = router.route_by_access_pattern("physics of superconductors")
    assert generic.kind is MemoryKind.SEMANTIC


def test_summary_returns_routes():
    router = MemoryRouter()
    s = router.summary()
    assert len(s["routes"]) == 8
