from __future__ import annotations

import os
import sys
import time
import subprocess
import threading
import secrets
from typing import Any, Dict, List, Optional


class DesktopHarness:
    """
    v1.1 desktop execution target with confirm/approve safety gate.

    Wraps NeuralAgent's desktop/aiagent/main.py loop as a BuildingHarness-style
    execution target with goal, plan, risks, live status, and confirmation state.
    """

    def __init__(
        self,
        repo_root: str = "/tmp/neuralagent",
        aiagent_dir: Optional[str] = None,
        backend_url: Optional[str] = None,
    ):
        self.repo_root = repo_root
        self.aiagent_dir = aiagent_dir or os.path.join(repo_root, "desktop", "aiagent")
        self.backend_url = backend_url or os.getenv("NEURALAGENT_API_URL", "http://127.0.0.1:8000")
        self.status: Dict[str, Any] = {
            "state": "idle",
            "pid": None,
            "thread_id": None,
            "user_token": None,
            "last_error": None,
        }
        self._lock = threading.Lock()
        self._pending: Dict[str, Dict[str, Any]] = {}
        self._runtime_results: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------
    # Step 1 – Goal interpretation
    # ------------------------------------------------------------------
    def requirement_extraction(self, goal: str) -> Dict[str, Any]:
        sentences = [s.strip() for s in goal.replace(".", "\n").split("\n") if s.strip()]
        requirements = []
        assumptions = []
        for idx, sentence in enumerate(sentences, 1):
            requirements.append(
                {
                    "id": f"DREQ-{idx:03d}",
                    "text": sentence,
                    "category": "desktop-action",
                    "assumptions": [
                        f"UI exposes actionable element for: {sentence}",
                        f"Target app is installed and reachable on this OS",
                        f"Permissions allow input automation",
                    ],
                }
            )
            assumptions.extend(requirements[-1]["assumptions"])
        return {"goal": goal, "requirements": requirements, "assumptions": assumptions}

    # ------------------------------------------------------------------
    # Step 2 – Risk heuristics
    # ------------------------------------------------------------------
    def risk_assessment(self, goal: str) -> Dict[str, Any]:
        text = goal.lower()
        high_risk_markers = [
            "launch", "open app", "open file", "delete", "remove", "move", "rename",
            "click on", "type into", "send message", "submit", "run script", "execute",
            "install", "sudo", "password", "login", "mailto:",
        ]
        med_risk_markers = ["screenshot", "find", "search", "read", "ui", "scroll", "browser"]

        high = [m for m in high_risk_markers if m in text]
        med = [m for m in med_risk_markers if m in text]

        if high:
            severity = "HIGH"
            category = "automation"
            desc = (
                "Goal includes high-risk desktop actions "
                f"`{', '.join(high)}`; requires explicit approval before execution"
            )
        elif med:
            severity = "MEDIUM"
            category = "observation"
            desc = (
                "Goal includes intermediate-risk actions "
                f"`{', '.join(med)}`; may mutate UI state"
            )
        else:
            severity = "LOW"
            category = "read-only"
            desc = "Goal appears read-only/low-risk; safe to execute without confirmation"

        return {"severity": severity, "category": category, "description": desc, "matched": high or med}

    # ------------------------------------------------------------------
    # Step 3 – Environment readiness
    # ------------------------------------------------------------------
    def environment_scan(self) -> Dict[str, Any]:
        python = sys.executable or "/opt/homebrew/Caskroom/miniforge/base/bin/python"
        main_py = os.path.join(self.aiagent_dir, "main.py")
        return {
            "python": python,
            "main_py": main_py,
            "exists": os.path.exists(main_py),
            "platform": sys.platform,
            "backend_url": self.backend_url,
        }

    def runtime_prerequisites(self) -> Dict[str, Any]:
        env = {
            "NEURALAGENT_API_URL": self.backend_url,
            "NEURALAGENT_USER_ACCESS_TOKEN": os.getenv("NEURALAGENT_USER_ACCESS_TOKEN", ""),
            "NEURALAGENT_THREAD_ID": os.getenv("NEURALAGENT_THREAD_ID", ""),
        }
        missing = [k for k, v in env.items() if not v]
        return {"env": env, "missing": missing, "ready": not missing}

    # ------------------------------------------------------------------
    # Step 4 – Plan + optional run
    # ------------------------------------------------------------------
    def plan(self, goal: str, timeout_s: float = 600.0) -> Dict[str, Any]:
        reqs = self.requirement_extraction(goal)
        env_scan = self.environment_scan()
        prereqs = self.runtime_prerequisites()
        risk = self.risk_assessment(goal)

        state = "pending_confirmation" if risk["severity"] == "HIGH" else "ready"
        if not env_scan["exists"] or prereqs["missing"]:
            state = "blocked"

        return {
            "goal": goal,
            "requirements": reqs["requirements"],
            "assumptions": reqs["assumptions"],
            "environment": env_scan,
            "prerequisites": prereqs,
            "risk": risk,
            "plan": {
                "command": [sys.executable or "python", "main.py"],
                "cwd": self.aiagent_dir,
                "timeout_s": timeout_s,
            },
            "risks": self._canned_risks(risk["severity"]),
            "status": self.status,
            "state": state,
        }

    def confirm_token(self, goal: str) -> str:
        token = secrets.token_urlsafe(16)
        self._pending[token] = {
            "goal": goal,
            "created_at": time.time(),
        }
        return token

    def approve_run(self, confirm_token: str, approved: bool = True, timeout_s: float = 600.0) -> Dict[str, Any]:
        pending = self._pending.pop(confirm_token, None)
        if not pending:
            return {"error": "Invalid or expired confirm_token", "state": "error"}
        if not approved:
            return {"error": "User rejected execution", "state": "rejected", "goal": pending["goal"]}

        goal = pending["goal"]
        return self._execute(goal, timeout_s=timeout_s)

    # Backward-compatible execute: plan-only for HIGH risk, run for low risk.
    def execute(self, goal: str, timeout_s: float = 600.0) -> Dict[str, Any]:
        plan = self.plan(goal, timeout_s=timeout_s)
        if plan["state"] == "blocked":
            return {
                "goal": goal,
                "requirements": plan["requirements"],
                "assumptions": plan["assumptions"],
                "environment": plan["environment"],
                "prerequisites": plan["prerequisites"],
                "risk": plan["risk"],
                "risks": plan["risks"],
                "state": "blocked",
                "started_at": time.time(),
                "elapsed_s": 0.0,
                "stdout": "",
                "stderr": "Missing binary/env; see prerequisites",
                **plan["plan"],
            }
        if plan["state"] == "pending_confirmation":
            token = self.confirm_token(goal)
            plan["confirm_token"] = token
            return plan
        return self._execute(goal, timeout_s=timeout_s)

    # Private actual execution
    def _execute(self, goal: str, timeout_s: float = 600.0) -> Dict[str, Any]:
        start = time.time()
        reqs = self.requirement_extraction(goal)
        env_scan = self.environment_scan()
        prereqs = self.runtime_prerequisites()
        risk = self.risk_assessment(goal)
        output: Dict[str, Any] = {
            "goal": goal,
            "requirements": reqs["requirements"],
            "assumptions": reqs["assumptions"],
            "environment": env_scan,
            "prerequisites": prereqs,
            "risk": risk,
            "plan": {
                "command": [sys.executable or "python", "main.py"],
                "cwd": self.aiagent_dir,
                "timeout_s": timeout_s,
            },
            "risks": self._canned_risks(risk["severity"]),
            "started_at": time.time(),
        }

        if not env_scan["exists"] or prereqs["missing"]:
            output.update({
                "state": "blocked",
                "elapsed_s": round(time.time() - start, 4),
                "stdout": "",
                "stderr": "Missing binary/env; see prerequisites",
            })
            return output

        with self._lock:
            self.status.update({"state": "running", "pid": None, "last_error": None})

        def _runner() -> None:
            try:
                env = os.environ.copy()
                env.update({
                    "NEURALAGENT_API_URL": self.backend_url,
                    "NEURALAGENT_USER_ACCESS_TOKEN": prereqs["env"]["NEURALAGENT_USER_ACCESS_TOKEN"],
                    "NEURALAGENT_THREAD_ID": prereqs["env"]["NEURALAGENT_THREAD_ID"],
                })
                proc = subprocess.Popen(
                    [sys.executable or "python", "main.py"],
                    cwd=self.aiagent_dir,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                with self._lock:
                    self.status["pid"] = proc.pid
                    self.status["state"] = "running"

                try:
                    out, err = proc.communicate(timeout=timeout_s)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    out, err = proc.communicate()
                    with self._lock:
                        self.status["state"] = "timeout"
                        self.status["last_error"] = "timeout"

                output.update({
                    "state": self.status["state"],
                    "stdout": out.decode("utf-8", errors="replace") if isinstance(out, bytes) else out,
                    "stderr": err.decode("utf-8", errors="replace") if isinstance(err, bytes) else err,
                })
            except Exception as e:
                output.update({"state": "error", "stderr": str(e)})
                with self._lock:
                    self.status["state"] = "error"
                    self.status["last_error"] = str(e)
            finally:
                output["elapsed_s"] = round(time.time() - start, 4)
                output["finished_at"] = time.time()
                with self._lock:
                    if self.status["state"] == "running":
                        self.status["state"] = "completed"

        t = threading.Thread(target=_runner, daemon=True)
        t.start()
        t.join(timeout=timeout_s + 5)
        return output

    # ------------------------------------------------------------------
    # Step 5 – Stop
    # ------------------------------------------------------------------
    def stop(self) -> Dict[str, Any]:
        with self._lock:
            pid = self.status.get("pid")
        if pid:
            try:
                os.kill(pid, 2)
                time.sleep(0.5)
            except ProcessLookupError:
                pass
        with self._lock:
            self.status.update({"state": "stopped", "pid": None})
        return {"stopped": True, "pid": pid}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _canned_risks(self, severity: str) -> List[Dict[str, Any]]:
        base = [
            {"id": "DR-3", "category": "vision", "description": "Screenshot interpretation can misread dynamic UI", "mitigation": "include previous action history + memory", "severity": "MEDIUM"},
            {"id": "DR-2", "category": "backend", "description": "Desktop agent depends on live NeuralAgent backend + DB", "mitigation": "start backend before execute()", "severity": "HIGH"},
            {"id": "DR-1", "category": "automation", "description": "PyAutoGUI fails if accessibility permissions are missing on macOS", "mitigation": "grant Accessibility access or run with sudo-prompt where needed", "severity": "HIGH"},
        ]
        if severity == "LOW":
            return [r for r in base if r["severity"] != "HIGH"]
        return base
