from __future__ import annotations

import asyncio

from msb_v2.aura.toolbelt import Toolbelt
from msb_v2.aura.aura_core import AURACore
from msb_v2.security.identity import AccessControl, Identity


def test_aura_core_wires_identity_to_toolbelt() -> None:
    toolbelt = Toolbelt()
    toolbelt._access_control = AccessControl()
    toolbelt._access_control.register("user-1", Identity(role="editor", name="Alice"))
    toolbelt._access_control.role_grants["editor"] = ["echo"]
    core = AURACore(toolbelt=toolbelt)
    state = asyncio.run(core.run(goal="say hello", session_id="acl-ok", identity_id="user-1"))
    assert state.current_goal == "say hello"


def test_aura_core_denies_tool_for_unknown_identity() -> None:
    toolbelt = Toolbelt()
    toolbelt._access_control = AccessControl()
    toolbelt._access_control.register("user-1", Identity(role="editor", name="Alice"))
    toolbelt._access_control.role_grants["editor"] = ["echo"]
    core = AURACore(toolbelt=toolbelt)
    try:
        asyncio.run(core.run(goal="say hello", session_id="acl-fail", identity_id="user-2"))
    except RuntimeError as exc:
        assert "identity 'user-2' cannot use" in str(exc)
