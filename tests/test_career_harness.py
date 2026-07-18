from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path("/Users/lordwilson/msb-v2").resolve()


def test_empty_cv_returns_still_plans(tmp_path):
    import importlib
    import cognitive_compiler.career_harness_v1 as mod
    importlib.reload(mod)
    h = mod.CareerHarness(project_root=tmp_path)
    out = h.plan("evaluate Acme AI role")
    assert out["ok"] is False
    assert "missing" in out


def test_evaluate_without_prereqs(tmp_path):
    import cognitive_compiler.career_harness_v1 as mod
    import importlib
    importlib.reload(mod)
    h = mod.CareerHarness(project_root=tmp_path)
    r = h.evaluate_jd_text("Acme", "AI Engineer", "fake jd")
    assert r.ok is False
    assert r.event == "blocked"


def test_evaluate_creates_report_and_tracker(tmp_path):
    import cognitive_compiler.career_harness_v1 as mod
    import importlib
    (tmp_path / "cv.md").write_text("me", encoding="utf-8")
    modes = tmp_path / "modes"
    modes.mkdir(parents=True, exist_ok=True)
    (modes / "_shared.md").write_text("ok", encoding="utf-8")
    (modes / "oferta.md").write_text("ok", encoding="utf-8")
    (tmp_path / "reports").mkdir(parents=True, exist_ok=True)
    importlib.reload(mod)
    h = mod.CareerHarness(project_root=tmp_path)
    out = h.evaluate_jd_text("Acme", "AI Engineer", "jd text", score=4.2)
    assert out.ok is True
    assert out.event == "evaluated"
    assert out.payload["score"] == 4.2
    assert out.payload["status"] == "Evaluated"
    report_path = tmp_path / out.payload["report"]
    assert report_path.exists()
    tracker = tmp_path / "data" / "applications.md"
    assert tracker.exists()
