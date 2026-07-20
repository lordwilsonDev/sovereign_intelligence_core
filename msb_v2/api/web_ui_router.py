"""Expose the sovereign web UI under /ui."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import FileResponse

from msb_v2.v3.contracts import HarnessContract, register as _register_contract

router = APIRouter(tags=["ui"])
prefix = "/ui"

_WEB_DIR = Path(__file__).resolve().parent.parent / "sovereign" / "web"


@router.get("/ui/", include_in_schema=False)
def ui_index() -> FileResponse:
    return FileResponse(_WEB_DIR / "index.html")


@router.get("/ui/static/css/style.css", include_in_schema=False)
def ui_css() -> FileResponse:
    return FileResponse(_WEB_DIR / "static" / "css" / "style.css")


@router.get("/ui/static/js/app.js", include_in_schema=False)
def ui_js() -> FileResponse:
    return FileResponse(_WEB_DIR / "static" / "js" / "app.js")


@router.get("/ui/chat", include_in_schema=False)
def ui_chat_redirect(_q: str = "") -> Dict[str, Any]:
    return {
        "chat": "/control/chat",
        "runtime_status": "/control/runtime/status",
        "sac_status": "/sac/status",
        "docs": "/docs",
    }


_register_contract(HarnessContract(route="/ui/", method="get", allow_anonymous=True))
_register_contract(HarnessContract(route="/ui/static/css/style.css", method="get", allow_anonymous=True))
_register_contract(HarnessContract(route="/ui/static/js/app.js", method="get", allow_anonymous=True))
_register_contract(HarnessContract(route="/ui/chat", method="get", allow_anonymous=True))
