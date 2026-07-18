from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

import cognitive_compiler.career_harness_v1 as career_mod
import cognitive_compiler.meta_router_v2 as router_mod
import importlib
from msb_v2.api.web import create_app

REPO = Path("/Users/lordwilson/msb-v2").resolve()


def run_case(name, fn):
    import traceback

    print(f"\nTEST: {name}")
    try:
        fn()
        print("PASS: " + name)
    except Exception as e:
        print("FAIL: " + name + " -> " + repr(e))
        traceback.print_exc()


def test_health_when_ready(tmp_path):
    import cognitive_compiler.career_harness_v1 as mod
    career_tmp = tmp_path / "career"
    career_tmp.mkdir(parents=True, exist_ok=True)
    (career_tmp / "cv.md").write_text("me", encoding="utf-8")
    modes = career_tmp / "modes"
    modes.mkdir(parents=True, exist_ok=True)
    (modes / "_shared.md").write_text("ok", encoding="utf-8")
    (modes / "oferta.md").write_text("ok", encoding="utf-8")
    saved_root = mod.PROJECT_ROOT
    mod.PROJECT_ROOT = career_tmp
    try:
        app = create_app()
        client = TestClient(app)
        r = client.get("/career/health")
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["ok"] is True, body
        assert body["event"] == "health"
    finally:
        mod.PROJECT_ROOT = saved_root


def test_evaluate_stub_creates_report(tmp_path):
    import cognitive_compiler.career_harness_v1 as mod
    career_tmp = tmp_path / "career"
    career_tmp.mkdir(parents=True, exist_ok=True)
    (career_tmp / "cv.md").write_text("me", encoding="utf-8")
    modes = career_tmp / "modes"
    modes.mkdir(parents=True, exist_ok=True)
    (modes / "_shared.md").write_text("ok", encoding="utf-8")
    (modes / "oferta.md").write_text("ok", encoding="utf-8")
    (career_tmp / "reports").mkdir(parents=True, exist_ok=True)
    saved_root = mod.PROJECT_ROOT
    mod.PROJECT_ROOT = career_tmp
    try:
        app = create_app()
        client = TestClient(app)
        r = client.post(
            "/career/evaluate",
            json={"company": "Acme", "role": "AI Engineer", "jd_text": "jd text", "score": 4.2},
        )
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["ok"] is True, body
        assert body["event"] == "evaluated", body
        assert body["report"].endswith(".md"), body
        assert body["score"] == 4.2
        assert body["status"] == "Evaluated"
        report_path = career_tmp / body["report"]
        assert report_path.exists(), report_path
        assert (career_tmp / "data" / "applications.md").exists()
    finally:
        mod.PROJECT_ROOT = saved_root


def test_meta_router_classifies_career():
    importlib.reload(router_mod)
    m = router_mod.MetaRoutingHarness()
    out = m.execute("evaluate this senior AI engineer job offer and scan portals")
    assert out.decision.primary == "career"
    assert out.decision.confidence >= 0.7
