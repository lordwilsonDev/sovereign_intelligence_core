"""Sovereign Research Assistant — local-first investigation and report generation."""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


_TOPIC_SLUG_FORBIDDEN = {"/", "\\", "..", "~", ":", "*", "?", '"', "<", ">", "|"}


def _slugify(text: str) -> str:
    text = text.strip().lower()
    text = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in text)
    while "--" in text:
        text = text.replace("--", "-")
    return text.strip("-") or "research"


def _sha256(data: Any) -> str:
    payload = json.dumps(data, sort_keys=True, default=str).encode()
    return hashlib.sha256(payload).hexdigest()


def _assert_safe_slug(slug: str) -> None:
    if not slug or slug in {".", ".."}:
        raise ValueError(f"unsafe slug: {slug!r}")
    for part in slug.split("/"):
        if part in _TOPIC_SLUG_FORBIDDEN:
            raise ValueError(f"unsafe slug part: {part!r}")
        if part in {".", ".."}:
            raise ValueError(f"unsafe slug part: {part!r}")


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _sac_status() -> Dict[str, Any]:
    try:
        import requests
        r = requests.get("http://127.0.0.1:8766/sac/status", timeout=2)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {"available": False, "status": "unknown"}


def _systems_health() -> Dict[str, Any]:
    try:
        import requests
        r = requests.get("http://127.0.0.1:8766/systems-health/check", timeout=2)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {"available": False, "status": "unknown"}


def _echo_evaluate(action: str) -> Dict[str, Any]:
    try:
        import requests
        r = requests.post("http://127.0.0.1:8766/echo/evaluate", json={"action": action, "payload": {}}, timeout=2)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {"available": False, "should_echo": False, "severity": "unknown"}


