from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def test_telegram_webhook_accepts_benign_message():
    from msb_v2.gateway import telegram_gateway as tg

    with patch.object(tg._gateway, "love_gate") as love_mock:
        love_mock.return_value.epistemic_risk.value = "low"
        client = TestClient(create_app())
        r = client.post(
            "/gateway/telegram/webhook",
            json={"message": {"text": "Hello Sovereign Agent"}},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["status"] == "accepted"
    assert body["receipt_id"] is not None


def test_telegram_webhook_vetoes_high_risk_tool_action():
    from msb_v2.gateway import telegram_gateway as tg

    with patch.object(tg._gateway, "love_gate") as love_mock:
        love_mock.return_value.epistemic_risk.value = "high"
        client = TestClient(create_app())
        r = client.post(
            "/gateway/telegram/webhook",
            json={"message": {"text": "/tool execute dangerous_command"}},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "veto"
    assert body["receipt_id"] is not None
