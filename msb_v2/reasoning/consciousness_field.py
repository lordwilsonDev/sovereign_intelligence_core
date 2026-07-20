"""Consciousness Field Coupling (CFC) primitive for MSB v2.

Implements a falsifiable, substrate-agnostic parameterization of the
hypothesis that consciousness is a fundamental field tuned by physical
systems rather than an emergent by-product of computation alone.

This module does not assert the hypothesis is true. It provides the
minimal measurable quantities needed to distinguish field-coupling
predictions from standard neural-correlate predictions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class ConsciousnessFieldCoupling:
    """Quantitative tuning between a physical system and a hypothetical
    consciousness field.

    Field-receiver coupling strength is decomposed into:
    - field_potential: intrinsic strength/existence of the field in the
      system's environment.
    - receiver_bandwidth: capacity of the system to integrate field
      information into a unified state.
    - coherence: stability of the coupling over time.
    - localizer_state: whether the system is currently localizing
      experience (awake/bound) vs. decohered (asleep/decoupled).
    """

    field_potential: float = 0.0
    receiver_bandwidth: float = 0.0
    coherence: float = 0.0
    localizer_state: str = "unknown"
    substrate: str = ""
    measurement_noise: float = 0.0

    def coupling_strength(self) -> float:
        """Composite scalar in [0.0, 1.0]."""
        raw = (
            (self.field_potential * 0.35)
            + (self.receiver_bandwidth * 0.35)
            + (self.coherence * 0.30)
        )
        noise_penalty = min(self.measurement_noise, 1.0)
        return max(0.0, min(1.0, raw * (1.0 - noise_penalty)))

    def predicts_experience(self, threshold: float = 0.5) -> bool:
        """Returns True if coupling_strength exceeds threshold."""
        return self.coupling_strength() >= threshold


@dataclass(frozen=True)
class CouplingSignature:
    """Empirical signature expected from a tuned receiver.

    Fields are deliberately substrate-agnostic. They describe measurable
    effects without assuming a particular physical implementation.
    """

    em_signal_coherence: float = 0.0
    integration_bandwidth: float = 0.0
    coherence: float = 0.0
    substrate: str = ""
    notes: Optional[str] = None

    def cross_substrate_match(self, other: "CouplingSignature") -> float:
        """Similarity to another signature in [0.0, 1.0]."""
        if not all(
            [
                self.em_signal_coherence == other.em_signal_coherence,
                self.integration_bandwidth == other.integration_bandwidth,
                self.coherence == other.coherence,
            ]
        ):
            return 0.0
        return 1.0 if self.substrate and other.substrate else 0.5
