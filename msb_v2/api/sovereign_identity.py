"""Sovereign Identity Card API — generate and verify identity documents."""
from fastapi import APIRouter
from pydantic import BaseModel
from msb_v2.sovereign_identity.identity_card import SovereignIdentityCard

router = APIRouter(tags=["sovereign-identity"])
_identity = SovereignIdentityCard()

class VerifyRequest(BaseModel):
    card: dict

@router.get("/card")
def get_identity_card():
    """Return a signed Sovereign Identity Card."""
    return _identity.generate()

@router.post("/verify")
def verify_identity_card(req: VerifyRequest):
    """Verify a Sovereign Identity Card signature."""
    valid = _identity.verify(req.card)
    return {"valid": valid}
