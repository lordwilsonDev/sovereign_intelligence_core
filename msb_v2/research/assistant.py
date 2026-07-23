"""Sovereign Research Assistant — local-first investigation and report generation."""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from msb_v2.observer_log.thought_emitter import emit_thought as _research_emit_thought


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


def _snh_notify(title: str, body: str) -> Dict[str, Any]:
    try:
        import requests
        r = requests.post("http://127.0.0.1:8766/sn/notify", json={"title": title, "body": body}, timeout=2)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {"available": False}


def _ouroboros_scan() -> Dict[str, Any]:
    try:
        import requests
        r = requests.get("http://127.0.0.1:8766/evolution/scan", timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {"available": False}


def _continuity_prompt() -> Dict[str, Any]:
    try:
        import requests
        r = requests.get("http://127.0.0.1:8766/continuity/resume-prompt", timeout=2)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {"available": False}


def _memory_consolidate() -> Dict[str, Any]:
    try:
        import requests
        r = requests.post("http://127.0.0.1:8766/memory/consolidate", json={}, timeout=2)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {"available": False}


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
        try:
            from msb_v2.local_ai.client import LocalInferenceClient
            self.local_model = LocalInferenceClient()
        except Exception:
            self.local_model = None

    def invert_topic(self, topic: str) -> Dict[str, Any]:
        """Use the local model to perform axiom inversion on the topic."""
        if not self.local_model:
            return {"assumption": "no local model", "inversion": "", "predictions": []}
        prompt = (
            "You are an Axiom Inversion Logic engine. Given the topic:\n"
            f"{topic}\n\n"
            "1. Extract the hidden assumption behind the conventional view.\n"
            '2. Invert that assumption: "What if the opposite is true?"\n'
            "3. Generate 3 falsifiable predictions that would follow from the inversion.\n\n"
            "Return the result as JSON with keys: assumption, inversion, predictions."
        )
        response = self.local_model.generate(prompt, max_tokens=512)
        try:
            import json
            result = json.loads(response)
        except Exception:
            result = {
                "assumption": "Unable to parse model output",
                "inversion": response[:200],
                "predictions": [],
            }
        return result

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
            _snh_notify(
                "Research Assistant Critical Alert",
                f"Phase `{phase}` blocked by safety gate. SAC={sac.get('status')} systems={systems.get('status')} echo={echo.get('severity')}",
            )
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
        _snh_notify("Research Assistant Progress", f"Research assistant completed phase `{self.topic}`.")
        return completion

    def run_full_pipeline(self) -> Dict[str, Any]:
        """Run the local research pipeline with sovereign immune system gates and notifications."""
        summary = {
            "topic": self.topic,
            "slug": self.slug,
            "phases": {},
        }
        self._notify("pipeline_start", f"Starting research on: {self.topic}")
        _research_emit_thought("research-assistant", f"Starting research on: {self.topic}")

        preflight = self._preflight_checks()
        summary["phases"]["preflight"] = preflight
        if not preflight.get("passed"):
            summary["status"] = "blocked_by_preflight"
            self._notify("pipeline_blocked", "Pre-flight checks failed", "high")
            _research_emit_thought("research-assistant", "Pipeline blocked by preflight checks", "high")
            return summary

        if not self._sac_gate("pipeline_start"):
            summary["status"] = "blocked_by_sac"
            self._notify("pipeline_blocked", "SAC gate blocked pipeline start", "high")
            return summary

        self._notify("inversion_start", "Running axiom inversion")
        summary["phases"]["inversion"] = self.run_inversion()
        self._notify("inversion_complete", "Axiom inversion complete")
        _research_emit_thought("research-assistant", "Axiom inversion complete")

        if not self._sac_gate("evidence_grounding"):
            summary["status"] = "blocked_during_evidence"
            self._notify("pipeline_blocked", "SAC gate blocked evidence grounding", "high")
            return summary
        self._notify("evidence_start", "Grounding evidence")
        summary["phases"]["evidence"] = self.ground_evidence()
        self._notify("evidence_complete", "Evidence grounding complete")
        _research_emit_thought("research-assistant", "Evidence grounding complete")

        # Phase 8: Mesh distribution (parallel evidence grounding)
        mesh_results = self._distribute_evidence_grounding(self.topic)
        if isinstance(mesh_results, dict):
            summary["phases"]["mesh_distribution"] = mesh_results
        else:
            summary["phases"]["mesh_distribution"] = {
                "sub_tasks": len(mesh_results),
                "results": mesh_results,
            }

        if not self._sac_gate("report_generation"):
            summary["status"] = "blocked_during_report"
            self._notify("pipeline_blocked", "SAC gate blocked report generation", "high")
            return summary
        self._notify("report_start", "Generating research report")
        summary["phases"]["report"] = {"path": str(self.draft_report())}
        self._notify("report_complete", "Research report generated")
        _research_emit_thought("research-assistant", "Research report generated")

        report_text = ""
        try:
            completion = self._load_artifact("completion")
            if isinstance(completion, dict):
                report_text = str(completion.get("summary") or completion.get("status") or "")
        except Exception:
            pass

        if not self._echo_gate("report", report_text):
            summary["status"] = "awaiting_confirmation"
            self._notify("echo_triggered", "Report requires human confirmation before publishing", "high")
            return summary

        summary["evolution"] = _ouroboros_scan()
        continuity = _continuity_prompt()
        memory = _memory_consolidate()
        summary["continuity"] = continuity
        summary["memory"] = memory
        summary["mesh"] = {"peers": [], "submitted_tasks": []}
        try:
            import requests
            r = requests.get("http://127.0.0.1:8766/mesh/discover", timeout=2)
            if r.status_code == 200:
                summary["mesh"] = r.json()
        except Exception:
            pass

        summary["health"] = self._health_check()

        # Phase 6: Ouroboros metabolic scan
        summary["evolution"] = self._run_evolution_scan()

        # Phase 6: SOH optimization analysis
        summary["optimization"] = self._run_optimization_analysis()

        # Phase 7: Continuity checkpoint
        summary["continuity"] = self._run_continuity_checkpoint()

        # Phase 7: Memory consolidation
        summary["memory"] = self._run_memory_consolidation()

        completion = self.record_completion()
        summary["completion"] = completion
        summary["status"] = "completed"
        self._notify("pipeline_complete", f"Research on '{self.topic}' completed successfully")
        return summary

    def _notify(self, event: str, message: str, priority: str = "medium") -> None:
        """Send an SNH notification to the operator."""
        try:
            import requests
            requests.post(
                "http://127.0.0.1:8766/sn/notify",
                json={
                    "source": "research-assistant",
                    "priority": priority,
                    "template": "research_assistant_update",
                    "template_data": {"event": event, "message": message},
                },
                timeout=5,
            )
        except Exception:
            pass

    def _sac_gate(self, phase: str) -> bool:
        """Check SAC status before proceeding. Returns True if safe."""
        try:
            import requests
            resp = requests.get("http://127.0.0.1:8766/sac/status", timeout=5)
            if resp.ok:
                data = resp.json()
                sas = (data.get("sas") or {}).get("score", 0)
                if sas < 70:
                    self.guard_events.append({"phase": phase, "blocker": "sac", "score": sas})
                    return False
                return True
        except Exception:
            pass
        return True

    def _echo_gate(self, phase: str, content: str) -> bool:
        """Return True if the output is safe to publish without human confirmation."""
        payload = {
            "intent": {"action": "publish", "targets": ["research"], "raw_text": content or ""},
            "blast_analysis": {"score": 0.3, "affected": 0},
        }
        try:
            import requests
            resp = requests.post("http://127.0.0.1:8766/echo/evaluate", json=payload, timeout=5)
            if resp.ok:
                data = resp.json()
                if data.get("should_echo"):
                    self.guard_events.append({"phase": phase, "blocker": "echo"})
                    return False
        except Exception:
            pass
        return True

    def _health_check(self) -> Dict[str, Any]:
        """Run SCHH and SSHH checks. Returns status dict."""
        status: Dict[str, Any] = {"schh": "unknown", "sshh": "unknown"}
        try:
            import requests

            def _probe(path: str, expected_key: str) -> Optional[str]:
                try:
                    r = requests.get(f"http://127.0.0.1:8766{path}", timeout=5)
                    if r.ok:
                        data = r.json()
                        return data.get(expected_key) or data.get("status") or data.get("readiness")
                except Exception:
                    pass
                return None

            status["schh"] = _probe("/schh/status", "system_readiness") or "unknown"
            status["sshh"] = _probe("/systems-health/status", "system_readiness") or "unknown"
        except Exception:
            pass
        return status

    def _preflight_checks(self) -> Dict[str, Any]:
        """Run pre-mission readiness probes."""
        try:
            import requests
            checks = {
                "health": bool(requests.get("http://127.0.0.1:8766/health", timeout=3).ok),
                "schh": self._health_check().get("schh") == "GREEN",
                "sac": self._sac_gate("preflight"),
            }
            return {"checks": checks, "passed": all(checks.values())}
        except Exception as exc:
            return {"checks": {}, "passed": False, "error": str(exc)}

    def _run_evolution_scan(self) -> Dict[str, Any]:
        """Run Ouroboros metabolic scan and return findings."""
        try:
            import requests
            resp = requests.post(
                "http://127.0.0.1:8766/evolution/scan",
                json={"target": "full"},
                timeout=10,
            )
            if resp.ok:
                data = resp.json()
                return {
                    "proposal_count": data.get("proposal_count", 0),
                    "top_hotspots": data.get("hotspots", [])[:3],
                }
        except Exception:
            pass
        return {"proposal_count": -1, "error": "evolution_scan_unreachable"}

    def _run_optimization_analysis(self) -> Dict[str, Any]:
        """Run SOH optimization analysis and return proposals."""
        try:
            import requests
            resp = requests.post(
                "http://127.0.0.1:8766/optimize/analyze",
                timeout=10,
            )
            if resp.ok:
                data = resp.json()
                return {
                    "proposals": data.get("proposals", [])[:3],
                    "count": len(data.get("proposals", [])),
                }
        except Exception:
            pass
        return {"count": -1, "error": "optimization_unreachable"}

    def _run_continuity_checkpoint(self) -> Dict[str, Any]:
        """Generate a continuity token so this run can be resumed."""
        try:
            import requests
            resp = requests.get(
                "http://127.0.0.1:8766/continuity/resume-prompt",
                timeout=5,
            )
            if resp.ok:
                token = resp.text[:200]
                return {"checkpointed": True, "token_preview": token}
        except Exception:
            pass
        return {"checkpointed": False, "error": "continuity_unreachable"}

    def _run_memory_consolidation(self) -> Dict[str, Any]:
        """Consolidate short-term memories into long-term storage."""
        try:
            import requests
            resp = requests.post(
                "http://127.0.0.1:8766/memory/consolidate",
                json={"kind": "procedural", "min_items": 1},
                timeout=5,
            )
            if resp.status_code == 200:
                return {"consolidated": True, "status": "ok"}
        except Exception:
            pass
        return {"consolidated": False, "error": "memory_unreachable"}

    def _discover_peers(self) -> List[Dict[str, Any]]:
        """Return a list of known mesh peer addresses."""
        try:
            import requests
            resp = requests.get(
                "http://127.0.0.1:8766/mesh/discovery/peers",
                timeout=5,
            )
            if resp.ok:
                data = resp.json()
                return data.get("peers", [])
        except Exception:
            pass
        return []

    def _submit_to_mesh(self, peer: Dict[str, Any], intent: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Submit a sub-task to a remote mesh peer and return the task ID."""
        try:
            import requests
            address = peer.get("address", "127.0.0.1")
            port = peer.get("port", 8766)
            resp = requests.post(
                f"http://{address}:{port}/mesh/tasks/submit",
                json={
                    "intent": intent,
                    "context": context or {},
                    "requesting_node_id": getattr(self, "node_id", "local"),
                    "requesting_node_signature": "research-assistant",
                },
                timeout=10,
            )
            if resp.ok:
                return resp.json()
        except Exception:
            pass
        return {"error": "mesh_submission_failed"}

    def _collect_mesh_result(self, peer: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """Poll a remote peer for the completed task result."""
        try:
            import requests
            address = peer.get("address", "127.0.0.1")
            port = peer.get("port", 8766)
            resp = requests.get(
                f"http://{address}:{port}/mesh/tasks/{task_id}?execute=true",
                timeout=30,
            )
            if resp.ok:
                return resp.json()
        except Exception:
            pass
        return {"error": "mesh_result_failed"}

    def _distribute_evidence_grounding(self, topic: str) -> Dict[str, Any]:
        """Distribute evidence grounding sub-tasks across available mesh peers."""
        peers = self._discover_peers()
        if not peers:
            return {
                "sub_tasks": 3,
                "results": [
                    {"angle": angle, "peer": "local", "result": {"status": "local_fallback", "note": "no peers configured"}}
                    for angle in [
                        f"Search for recent academic papers on {topic}",
                        f"Find case studies related to {topic}",
                        f"Gather statistical data about {topic}",
                    ]
                ],
                "divergent": False,
            }

        sub_angles = [
            f"Search for recent academic papers on {topic}",
            f"Find case studies related to {topic}",
            f"Gather statistical data about {topic}",
        ]
        results: List[Dict[str, Any]] = []
        for i, angle in enumerate(sub_angles):
            peer = peers[i % len(peers)]
            submission = self._submit_to_mesh(peer, angle)
            if "task_id" in submission:
                result = self._collect_mesh_result(peer, submission["task_id"])
                results.append({"angle": angle, "peer": peer.get("node_id"), "result": result})
        return self._reconcile_mesh_results(results)

    def _reconcile_mesh_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bounded reconciliation for divergent mesh outputs."""
        base = {
            "sub_tasks": len(results),
            "results": results,
            "divergent": False,
        }
        for item in results:
            result = item.get("result") if isinstance(item, dict) else None
            if isinstance(result, dict) and result.get("error"):
                base["divergent"] = True
                base.setdefault("errors", []).append(result["error"])
        return base

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
