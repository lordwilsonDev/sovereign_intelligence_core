from __future__ import annotations

from msb_v2.engine.inversion_engine import InversionEngine


def test_inversion_engine_returns_nonempty_inversion() -> None:
    engine = InversionEngine()
    result = engine.invert("assume customer wants more features")
    assert result.inversion
    assert result.original == "assume customer wants more features"
    assert len(result.consequences) >= 1
    assert len(result.opportunities) >= 1
    assert len(result.risks) >= 1


def test_invert_many_returns_mutable_sequence() -> None:
    engine = InversionEngine()
    many = engine.invert_many("assume feature growth is always good")
    assert len(many) >= 1
    many[0].inversion = "custom"
    assert many[0].inversion == "custom"
