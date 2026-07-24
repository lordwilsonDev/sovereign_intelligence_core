"""Sovereign Identity Card tests."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from msb_v2.sovereign_identity.identity_card import SovereignIdentityCard


@pytest.fixture()
def identity_card():
    with patch("msb_v2.sovereign_identity.identity_card.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout.strip.return_value = ""
        card = SovereignIdentityCard()
    return card


def test_generate_card_returns_signed_document(identity_card: SovereignIdentityCard) -> None:
    with patch("msb_v2.sovereign_identity.identity_card.requests.get") as mock_get, \
         patch("msb_v2.sovereign_identity.identity_card.requests.post") as mock_post:
        mock_get.return_value.ok = False
        mock_post.return_value.ok = False
        document = identity_card.generate()
    assert "node_id" in document
    assert "signature" in document
    assert "timestamp" in document
    assert document["sas"] == 0
    assert document["attestation"] == "UNKNOWN"
    assert document["node_id"] == identity_card.node_id


def test_verify_valid_card(identity_card: SovereignIdentityCard) -> None:
    with patch("msb_v2.sovereign_identity.identity_card.requests.get") as mock_get, \
         patch("msb_v2.sovereign_identity.identity_card.requests.post") as mock_post:
        mock_get.return_value.ok = False
        mock_post.return_value.ok = False
        original = identity_card.generate()
    card = original.copy()
    assert identity_card.verify(card) is True


def test_verify_tampered_card_fails(identity_card: SovereignIdentityCard) -> None:
    with patch("msb_v2.sovereign_identity.identity_card.requests.get") as mock_get, \
         patch("msb_v2.sovereign_identity.identity_card.requests.post") as mock_post:
        mock_get.return_value.ok = False
        mock_post.return_value.ok = False
        original = identity_card.generate()
    card = original.copy()
    card["node_id"] = "tampered"
    assert identity_card.verify(card) is False


def test_verify_missing_signature_fails(identity_card: SovereignIdentityCard) -> None:
    assert identity_card.verify({"node_id": "abc"}) is False