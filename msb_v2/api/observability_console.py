from __future__ import annotations

import json
from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from msb_v2.api.observability_metrics import MetricsStore
from msb_v2.api.reasoning_integrity import _stream as reasoning_stream
from msb_v2.api.memory import _get_store as _memory_store_getter

router = APIRouter(tags=["observability"])
_metrics = MetricsStore()
_PENDING: Dict[str, Dict[str, Any]] = {}


@router.get("/console/replay/{trace_id}")
def replay_trace(trace_id: str) -> JSONResponse:
    all_events = list(reasoning_stream.global_stream(limit=1000))
    events = [
        {
            "event_id": e.event_id,
            "sequence": e.sequence,
            "kind": e.kind.value,
            "source": e.source,
            "ts": e.ts,
            "payload": e.payload or {},
        }
        for e in all_events
        if e.trace_id == trace_id
    ]
    events.sort(key=lambda e: e.get("sequence", 0))
    transitions = []
    for idx, ev in enumerate(events):
        transitions.append({
            "step": idx + 1,
            "event_id": ev.get("event_id"),
            "kind": ev.get("kind"),
            "source": ev.get("source"),
            "state": ev.get("payload", {}).get("verdict") or ev.get("payload", {}).get("status") or ev.get("kind"),
            "ts": ev.get("ts"),
        })
    continuity = reasoning_stream.verify_continuity(trace_id)
    return JSONResponse({
        "trace_id": trace_id,
        "event_count": len(events),
        "continuous": continuity.get("continuous", False),
        "gaps": continuity.get("gaps", []),
        "events": events,
        "transitions": transitions,
    })


@router.get("/console/replay/html/{trace_id}", response_class=HTMLResponse)
def replay_trace_html(trace_id: str) -> HTMLResponse:
    data = replay_trace(trace_id).body
    data = json.loads(data)
    rows = []
    for t in data["transitions"]:
        rows.append(
            "<div class='event'><div class='seq'>" + str(t["step"]) + "</div>"
            "<div class='kind'>" + str(t["kind"]) + "</div>"
            "<div class='src'>" + str(t["source"]) + "</div>"
            "<div class='payload'>state=" + str(t["state"]) + "</div></div>"
        )
    continuity = "continuous" if data.get("continuous") else "gaps=" + str(data.get("gaps"))
    html = (
        "<!doctype html><html><head><meta charset='utf-8'><title>Replay</title><style>"
        "body{background:#0b0c10;color:#c5c6c7;font-family:ui-sans-serif,system-ui,sans-serif;padding:24px}"
        ".event{display:flex;gap:12px;padding:8px 10px;border-bottom:1px solid #1f2833;font-size:13px}"
        ".seq{color:#8a8f98;width:40px;flex:none}.kind{width:180px;flex:none;color:#66fcf1}.src{width:220px;flex:none;color:#8a8f98}.payload{color:#e6e6e6;word-break:break-word}"
        "</style></head><body>"
        "<h1>Replay: " + trace_id + "</h1>"
        "<div class='sub'>trace_id=" + trace_id + " · events=" + str(data["event_count"]) + " · continuity=" + continuity + "</div>"
        "<div style='margin-top:14px;'>" + "\n".join(rows) + "</div>"
        "</body></html>"
    )
    return HTMLResponse(html)


def _refresh() -> tuple[Dict[str, Any], Dict[str, Any]]:
    return _metrics.recompute(reasoning_stream, _memory_store_getter())


def _fmt_payload(payload: Dict[str, Any]) -> str:
    if not payload:
        return ""
    return " - ".join(str(k) + "=" + str(v) for k, v in list(payload.items())[:6])


def _health(score: float, confidence: float, entropy: float, drift_count: int, error_count: int, continuous: bool) -> str:
    if not continuous or error_count > 0 or drift_count > 0:
        return "weak"
    if score >= 0.6 and confidence >= 0.8:
        return "healthy"
    if score < 0.6 and confidence >= 0.8:
        return "uncertain"
    return "weak"


def _health_class(health: str) -> str:
    return {"healthy": "ok", "uncertain": "warn", "weak": "bad"}.get(health, "")


