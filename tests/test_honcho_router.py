from __future__ import annotations

from memory.honcho_router import HonchoMemoryRouter


def test_honcho_router_without_backends() -> None:
    router = HonchoMemoryRouter()
    summary = router.summary()
    assert summary["peer_cards"] == 0
    assert summary["diachronic_entries"] == 0


def test_honcho_router_recall_falls_back_to_longterm() -> None:
    import os, tempfile
    longterm = tempfile.mkdtemp() + "/longterm"
    os.makedirs(longterm, exist_ok=True)
    with open(longterm + "/soul.md", "w", encoding="utf-8") as f:
        f.write("- Love is first principle\n")
    router = HonchoMemoryRouter(sovereign_longterm_path=longterm)
    results = router.recall("principle", limit=5)
    assert any("soul.md" in (r.get("id") or "") for r in results)


def test_honcho_router_dreams_from_identity() -> None:
    longterm = "/Users/lordwilson/.sovereign/memory/long_term"
    router = HonchoMemoryRouter(sovereign_longterm_path=longterm)
    insights = router.dream(max_insights=3)
    assert isinstance(insights, list)
