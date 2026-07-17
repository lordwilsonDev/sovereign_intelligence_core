from __future__ import annotations

from msb_v2.security.identity import AccessControl, Identity


def test_access_control_registers_and_grants() -> None:
    ac = AccessControl()
    ac.register("user-1", Identity(role="editor", name="Alice"))
    ac.role_grants["editor"] = ["echo", "get_time"]
    assert ac.has_access("user-1", "echo") is True
    assert ac.has_access("user-1", "write_file") is False
    assert ac.has_access("unknown", "echo") is False


def test_access_control_api_for_identities() -> None:
    ac = AccessControl()
    ac.register("user-1", Identity(role="editor", name="Alice"))
    ac.register("user-2", Identity(role="viewer", name="Bob"))
    ac.role_grants["editor"] = ["echo"]
    ac.role_grants["viewer"] = ["get_time"]
    assert ac.has_access("user-1", "get_time") is False
    assert ac.has_access("user-2", "get_time") is True
    assert set(ac.allowed_tools("user-1")) == {"echo"}
    assert set(ac.allowed_tools("user-2")) == {"get_time"}


def test_toolbelt_identity_access_check() -> None:
    from msb_v2.aura.toolbelt import Toolbelt

    toolbelt = Toolbelt()
    toolbelt._access_control = AccessControl()
    toolbelt._access_control.register("editor-1", Identity(role="editor", name="Alice"))
    toolbelt._access_control.role_grants["editor"] = ["echo"]
    allowed = __import__("asyncio").run(toolbelt.call("echo", state=None, arguments={"message": "a"}, identity_id="editor-1"))
    assert allowed["status"] == "ok"
    denied = __import__("asyncio").run(toolbelt.call("get_time", state=None, arguments={}, identity_id="editor-1"))
    assert denied["status"] == "error"
    assert "identity 'editor-1' cannot use get_time" in denied["message"]
