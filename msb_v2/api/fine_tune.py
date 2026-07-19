from __future__ import annotations

import os
import subprocess
import sys
import time
from dataclasses import asdict
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from cognitive_compiler.sovereign_finetune_harness_v1 import SovereignFineTuningHarness

router = APIRouter(tags=["fine-tuning"])

_UNSLOTH_REPO_PATH = "/Users/lordwilson/unsloth"
_MLX_PYTHON = "/opt/homebrew/Caskroom/miniforge/base/bin/python"


class ScanRequest(BaseModel):
    repo_path: str
    privacy_boundary: str = "local-only"


class DistillRequest(BaseModel):
    repo_path: str
    max_pairs: int = 64
    chunk_words: int = 512
    overlap: int = 64


class TrainRequest(BaseModel):
    repo_path: str
    base_model: str
    execute: bool = False


class MLXGenerateRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int = 64
    temp: float = 0.0
    adapter_path: str = ""


def _ensure_unsloth_available() -> Dict[str, Any]:
    sys.path.insert(0, _UNSLOTH_REPO_PATH)
    try:
        import unsloth  # noqa: F401

        return {"unsloth_available": True, "repo": _UNSLOTH_REPO_PATH}
    except Exception as exc:
        return {"unsloth_available": False, "error": str(exc), "repo": _UNSLOTH_REPO_PATH}


def _local_site_path() -> str:
    return os.path.expanduser("~/.local/lib/python3.12/site-packages")


def _clean_subprocess_env() -> Dict[str, str]:
    allowed = {"HOME", "PATH", "USER", "TMPDIR", "TEMP", "TMP", "SHELL", "TERM", "LANG"}
    env = {k: v for k, v in os.environ.items() if k in allowed}
    local_site = _local_site_path()
    env["PYTHONPATH"] = (
        f"/Users/lordwilson/msb-v2{os.pathsep}"
        f"/Users/lordwilson/unsloth{os.pathsep}"
        f"{local_site}{os.pathsep}"
        "/opt/homebrew/Caskroom/miniforge/base/lib/python3.12/site-packages"
    )
    env["PATH"] = "/opt/homebrew/Caskroom/miniforge/base/bin:" + env.get("PATH", "/usr/local/bin:/usr/bin:/bin")
    env["PYTHONNOUSERSITE"] = "1"
    env.pop("VIRTUAL_ENV", None)
    env.pop("CONDA_PREFIX", None)
    return env


def _summarize_failure(output: str, limit: int = 500) -> str:
    output = output or ""
    if "ValueError: To use optimized download using Xet storage" in output:
        return "dependency-failure: huggingface_hub requires hf_xet in this Python"
    return output[-limit:]


@router.post("/fine-tune/scan")
def fine_tune_scan(body: ScanRequest) -> Dict[str, Any]:
    if not os.path.isdir(body.repo_path):
        raise HTTPException(status_code=400, detail="repo_path must be a directory")
    harness = SovereignFineTuningHarness(repo_path=body.repo_path, privacy_boundary=body.privacy_boundary)
    report = harness.scan_documents()
    availability = _ensure_unsloth_available()
    return {
        "source_hash": report.source_hash,
        "document_count": len(report.documents),
        "total_tokens": report.total_tokens,
        "recommendation": report.recommendation,
        "assumption_risks": [asdict(r) for r in report.assumption_risks],
        "failure_patterns": report.failure_patterns,
        "unsloth": availability,
    }


@router.post("/fine-tune/distill")
def fine_tune_distill(body: DistillRequest) -> Dict[str, Any]:
    if not os.path.isdir(body.repo_path):
        raise HTTPException(status_code=400, detail="repo_path must be a directory")
    harness = SovereignFineTuningHarness(repo_path=body.repo_path)
    pairs = harness.synthesize_pairs(max_pairs=body.max_pairs, chunk_words=body.chunk_words, overlap=body.overlap)
    validation = harness.validate_pairs()
    return {
        "pairs_generated": len(pairs),
        "validation": validation,
        "privacy_boundary": harness.privacy_boundary,
    }


