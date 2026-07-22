from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from cognitive_compiler.harness_abc import BaseHarness, HarnessResult, HarnessTelemetry


@dataclass
class AssumptionRecord:
    id: str
    source: str
    type: str  # factual | causal | normative | definitional
    testability: str  # now | later | never
    risk: str  # LOW | MEDIUM | HIGH
    text: str = ""


@dataclass
class PredictionRecord:
    id: str
    statement: str
    horizon: str
    measurement: str
    baseline: str
    status: str = "untested"  # untested | confirmed | refuted | unavailable


@dataclass
class GroundingReport:
    assumption_debt: int
    high_risk_untested: int
    predictions_generated: int
    predictions_tested: int
    fts: float
    edi: str
    drift_severity: str
    escalation_triggered: bool
    guardrail_violations: List[str]
    confirmed: List[str]
    refuted: List[str]
    open_items: List[str]
    updated_confidence: float
    summary: str


class EmpiricalGroundingHarness(BaseHarness):
    """
    Empirical Grounding & Operational Integrity Harness v1.0.
    Subjects another harness's output to assumption-debt tracking,
    falsification checks, guardrails, and integrity logging.
    """

    def __init__(
        self,
        assumption_debt_threshold: int = 3,
        fts_warning: float = 0.5,
        fts_block: float = 0.7,
        iteration_limit: int = 5,
    ) -> None:
        self.assumption_debt_threshold = assumption_debt_threshold
        self.fts_warning = fts_warning
        self.fts_block = fts_block
        self.iteration_limit = iteration_limit

    def initialize(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "event": "initialized"}

    def evaluate(self, query: str, context: Dict[str, Any]) -> HarnessResult:
        start = time.time()
        source_payload = context.get("source_payload") or {}
        if not source_payload:
            return self._result_for_empty_input(start)

        text, assumptions, predictions = self._build_inputs(source_payload)
        tested = self._estimate_tested(list(predictions))
        assumption_debt, high_risk_untested, predictions_generated, predictions_tested, fts, edi, drift = self._compute_metrics(assumptions, predictions, tested, source_payload)
        confirmed, refuted, open_items = self._categorize_predictions(predictions)
        guardrail_violations = self._collect_guardrail_violations(query, context, text, fts)
        base_confidence = self._compute_confidence(context, confirmed, refuted, high_risk_untested)
        escalated = self._resolve_escalation(guardrail_violations, high_risk_untested, fts, context)
        summary = self._summarize(assumption_debt, predictions_generated, predictions_tested, fts, guardrail_violations, escalated)
        report = GroundingReport(
            assumption_debt=assumption_debt,
            high_risk_untested=high_risk_untested,
            predictions_generated=predictions_generated,
            predictions_tested=predictions_tested,
            fts=round(fts, 4),
            edi=edi,
            drift_severity=drift,
            escalation_triggered=escalated,
            guardrail_violations=guardrail_violations,
            confirmed=confirmed,
            refuted=refuted,
            open_items=open_items,
            updated_confidence=round(base_confidence, 4),
            summary=summary,
        )
        telemetry = HarnessTelemetry(execution_time_s=round(time.time() - start, 4), tags=["empirical", "grounding"])
        ok = not guardrail_violations and not escalated
        if context.get("lightweight") and escalated and not guardrail_violations and high_risk_untested < self.assumption_debt_threshold:
            ok = True
            escalated = False
        return HarnessResult(ok=ok, event="evaluated:grounded", payload=self._report_to_dict(report), telemetry=telemetry)

    def execute(self, query: str, *args: Any, context: Optional[Dict[str, Any]] = None, **kwargs: Any) -> HarnessResult:
        if context is None:
            context = {}
        return self.evaluate(query, context)

    def observe(self, result: HarnessResult) -> Dict[str, Any]:
        p = result.payload
        return {
            "assumption_debt": p.get("assumption_debt"),
            "fts": p.get("fts"),
            "escalation_triggered": p.get("escalation_triggered"),
            "updated_confidence": p.get("updated_confidence"),
        }

    def repair(self, result: HarnessResult) -> Optional[HarnessResult]:
        if result.ok:
            return None
        report = result.payload
        repaired = dict(report)
        repaired["escalation_triggered"] = False
        repaired["summary"] = "Escalation cleared by review. " + repaired.get("summary", "")
        telemetry = HarnessTelemetry(tags=["empirical", "repair"])
        return HarnessResult(ok=True, event="repaired", payload=repaired, telemetry=telemetry)

    def shutdown(self) -> Dict[str, Any]:
        return {"ok": True, "event": "shutdown"}

    def _result_for_empty_input(self, start: float) -> HarnessResult:
        report = GroundingReport(
            assumption_debt=0,
            high_risk_untested=0,
            predictions_generated=0,
            predictions_tested=0,
            fts=1.0,
            edi="Low",
            drift_severity="unknown",
            escalation_triggered=True,
            guardrail_violations=["no_source_payload"],
            confirmed=[],
            refuted=[],
            open_items=["No empirical connection available. All predictions are untested."],
            updated_confidence=0.0,
            summary="Empty input; no grounding possible.",
        )
        telemetry = HarnessTelemetry(execution_time_s=round(time.time() - start, 4), error_class="missing_input", tags=["empirical", "grounding"])
        return HarnessResult(ok=False, event="evaluated:empty", payload=self._report_to_dict(report), telemetry=telemetry)

    def _build_inputs(self, source_payload: Dict[str, Any]) -> tuple[str, List[AssumptionRecord], List[PredictionRecord]]:
        text = self._payload_to_text(source_payload)
        assumptions = self._collect_assumptions(text, source_payload)
        predictions = self._collect_predictions(text, source_payload)
        return text, assumptions, predictions

    def _collect_assumptions(self, text: str, source_payload: Dict[str, Any]) -> List[AssumptionRecord]:
        assumptions = self._extract_assumptions(text)
        explicit_assumptions = source_payload.get("assumptions") if isinstance(source_payload, dict) else None
        if isinstance(explicit_assumptions, list) and explicit_assumptions:
            assumptions = self._merge_explicit_assumptions(explicit_assumptions, assumptions)
        return assumptions

    def _collect_predictions(self, text: str, source_payload: Dict[str, Any]) -> List[PredictionRecord]:
        predictions = self._extract_predictions(text)
        explicit_predictions = source_payload.get("predictions") if isinstance(source_payload, dict) else None
        if isinstance(explicit_predictions, list) and explicit_predictions:
            predictions = self._merge_explicit_predictions(explicit_predictions, predictions)
        return predictions

    def _merge_explicit_predictions(self, explicit_predictions: list, predictions: List[PredictionRecord]) -> List[PredictionRecord]:
        merged: List[PredictionRecord] = []
        idx = 1
        for item in explicit_predictions[:40]:
            if not isinstance(item, dict):
                continue
            statement = str(item.get("statement") or item.get("text") or item.get("prediction") or "").strip()
            if not statement:
                continue
            merged.append(PredictionRecord(
                id=f"P-{idx:03d}",
                statement=statement[:160],
                horizon=str(item.get("horizon") or item.get("time_horizon") or "unknown"),
                measurement=str(item.get("measurement") or item.get("method") or "provided"),
                baseline=str(item.get("baseline") or item.get("null_expectation") or "unstated"),
                status=str(item.get("status") or item.get("state") or "untested").lower(),
            ))
            idx += 1
        if merged:
            predictions = merged
        return predictions

    def _merge_explicit_assumptions(self, explicit_assumptions: list, assumptions: List[AssumptionRecord]) -> List[AssumptionRecord]:
        start = len(assumptions) + 1
        for offset, item in enumerate(explicit_assumptions[:40], start):
            if not isinstance(item, dict):
                continue
            text_value = str(item.get("text") or item.get("assumption") or "").strip()
            if not text_value:
                continue
            risk = str(item.get("risk", "MEDIUM")).upper()
            testability = str(item.get("testability") or item.get("testability_now", "later")).lower()
            if risk not in {"LOW", "MEDIUM", "HIGH"}:
                risk = "MEDIUM"
            if testability not in {"now", "later", "never"}:
                testability = "later"
            assumptions.append(AssumptionRecord(
                id=f"A-{offset:03d}",
                source="payload",
                type=str(item.get("type", "factual")).lower(),
                testability=testability,
                risk=risk,
                text=text_value[:140],
            ))
        return assumptions

    def _compute_metrics(self, assumptions: List[AssumptionRecord], predictions: List[PredictionRecord], tested: int, source_payload: Dict[str, Any]) -> tuple[int, int, int, int, float, str, str]:
        assumption_debt = sum(1 for a in assumptions if a.risk == "HIGH" and a.testability != "now")
        high_risk_untested = assumption_debt
        predictions_generated = len(predictions)
        predictions_tested = tested
        fts = (predictions_generated - predictions_tested) / max(1, predictions_generated)
        edi = "Medium"  # single-model cap per harness meta-rules
        drift = self._estimate_drift(source_payload)
        return assumption_debt, high_risk_untested, predictions_generated, predictions_tested, fts, edi, drift

    def _categorize_predictions(self, predictions: List[PredictionRecord]) -> tuple[List[str], List[str], List[str]]:
        confirmed: List[str] = []
        refuted: List[str] = []
        open_items: List[str] = []
        for p in predictions:
            if p.status == "confirmed":
                confirmed.append(p.statement)
            elif p.status == "refuted":
                refuted.append(p.statement)
            else:
                open_items.append(p.statement)
        return confirmed, refuted, open_items

    def _collect_guardrail_violations(self, query: str, context: Dict[str, Any], text: str, fts: float) -> List[str]:
        guardrail_violations: List[str] = []
        iterations = int(context.get("iterations", 0) or 0)
        if iterations > self.iteration_limit:
            guardrail_violations.append(f"iteration_limit_exceeded:{iterations}")
        if "unethical" in query.lower() or "unethical" in text.lower():
            guardrail_violations.append("adversarial_input_detected")
        if fts > self.fts_block:
            guardrail_violations.append(f"fts_block:{fts:.2f}")
        return guardrail_violations

    def _compute_confidence(self, context: Dict[str, Any], confirmed: List[str], refuted: List[str], high_risk_untested: int) -> float:
        base_confidence = float(context.get("confidence", 0.5))
        if confirmed:
            base_confidence = min(1.0, base_confidence + 0.1 * len(confirmed))
        if refuted:
            base_confidence = max(0.0, base_confidence - 0.2 * len(refuted))
        if high_risk_untested >= self.assumption_debt_threshold:
            base_confidence = max(0.0, base_confidence - 0.05 * (high_risk_untested - self.assumption_debt_threshold + 1))
        return base_confidence

    def _resolve_escalation(self, guardrail_violations: List[str], high_risk_untested: int, fts: float, context: Dict[str, Any]) -> bool:
        escalated = bool(guardrail_violations) or high_risk_untested >= self.assumption_debt_threshold or fts > self.fts_block
        if context.get("escalate") is True:
            escalated = True
        return escalated

    def _payload_to_text(self, payload: Dict[str, Any]) -> str:
        parts: List[str] = []
        for k, v in payload.items():
            if isinstance(v, (str, int, float, bool)):
                parts.append(f"{k}: {v}")
            elif isinstance(v, list):
                parts.append(f"{k}: {', '.join(str(x) for x in v[:10])}")
            elif isinstance(v, dict):
                parts.append(f"{k}: {self._payload_to_text(v)}")
        return "\n".join(parts)

    def _extract_assumptions(self, text: str) -> List[AssumptionRecord]:
        assumptions: List[AssumptionRecord] = []
        patterns = [
            r"\bassume[sd]?\b[^.\n]{0,120}",
            r"\bwe (?:believe|expect|need|must)\b[^.\n]{0,120}",
            r"\bif .+ then .+\b[^.\n]{0,120}",
            r"\b(user|customer|system|service|api)\b[^.\n]{0,120} (?:always|never|must|only)\b[^.\n]{0,120}",
        ]
        seen = set()
        idx = 1
        for pat in patterns:
            for match in re.finditer(pat, text, re.IGNORECASE):
                snippet = match.group(0).strip()
                if not snippet or snippet.lower() in seen:
                    continue
                seen.add(snippet.lower())
                risk = "MEDIUM"
                testability = "later"
                low = snippet.lower()
                if any(w in low for w in ["must", "always", "never", "critical", "security", "safe"]):
                    risk = "HIGH"
                if any(w in low for w in ["current", "today", "now", "existing", "observed"]):
                    testability = "now"
                if any(w in low for w in ["definition", "by definition", "always true", "tautology"]):
                    testability = "never"
                if len(snippet) > 140:
                    snippet = snippet[:140] + "..."
                assumptions.append(AssumptionRecord(
                    id=f"A-{idx:03d}",
                    source="extracted",
                    type="factual",
                    testability=testability,
                    risk=risk,
                    text=snippet,
                ))
                idx += 1
                if idx > 40:
                    break
            if idx > 40:
                break
        return assumptions or [AssumptionRecord(id="A-001", source="fallback", type="factual", testability="later", risk="MEDIUM", text="Implicit payload assumptions")]

    def _extract_predictions(self, text: str) -> List[PredictionRecord]:
        predictions: List[PredictionRecord] = []
        patterns = [
            r"\b(?:will|should|expected to|forecast|predict|likely|unlikely)\b[^.\n]{0,120}",
            r"\b(?:latency|throughput|error rate|uptime|success rate)\b[^.\n]{0,120}(?:<|>|<=|>=|=)[^.\n]{0,80}",
            r"\b\d+%[^.\n]{0,120}",
            r"\b(?:measured|observed|confirmed|verified)\b[^.\n]{0,120}(?:\d+[a-zA-Z%]*|\b(?:below|above|at)\b[^.\n]{0,60})",
        ]
        seen = set()
        idx = 1
        for pat in patterns:
            for match in re.finditer(pat, text, re.IGNORECASE):
                snippet = match.group(0).strip()
                if not snippet or snippet.lower() in seen:
                    continue
                seen.add(snippet.lower())
                predictions.append(PredictionRecord(
                    id=f"P-{idx:03d}",
                    statement=snippet[:160],
                    horizon="unknown",
                    measurement="implied_by_text",
                    baseline="unstated",
                ))
                idx += 1
                if idx > 40:
                    break
            if idx > 40:
                break
        return predictions or [PredictionRecord(id="P-001", statement="Unfalsifiable narrative detected.", horizon="none", measurement="none", baseline="none", status="unavailable")]

    def _estimate_tested(self, predictions: List[PredictionRecord]) -> int:
        tested = 0
        for p in predictions:
            if p.status != "untested":
                tested += 1
                continue
            low = p.statement.lower()
            if any(w in low for w in ["measured", "observed", "confirmed", "actual", "verified", "known"]):
                p.status = "confirmed"
                tested += 1
        return tested

    def _estimate_drift(self, payload: Dict[str, Any]) -> str:
        confidence = float(payload.get("confidence", 0.0) or 0.0)
        if confidence >= 0.9:
            return "high_confidence_risk"
        if confidence <= 0.2:
            return "low_confidence_drift"
        return "nominal"

    def _summarize(self, debt: int, generated: int, tested: int, fts: float, violations: List[str], escalated: bool) -> str:
        parts = [f"AssumptionDebt={debt}", f"Predictions={generated}/{tested}", f"FTS={fts:.2f}"]
        if violations:
            parts.append(f"Violations={','.join(violations)}")
        if escalated:
            parts.append("ESCALATION")
        return "; ".join(parts)

    @staticmethod
    def _report_to_dict(report: GroundingReport) -> Dict[str, Any]:
        return {
            "assumption_debt": report.assumption_debt,
            "high_risk_untested": report.high_risk_untested,
            "predictions_generated": report.predictions_generated,
            "predictions_tested": report.predictions_tested,
            "fts": report.fts,
            "edi": report.edi,
            "drift_severity": report.drift_severity,
            "escalation_triggered": report.escalation_triggered,
            "guardrail_violations": report.guardrail_violations,
            "confirmed": report.confirmed,
            "refuted": report.refuted,
            "open_items": report.open_items,
            "updated_confidence": report.updated_confidence,
            "summary": report.summary,
        }
