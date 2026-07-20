from __future__ import annotations

from typing import Any, Generator

import pytest

from msb_v2.api.continuity import router as continuity_router
from msb_v2.api.middleware import set_local_bypass
from msb_v2.api.web import create_app
from starlette.testclient import TestClient


@pytest.fixture()
def app_with_bypass() -> Generator[Any, None, None]:
    set_local_bypass(True)
    application = create_app()
    yield application
    set_local_bypass(None)


def test_continuity_resume_prompt(app_with_bypass: Any) -> None:
    client = TestClient(app_with_bypass)
    response = client.get("/continuity/resume-prompt")
    assert response.status_code == 200
    body = response.json()
    assert "prompt" in body
    assert "### MSB_SESSION_CONTINUITY_V1 ###" in body["prompt"]


def test_continuity_fidelity(app_with_bypass: Any) -> None:
    client = TestClient(app_with_bypass)
    response = client.get("/continuity/fidelity")
    assert response.status_code == 200
    body = response.json()
    assert "continuity_fidelity" in body
    assert "event_count" in body
    assert "source" in body
