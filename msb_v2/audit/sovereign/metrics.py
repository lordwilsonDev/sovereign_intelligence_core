from __future__ import annotations


def compute_audit_sovereignty_score(
    merkle_ok: bool,
    fts: float,
    assumption_debt: int,
    veto_active: bool,
) -> float:
    score = 100.0
    if not merkle_ok:
        score -= 40.0
    if fts > 0.5:
        score -= 20.0
    if assumption_debt > 3:
        score -= 20.0
    if not veto_active:
        score -= 10.0
    return max(0.0, score)
