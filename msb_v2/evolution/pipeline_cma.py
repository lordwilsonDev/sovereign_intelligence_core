"""Ouroboros pipeline cognitive mirage audit scan."""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from msb_v2.evolution.scanner import OuroborosScanner

logger = logging.getLogger(__name__)


class PipelineCMA:
    def __init__(
        self,
        root: Path,
        audit_log_path: Path,
        interval_hours: int = 6,
    ) -> None:
        self.root = root
        self.audit_log_path = audit_log_path
        self.interval_hours = int(interval_hours)
        self.scanner = OuroborosScanner(self.root)

    def scan(self) -> Dict[str, Any]:
        events = self._read_audit_events()
        rejected = [e for e in events if str(e.get("type", "")) == "SOVEREIGN_ARTIFACT_REJECTED"]
        mirages = [e for e in events if str(e.get("type", "")).endswith("_MIRAGE_ALERT")]
        scan = self.scanner.scan()
        return {
            "rejected_artifacts": len(rejected),
            "mirage_alerts": len(mirages),
            "scanner_issues": scan.get("proposal_count", 0),
            "hotspots": scan.get("hotspots", []),
            "duplication": scan.get("duplication", []),
            "dead_symbols": scan.get("dead_symbols", []),
        }

    def _read_audit_events(self) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []
        try:
            if not self.audit_log_path.exists():
                return events
            for line in self.audit_log_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except Exception:
                    continue
        except Exception as exc:
            logger.debug("read_audit_events_failed: %s", exc)
        return events
