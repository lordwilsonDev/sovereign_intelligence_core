"""Axiom Library store tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from msb_v2.axiom_library.store import AxiomLibraryStore, AxiomRecord


@pytest.fixture()
def store(tmp_path: Path):
    s = AxiomLibraryStore(dir=tmp_path)
    yield s
    s.close()


def test_ingest_returns_envelope(store: AxiomLibraryStore) -> None:
    record = AxiomRecord(source="test", axiom="x", inversion="not x")
    out = store.ingest(record)
    assert out["status"] == "ingested"
    assert out["id"]
    assert out["merkle_root"]


def test_round_trip_and_search(store: AxiomLibraryStore) -> None:
    record = AxiomRecord(source="test", axiom="sovereign default", inversion="sovereign not default", topic="sovereignty")
    out = store.ingest(record)
    axiom_id = out["id"]
    fetched = store.get(axiom_id)
    assert fetched is not None
    assert fetched["source"] == "test"
    assert fetched["topic"] == "sovereignty"
    assert "sovereign" in store.search("sovereign default")[0]["axiom"]


def test_chained_merkle_roots_change(store: AxiomLibraryStore) -> None:
    a = AxiomRecord(source="a", axiom="a", inversion="b")
    b = AxiomRecord(source="b", axiom="a2", inversion="b2")
    oa = store.ingest(a)
    ob = store.ingest(b)
    assert oa["merkle_root"] != ob["merkle_root"]


def test_recent_and_count(store: AxiomLibraryStore) -> None:
    for i in range(3):
        store.ingest(AxiomRecord(source=str(i), axiom=f"a{i}", inversion=f"b{i}"))
    assert store.count() == 3
    assert len(store.recent(limit=2)) == 2


def test_random_returns_record(store: AxiomLibraryStore) -> None:
    store.ingest(AxiomRecord(source="r", axiom="r", inversion="not r"))
    assert store.random()["source"] == "r"
