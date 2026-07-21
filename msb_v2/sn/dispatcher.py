from __future__ import annotations

from typing import Any, Dict, List

from msb_v2.sn.models import NotificationRequest, NotificationResponse


class Dispatcher:
    def dispatch(self, request: NotificationRequest, rendered: str) -> List[NotificationResponse]:
        responses: List[NotificationResponse] = []
        for channel in request.channels or ["console"]:
            status = self._send(channel, request, rendered)
            responses.append(status)
        return responses

    def _send(self, channel: str, request: NotificationRequest, rendered: str) -> NotificationResponse:
        if channel == "telegram":
            return self._send_telegram(request, rendered)
        if channel == "email":
            return self._send_email(request, rendered)
        if channel == "slack":
            return self._send_slack(request, rendered)
        print(f"[SNH] {request.source} | {request.template} | {rendered}")
        return NotificationResponse(id=request.template, status="sent", channel="console")

    def _send_telegram(self, request: NotificationRequest, rendered: str) -> NotificationResponse:
        try:
            from msb_v2.gateway.telegram_gateway import send_telegram_message
            send_telegram_message(rendered)
            return NotificationResponse(id=request.template, status="sent", channel="telegram")
        except Exception as exc:  # pragma: no cover - defensive
            return NotificationResponse(id=request.template, status="failed", channel="telegram", detail=str(exc))

    def _send_email(self, request: NotificationRequest, rendered: str) -> NotificationResponse:
        return NotificationResponse(id=request.template, status="skipped", channel="email", detail="email not configured")

    def _send_slack(self, request: NotificationRequest, rendered: str) -> NotificationResponse:
        return NotificationResponse(id=request.template, status="skipped", channel="slack", detail="slack webhook not configured")
