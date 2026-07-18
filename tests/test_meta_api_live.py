import os
import sys
from pathlib import Path

REPO = Path("/Users/lordwilson/msb-v2").resolve()
# Scrub Hermes venv / other site-packages pollution so fastapi/pydantic resolve to miniforge.
sys.path = [p for p in sys.path if "/.hermes/" not in p and "/site-packages" not in p]
sys.path.insert(0, str(REPO))
sys.path.insert(0, "/opt/homebrew/Caskroom/miniforge/base/lib/python3.12/site-packages")

from fastapi.testclient import TestClient  # noqa: E402
from msb_v2.api.web import create_app  # noqa: E402


client = TestClient(create_app())


def test_meta_health():
    r = client.get("/meta/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_meta_route_building():
    r = client.post("/meta/route", json={"query": "Design a fault-tolerant event bus", "context": {}})
    assert r.status_code == 200
    body = r.json()
    assert body["routing"]["primary"] == "building"
    assert body["routing"]["confidence"] == 1.0
    assert body["temperature"]["score"] <= 1.0
    assert body["primary_output"] is not None


def test_brain_meta_run_default_intent():
    r = client.post("/brain/meta-run", json={"query": "Design a fault-tolerant event bus", "intent": "default", "trace_id": "trace-1"})
    assert r.status_code == 200
    body = r.json()
    assert body["meta_routing"]["primary"] == "building"
    assert body["temperature"]["score"] <= 1.0


def test_brain_meta_run_research_intent():
    r = client.post("/brain/meta-run", json={"query": "Literature review on causal inference", "intent": "research", "trace_id": "trace-research"})
    assert r.status_code == 200
    body = r.json()
    assert body["intent"] == "research"
    assert body["meta_routing"]["primary"] == "research"


def test_brain_meta_run_complex_reasoning_intent():
    r = client.post("/brain/meta-run", json={"query": "Resolve the ethics/strategy tension in this policy proposal", "intent": "complex_reasoning", "trace_id": "trace-cr"})
    assert r.status_code == 200
    body = r.json()
    assert body["intent"] == "complex_reasoning"
    assert body["meta_routing"]["primary"] == "complex_reasoning"
