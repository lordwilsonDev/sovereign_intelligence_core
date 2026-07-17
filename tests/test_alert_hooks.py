from __future__ import annotations

def test_alerts_webhook_ingests_firing_alert():
    from fastapi.testclient import TestClient
    from msb_v2.api.web import create_app
    client = TestClient(create_app())
    payload = {
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "labels": {"alertname": "MSB cognitively weak", "severity": "warning"},
                "annotations": {"summary": "score below 0.6"},
                "startsAt": "2026-07-16T00:00:00Z",
                "endsAt": "2026-07-16T01:00:00Z",
                "fingerprint": "fingerprint-weak",
            }
        ],
        "externalURL": "http://127.0.0.1:9090",
    }
    response = client.post("/alerts/webhook", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["alerts"] == 1
    assert data["events"][0]["kind"] == "alert"
    assert data["events"][0]["alertname"] == "MSB cognitively weak"
    assert data["events"][0]["severity"] == "warning"
    assert data["events"][0]["fingerprint"] == "fingerprint-weak"


def test_alerts_webhook_resolves_empty_alerts():
    from fastapi.testclient import TestClient
    from msb_v2.api.web import create_app
    client = TestClient(create_app())
    response = client.post("/alerts/webhook", json={})
    assert response.status_code == 200
    assert response.json()["alerts"] == 0
