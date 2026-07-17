from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from msb_v2.api.observability_metrics import MetricsStore
from msb_v2.api.reasoning_integrity import _stream as reasoning_stream
from msb_v2.api.memory import _get_store as _memory_store_getter

router = APIRouter(tags=["observability"])
_metrics = MetricsStore()


def _refresh() -> tuple[Dict[str, Any], Dict[str, Any]]:
    return _metrics.recompute(reasoning_stream, _memory_store_getter())


@router.get("/metrics")
def metrics() -> Dict[str, Any]:
    reasoning, memory = _refresh()
    return {
        "reasoning": reasoning.payload(),
        "memory": memory.payload(),
    }


@router.get("/dashboard")
def dashboard() -> HTMLResponse:
    reasoning, memory = _refresh()
    return HTMLResponse(
        f"""<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>MSB Observability</title>
  <style>
    body {{ font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; background:#0b0c10; color:#c5c6c7; margin:0; padding:24px; }}
    .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:16px; }}
    .card {{ background:#111318; border:1px solid #1f2833; border-radius:14px; padding:18px 20px; }}
    .card h3 {{ margin:0 0 8px; font-size:13px; color:#66fcf1; text-transform: uppercase; letter-spacing:0.18em; }}
    .metric {{ font-size:34px; font-weight:700; color:#ffffff; }}
    .sub {{ color:#8a8f98; font-size:12px; margin-top:8px; }}
    a {{ color:#66fcf1; }}
    .ok {{ color:#66fcf1; }} .warn {{ color:#ffd166; }} .bad {{ color:#ef476f; }}
  </style>
</head>
<body>
  <h1 style=\"margin-top:0\">MSB Observability</h1>
  <div class=\"grid\">
    <div class=\"card\"><h3>Traces</h3><div class=\"metric\">{reasoning.total_traces}</div><div class=\"sub\">Active: {reasoning.active_traces}</div></div>
    <div class=\"card\"><h3>Events</h3><div class=\"metric\">{reasoning.total_events}</div><div class=\"sub\">Tool: {reasoning.tool_call_count} | Memory: {reasoning.memory_read_count} | Human: {reasoning.human_feedback_count}</div></div>
    <div class=\"card\"><h3>Avg Score</h3><div class=\"metric\">{round(reasoning.avg_score,4)}</div><div class=\"sub\">Confidence: {round(reasoning.avg_confidence,4)}</div></div>
    <div class=\"card\"><h3>Avg Entropy</h3><div class=\"metric\">{round(reasoning.avg_entropy,4)}</div><div class=\"sub\">Drift events: {reasoning.drift_count}</div></div>
    <div class=\"card\"><h3>Memory</h3><div class=\"metric\">{memory.total_memories}</div><div class=\"sub\">Active: {memory.active_memories} | Archived: {memory.archived_memories}</div></div>
    <div class=\"card\"><h3>Verification</h3><div class=\"metric\">{round(memory.verification_rate,4)}</div><div class=\"sub\">Avg reliability: {round(memory.avg_source_reliability,4)}</div></div>
  </div>
  <div style=\"margin-top:18px\" class=\"sub\">Endpoints: <a href=\"/metrics\">/metrics</a> · <a href=\"/reasoning/integrity/events\">reasoning events</a> · <a href=\"/reasoning/counterfactual/scan\">counterfactual scan</a></div>
</body>
</html>"""
    )
