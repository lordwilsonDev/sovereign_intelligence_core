from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from msb_v2.audit.business_metrics import BusinessMetrics


class IntegrityReportPDF:
    def __init__(self, audit=None) -> None:
        self._metrics = BusinessMetrics(audit=audit)

    def generate(self, output_path: str | Path, client_name: str = "Client") -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        snapshot = self._metrics.snapshot()
        summary = snapshot.get("summary", {})
        impact = snapshot.get("business_impact", {})

        doc = SimpleDocTemplate(str(output_path), pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=22,
            spaceAfter=20,
            textColor=colors.HexColor("#1a3a5c"),
        )
        story.append(Paragraph("Business Integrity Report", title_style))
        story.append(Paragraph(f"Generated for: {client_name}", styles["Heading2"]))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", styles["Normal"]))
        story.append(Spacer(1, 0.25 * inch))

        story.append(Paragraph("Executive Summary", styles["Heading2"]))
        story.append(Paragraph(
            f"This period, your automated systems processed {summary.get('total_workflows', 0)} workflows "
            f"with a {summary.get('success_rate', 0) * 100:.1f}% success rate. "
            f"The system autonomously recovered from {summary.get('errors_recovered', 0)} errors, "
            f"saving approximately {impact.get('hours_saved', 0):.1f} hours of manual work.",
            styles["Normal"],
        ))
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph("Business Impact", styles["Heading2"]))
        impact_data = [
            ["Metric", "Value"],
            ["Hours Saved", f"{impact.get('hours_saved', 0):.1f}"],
            ["Revenue Influenced", f"${impact.get('revenue_influenced', 0):,.0f}"],
            ["Error Reduction", f"{impact.get('error_reduction', 0):.1f}%"],
            ["Automation Adoption", f"{impact.get('automation_adoption_rate', 0) * 100:.1f}%"],
        ]
        impact_table = Table(impact_data, colWidths=[3 * inch, 2 * inch])
        impact_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(impact_table)
        story.append(Spacer(1, 0.2 * inch))

        immutable = snapshot.get("immutable_record", {})
        sovereign = snapshot.get("sovereign", {})
        story.append(Paragraph("Sovereign Audit", styles["Heading2"]))
        story.append(Paragraph(
            f"Falsified Policy Actions: {sovereign.get('falsified_count', 0)} "
            f"| FTS: {sovereign.get('fts', 0) * 100:.1f}% "
            f"| Assumption Debt: {sovereign.get('assumption_debt', 0)}",
            styles["Normal"],
        ))
        story.append(Spacer(1, 0.1 * inch))
        records = sovereign.get("records") or []
        if records:
            story.append(Paragraph("Falsification Trend", styles["Heading2"]))
            story.append(Spacer(1, 0.05 * inch))
            trend_data = [["Policy", "Outcome", "Improvement"]]
            for record in records[:20]:
                trend_data.append([
                    str(record.get("policy", "")),
                    str(record.get("outcome", "")),
                    str(record.get("improvement", "")),
                ])
            trend_table = Table(trend_data, colWidths=[2.5 * inch, 1.2 * inch, 1.2 * inch])
            trend_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3a5c")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(trend_table)
            story.append(Spacer(1, 0.1 * inch))

        story.append(Paragraph("Immutable Record", styles["Heading2"]))
        story.append(Paragraph(
            f"Root Hash: {immutable.get('root_hash', 'N/A')}",
            styles["Normal"],
        ))
        story.append(Paragraph(
            f"Total Blocks: {immutable.get('total_blocks', 0)}",
            styles["Normal"],
        ))

        doc.build(story)
        return output_path
