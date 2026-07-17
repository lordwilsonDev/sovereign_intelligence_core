from __future__ import annotations

from pathlib import Path


from msb_v2.knowledge import snapshot


def test_snapshot_counts_markdown_files_and_links(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("hello [[link]]")
    (tmp_path / "b.md").write_text("world")
    result = snapshot([tmp_path])
    assert result.entries == 2
    assert result.links == 2
