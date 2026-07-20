from __future__ import annotations

import re
from typing import Optional

HEADER = "### MSB_SESSION_CONTINUITY_V1 ###"


class ResumePromptLoader:
    @staticmethod
    def is_resume_prompt(text: str) -> bool:
        return text.strip().startswith(HEADER)

    @staticmethod
    def load(text: str) -> dict[str, str]:
        if not ResumePromptLoader.is_resume_prompt(text):
            return {}
        payload = text.split(HEADER, 1)[1].strip()
        state: dict[str, str] = {}
        for line in payload.splitlines():
            if "=" in line:
                key, _, value = line.partition("=")
                state[key.strip()] = value.strip()
        return state
