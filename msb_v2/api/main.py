from __future__ import annotations

import os
import sys

from fastapi.middleware.cors import CORSMiddleware

from msb_v2.api.web import create_app
from msb_v2.transport.tls import resolve_tls_paths

app = create_app()


def _parse_args(argv: list[str]) -> dict[str, str | None]:
    args: dict[str, str | None] = {"cert": None, "key": None}
    for item in argv:
        if item.startswith("--cert="):
            args["cert"] = item.split("=", 1)[1]
        if item.startswith("--key="):
            args["key"] = item.split("=", 1)[1]
    return args


def run(cert: str | None = None, key: str | None = None, host: str = "0.0.0.0", port: int = 8765, reload: bool = False) -> str:
    app = create_app()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    tls_pair = resolve_tls_paths(cert, key)
    import uvicorn
    if tls_pair:
        c, k = tls_pair
        uvicorn.run(app, host=host, port=int(port), ssl_certfile=c, ssl_keyfile=k)
        return f"tls://{host}:{port}"
    uvicorn.run(app, host=host, port=int(port), reload=reload)
    return f"http://{host}:{port}"


if __name__ == "__main__":
    parsed = _parse_args(sys.argv[1:])
    run(**parsed, host="0.0.0.0", port=int(os.environ.get("PORT", 8765)))
