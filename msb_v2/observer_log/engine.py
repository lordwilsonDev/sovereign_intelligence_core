"""Observer's Log — narrative thought stream for the sovereign organism."""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

LOG_PATH = Path(__file__).resolve().parent.parent.parent / "runtime" / "observer_log.jsonl"


class ObserverLog:
    def __init__(self, log_path: Path = LOG_PATH):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, source: str, message: str, priority: str = "info"):
        event = {
            "source": source,
            "message": message,
            "priority": priority,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(event) + "\n")
        if priority in ("high", "critical"):
            try:
                import requests
                requests.post("http://127.0.0.1:8766/sn/notify", json={
                    "source": "observer-log",
                    "priority": priority,
                    "template": "observer_log_thought",
                    "template_data": {"source": source, "message": message},
                }, timeout=5)
            except Exception:
                pass

    def recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        if not self.log_path.exists():
            return []
        lines = self.log_path.read_text().strip().splitlines()[-limit:]
        return [json.loads(line) for line in lines if line.strip()]
