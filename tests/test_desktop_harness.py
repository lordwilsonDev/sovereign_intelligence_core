from __future__ import annotations

import os
import time
import pytest
from cognitive_compiler.desktop_harness_v1 import DesktopHarness


def test_high_risk_keywords_raise_to_high():
    h = DesktopHarness()
    risk = h.risk_assessment("Launch Finder, click menu and send message")
    assert risk["severity"] == "HIGH"
    assert risk["category"] == "automation"
    assert risk["matched"]


def test_observation_keywords_are_medium():
    h = DesktopHarness()
    risk = h.risk_assessment("Search for files and open browser")
    assert risk["severity"] == "MEDIUM"
    assert risk["category"] == "observation"


def test_low_risk_when_no_markers():
    h = DesktopHarness()
    risk = h.risk_assessment("Purple elephant circles moon")
    assert risk["severity"] == "LOW"
    assert risk["category"] == "read-only"


def test_blocked_when_env_incomplete(monkeypatch):
    monkeypatch.setenv("NEURALAGENT_USER_ACCESS_TOKEN", "")
    monkeypatch.setenv("NEURALAGENT_THREAD_ID", "thr")
    h = DesktopHarness(aiagent_dir="/tmp/does-not-exist")
    out = h.execute("Launch app and send message")
    assert out["state"] == "blocked"
    assert out.get("confirm_token") is None


def test_pending_confirmation_with_env_ready(monkeypatch, tmp_path):
    monkeypatch.setenv("NEURALAGENT_USER_ACCESS_TOKEN", "tok")
    monkeypatch.setenv("NEURALAGENT_THREAD_ID", "thr")
    main_py = tmp_path / "main.py"
    main_py.write_text("print('ok')")

    h = DesktopHarness(aiagent_dir=str(tmp_path))
    out = h.execute("Launch app and send message")
    assert out["state"] == "pending_confirmation"
    token = out.get("confirm_token")
    assert token

    approved = h.approve_run(token, approved=True)
    assert approved.get("state") in {"blocked", "error", "completed", "timeout", "running", "pending_confirmation"}

    token2 = h.confirm_token("same goal")
    rejected = h.approve_run(token2, approved=False)
    assert rejected["state"] == "rejected"


def test_invalid_confirm_token():
    h = DesktopHarness()
    out = h.approve_run("missing", approved=True)
    assert out["state"] == "error"
    assert "confirm_token" not in out or out.get("state") == "error"
