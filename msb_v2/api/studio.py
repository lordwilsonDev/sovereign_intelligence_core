from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict

import urllib.error
import urllib.request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from msb_v2.evolution.memory import EvolutionMemory
from msb_v2.memory.persistence import PersistentMemoryStore
from msb_v2.reasoning.integrity import EventStreamStore
from msb_v2.verification.integrity_verifier import IntegrityVerifier
from msb_v2.engine.neuralagent import execute_neuralagent
from msb_v2.api.observability_metrics import MetricsStore

router = APIRouter(tags=["studio"])
logger = logging.getLogger(__name__)
_REPO_ROOT = Path("/Users/lordwilson/msb-v2")


def _safe(call):
    try:
        return {"ok": True, "value": call()}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


@router.get("/", response_class=JSONResponse, include_in_schema=False)
async def studio_dashboard() -> Dict[str, Any]:
    return {
        "name": "msb-studio",
        "version": "0.1.0",
        "endpoints": {
            "studio": "/studio/status",
            "sovereign": "/sovereign/status",
            "environment": "/environment/status",
            "agent": "/agent/run",
            "agent_loop": "/agent/run/loop",
            "evolution": "/evolution/scan",
            "verification": "/verification/integrity/trace/{trace_id}",
            "agent_dashboard": "/agent-dashboard",
        },
    }


@router.get("/studio/status")
def studio_status() -> JSONResponse:
    runtime_summary = _safe(_runtime_summary)
    memory = _safe(_memory_summary)
    verification = _safe(_verification_summary)
    evolution = _safe(_evolution_summary)
    return JSONResponse(
        {
            "runtime": runtime_summary,
            "memory": memory,
            "verification": verification,
            "evolution": evolution,
            "agent": {
                "run_endpoint": "/agent/run",
                "status_endpoint": "/agent/run/{run_id}",
                "loop_endpoint": "/agent/run/loop",
            },
        }
    )


@router.get("/studio/health")
def studio_health() -> JSONResponse:
    ollama = _safe(_ollama_reachable)
    fs = _safe(_filesystem_sanity)
    return JSONResponse({"ollama": ollama, "filesystem": fs})


@router.get("/agent-dashboard")
def agent_dashboard() -> JSONResponse:
    prompt = "Return a one-line sovereign OS status assessment in plain English. No markdown, no JSON, no preface."
    started = time.perf_counter()
    result = execute_neuralagent(
        {
            "provider": "ollama",
            "endpoint": "http://localhost:11434",
            "model": "qwen2.5:0.5b",
            "prompt": prompt,
        }
    )
    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    result.setdefault("latency_ms", latency_ms)
    return JSONResponse(
        {
            "model": "qwen2.5:0.5b",
            "provider": "ollama",
            "prompt": prompt,
            "result": result,
            "latency_ms": latency_ms,
        }
    )


