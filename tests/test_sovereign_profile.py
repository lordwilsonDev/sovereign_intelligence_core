from __future__ import annotations

from msb_v2.security.sovereign import SovereignProfile, get_sovereign_profile


def test_default_sovereign_profile_airgapped() -> None:
    profile = get_sovereign_profile()
    assert isinstance(profile, SovereignProfile)
    assert profile.airgap is True
    assert profile.telemetry_opt_out is True
    assert profile.capability.allow_exec is False
    assert profile.capability.allow_network is False
    assert profile.identity_role == "default"
    assert isinstance(profile.pubkey_hex, str)