@router.post("/fine-tune/train")
def fine_tune_train(body: TrainRequest) -> Dict[str, Any]:
    if not os.path.isdir(body.repo_path):
        raise HTTPException(status_code=400, detail="repo_path must be a directory")
    availability = _ensure_unsloth_available()
    if not availability.get("unsloth_available"):
        raise HTTPException(status_code=500, detail=f"Unsloth unavailable: {availability.get('error')}")

    harness = SovereignFineTuningHarness(repo_path=body.repo_path)
    harness.scan_documents()
    harness.synthesize_pairs()
    job = harness.create_training_job(base_model=body.base_model)

    start = time.perf_counter()
    error = ""
    execution: Dict[str, Any] = {"executed": False}
    if body.execute:
        output_dir = f"/tmp/msb-finetune-{job.job_id}"
        cmd = [
            _MLX_PYTHON,
            "-m",
            "unsloth_cli",
            "train",
            "--model_name",
            body.base_model,
            "--max_seq_length",
            "1024",
            "--dtype",
            "None",
            "--load_in_4bit",
            "--r",
            "64",
            "--lora_alpha",
            "32",
            "--lora_dropout",
            "0.1",
            "--bias",
            "none",
            "--use_gradient_checkpointing",
            "unsloth",
            "--random_state",
            "3407",
            "--per_device_train_batch_size",
            "1",
            "--gradient_accumulation_steps",
            "1",
            "--warmup_steps",
            "0",
            "--max_steps",
            "1",
            "--learning_rate",
            "2e-4",
            "--logging_steps",
            "1",
            "--optim",
            "adamw_8bit",
            "--weight_decay",
            "0",
            "--lr_scheduler_type",
            "linear",
            "--seed",
            "3407",
            "--output_dir",
            output_dir,
            "--report_to",
            "none",
            "--max_length",
            "1024",
            "--dataset_num_proc",
            "1",
            "--no-packing",
        ]
        try:
            completed = subprocess.run(
                cmd,
                cwd=_UNSLOTH_REPO_PATH,
                capture_output=True,
                text=True,
                timeout=1800,
                env=_clean_subprocess_env(),
            )
            execution = {
                "executed": True,
                "returncode": completed.returncode,
                "stdout": (completed.stdout or "")[-2000:],
                "stderr": (completed.stderr or "")[-2000:],
                "output_dir": output_dir,
            }
            if completed.returncode != 0:
                error = f"unsloth exit {completed.returncode}: {_summarize_failure(completed.stderr or '')}"
        except subprocess.TimeoutExpired:
            error = "unsloth training timed out"
        except Exception as exc:  # pragma: no cover
            error = str(exc)
    elapsed_s = round(time.perf_counter() - start, 3)

    baseline = harness.validate_baseline_coherence()
    report = harness.run_post_training_validation(job_id=job.job_id)
    return {
        "job_id": job.job_id,
        "status": job.status,
        "dataset_size": job.dataset_size,
        "baseline_coherence": baseline,
        "execution": {**execution, "elapsed_s": elapsed_s, "error": error, "unsloth_repo": _UNSLOTH_REPO_PATH},
        "integration_report": {
            "model_name": report.model_name,
            "validation_passed": report.validation_passed,
            "coherence_score": report.coherence_score,
            "confidence_score": report.confidence_score,
            "recommendation": report.recommendation,
            "falsification_condition": report.falsification_condition,
        },
    }


@router.post("/fine-tune/mlx-generate")
def fine_tune_mlx_generate(body: MLXGenerateRequest) -> Dict[str, Any]:
    cmd = [
        _MLX_PYTHON,
        "-m",
        "mlx_lm.generate",
        "--model",
        body.model,
        "--prompt",
        body.prompt,
        "--max-tokens",
        str(body.max_tokens),
        "--temp",
        str(body.temp),
    ]
    if body.adapter_path:
        cmd.extend(["--adapter-path", body.adapter_path])
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, env=_clean_subprocess_env())
    out = _summarize_failure((proc.stdout or proc.stderr or "").strip(), limit=4000)
    return {"returncode": proc.returncode, "output": out}
