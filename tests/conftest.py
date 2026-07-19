from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def local_auth_bypass(monkeypatch: "pytest.MonkeyPatch") -> None:
    monkeypatch.setenv("MSB_AUTH_LOCAL_BYPASS", "1")