def _signals(by_trace: Dict[str, list[dict[str, Any]]]) -> Dict[str, Any]:
    signals = []
    for trace_id, events in by_trace.items():
        assessments = [e for e in events if e.get("kind") == "confidence_assessment"]
        drift = [e for e in events if e.get("kind") == "drift"]
        errors = [e for e in events if e.get("kind") == "error"]
        latest = assessments[-1] if assessments else None
        score = float(latest.get("payload", {}).get("score", 0.0)) if latest else 0.0
        confidence = float(latest.get("payload", {}).get("confidence", 0.0)) if latest else 0.0
        entropy = float(latest.get("payload", {}).get("entropy", 0.0)) if latest else 0.0
        grounded = bool(latest.get("payload", {}).get("ground_truth_accepted")) if latest else False
        signals.append({
            "trace_id": trace_id,
            "score": round(score, 4),
            "confidence": round(confidence, 4),
            "entropy": round(entropy, 4),
            "ground_truth_accepted": grounded,
            "drift_count": len(drift),
            "error_count": len(errors),
            "assessment_count": len(assessments),
        })
    signals.sort(key=lambda x: x.get("score", 0.0))
    strong = [s for s in signals if s.get("confidence", 0.0) >= 0.8 and s.get("score", 0.0) >= 0.6]
    weak = [s for s in signals if s.get("score", 0.0) < 0.6 and s.get("confidence", 0.0) < 0.6]
    return {
        "count": len(signals),
        "average": {
            "score": round(sum(s["score"] for s in signals)/len(signals), 4) if signals else 0.0,
            "confidence": round(sum(s["confidence"] for s in signals)/len(signals), 4) if signals else 0.0,
            "entropy": round(sum(s["entropy"] for s in signals)/len(signals), 4) if signals else 0.0,
        },
        "strong_signals": len(strong),
        "weak_signals": len(weak),
        "signals": signals,
    }


_CSS = """:root{--bg:#0b0c10;--panel:#111318;--line:#1f2833;--text:#c5c6c7;--muted:#8a8f98;--accent:#66fcf1;--good:#66fcf1;--warn:#ffd166;--bad:#ef476f}*{box-sizing:border-box}body{font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);margin:0;padding:24px}h1{margin:0 0 18px;font-size:22px;color:#fff}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-bottom:18px}.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px}.card h3{margin:0 0 6px;font-size:12px;color:var(--accent);text-transform:uppercase;letter-spacing:.16em}.metric{font-size:30px;font-weight:700;color:#fff}.sub{color:var(--muted);font-size:12px;margin-top:6px;line-height:1.5}.ok{color:var(--good)}.warn{color:var(--warn)}.bad{color:var(--bad)}table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden}th,td{padding:10px 12px;text-align:left;font-size:13px;border-bottom:1px solid var(--line)}th{color:var(--accent);text-transform:uppercase;letter-spacing:.12em;font-size:11px}tr:hover td{background:#15171d}a{color:var(--accent);text-decoration:none}.pill{display:inline-block;padding:4px 8px;border-radius:999px;font-size:11px;background:var(--line);color:#fff}.nav{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}.nav a{background:var(--panel);border:1px solid var(--line);padding:8px 12px;border-radius:10px;font-size:12px}.event{display:flex;gap:12px;padding:8px 10px;border-bottom:1px solid var(--line);font-size:12px}.seq{color:var(--muted);width:40px;flex:none}.kind{width:160px;flex:none;color:var(--accent)}.src{width:180px;flex:none;color:var(--muted)}.payload{color:#e6e6e6;word-break:break-word}"""


