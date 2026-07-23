"""Contract test: SAC response shape must match observed live schema."""
import pytest
from fastapi.testclient import TestClient
from msb_v2.api.web import create_app

client = TestClient(create_app())


def test_sac_status_returns_observed_top_level_keys():
    """The /sac/status response must preserve the current live key set."""
    resp = client.get("/sac/status")
    assert resp.status_code == 200
    data = resp.json()
    expected_keys = {"quarantine", "rnr", "eig", "cma", "psa", "sas", "interventions"}
    missing = expected_keys - set(data.keys())
    assert not missing, f"SAC status missing keys: {missing}"


def test_sac_status_sas_score_is_numeric():
    """The sas.score field must be numeric between 0 and 100."""
    resp = client.get("/sac/status")
    data = resp.json()
    sas = data.get("sas")
    assert isinstance(sas, dict), f"sas should be a dict, got {type(sas)}"
    score = sas.get("score")
    assert isinstance(score, (int, float)), f"sas.score should be numeric, got {type(score)}"
    assert 0 <= score <= 100, f"sas.score out of range: {score}"


def test_sac_status_rnr_ratio_is_numeric():
    """The rnr.ratio field must be numeric between 0 and 1."""
    resp = client.get("/sac/status")
    data = resp.json()
    rnr = data.get("rnr")
    assert isinstance(rnr, dict), f"rnr should be a dict, got {type(rnr)}"
    ratio = rnr.get("ratio")
    assert isinstance(ratio, (int, float)), f"rnr.ratio should be numeric, got {type(ratio)}"
    assert 0 <= ratio <= 1, f"rnr.ratio out of range: {ratio}"
