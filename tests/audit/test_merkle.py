from __future__ import annotations

import json
from pathlib import Path

import pytest

from msb_v2.audit.sovereign.merkle import AuditMerkleChain


def test_merkle_verify_empty_and_single_event(tmp_path: Path):
    chain = AuditMerkleChain(tmp_path / "audit.jsonl")
    assert chain.verify_chain() is True
    h1 = chain.append({"kind": "boot", "ok": True})
    assert chain.verify_chain() is True
    assert len(h1) == 64


def test_merkle_tampering_detected(tmp_path: Path):
    chain = AuditMerkleChain(tmp_path / "audit.jsonl")
    chain.append({"kind": "a", "v": 1})
    chain.append({"kind": "b", "v": 2})
    # mutate first event payload in the log
    path = Path(tmp_path / "audit.jsonl")
    with open(path) as f:
        lines = f.readlines()
    entry = json.loads(lines[0])
    entry["event"]["v"] = 999
    with open(path, "w") as f:
        f.write(json.dumps(entry) + "\n")
        f.writelines(lines[1:])
    assert chain.verify_chain() is False
