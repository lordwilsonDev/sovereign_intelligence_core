from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

from cognitive_compiler.harness_abc import BaseHarness, HarnessResult, HarnessTelemetry
from cognitive_compiler.router_observer import RouterObserver


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"
TRACKER_FILE = PROJECT_ROOT / "data" / "applications.md"


def _next_job_num(reports_dir: Path) -> Optional[str]:
    if not reports_dir.exists():
        return None
    nums = []
    for p in reports_dir.glob("*/*.md"):
        m = re.match(r"(\d{3})-", p.name)
        if m:
            nums.append(int(m.group(1)))
    return f"{max(nums)+1:03d}" if nums else "001"


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


class CareerHarness(BaseHarness):
    def __init__(self, project_root: Optional[Path | str] = None, observer: Optional[RouterObserver] = None) -> None:
        self.root = Path(project_root).resolve() if project_root else PROJECT_ROOT
        self.observer = observer or RouterObserver()
        self.ready = False
        self._cached_cv: Optional[str] = None
        self._last_result: Optional[HarnessResult] = None

    def initialize(self, context: Dict[str, Any]) -> Dict[str, Any]:
        p = self._resolve()
        self.ready = p["cv"].exists() and p["shared"].exists() and p["oferta"].exists()
        if self.ready:
            try:
                self._cached_cv = p["cv"].read_text(encoding="utf-8")
            except Exception:
                self._cached_cv = ""
        return {"ok": self.ready, "missing": [str(p[k]) for k in ("cv", "shared", "oferta") if not p[k].exists()]}

    def evaluate_jd_text(self, company: str, role: str, jd_text: str, score: Optional[float] = None) -> HarnessResult:
        return self.evaluate(
            jd_text,
            context={
                "career_company": company,
                "career_role": role,
                "career_jd": jd_text,
                "career_score": score,
            },
        )

    def evaluate(self, query: str, context: Dict[str, Any]) -> HarnessResult:
        company = context.get("career_company") or self._guess_company(query)
        role = context.get("career_role") or self._guess_role(query)
        jd = context.get("career_jd", query)
        parsed = self._parse_jd(jd, fallback_company=company, fallback_role=role)
        score_raw = context.get("career_score")
        score = self._score(parsed)
        if score_raw is not None:
            try:
                score = float(score_raw)
            except Exception:
                pass

        p = self._resolve()
        if not p["cv"].exists() or not p["shared"].exists() or not p["oferta"].exists():
            return HarnessResult(ok=False, event="blocked", error="missing cv.md / modes/_shared.md / modes/oferta.md", telemetry=HarnessTelemetry(error_class="prerequisite"))

        p = self._resolve()
        report = self._write_report(parsed, score)
        _append_tracker_row(parsed.company, parsed.role, score, p["tracker"], p["reports"])

        payload = {
            "company": parsed.company,
            "role": parsed.role,
            "score": score,
            "report": str(report.relative_to(self.root)),
            "status": "Evaluated",
            "parsed": {
                "skills": parsed.skills[:8],
                "requirements": parsed.requirements[:8],
                "seniority": parsed.seniority,
                "remote": parsed.remote,
            },
        }
        telemetry = HarnessTelemetry(routing_confidence=context.get("confidence", 0.0), tags=["career", "evaluate"])
        result = HarnessResult(ok=True, event="evaluated", payload=payload, telemetry=telemetry)
        self._last_result = result
        try:
            self.observer.record({"decision": {"primary": "career", "confidence": telemetry.routing_confidence}}, query=query)
        except Exception:
            pass
        return result

    def execute(self, query: str, *args: Any, context: Optional[Dict[str, Any]] = None, **kwargs: Any) -> HarnessResult:
        if context is None:
            context = {}
        if not self.ready:
            return HarnessResult(ok=False, event="blocked", error="missing cv.md / modes/_shared.md / modes/oferta.md", telemetry=HarnessTelemetry(error_class="prerequisite"))
        if self._last_result and self._last_result.event == "evaluated":
            return self._last_result
        return self.evaluate(query, context)

    def observe(self, result: HarnessResult) -> Dict[str, Any]:
        return {
            "event": result.event,
            "score": result.payload.get("score"),
            "telemetry": {
                "execution_time_s": result.telemetry.execution_time_s,
                "fallback_reason": result.telemetry.fallback_reason,
                "error_class": result.telemetry.error_class,
            },
        }

    def repair(self, result: HarnessResult) -> Optional[HarnessResult]:
        if result.ok:
            return None
        if result.telemetry.error_class == "prerequisite":
            return None
        repaired = HarnessResult(ok=True, event="repaired", payload={"previous": result.event}, telemetry=HarnessTelemetry(tags=["career", "repair"]))
        self._last_result = repaired
        return repaired

    def shutdown(self) -> Dict[str, Any]:
        return {"ok": True, "event": "shutdown"}

    def plan(self, goal: str) -> Dict[str, Any]:
        init = self.initialize({})
        return {"ok": init["ok"], "goal": goal, "missing": init.get("missing", [])}

    def _resolve(self):
        return {
            "reports": self.root / "reports",
            "tracker": self.root / "data" / "applications.md",
            "cv": self.root / "cv.md",
            "shared": self.root / "modes" / "_shared.md",
            "oferta": self.root / "modes" / "oferta.md",
        }

    def _parse_jd(self, jd: str, fallback_company: str, fallback_role: str) -> Any:
        p = _ParsedJD()
        p.text = jd
        lines = [ln.strip() for ln in jd.splitlines() if ln.strip()]
        if lines:
            p.role = lines[0].strip()[:120] or fallback_role
        for ln in lines:
            if not p.company or p.company == "Unknown":
                m = re.search(r"at\s+([A-Za-z0-9 &._-]+)", ln)
                if m:
                    p.company = m.group(1).strip()
            for marker in ["remote", "hybrid", "onsite"]:
                if marker in ln.lower() and p.remote is None:
                    p.remote = marker
            for marker in ["junior", "mid", "senior", "staff", "lead", "principal", "director", "vp"]:
                if marker in ln.lower() and p.seniority is None:
                    p.seniority = marker
            m = re.findall(r"(?i)(?:experience|proficient|skilled|built|led|using|with)\s+(?:in\s+)?([A-Za-z0-9#+./_-]+(?:[,\s]+[A-Za-z0-9#+./_-]+){0,4})", ln)
            if m:
                p.skills.extend(m[:3])
        p.skills = sorted(set([s.strip(".,; ") for s in p.skills if s]))[:20]
        p.requirements = [ln for ln in lines if any(k in ln.lower() for k in ["require", "responsib", "build", "design", "implement", "deliver", "manage", "lead", "develop"])][:20]
        p.responsibilities = [ln for ln in lines if any(k in ln.lower() for k in ["collaborate", "partner", "mentor", "communicate", "drive", "own", "support"])][:20]
        if p.company == "Unknown":
            p.company = fallback_company
        if p.role == "Unknown":
            p.role = fallback_role
        return p

    def _guess_company(self, query: str) -> str:
        candidates = re.findall(r"(?<![\w])([A-Z][A-Za-z0-9 &._-]{2,40})(?:\s+is\s+looking|\s+seeks\s+|\s+role\s+at\s+|\s+at\s+)(?=[A-Z])", query)
        return candidates[0].strip() if candidates else "Unknown"

    def guess_role(self, query: str) -> str:
        for token in query.split("|"):
            token = token.strip()
            if any(k in token.lower() for k in ["engineer", "manager", "designer", "analyst", "researcher", "lead", "director"]):
                return token[:120]
        return query[:120].strip() or "Unknown"

    def _guess_role(self, query: str) -> str:
        return self.guess_role(query)

    def _score(self, parsed: Any) -> float:
        base = 3.0
        evidence = 0
        evidence += 1 if parsed.skills else 0
        evidence += 1 if parsed.requirements else 0
        evidence += 1 if parsed.responsibilities else 0
        evidence += 0.5 if parsed.seniority else 0
        evidence += 0.5 if parsed.remote else 0
        score = min(5.0, base + ((evidence / 5) * 2))
        return round(score, 2)

    def _write_report(self, parsed: Any, score: float) -> Path:
        n = _next_job_num(self.root / "reports")
        if not n:
            raise RuntimeError("reports/ directory unavailable")
        report_dir = self.root / "reports" / n
        report_dir.mkdir(parents=True, exist_ok=True)
        name = f"{n}-{_slugify(parsed.company)}-{_today_iso()}.md"
        path = report_dir / name
        cv_preview = (self._cached_cv or "").splitlines()[:6]
        body = "\n".join([
            f"# Evaluation: {parsed.company} — {parsed.role}",
            "",
            f"**Date:** {_today_iso()}",
            "**URL:**",
            "**Via:** —",
            f"**Archetype:** {self._classify_archetype(parsed)}",
            f"**Score:** {score}/5",
            "**Legitimacy:** pending",
            "**PDF:** ❌",
            "---",
            "",
            "## Machine Summary",
            "```yaml",
            f"company: {parsed.company}",
            f"role: {parsed.role}",
            f"date: {_today_iso()}",
            "archetype: pending",
            f"score: {score}",
            "legitimacy: pending",
            "risk_summary:",
            "  posting_legitimacy: '— not evaluated'",
            "  employment_classification: '— not evaluated'",
            "  culture_screen: '— not evaluated'",
            "  interview_red_flags: '— no interview sessions yet'",
            "  ai_claims_vs_infrastructure: '— not evaluated'",
            "```",
            "",
            "## A) Role Summary",
            f"- **Detected role:** {parsed.role}",
            f"- **Likely company:** {parsed.company}",
            f"- **Seniority:** {parsed.seniority or '—'}",
            f"- **Remote:** {parsed.remote or '—'}",
            f"- **CV status:** {'loaded' if self._cached_cv else 'missing'}",
            "",
            "## B) Match with CV",
            "| JD Requirement | CV Evidence | Match |",
            "|----------------|-------------|-------|",
            *[f"| {r} | {'/'.join(cv_preview[:2])} | partial |" for r in parsed.requirements[:5]],
            "",
            "## C) Level and Strategy",
            f"- Detected seniority: {parsed.seniority or '—'}",
            "- Position against current trajectory below",
            "",
            "## D) Comp and Demand",
            "- Advertised (JD): not stated",
            "",
            "## E) Customization Plan",
            "| # | Section | Current status | Proposed change | Why |",
            "|---|---------|---------------|-----------------|-----|",
            "| 1 | Summary | Generic | Tailor to detected role keywords | Improve ATS/human match |",
            "| 2 | Bullets | Static | Mirror top JD skills | Increase relevance |",
            "| 3 | LinkedIn | Default | Add JD phrases | Signal fit |",
            "",
            "## F) Interview Plan",
            "| # | JD Requirement | STAR+R Story | S | T | A | R | Reflection |",
            "|---|-----------------|-----------------|---|---|---|---|------------|",
            "| 1 | " + (parsed.requirements[0] if parsed.requirements else "Role fit") + " | Pending story bank | ... | ... | ... | ... | ... |",
            "",
            "## G) Posting Legitimacy",
            "- Assessment: Proceed with Caution — limited signals",
            "",
            "## Risk Summary",
            "",
            "| Signal | Status |",
            "|--------|--------|",
            "| Posting legitimacy | — not evaluated |",
            "| Employment classification | — not evaluated |",
            "| Culture screen | — not evaluated |",
            "| Interview red flags | — no interview sessions yet |",
            "| AI claims vs. infrastructure | — not evaluated |",
            "",
        ])
        path.write_text(body, encoding="utf-8")
        return path

    def _classify_archetype(self, parsed: Any) -> str:
        blob = " ".join(parsed.skills + parsed.requirements + parsed.responsibilities).lower()
        if any(k in blob for k in ["ml", "pytorch", "tensorflow", "deep learning", "nlp", "cv"]):
            return "AI/ML"
        if any(k in blob for k in ["backend", "api", "microservice", "distributed", "golang", "java", "python"]):
            return "Engineering"
        if any(k in blob for k in ["product", "roadmap", "stakeholder", "discovery"]):
            return "Product"
        if any(k in blob for k in ["infrastructure", "cloud", "devops", "platform", "sre"]):
            return "Infrastructure"
        return "General"


@dataclass
class _ParsedJD:
    company: str = "Unknown"
    role: str = "Unknown"
    skills: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    seniority: Optional[str] = None
    remote: Optional[str] = None
    text: str = ""
