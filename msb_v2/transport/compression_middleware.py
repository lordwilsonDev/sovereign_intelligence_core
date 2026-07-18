from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from msb_v2.transport.compression import compress_content


class ResponseCompressionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, threshold: int = 2000) -> None:
        super().__init__(app)
        self._threshold = threshold

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        if response.status_code < 200 or response.status_code >= 300:
            return response
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        if len(body) > self._threshold:
            compressed = compress_content("transport", body)
            if compressed is not None and len(compressed) < len(body):
                body = compressed
        return Response(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
            background=response.background,
        )