@router.get("/studio/metrics")
def studio_metrics() -> JSONResponse:
    started = time.perf_counter()
    reasoning: Any = {}
    memory: Any = {}
    prometheus_fragment = ""
    try:
        store = MetricsStore()
        raw_reasoning, raw_memory = store.recompute(EventStreamStore(), PersistentMemoryStore())
        reasoning = {k: getattr(raw_reasoning, k) for k in dir(raw_reasoning) if not k.startswith("_") and not callable(getattr(raw_reasoning, k))}
        memory = {k: getattr(raw_memory, k) for k in dir(raw_memory) if not k.startswith("_") and not callable(getattr(raw_memory, k))}
    except Exception as exc:
        reasoning = {"error": str(exc)}
        memory = {"error": str(exc)}
    try:
        req = urllib.request.Request("http://127.0.0.1:8766/metrics", method="GET")
        with urllib.request.urlopen(req, timeout=1.0) as r:
            prometheus_fragment = r.read().decode("utf-8", "ignore")[:256]
    except Exception:
        prometheus_fragment = ""
    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    return JSONResponse(
        {
            "dashboard_latency_ms": latency_ms,
            "reasoning": reasoning,
            "memory": memory,
            "prometheus_fragment": prometheus_fragment,
        }
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def studio_dashboard_html() -> HTMLResponse:
    js = """
    const ENDPOINTS = [
      {name:'studio', url:'/studio/status'},
      {name:'agent', url:'/agent-dashboard'},
      {name:'observability', url:'/observability/status'},
      {name:'metrics', url:'/studio/metrics'},
    ];
    async function loadAll() {
      const root = document.getElementById('grid');
      const results = await Promise.allSettled(ENDPOINTS.map(async e => {
        const r = await fetch(e.url);
        const text = await r.text();
        return {name:e.name, ok:r.ok, text};
      }));
      root.innerHTML = results.map((r, i) => {
        const meta = ENDPOINTS[i];
        const status = r.status === 'fulfilled' ? (r.value.ok ? 'ok' : 'err') : 'fail';
        const body = r.status === 'fulfilled' ? r.value.text : String(r.reason);
        let content = '';
        try { content = JSON.stringify(JSON.parse(body), null, 2); } catch { content = body; }
        return `<div class='card ${status}'><h3>${meta.name} · <span class='pill ${status}'>${status}</span></h3><pre>${content}</pre></div>`;
      }).join('');
    }
    """
    css = """:root{--bg:#0b0c10;--panel:#111318;--line:#1f2833;--text:#c5c6c7;--accent:#66fcf1;--good:#66fcf1;--warn:#ffd166;--bad:#ef476f}*{box-sizing:border-box}body{font-family:ui-sans-serif,system-ui,sans-serif;background:var(--bg);color:var(--text);margin:0;padding:24px}h1{margin:0 0 18px;font-size:22px;color:#fff}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px 16px}.card h3{margin:0 0 8px;font-size:12px;color:var(--accent);text-transform:uppercase;letter-spacing:.12em}.card pre{white-space:pre-wrap;word-break:break-word;font-size:12px;color:#e6e6e6;max-height:320px;overflow:auto;margin:0}.ok{border-color:var(--good)}.ok h3{color:var(--good)}.err{border-color:var(--bad)}.err h3{color:var(--bad)}.fail{border-color:var(--warn)}.fail h3{color:var(--warn)}.pill{display:inline-block;padding:3px 8px;border-radius:999px;font-size:10px;background:var(--line);color:#fff}.ok .pill{background:var(--good);color:#0b0c10}.err .pill{background:var(--bad);color:#0b0c10}.fail .pill{background:var(--warn);color:#0b0c10}"""
    html = (
        "<!doctype html><html><head><meta charset='utf-8'><title>msb-studio</title><style>"
        + css
        + "</style></head><body>"
        + "<h1>msb-studio</h1>"
        + "<div class='grid' id='grid'>loading...</div>"
        + f"<script>const TS=document.createElement('div');TS.className='sub';TS.id='ts';document.body.insertBefore(TS,document.body.firstChild.nextSibling);{js}loadAll();setInterval(()=>{{loadAll();document.getElementById('ts').textContent='updated '+new Date().toISOString();}},5000);</script></body></html>"
    )
    return HTMLResponse(html)


@router.get("/studio/dashboard", response_class=HTMLResponse)
async def studio_dashboard_html_alias() -> HTMLResponse:
    return await studio_dashboard_html()


def _runtime_summary() -> Dict[str, Any]:
    from msb_v2.runtime.context import RuntimeContext

    ctx = RuntimeContext()
    summary = ctx.summary()
    return {
        "app": summary.get("app"),
        "env": summary.get("env"),
        "uptime_seconds": summary.get("uptime_seconds"),
        "worker_pool": summary.get("worker_pool"),
        "health": summary.get("health"),
    }


def _memory_summary() -> Dict[str, Any]:
    store = PersistentMemoryStore()
    health = store.health()
    return {
        "status": "ok",
        "verified_facts": getattr(health, "verified_facts", 0),
        "unverified_facts": getattr(health, "unverified_facts", 0),
        "avg_confidence": getattr(health, "avg_confidence", 0.0),
        "stale_records": getattr(health, "stale_records", 0),
        "retrievals": getattr(health, "retrievals", 0),
        "avg_decision_impact_score": getattr(health, "avg_decision_impact_score", 0.0),
    }


def _verification_summary() -> Dict[str, Any]:
    stream = EventStreamStore()
    verifier = IntegrityVerifier(stream=stream)
    trace = verifier.verify_trace("studio")
    try:
        from msb_v2.verification.hardware_attestation import HardwareAttestation

        attestation = HardwareAttestation(
            binary_path=Path(__file__).resolve().parents[2] / "msb_v2" / "api" / "verification.py"
        ).verify()
    except Exception as exc:
        attestation = {"verdict": "ERROR", "error": str(exc)}
    return {"trace": trace, "hardware_attestation": attestation}


def _evolution_summary() -> Dict[str, Any]:
    memory = EvolutionMemory(path=_REPO_ROOT / "evolution_memory.db")
    proposals = memory.all()
    return {"count": len(proposals), "proposals": proposals}


def _ollama_reachable() -> Dict[str, Any]:
    import socket

    host = "127.0.0.1"
    port = 11434
    try:
        with socket.create_connection((host, port), timeout=1.0):
            pass
    except Exception as exc:
        return {"reachable": False, "error": str(exc)}
    return {"reachable": True, "host": host, "port": port}


def _filesystem_sanity() -> Dict[str, Any]:
    import os
    import shutil

    try:
        usage = shutil.disk_usage(_REPO_ROOT)
        writable = os.access(_REPO_ROOT, os.W_OK)
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
    return {
        "ok": True,
        "repo_path": str(_REPO_ROOT),
        "disk_usage": {
            "total_gb": round(usage.total / 1e9, 2),
            "used_gb": round(usage.used / 1e9, 2),
            "free_gb": round(usage.free / 1e9, 2),
            "percent_used": round((usage.used / usage.total) * 100, 2),
        },
        "writable": bool(writable),
    }
