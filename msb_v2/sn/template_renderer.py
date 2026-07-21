from __future__ import annotations

import os
import re
from pathlib import Path
from string import Template
from typing import Any, Dict, Optional


class TemplateRenderer:
    def __init__(self, templates_dir: Optional[Path] = None) -> None:
        self._templates_dir = templates_dir or Path(os.getenv("SN_TEMPLATES_DIR", "msb_v2/sn/templates"))

    def render(self, template_name: str, data: Dict[str, Any]) -> str:
        path = self._templates_dir / f"{template_name}.md"
        if not path.exists():
            return f"[{template_name}] " + ", ".join(f"{k}={v}" for k, v in data.items())
        text = path.read_text()
        text = re.sub(r"\{\{\s*(\w+)\s*\}\}", r"${\1}", text)
        return Template(text).safe_substitute(**{str(k): str(v) for k, v in data.items()})
