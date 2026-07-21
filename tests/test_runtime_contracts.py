from __future__ import annotations

import pytest

from msb_v2.runtime.contracts import ContractRegistry, RuntimeContract, registry


def test_registry_singleton() -> None:
    assert registry() is registry()


def test_register_and_get() -> None:
    r = registry()
    r.register(RuntimeContract(name="demo", version="1.0.0"))
    assert r.get("demo").version == "1.0.0"  # type: ignore[union-attr]


def test_missing_key_returns_none() -> None:
    assert registry().get("missing") is None


def test_initialize_all_calls_initialize() -> None:
    calls = []
    r = ContractRegistry()
    r.register(
        RuntimeContract(
            name="c1",
            version="0.1",
            initialize=lambda: calls.append("c1"),
        )
    )
    r.register(
        RuntimeContract(
            name="c2",
            version="0.1",
            initialize=lambda: (_ for _ in ()).throw(RuntimeError("fail")),
        )
    )
    results = r.initialize_all()
    assert results["c1"] is True
    assert results["c2"] is False


def test_shutdown_all_reversed() -> None:
    order = []
    r = ContractRegistry()
    r.register(
        RuntimeContract(
            name="first",
            shutdown=lambda: order.append("first"),
        )
    )
    r.register(
        RuntimeContract(
            name="second",
            shutdown=lambda: order.append("second"),
        )
    )
    r.shutdown_all()
    assert order == ["second", "first"]