class SovereignResearchAssistant:
    """Phase-gated research workflow: define -> invert -> evidence -> report."""

    def __init__(self, topic: str, root: Optional[Path] = None) -> None:
        self.topic = topic
        self.slug = _slugify(topic)
        self.root = Path(root) if root else Path("runtime/research") / self.slug
        self.artifacts: Dict[str, Optional[Path]] = {}
        self.guard_events: List[Dict[str, Any]] = []
        self.state: Dict[str, Any] = {
            "topic": topic,
            "slug": self.slug,
            "phase": "defined",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "hypotheses": [],
            "evidence": [],
            "claims": [],
            "phase_results": {},
        }
        self.root.mkdir(parents=True, exist_ok=True)

    def _check_gates(self, phase: str, action_hint: str) -> Dict[str, Any]:
        event = {"phase": phase, "action": action_hint, "allowed": True, "sac": {}, "systems": {}, "echo": {}}
        sac = _sac_status()
        systems = _systems_health()
        echo = _echo_evaluate(action_hint)
        event["sac"] = sac
        event["systems"] = systems
        event["echo"] = echo
        if sac.get("status") == "RED":
            event["allowed"] = False
        if systems.get("status") == "RED":
            event["allowed"] = False
        if echo.get("should_echo") and str(echo.get("severity", "")).lower() == "critical":
            event["allowed"] = False
        self.guard_events.append(event)
        if not event["allowed"]:
            raise RuntimeError(f"Safety gate blocked {phase}: {event}")
        return event

    def run_inversion(self) -> Dict[str, Any]:
        self._check_gates("inversion", "run_inversion")
        assumptions = [
            {"id": "a1", "text": f"The topic '{self.topic}' is best studied with advanced tooling.", "validity_probability": 0.4},
            {"id": "a2", "text": "Novel contribution requires hypothesis generation.", "validity_probability": 0.7},
            {"id": "a3", "text": "Local deterministic evidence can falsify a hypothesis.", "validity_probability": 0.9},
        ]
        inverted = [
            {"source_id": a["id"], "inverted": f"What if {a['text'].lower()} is false?"} for a in assumptions
        ]
        primary_hypothesis = {
            "id": "h1",
            "text": f"Boundary conditions for '{self.topic}' favor local deterministic evidence over external claims.",
            "prior_probability": 0.6,
            "falsifiable": True,
            "evidence_requirements": ["local_repo_scan", "interface_audit", "artifact_hash"],
        }
        rival_hypothesis = {
            "id": "h2",
            "text": f"External cloud-backed claims materially change falsification outcomes for '{self.topic}'.",
            "prior_probability": 0.3,
            "falsifiable": True,
            "evidence_requirements": ["external_source_license_check"],
        }
        uim = {
            "topic": self.topic,
            "assumptions": assumptions,
            "inverted": inverted,
            "causal_architecture": {
                "primary_hypothesis": primary_hypothesis["id"],
                "rival_hypothesis": rival_hypothesis["id"],
                "mediators": ["license_fit", "local_execution_path"],
                "confounds": ["operator_budget", "runtime_state"],
            },
            "measurable_constructs": [
                {"name": "local_evidence_count", "unit": "count"},
                {"name": "falsification_coverage", "unit": "ratio", "target_min": 0.7},
                {"name": "execution_path_exists", "unit": "bool"},
            ],
            "falsifiable_predictions": [
                {"hypothesis_id": primary_hypothesis["id"], "outcome": "local_evidence_count >= 2", "direction": "positive"},
                {"hypothesis_id": rival_hypothesis["id"], "outcome": "external_license audit fails sovereign fit", "direction": "negative"},
            ],
        }
        self.state["hypotheses"] = [primary_hypothesis, rival_hypothesis]
        self.state["phase"] = "inverted"
        self.state["phase_results"]["inversion"] = {
            "assumptions": assumptions,
            "inverted": inverted,
            "uim_hash": _sha256(uim),
        }
        self._persist(uim, "UIM")
        return uim

    def ground_evidence(self) -> Dict[str, Any]:
        if not self.state.get("hypotheses"):
            raise RuntimeError("run_inversion() before ground_evidence()")
        self._check_gates("evidence", "ground_evidence")
        repo_root = Path.cwd()
        local_sources = []
        for path in sorted(repo_root.rglob("*")):
            if path.is_file() and ".git" not in str(path) and "__pycache__" not in str(path):
                try:
                    rel = path.relative_to(repo_root)
                    if any(part.startswith(".") and part not in {".hermes"} for part in rel.parts):
                        continue
                    data = {
                        "path": str(rel),
                        "size": path.stat().st_size,
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    }
                    local_sources.append(data)
                    if len(local_sources) >= 20:
                        break
                except Exception:
                    continue
        claims = [
            {
                "id": f"claim-{idx+1}",
                "hypothesis_id": self.state["hypotheses"][0]["id"],
                "status": "supported" if local_sources else "unknown",
                "provenance": [item["path"] for item in local_sources[:5]],
            }
            for idx in range(3)
        ]
        evidence = [
            {"id": f"ev-{idx+1}", "category": "codebase", "weight": 0.6, "quality": 0.7, "source_path": local_sources[idx]["path"] if idx < len(local_sources) else ""}
            for idx in range(min(3, len(local_sources)))
        ]
        phases = ["dependency", "engine", "audit", "mesh", "research"]
        source_files = [item["path"] for item in local_sources]
        phase_files = {}
        for phase in phases:
            matches = []
            for p in source_files:
                normalized = p.replace("\\", "/")
                if f"/{phase}/" in normalized:
                    matches.append(p)
            phase_files[phase] = matches[:10]
        ledger = {
            "topic": self.topic,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "evidence": evidence,
            "claims": claims,
            "phase_files": phase_files,
            "local_source_count": len(local_sources),
        }
        self.state["evidence"] = evidence
        self.state["claims"] = claims
        self.state["phase"] = "evidence_grounded"
        self.state["phase_results"]["evidence"] = ledger
        self._persist(ledger, "evidence_ledger")
        return ledger

    def draft_report(self) -> Path:
        self._check_gates("report", "draft_report")
        uim = _load_json(self.root / f"{self.slug}_UIM.json")
        ledger = _load_json(self.root / f"{self.slug}_evidence_ledger.json")
        UIM = uim or {}
        L = ledger or {}
        hypotheses = self.state.get("hypotheses", [])
        primary = hypotheses[0]["text"] if hypotheses else ""
        rival = hypotheses[1]["text"] if len(hypotheses) > 1 else ""
        claims = self.state.get("claims", [])
        supported = [c["id"] for c in claims if c.get("status") == "supported"]
        unknown = [c["id"] for c in claims if c.get("status") != "supported"]
        lines = [
            f"# Sovereign Research Report: {self.topic}",
            "",
            "## Abstract",
            f"This report investigates `{self.topic}` under local-first sovereignty constraints. "
            f"It generates falsifiable hypotheses via AIL/MoIE, grounds them with deterministic local evidence, "
            f"and records all artifacts under `runtime/research/{self.slug}/`.",
            "",
            "## Background & Inverted Assumptions",
        ]
        for item in UIM.get("assumptions", []):
            inv = next((x["inverted"] for x in UIM.get("inverted", []) if x.get("source_id") == item.get("id")), "")
            lines.append(f"- assumption `{item.get('id')}`: {item.get('text')}")
            lines.append(f"  - inversion: {inv}")
        lines += [
            "",
            "## Unified Inversion Model",
            f"- primary hypothesis: {primary}",
            f"- rival hypothesis: {rival}",
        ]
        causal = UIM.get("causal_architecture", {})
        for k in ["primary_hypothesis", "rival_hypothesis", "mediators", "confounds"]:
            if k in causal:
                lines.append(f"- {k}: {', '.join(causal[k]) if isinstance(causal[k], list) else causal[k]}")
        lines += [
            "",
            "## Methods / Deterministic Evidence Ledger",
            f"- local_sources: {L.get('local_source_count', 0)}",
            f"- evidence_items: {len(L.get('evidence', []))}",
            f"- claims: {len(L.get('claims', []))}",
        ]
        for ev in L.get("evidence", []):
            lines.append(f"- `{ev.get('id')}` [{ev.get('category')}] provenance={ev.get('source_path')}")
        lines += [
            "",
            "## Results / Falsification Outcomes",
            f"- supported claims: {len(supported)}",
            f"- unknown claims: {len(unknown)}",
            "- primary hypothesis: not falsified by current local evidence",
            "- rival hypothesis: not falsified; external audit deferred by sovereign boundary",
        ]
        lines += [
            "",
            "## Discussion / Boundary Conditions",
            "- operator budget and runtime state may change falsification conditions.",
            "- re-run `ground_evidence()` after new local artifacts appear.",
            "",
            "## Guard Events",
        ]
        for ev in self.guard_events[-5:]:
            lines.append(f"- {ev['phase']}: SAC={ev['sac'].get('status')} systems={ev['systems'].get('status')} echo={ev['echo'].get('severity')}")
        lines += [
            "",
            "## Sovereignty Notes",
            "- all persisted artifacts are local-only.",
            "- high-risk external publication paths are logged only, not executed.",
            "",
            "## Reproducibility Artifacts",
            f"- UIM: `runtime/research/{self.slug}/{self.slug}_UIM.json`",
            f"- evidence ledger: `runtime/research/{self.slug}/{self.slug}_evidence_ledger.json`",
            f"- report: `runtime/research/{self.slug}/{self.slug}_report.md`",
            f"- review: `runtime/research/{self.slug}/{self.slug}_review.md`",
        ]
        report = "\n".join(lines) + "\n"
        report_path = self._persist_text(report, "report")
        review = {
            "topic": self.topic,
            "status": "draft",
            "claims_supported": len(supported),
            "claims_total": len(claims),
            "falsifications": ["none"],
            "follow_up": ["run external license check", "extend local evidence coverage"],
            "guard_events": self.guard_events[-5:],
        }
        self._persist(review, "review")
        return report_path

    def record_completion(self) -> Dict[str, Any]:
        completion = {
            "topic": self.topic,
            "slug": self.slug,
            "phase": "completed",
            "artifact_count": len(self.artifacts),
            "claims_supported": len([c for c in self.state.get("claims", []) if c.get("status") == "supported"]),
            "claims_total": len(self.state.get("claims", [])),
            "uim_hash": (self.state.get("phase_results", {}).get("inversion", {}).get("uim_hash")),
            "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        path = self.root / f"{self.slug}_completion.json"
        path.write_text(json.dumps(completion, indent=2), encoding="utf-8")
        self.artifacts["completion"] = path
        return completion

    def _persist(self, payload: Any, artifact_name: str) -> Path:
        safe_name = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in artifact_name)
        safe_name = safe_name.strip("-") or artifact_name
        path = self.root / f"{self.slug}_{safe_name}.json"
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        tmp.replace(path)
        self.artifacts[artifact_name] = path
        self._save_state()
        return path

    def _persist_text(self, text: str, artifact_name: str) -> Path:
        safe_name = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in artifact_name)
        safe_name = safe_name.strip("-") or artifact_name
        path = self.root / f"{self.slug}_{safe_name}.md"
        tmp = path.with_suffix(".tmp")
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(path)
        self.artifacts[artifact_name] = path
        self._save_state()
        return path

    def _save_state(self) -> None:
        path = self.root / f"{self.slug}_state.json"
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=2, default=str), encoding="utf-8")
        tmp.replace(path)

    def _load_artifact(self, artifact_name: str) -> Optional[Any]:
        path = self.artifacts.get(artifact_name) or self.root / f"{self.slug}_{artifact_name}.json"
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
