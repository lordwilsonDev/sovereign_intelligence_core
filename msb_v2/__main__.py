from __future__ import annotations

import os
import sys
import uvicorn

if __name__ == "__main__":
    os.environ.setdefault("PYTHONPATH", os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault("MSB_REASONING_SCORER", "1")
    uvicorn.run(
        "msb_v2.api.main:create_app",
        factory=True,
        host=os.getenv("MSB_HOST", "127.0.0.1"),
        port=int(os.getenv("MSB_PORT", "8766")),
        reload=os.getenv("MSB_RELOAD", "0") == "1",
    )
