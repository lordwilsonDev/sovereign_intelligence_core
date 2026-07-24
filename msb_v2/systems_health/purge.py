"""Safe, bounded purging of MSB temp and cache artifacts."""
from __future__ import annotations

import glob
import os
import shutil
import time
from typing import Any, Dict, List


_PURGE_PATTERNS = [
    "/tmp/msb-v2-*",
    "/private/var/tmp/msb-v2-*",
    os.path.expanduser("~/Library/Caches/msb-v2/*"),
    os.path.expanduser("~/Library/Caches/*/msb-v2/*"),
]


def _safe_size(path: str) -> int:
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        total = 0
        for root, _, files in os.walk(path):
            for fp in files:
                full = os.path.join(root, fp)
                if os.path.exists(full):
                    total += os.path.getsize(full)
        return total
    except Exception:
        return 0


def purge_stale_artifacts(max_age_days: int = 1) -> Dict[str, Any]:
    """Remove stale MSB temp/cache artifacts older than max_age_days.
    
    Returns a structured result with removed paths and freed bytes.
    """
    cutoff = time.time() - (max_age_days * 86400)
    removed: List[str] = []
    errors: List[Dict[str, str]] = []
    for pattern in _PURGE_PATTERNS:
        for path in glob.glob(pattern):
            try:
                if os.path.isdir(path):
                    if os.path.getmtime(path) <= cutoff:
                        shutil.rmtree(path)
                        removed.append(path)
                elif os.path.isfile(path):
                    if os.path.getmtime(path) <= cutoff:
                        os.remove(path)
                        removed.append(path)
            except Exception as exc:
                errors.append({"path": path, "error": str(exc)[:120]})
    freed_bytes = _safe_size("/tmp/msb-v2-*")
    return {"removed": removed, "freed_bytes": freed_bytes, "errors": errors}
