from __future__ import annotations

import re
from typing import Optional

HEADER = "### MSB_SESSION_CONTINUITY_V1 ###"
_KEY_VALUE = re.compile(
    r"^(project|version|timestamp|simple_assumption_score|active_task|topic|last_turn_summary|recent_decisions|open_questions|reliable_findings|code_references|pending_actions|recent_tool_calls|memory_pointer|active_harness|assumption_debt_ids)\s*=\s*(.*?)(?:\s\w+=|$)"
)


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
            match = _KEY_VALUE.match(line.strip())
            if match:
                state[match.group(1)] = match.group(2).strip()
        return state
