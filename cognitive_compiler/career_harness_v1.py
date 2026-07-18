from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"
TRACKER_FILE = PROJECT_ROOT / "data" / "applications.md"


@dataclass
class CareerHarnessResult:
    ok: bool
    event: str
    payload: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


def _next_job_num(reports_dir: Path) -> Optional[str]:
    if not reports_dir.exists():
        return None
    nums = []
    for p in reports_dir.glob("*/*.md"):
        m = re.match(r"(\d{3})-", p.name)
        if m:
            nums.append(int(m.group(1)))
    return f"{max(nums)+1:03d}" if nums else "001"


def _next_report_number_dir(reports_dir: Path) -> Optional[Path]:
    n = _next_job_num(reports_dir)
    if not n:
        return None
    next_dir = reports_dir / n
    return next_dir


def _today_iso() -> str:
    return date.today().isoformat()


def _slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "job"


def _tracker_next_seq(tracker_file: Path) -> int:
    if not tracker_file.exists():
        return 1
    seq = 0
    for line in tracker_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("| "):
            parts = [p.strip() for p in line.strip().strip("|").split("|")]
            if parts and parts[0].isdigit():
                seq = max(seq, int(parts[0]))
    return seq + 1


def _append_tracker_row(company: str, role: str, score: float, tracker_file: Path, reports_dir: Path) -> None:
    tracker_file.parent.mkdir(parents=True, exist_ok=True)
    seq = _tracker_next_seq(tracker_file)
    today = _today_iso()
    report_name = f"{seq:03d}-{_slugify(company)}-{today}.md"
    row = f"| {seq} | {today} | {company} | — | {role} | {score:.1f} | Evaluated | ❌ | [{seq}](reports/{seq}-{_slugify(company)}-{today}) | |\n"
    if not tracker_file.exists():
        tracker_file.write_text("| # | Date | Company | Via | Role | Score | Status | PDF | Report | Notes |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n", encoding="utf-8")
    with tracker_file.open("a", encoding="utf-8") as f:
        f.write(row)


class CareerHarness:
    def __init__(self, project_root: Optional[Path | str] = None) -> None:
        self.root = Path(project_root).resolve() if project_root else PROJECT_ROOT
        self.ready = self._check_prereqs()

    def _resolve(self):
        return {
            "reports": self.root / "reports",
            "tracker": self.root / "data" / "applications.md",
            "cv": self.root / "cv.md",
            "shared": self.root / "modes" / "_shared.md",
            "oferta": self.root / "modes" / "oferta.md",
        }

    def _check_prereqs(self) -> bool:
        p = self._resolve()
        return p["cv"].exists() and p["shared"].exists() and p["oferta"].exists()

    def plan(self, goal: str) -> Dict[str, Any]:
        p = self._resolve()
        return {
            "ok": self.ready,
            "goal": goal,
            "missing": [str(p[k]) for k in ("cv", "shared", "oferta") if not p[k].exists()],
        }

    def evaluate_jd_text(self, company: str, role: str, jd_text: str, score: Optional[float] = None) -> CareerHarnessResult:
        if not self.ready:
            return CareerHarnessResult(ok=False, event="blocked", error="missing cv.md / modes/_shared.md / modes/oferta.md")

        p = self._resolve()
        n = _next_job_num(p["reports"])
        if n is None:
            return CareerHarnessResult(ok=False, event="blocked", error="reports/ directory unavailable")

        report_dir = p["reports"] / n
        report_dir.mkdir(parents=True, exist_ok=True)
        report_name = f"{n}-{_slugify(company)}-{_today_iso()}.md"
        report_path = report_dir / report_name

        header = (
            f"# Evaluation: {company} — {role}\n\n"
            f"**Date:** {_today_iso()}\n**URL:**\n**Via:** —\n**Archetype:** pending-agent-evaluation\n"
            f"**Score:** {score if score is not None else 'pending'}/5\n**Legitimacy:** pending\n**PDF:** ❌\n---\n\n"
        )

        machine_summary = (
            "## Machine Summary\n"
            "```\n"
            f"company: {company}\nrole: {role}\ndate: {_today_iso()}\narchetype: pending\n"
            "score: null\nlegitimacy: pending\nrisk_summary:\n  posting_legitimacy: '— not evaluated'\n"
            "  employment_classification: '— not evaluated'\n  culture_screen: '— not evaluated'\n"
            "  interview_red_flags: '— no interview sessions yet'\n  ai_claims_vs_infrastructure: '— not evaluated'\n"
            "```\n\n"
        )

        blocks = (
            "## A) Role Summary\n_AUTO-PIPELINE STUB — run the agent with this JD + cv.md to generate full blocks A-G._\n\n"
            "## B) Match with CV\n_AUTO-PIPELINE STUB_\n\n"
            "## C) Level and Strategy\n_AUTO-PIPELINE STUB_\n\n"
            "## D) Comp and Demand\n_AUTO-PIPELINE STUB_\n\n"
            "## E) Customization Plan\n_AUTO-PIPELINE STUB_\n\n"
            "## F) Interview Plan\n_AUTO-PIPELINE STUB_\n\n"
            "## G) Posting Legitimacy\n_AUTO-PIPELINE STUB_\n\n## Risk Summary\n\n| Signal | Status |\n|--------|--------|\n| Posting legitimacy | — not evaluated |\n| Employment classification | — not evaluated |\n| Culture screen | — not evaluated |\n| Interview red flags | — no interview sessions yet |\n| AI claims vs. infrastructure | — not evaluated |\n\n\n"
        )

        body_md = header + machine_summary + blocks
        report_path.write_text(body_md, encoding="utf-8")

        if score is None:
            _append_tracker_row(company, role, 0.0, p["tracker"], p["reports"])
            tracker_score = 0.0
        else:
            _append_tracker_row(company, role, float(score), p["tracker"], p["reports"])
            tracker_score = float(score)

        return CareerHarnessResult(
            ok=True,
            event="evaluated",
            payload={
                "report": str(report_path.relative_to(self.root)),
                "company": company,
                "role": role,
                "score": tracker_score,
                "status": "Evaluated",
            },
        )
