from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass


@pytest.fixture()
def client():
    set_local_bypass(True)
    client = TestClient(create_app())
    yield client
    set_local_bypass(None)


def test_report_html_schema(client):
    response = client.get("/audit/report/html")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "ETag" in response.headers
    assert "Cache-Control" in response.headers


def test_report_html_client_name(client):
    response = client.get("/audit/report/html?client_name=Acme")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"
    assert response.headers["ETag"].startswith('"') and response.headers["ETag"].endswith('"')
    html = response.text
    assert "Acme" in html


def test_report_html_contains_sections(client):
    response = client.get("/audit/report/html")
    assert response.status_code == 200
    html = response.text.lower()
    assert "executive summary" in html
    assert "business impact" in html
    assert "immutable record" in html


def test_report_pdf_schema(client):
    response = client.get("/audit/report/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.headers["Cache-Control"] == "no-store"
    assert "Client_integrity_report.pdf" in response.headers["content-disposition"]


def test_report_pdf_client_name(client):
    response = client.get("/audit/report/pdf?client_name=AcmeCorp")
    assert response.status_code == 200
    assert 'filename="AcmeCorp_integrity_report.pdf"' in response.headers["content-disposition"]
    assert len(response.content) > 0


