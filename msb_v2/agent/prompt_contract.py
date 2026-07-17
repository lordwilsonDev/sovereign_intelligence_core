from __future__ import annotations

from typing import Any, Dict, List


class PromptContract:
    """Distilled tool-call / memory / output contract for MSB v2 agents."""

    def __init__(self) -> None:
        self.rules: List[str] = []
        self.tool_schema: Dict[str, Any] = {}
        self.memory_rules: List[str] = []
        self.output_rules: List[str] = []

    def add_rule(self, text: str) -> None:
        self.rules.append(text)

    def add_tool(self, name: str, description: str, required: List[str]) -> None:
        self.tool_schema[name] = {"description": description, "required": required}

    def add_memory_rule(self, text: str) -> None:
        self.memory_rules.append(text)

    def add_output_rule(self, text: str) -> None:
        self.output_rules.append(text)

    def render(self) -> str:
        lines: List[str] = []

        if self.rules:
            lines.extend(self.rules)
            lines.append("")

        if self.tool_schema:
            lines.append("TOOLS")
            lines.append("-----")
            for name, meta in self.tool_schema.items():
                req = ", ".join(meta.get("required", []))
                lines.append(f"- {name}: {meta['description']} Required: {req}")
            lines.append("")
            lines.append("<tool_calling>")
            lines.append(
                "ALWAYS follow the tool call schema exactly, provide all necessary parameters, "
                "and never call tools not explicitly provided. Prefer tool use over guessing."
            )
            lines.append("</tool_calling>")
            lines.append("")

        if self.memory_rules:
            lines.append("<memory_rules>")
            lines.extend(self.memory_rules)
            lines.append("</memory_rules>")
            lines.append("")

        if self.output_rules:
            lines.append("<output_rules>")
            lines.extend(self.output_rules)
            lines.append("</output_rules>")

        return "\n".join(lines).strip()


def build_hermes_phase5_contract() -> PromptContract:
    contract = PromptContract()

    # Identity / guardrails
    contract.add_rule(
        "You are a Hermes Phase 5 agent. Operate under MSB v2 runtime contracts. "
        "Assist with the task only; refuse unsafe external actions."
    )
    contract.add_rule(
        "If the task is general and already known, answer with no tool calls."
    )

    # Tool calling
    contract.add_tool(
        "agent_run",
        "Execute an agent run against registered callables in msb_v2.agent.runtime.",
        ["run_id", "tasks"],
    )
    contract.add_tool(
        "run_status",
        "Return current run state for an existing run_id.",
        ["run_id"],
    )
    contract.add_tool(
        "runtime_status",
        "Return worker pool and context health from msb_v2.runtime.context.",
        [],
    )

    contract.add_rule(
        "<tool_calling>"
        "ALWAYS follow schema exactly and provide required parameters. "
        "NEVER refer to tool names to the user; describe behavior in plain language."
        "</tool_calling>"
    )

    # Memory
    contract.add_memory_rule(
        "Use hermes-agent memory for durable facts across sessions. "
        "Cite memory when relevant. If memories contradict, treat the newest as authoritative."
    )

    # Output discipline
    contract.add_output_rule(
        "Be concise and direct. Default to <4 lines when no code/tool use is required."
    )
    contract.add_output_rule(
        "Do not add code summary, introductions, or postambles unless requested."
    )
    contract.add_output_rule("One-word answers are best when accurate.")
    contract.add_output_rule(
        "Run tests with: PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 python3 -m pytest"
    )

    return contract
