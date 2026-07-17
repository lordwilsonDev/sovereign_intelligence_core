from __future__ import annotations

from pathlib import Path

from msb_v2.eve.discovery import discover, discover_schedules, discover_skills, discover_tools
from msb_v2.eve.manifest import compile_manifest, manifest_to_dict


FIXTURE_ROOT = Path("/Users/lordwilson/msb-v2/tests/fixtures/eve_agent")


def test_discover_tools_from_fixture() -> None:
    tools = discover_tools(FIXTURE_ROOT)
    assert [t.name for t in tools] == ["get_time"]
    assert tools[0].kind == "python"
    assert tools[0].docstring == "Return current local time as a string."


def test_discover_skills_from_fixture() -> None:
    skills = discover_skills(FIXTURE_ROOT)
    assert [s.name for s in skills] == ["sovereign"]
    assert skills[0].path.endswith("sovereign.md")


def test_discover_schedules_from_fixture() -> None:
    schedules = discover_schedules(FIXTURE_ROOT)
    assert [s.name for s in schedules] == ["morning_check"]
    assert schedules[0].raw["cron"] == "0 9 * * *"


def test_full_discovery_result() -> None:
    result = discover(FIXTURE_ROOT)
    assert len(result.tools) == 1
    assert len(result.skills) == 1
    assert len(result.schedules) == 1
    assert result.diagnostics == []


def test_compile_manifest_is_deterministic() -> None:
    result = discover(FIXTURE_ROOT)
    first = compile_manifest(result)
    second = compile_manifest(result)
    assert first == second
    assert first.kind == "msb-eve-compiled-manifest"
    assert first.version == 1
    assert len(first.tools) == 1
    assert len(first.skills) == 1
    assert first.skills[0].frontmatter["name"] == "sovereign"
    assert len(first.schedules) == 1


def test_manifest_to_dict_contains_hashes() -> None:
    result = discover(FIXTURE_ROOT)
    manifest = compile_manifest(result)
    payload = manifest_to_dict(manifest)
    assert payload["skills"][0]["sha256"]
    assert payload["schedules"][0]["sha256"]
