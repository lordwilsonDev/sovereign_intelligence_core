from __future__ import annotations

import os
import subprocess
from typing import Any, Dict, List, Optional


MLX_PYTHON = "/opt/homebrew/Caskroom/miniforge/base/bin/python"
_UNSLOTH_REPO = "/Users/lordwilson/unsloth"


def _clean_env() -> Dict[str, str]:
    env = {
        k: v
        for k, v in os.environ.items()
        if k in {"HOME", "PATH", "USER", "TMPDIR", "TEMP", "TMP"}
    }
    env["PATH"] = "/opt/homebrew/Caskroom/miniforge/base/bin:" + env.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    env.pop("PYTHONPATH", None)
    env.pop("VIRTUAL_ENV", None)
    return env


def mlx_generate(model: str, prompt: str, max_tokens: int = 64, temp: float = 0.0, adapter_path: Optional[str] = None) -> Dict[str, Any]:
    cmd = [
        MLX_PYTHON, "-m", "mlx_lm.generate",
        "--model", model,
        "--prompt", prompt,
        "--max-tokens", str(max_tokens),
        "--temp", str(temp),
    ]
    if adapter_path:
        cmd.extend(["--adapter-path", adapter_path])
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600, env=_clean_env())
    out = (proc.stdout or proc.stderr or "").strip()
    return {"returncode": proc.returncode, "output": out}


def mlx_chat(model: str, prompt: str, max_tokens: int = 64, temp: float = 0.0, adapter_path: Optional[str] = None) -> Dict[str, Any]:
    chat_prompt = json_dumps_chat(prompt)
    cmd = [
        MLX_PYTHON, "-m", "mlx_lm.chat",
        "--model", model,
        "--temp", str(temp),
        "--max-tokens", str(max_tokens),
    ]
    if adapter_path:
        cmd.extend(["--adapter-path", adapter_path])
    proc = subprocess.run(cmd, input=chat_prompt, capture_output=True, text=True, timeout=600, env=_clean_env())
    out = (proc.stdout or proc.stderr or "").strip()
    return {"returncode": proc.returncode, "output": out}


def mlx_finetune(model: str, data: str, adapter_path: str, max_steps: int = 16, batch_size: int = 1, lora_rank: int = 32) -> Dict[str, Any]:
    cmd = [
        MLX_PYTHON, "-m", "unsloth_cli",
        "train",
        "--model_name", model,
        "--max_seq_length", "1024",
        "--dtype", "None",
        "--load_in_4bit",
        "--r", str(lora_rank),
        "--lora_alpha", str(max(16, lora_rank)),
        "--lora_dropout", "0.1",
        "--bias", "none",
        "--use_gradient_checkpointing", "unsloth",
        "--random_state", "3407",
        "--per_device_train_batch_size", str(batch_size),
        "--gradient_accumulation_steps", "1",
        "--warmup_steps", "0",
        "--max_steps", str(max_steps),
        "--learning_rate", "2e-4",
        "--logging_steps", "1",
        "--optim", "adamw_8bit",
        "--weight_decay", "0",
        "--lr_scheduler_type", "linear",
        "--seed", "3407",
        "--output_dir", adapter_path,
        "--report_to", "none",
        "--max_length", "1024",
        "--dataset_num_proc", "1",
        "--no-packing",
    ]
    if data:
        cmd.extend(["--train_data", data])
    cwd = _UNSLOTH_REPO if os.path.isdir(_UNSLOTH_REPO) else os.getcwd()
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=1800, env=_clean_env())
    return {
        "returncode": proc.returncode,
        "stdout": (proc.stdout or "")[-4000:],
        "stderr": (proc.stderr or "")[-4000:],
        "output_dir": adapter_path,
    }


def json_dumps_chat(prompt: str) -> str:
    import json

    return json.dumps({"messages": [{"role": "user", "content": prompt}]})