def _build_html(reasoning, memory, signals, trace_rows, by_trace, proposal, last_cycle):
    trace_table_rows_parts = []
    for r in trace_rows:
        trace_id = r['trace_id']
        trace_table_rows_parts.append(
            "<tr><td><a href='/reasoning/trace/" + trace_id + "' target='_blank'>" + trace_id + "</a></td>"
            "<td><span class='pill " + _health_class(r['health']) + "'>" + r['health'] + "</span></td>"
            "<td>" + str(r['score']) + "</td>"
            "<td>" + str(r['confidence']) + "</td>"
            "<td>" + str(r['entropy']) + "</td>"
            "<td><a href='/reasoning/drift/" + trace_id + "'>drift</a> · <a href='/reasoning/counterfactual/branch' onclick=\"var id=prompt('trace_id', '" + trace_id + "');if(!id){id='" + trace_id + "';}fetch('/reasoning/counterfactual/branch',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({trace_id:id,step_index:0,delta:{query:'calibration_probe'}})}).then(()=>alert('branched'));return false;\" >branch</a></td>"
            "<td>" + ("continuous" if r['continuous'] else "gaps") + "</td>"
            "<td><a href='/reasoning/integrity/events?trace_id=" + trace_id + "'>events</a></td></tr>"
        )
    trace_table_rows = "\n".join(trace_table_rows_parts)

    trace_replays_parts = []
    for r in trace_rows:
        trace_id = r['trace_id']
        events = by_trace.get(trace_id, [])
        replay_rows_parts = []
        for e in events:
            replay_rows_parts.append(
                "<div class='event'><div class='seq'>" + str(e.get('sequence')) + "</div>"
                "<div class='kind'>" + str(e.get('kind')) + "</div>"
                "<div class='src'>" + str(e.get('source', '')) + "</div>"
                "<div class='payload'>" + _fmt_payload(e.get('payload')) + "</div></div>"
            )
        replay_rows = "\n".join(replay_rows_parts)
        trace_replays_parts.append(
            "<div id='trace-" + trace_id + "'><h2 style='font-size:16px; color:#fff; margin:18px 0 8px;'>Replay: " + trace_id + "</h2>"
            "<div class='card'><div class='sub'>Health: <span class='pill " + _health_class(r['health']) + "'>" + r['health'] + "</span> - Score: " + str(r['score']) + " - Confidence: " + str(r['confidence']) + " - Entropy: " + str(r['entropy']) + "</div>"
            "<div style='margin-top:10px;'>" + replay_rows + "</div></div></div>"
        )
    trace_replays_html = "\n".join(trace_replays_parts)

    style = "<style>" + _CSS + "</style>\n"
    nav = (
        "<div class='nav'>"
        "<a href='/observability/dashboard'>Dashboard</a>"
        "<a href='/observability/metrics'>Metrics JSON</a>"
        "<a href='/reasoning/integrity/events'>Events</a>"
        "<a href='/reasoning/counterfactual/scan'>Counterfactual Scan</a>"
        "</div>\n"
    )
    metrics_grid = (
        "<div class='grid'>"
        "<div class='card'><h3>Traces</h3><div class='metric'>" + str(reasoning.total_traces) + "</div><div class='sub'>Active: " + str(reasoning.active_traces) + "</div></div>"
        "<div class='card'><h3>Events</h3><div class='metric'>" + str(reasoning.total_events) + "</div><div class='sub'>Tool: " + str(reasoning.tool_call_count) + " | Memory: " + str(reasoning.memory_read_count) + " | Human: " + str(reasoning.human_feedback_count) + "</div></div>"
        "<div class='card'><h3>Avg Score</h3><div class='metric'>" + str(round(reasoning.avg_score,4)) + "</div><div class='sub'>Confidence: " + str(round(reasoning.avg_confidence,4)) + "</div></div>"
        "<div class='card'><h3>Avg Entropy</h3><div class='metric'>" + str(round(reasoning.avg_entropy,4)) + "</div><div class='sub'>Drift events: " + str(reasoning.drift_count) + "</div></div>"
        "<div class='card'><h3>Memory</h3><div class='metric'>" + str(memory.total_memories) + "</div><div class='sub'>Active: " + str(memory.active_memories) + " | Archived: " + str(memory.archived_memories) + "</div></div>"
        "<div class='card'><h3>Verification</h3><div class='metric'>" + str(round(memory.verification_rate,4)) + "</div><div class='sub'>Avg reliability: " + str(round(memory.avg_source_reliability,4)) + "</div></div>"
        "</div>\n"
    )
    pending_block = ""
    if proposal:
        pending_block = (
            "<div class='card'><h3>Pending Proposal</h3>"
            "<div class='sub'>module=" + proposal.get("module", "") + " · proposal_id=" + proposal.get("proposal_id", "") + "</div>"
            "<div class='sub'><a href='/observability/console/cycle'>Run evaluation cycle</a></div>"
            "</div>\n"
        )
    last_cycle_block = ""
    if last_cycle:
        decision = last_cycle.get("decision", "?")
        color = "ok" if decision == "accepted" else "bad"
        last_cycle_block = (
            "<div class='card'><h3>Last Evaluation</h3>"
            "<div class='sub'>module=" + last_cycle.get("module", "") + " · proposal_id=" + last_cycle.get("proposal_id", "") + "</div>"
            "<div class='sub'>R_i=" + str(last_cycle.get("reality_coherence_rate")) + " · decision=<span class='" + color + "'>" + decision + "</span></div>"
            "<div class='sub'>recorded_proposal_id=" + last_cycle.get("recorded_proposal_id", "") + "</div>"
            "</div>\n"
        )
    signals_grid = (
        "<div class='grid'>"
        "<div class='card'><h3>Signals</h3>"
        "<div class='sub'>Strong: <span class='ok'>" + str(signals['strong_signals']) + "</span> - Weak: <span class='bad'>" + str(signals['weak_signals']) + "</span> - Total: " + str(signals['count']) + "</div>"
        "<div class='sub'>Avg score: " + str(signals['average']['score']) + " - Avg confidence: " + str(signals['average']['confidence']) + " - Avg entropy: " + str(signals['average']['entropy']) + "</div>"
        "<div class='sub'>Counterfactual scan: <a href='/reasoning/counterfactual/scan'>run scan</a> · Drift: <a href='/reasoning/drift/all'>all traces</a></div>"
        "</div>"
        "<div class='card'><h3>Legend</h3>"
        "<div class='sub'><span class='pill ok'>Healthy</span> score >= 0.6 and confidence >= 0.8</div>"
        "<div class='sub'><span class='pill warn'>Uncertain</span> score < 0.6 and confidence >= 0.8</div>"
        "<div class='sub'><span class='pill bad'>Weak</span> score < 0.6 and confidence < 0.6</div>"
        "</div></div>\n"
    )
    proposal_grid = pending_block + last_cycle_block
    traces_section = (
        "<div id='traces'>"
        "<h2 style='font-size:16px; color:#fff; margin:18px 0 8px;'>Trace Provenance &amp; Health</h2>"
        "<table><thead><tr><th>Trace</th><th>Health</th><th>Score</th><th>Confidence</th><th>Entropy</th><th>Drift</th><th>Errors</th><th>Continuity</th><th>Events</th></tr></thead>"
        "<tbody>\n" + trace_table_rows + "\n</tbody></table></div>\n"
    )

    return (
        "<!doctype html><html><head><meta charset='utf-8' /><meta name='viewport' content='width=device-width, initial-scale=1' /><title>MSB Operator Console</title>"
        + style +
        "</head><body><h1>MSB Operator Console</h1>" + nav + metrics_grid + signals_grid + proposal_grid + traces_section + trace_replays_html + "</body></html>"
    )


