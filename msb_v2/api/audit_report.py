from __future__ import annotations

import hashlib
from typing import Any

from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse

from msb_v2.api.middleware import require_bearer_token
from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.business_metrics import BusinessMetrics
from msb_v2.audit.storage import AuditStore

router = APIRouter()


def _engine() -> AuditEngine:
    return AuditEngine(store=AuditStore())


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _render_report(client_name: str, snapshot: dict[str, Any]) -> str:
    summary = snapshot.get("summary", {})
    impact = snapshot.get("business_impact", {})
    recommendations = snapshot.get("recommendations", [])
    immutable = snapshot.get("immutable_record", {})

    recommendation_rows = "".join(
        f"<li>{_escape(rec.get('suggestion', ''))}</li>" for rec in recommendations
    )

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Business Integrity Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; color: #1a1a1a; max-width: 900px; margin: 0 auto; padding: 24px; }}
    header {{ border-bottom: 2px solid #1a3a5c; padding-bottom: 12px; }}
    h1 {{ color: #1a3a5c; margin: 0; }}
    h2 {{ color: #1a3a5c; margin-top: 28px; font-size: 18px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 10px; }}
    th, td {{ border: 1px solid #9ab0c8; padding: 8px 10px; text-align: left; }}
    th {{ background: #1a3a5c; color: #ffffff; }}
    td {{ background: #f5f8fb; }}
    .meta {{ color: #4a5568; }}
    .metric-value {{ font-weight: 700; }}
    ul {{ margin-top: 6px; }}
    .immutable {{ color: #4a5568; font-family: monospace; }}
  </style>
</head>
<body>
  <header>
    <h1>Business Integrity Report</h1>
    <p class="meta">Generated for: <strong>{_escape(client_name)}</strong></p>
    <p class="meta">Period workflows: <strong>{summary.get('total_workflows', 0)}</strong> &middot; Success rate: <strong>{summary.get('success_rate', 0) * 100:.1f}%</strong></p>
  </header>

  <section>
    <h2>Executive Summary</h2>
    <p>This period, your automated systems processed <strong>{summary.get('total_workflows', 0)}</strong> workflows with a <strong>{summary.get('success_rate', 0) * 100:.1f}%</strong> success rate. The system autonomously recovered from <strong>{summary.get('errors_recovered', 0)}</strong> errors, saving approximately <strong>{impact.get('hours_saved', 0):.1f}</strong> hours of manual work.</p>
  </section>

  <section>
    <h2>Workflow Integrity</h2>
    <table>
      <tr><th>Metric</th><th>Value</th></tr>
      <tr><td>Total Workflows</td><td class="metric-value">{summary.get('total_workflows', 0)}</td></tr>
      <tr><td>Succeeded</td><td class="metric-value">{summary.get('succeeded', 0)}</td></tr>
      <tr><td>Failed</td><td class="metric-value">{summary.get('failed', 0)}</td></tr>
      <tr><td>Success Rate</td><td class="metric-value">{summary.get('success_rate', 0) * 100:.1f}%</td></tr>
      <tr><td>Errors Recovered</td><td class="metric-value">{summary.get('errors_recovered', 0)}</td></tr>
    </table>
  </section>

  <section>
    <h2>Business Impact</h2>
    <table>
      <tr><th>Metric</th><th>Value</th></tr>
      <tr><td>Hours Saved</td><td class="metric-value">{impact.get('hours_saved', 0):.1f}</td></tr>
      <tr><td>Revenue Influenced</td><td class="metric-value">${impact.get('revenue_influenced', 0):,.0f}</td></tr>
      <tr><td>Error Reduction</td><td class="metric-value">{impact.get('error_reduction', 0):.1f}%</td></tr>
      <tr><td>Automation Adoption</td><td class="metric-value">{impact.get('automation_adoption_rate', 0) * 100:.1f}%</td></tr>
    </table>
  </section>

  {f'''<section>
    <h2>Improvement Recommendations</h2>
    <ul>{recommendation_rows}</ul>
  </section>''' if recommendation_rows else ''}

  <section>
    <h2>Immutable Record</h2>
    <p class="immutable">Root Hash: <code>{immutable.get('root_hash', 'N/A')}</code></p>
    <p class="immutable">Total Blocks: <code>{immutable.get('total_blocks', 0)}</code></p>
    <p class="immutable">This record is derived from the current audit ledger snapshot.</p>
  </section>
</body>
</html>
"""


@router.get("/report/html")
def generate_report_html(
    client_name: str = Query("Client", description="Client name for the report"),
    engine: AuditEngine = Depends(_engine),
) -> HTMLResponse:
    snapshot = BusinessMetrics(audit=engine).snapshot()
    html = _render_report(client_name, snapshot)
    etag = hashlib.sha256(html.encode("utf-8")).hexdigest()
    return HTMLResponse(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={
            "Cache-Control": "no-store",
            "ETag": f'"{etag}"',
        },
    )
