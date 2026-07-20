from __future__ import annotations

import os
from typing import Any, Generator

import pytest

from msb_v2.api.middleware import set_local_bypass
from msb_v2.api.web import create_app
from starlette.testclient import TestClient


@pytest.fixture()
def app_no_bypass() -> Generator[Any, None, None]:
    set_local_bypass(None)
    application = create_app()
    yield application
    set_local_bypass(None)


def test_memory_search_route_exists(app_no_bypass: Any) -> None:
    client = TestClient(app_no_bypass)
    response = client.get("/memory/search")
    assert response.status_code == 200
    body = response.json()
    assert "query" in body
    assert "results" in body
