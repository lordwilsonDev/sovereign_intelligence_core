from __future__ import annotations

from typing import Any, Dict

import pytest

from msb_v2.provider.sovereign_provider import SovereignProviderWrapper, ProviderStatus


class DummyProvider:
    def chat(self, messages, max_tokens=256, **kwargs):
        return {"role": "assistant", "content": "ok", "model": "dummy", "latency_ms": 1.0, "tokens": {}}


def test_provider_status_reflects_runtime_state():
    wrapper = SovereignProviderWrapper(DummyProvider(), source_label="test")
    wrapper._quarantine = None

    status = wrapper.status()
    assert isinstance(status, ProviderStatus)
    assert status.source_label == "test"
    assert status.provider_trusted in (True, False)
    assert status.veto_count == 0
    assert status.coherence_avg == 0.0
    assert status.sovereignty_score >= 0.0
    assert status.jitter_min_ms == 5.0
    assert status.jitter_max_ms == 50.0
