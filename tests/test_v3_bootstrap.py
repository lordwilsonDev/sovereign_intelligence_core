from __future__ import annotations

from msb_v2.v3.bootstrap import BootstrapV3, bootstrap_v3


def test_bootstrap_returns_singleton():
    b1 = bootstrap_v3()
    b2 = bootstrap_v3()
    assert b1 is b2


def test_bootstrap_summary_has_all_subsystems():
    b = bootstrap_v3()
    summary = b.summary()
    assert "capabilities" in summary
    assert "memory" in summary
    assert "constraints" in summary
    assert "inversion" in summary


def test_bootstrap_subsystems_are_live():
    b = bootstrap_v3()
    assert hasattr(b, "capabilities")
    assert hasattr(b, "memory_router")
    assert hasattr(b, "constraint_engine")
    assert hasattr(b, "inversion_registry")
