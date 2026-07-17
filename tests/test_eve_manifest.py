from __future__ import annotations

from pathlib import Path

from msb_v2.eve.discovery import discover
from msb_v2.eve.manifest import CompiledManifest, compile_manifest, manifest_to_dict


def test_compile_manifest_from_fixture() -> None:
    fixture_root = Path("/Users/lordwilson/msb-v2/tests/fixtures/eve_agent")
    result = discover(fixture_root)
    manifest = compile_manifest(result)
    assert manifest.kind == "msb-eve-compiled-manifest"
    assert manifest.version == 1
    assert len(manifest.tools) >= 1
    assert [t.name for t in manifest.tools] == ["get_time"]
    assert len(manifest.skills) >= 1
    assert manifest.skills[0].frontmatter.get("name") == "sovereign"
    assert len(manifest.schedules) >= 1


def test_manifest_deterministic() -> None:
    fixture_root = Path("/Users/lordwilson/msb-v2/tests/fixtures/eve_agent")
    result = discover(fixture_root)
    first = compile_manifest(result)
    second = compile_manifest(result)
    assert first == second
    assert len(set(id(obj) for obj in first.skills)) == len(first.skills)


def test_compile_manifest_manual_types() -> None:
    manifest = CompiledManifest(
        tools=[],
        skills=[],
        schedules=[],
    )
    assert manifest_to_dict(manifest)["kind"] == "msb-eve-compiled-manifest"
    assert manifest_to_dict(manifest)["version"] == 1
