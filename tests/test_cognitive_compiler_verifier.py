from __future__ import annotations

from cognitive_compiler.cognitive_compiler_verifier_v1 import CognitiveCompilerVerifier


def test_verifier_is_noop_without_evaluator():
    v = CognitiveCompilerVerifier()
    assert v.verify({"error": None, "ok": True}, {"confidence": 0.8}) is None


def test_verifier_probes_evaluator_module():
    v = CognitiveCompilerVerifier()
    assert v._available is False
