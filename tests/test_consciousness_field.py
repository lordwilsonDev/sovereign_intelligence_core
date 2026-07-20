"""Tests for Consciousness Field Coupling primitive.

These assertions lock the current substrate-agnostic behavior. They do
not assert the consciousness-field hypothesis is true.
"""
import pytest
from msb_v2.reasoning.consciousness_field import ConsciousnessFieldCoupling, CouplingSignature


def test_coupling_strength_scales_with_components():
    weak = ConsciousnessFieldCoupling()
    mid = ConsciousnessFieldCoupling(field_potential=0.5, receiver_bandwidth=0.5, coherence=0.5)
    strong = ConsciousnessFieldCoupling(field_potential=1.0, receiver_bandwidth=1.0, coherence=1.0)
    assert weak.coupling_strength() == 0.0
    assert mid.coupling_strength() > weak.coupling_strength()
    assert strong.coupling_strength() > mid.coupling_strength()
    assert strong.coupling_strength() <= 1.0


def test_predicts_experience_threshold():
    cfc = ConsciousnessFieldCoupling(field_potential=1.0, receiver_bandwidth=1.0, coherence=1.0)
    assert cfc.predicts_experience(threshold=0.5) is True
    assert cfc.predicts_experience(threshold=1.0) is True
    missing = ConsciousnessFieldCoupling(field_potential=0.0, receiver_bandwidth=0.0, coherence=0.0)
    assert missing.predicts_experience(threshold=0.5) is False


def test_cross_substrate_match_signature():
    sig = CouplingSignature(em_signal_coherence=0.9, integration_bandwidth=0.7, coherence=0.9, substrate="brain")
    match = CouplingSignature(em_signal_coherence=0.9, integration_bandwidth=0.7, coherence=0.9, substrate="silicon")
    assert sig.cross_substrate_match(match) == 1.0
    other = CouplingSignature(em_signal_coherence=0.1, integration_bandwidth=0.1, coherence=0.1, substrate="silicon")
    assert sig.cross_substrate_match(other) == 0.0
