from __future__ import annotations

from typing import Any


def _try_smart_crusher(content: Any) -> bytes | None:
    try:
        from headroom.transport.compression import SmartCrusher  # type: ignore[import]
        if isinstance(content, bytes):
            raw = content
        elif hasattr(content, "encode"):
            raw = content.encode("utf-8")
        else:
            import json
            raw = json.dumps(content, default=str).encode("utf-8")
        return SmartCrusher().crush(raw)
    except Exception:
        return None


def _try_code_compressor(content: Any, ctype: str | None = None) -> bytes | None:
    try:
        from headroom.transport.compression import CodeCompressor  # type: ignore[import]
        if isinstance(content, bytes):
            raw = content
        elif hasattr(content, "encode"):
            raw = content.encode("utf-8")
        else:
            import json
            raw = json.dumps(content, default=str).encode("utf-8")
        level = ctype or "default"
        return CodeCompressor(level=level).compress(raw)
    except Exception:
        return None


def compress_content(ctype: str, bytes_or_str: bytes | str) -> bytes:
    if isinstance(bytes_or_str, str):
        payload: bytes = bytes_or_str.encode("utf-8")
    else:
        payload = bytes_or_str

    compressed = _try_smart_crusher(payload)
    if compressed is not None:
        return compressed

    compressed = _try_code_compressor(payload, ctype=ctype)
    if compressed is not None:
        return compressed

    return payload
