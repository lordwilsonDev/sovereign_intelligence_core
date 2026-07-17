# architecture/brain_core.py
from __future__ import annotations

from typing import Any, Dict, Optional

from msb_v2.sovereign.model_gateway import ModelGateway

_MODEL = ModelGateway()


def _require_autogen() -> Optional[Any]:
    try:
        import autogen  # type: ignore[import-untyped]

        return autogen
    except Exception:  # pragma: no cover - optional integration
        return None


def build_brain() -> Dict[str, Any]:
    """Build and return the AutoGen agents when the dependency is installed."""
    autogen = _require_autogen()
    if autogen is None:
        return {
            "available": False,
            "reason": "pyautogen is not installed",
            "config_list": [],
            "solver": None,
            "user_proxy": None,
        }

    # Configuration for Gemma 2 9B via Ollama is preserved for reference,
    # but actual LLM calls are mediated through ModelGateway.
    config_list = [
        {
            "model": "gemma2:9b",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
            "price": [0, 0],
        }
    ]

    # 1. The Solver: Physical Agent
    solver = autogen.AssistantAgent(
        name="Physical_Solver",
        system_message="""You are a macOS automation expert.
You have a tool 'safe_click'.
Plan your actions.
If a click fails, reflect on why (wrong coordinates?) and retry.
Output 'TERMINATE' when the task is visually complete.""",
        llm_config={
            "config_list": config_list,
            "timeout": 120,
            "functions": [
                {
                    "name": "safe_click",
                    "description": "Click a pixel on screen",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "integer"},
                            "y": {"type": "integer"},
                        },
                        "required": ["x", "y"],
                    },
                }
            ],
        },
    )

    # 2. The User Proxy: The Executor
    user_proxy = autogen.UserProxyAgent(
        name="Executor",
        human_input_mode="ALWAYS",  # Safety First for Level 33
        max_consecutive_auto_reply=5,
        code_execution_config={
            "work_dir": "workspace",
            "use_docker": False,  # Disable Docker requirement
        },
        function_map={"safe_click": _safe_click},
    )

    return {
        "available": True,
        "reason": "",
        "config_list": config_list,
        "solver": solver,
        "user_proxy": user_proxy,
    }


def _safe_click(x: int, y: int, confirm: bool = True) -> str:
    """Soft model-gated click shim."""
    event = _MODEL.emit_capability_event(
        module="tools.physical_hand",
        tool="safe_click",
        status="skipped",
        detail="model disabled; click execution skipped",
    )
    if not _MODEL.available():
        return f"Model backend unavailable: {event.detail}"

    raise RuntimeError("active model backend is disabled in this integration")


if __name__ == "__main__":
    print("Level 33 Sovereign Architecture - Brain Core")
    print("Physical Agent initialized with Gemma 2 9B")

    brain = build_brain()
    if not brain["available"]:
        print(f"Brain unavailable: {brain['reason']}")
    else:
        print("Brain ready.")
