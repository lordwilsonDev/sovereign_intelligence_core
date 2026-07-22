from __future__ import annotations

from msb_v2.api.schh import status as status_endpoint, list_components as list_components_endpoint


def test_schh_status_returns_readiness():
    response = status_endpoint()
    assert "system_readiness" in response


def test_schh_components_lists_entries():
    response = list_components_endpoint()
    assert "components" in response
    assert isinstance(response["components"], list)
