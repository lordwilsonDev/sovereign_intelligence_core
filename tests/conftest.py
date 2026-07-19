from __future__ import annotations

import os

import pytest


@pytest.fixture(autouse=True)
def _local_auth_bypass(monkeypatch: "pytest.MonkeyPatch") -> None:
    monkeypatch.setenv("MSB_AUTH_LOCAL_BYPASS", "1")
