"""Null-torsion heartbeat for the live substrate."""
from __future__ import annotations

import json
import time
from typing import Any, Dict
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


HEALTH_URL = "http://127.0.0.1:8766/health"
INTERVAL_SECONDS = 60


def probe(timeout: int = 5) -> Dict[str, Any]:
    payload = {"timestamp": time.time(), "target": HEALTH_URL}
    try:
        with urlopen(Request(HEALTH_URL), timeout=timeout) as resp:
            payload["status_code"] = resp.status
            payload["body"] = json.loads(resp.read().decode("utf-8", "ignore"))
            payload["status"] = "ok"
    except HTTPError as exc:
        payload["status"] = "error"
        payload["status_code"] = exc.code
        payload["error"] = str(exc)
    except URLError as exc:
        payload["status"] = "error"
        payload["status_code"] = None
        payload["error"] = str(exc.reason)
    return payload