@router.get("/console")
def console() -> HTMLResponse:
    reasoning, memory = _refresh()
    all_events = reasoning_stream.global_stream(limit=1000)
    by_trace: Dict[str, list[dict[str, Any]]] = {}
    for e in all_events:
        key = e.trace_id or e.decision_id
        if not key:
            continue
        by_trace.setdefault(key, []).append({
            "event_id": e.event_id,
            "sequence": e.sequence,
            "kind": e.kind.value,
            "source": e.source,
            "payload": e.payload,
            "ts": e.ts,
        })

    trace_rows = []
    for trace_id, events in by_trace.items():
        assessments = [e for e in events if e.get("kind") == "confidence_assessment"]
        drift = [e for e in events if e.get("kind") == "drift"]
        errors = [e for e in events if e.get("kind") == "error"]
        latest = assessments[-1] if assessments else None
        score = float(latest.get("payload", {}).get("score", 0.0)) if latest else 0.0
        confidence = float(latest.get("payload", {}).get("confidence", 0.0)) if latest else 0.0
        entropy = float(latest.get("payload", {}).get("entropy", 0.0)) if latest else 0.0
        continuity = reasoning_stream.verify_continuity(trace_id)
        health = _health(score, confidence, entropy, len(drift), len(errors), continuity.get("continuous", True))
        trace_rows.append({
            "trace_id": trace_id,
            "score": round(score, 4),
            "confidence": round(confidence, 4),
            "entropy": round(entropy, 4),
            "drift_count": len(drift),
            "error_count": len(errors),
            "assessment_count": len(assessments),
            "event_count": len(events),
            "continuous": continuity.get("continuous", False),
            "health": health,
        })

    trace_rows.sort(key=lambda x: x.get("score", 0.0))
    signals = _signals(by_trace)
    proposal = _PENDING.get("latest")
    last_cycle = _PENDING.get("last_cycle")
    return HTMLResponse(_build_html(reasoning, memory, signals, trace_rows, by_trace, proposal, last_cycle))


@router.post("/console/propose")
def console_propose(proposal: Dict[str, Any]) -> JSONResponse:
    proposal.setdefault("proposal_id", "console-" + str(hash(str(proposal)))[-6:])
    _PENDING["latest"] = proposal
    return JSONResponse({"status": "pending", "proposal": proposal})


@router.get("/console/seed")
def console_seed() -> JSONResponse:
    from msb_v2.core.reasoning_bootstrap import seed_demo_baseline
    return JSONResponse(seed_demo_baseline())


@router.get("/console/cycle")
def console_cycle() -> JSONResponse:
    from msb_v2.core.reasoning_bootstrap import get_persistent_scheduler, seed_demo_baseline

    proposal = _PENDING.get("latest", {
        "proposal_id": "console-cycle",
        "module": "operator-console",
        "update_baseline": False,
    })
    if proposal.get("update_baseline"):
        seed_demo_baseline()
    scheduler = get_persistent_scheduler()
    outcome = scheduler.execute_cycle(proposal, mode="operator")
    _PENDING["last_cycle"] = outcome
    return JSONResponse(outcome)
