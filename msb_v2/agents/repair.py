from __future__ import annotations

from typing import Any, Dict


def run_repair(**kwargs: Any) -> Dict[str, Any]:
    """Diagnose a problem and propose a deterministic repair action."""
    problem = str(kwargs.get("problem", "") or "").strip()
    context = str(kwargs.get("context", "") or "").strip()
    if not problem:
        return {"status": "error", "message": "missing problem", "confidence": 0.0}
    valid = "invert" in problem.lower() or "break" in problem.lower() or "fix" in problem.lower()
    action = "propose_inversion" if valid else "escalate_to_human"
    return {
        "status": "ok",
        "message": f"Repair plan for: {problem[:120]}",
        "confidence": 0.75 if valid else 0.4,
        "action": action,
        "context": context[:200],
    }
