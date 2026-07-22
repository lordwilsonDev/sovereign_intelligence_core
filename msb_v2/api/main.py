from __future__ import annotations

import os
import sys
from typing import Any, Dict, Optional

from fastapi.middleware.cors import CORSMiddleware

from msb_v2.api.web import create_app

app = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _parse_args(args: list[str]) -> Dict[str, Optional[str]]:
    result: Dict[str, Optional[str]] = {"cert": None, "key": None}
    for arg in args:
        if arg.startswith("--cert="):
            result["cert"] = arg.split("=", 1)[1]
        elif arg.startswith("--key="):
            result["key"] = arg.split("=", 1)[1]
    return result


def run(host: str = "127.0.0.1", port: int = 8766, reload: bool = False, cert: Optional[str] = None, key: Optional[str] = None) -> str:
    import uvicorn

    kwargs: Dict[str, Any] = {"host": host, "port": port, "reload": reload}
    if cert and key:
        kwargs.update({"ssl_certfile": cert, "ssl_keyfile": key})
        target = f"tls://{host}:{port}"
    else:
        target = f"http://{host}:{port}"
    uvicorn.run(app, **kwargs)
    return target


if __name__ == "__main__":
    run()
