from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from cognitive_compiler.harness_abc import BaseHarness, HarnessResult, HarnessTelemetry


@dataclass
class TeleportState:
    tctl: Optional[str] = None
    tsh: Optional[str] = None
    profile: Optional[str] = None
    ok: bool = False


class TeleportAccessHarness(BaseHarness):
    def __init__(self, bin_dir: Optional[str | Path] = None, profile: Optional[str] = None) -> None:
        self.state = TeleportState()
        self._detect(bin_dir, profile)

    def initialize(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self._detect(context.get("bin_dir"), context.get("profile"))
        return {
            "ok": self.state.ok,
            "tctl": self.state.tctl,
            "tsh": self.state.tsh,
            "profile": self.state.profile,
        }

    def evaluate(self, query: str, context: Dict[str, Any]) -> HarnessResult:
        if not self.state.ok:
            return HarnessResult(
                ok=False,
                event="blocked",
                error="Teleport CLI not found. Install tsh/tctl.",
                telemetry=HarnessTelemetry(error_class="prerequisite"),
            )
        q = (query or "").lower()
        if any(k in q for k in ["node", "server", "host", "endpoint"]):
            return self._run_tctl(["tsh", "ls", "--format=json"], context)
        if any(k in q for k in ["session", "ssh session", "play", "replay"]):
            return self._run_tctl(["tsh", "sessions", "--format=json"], context)
        if any(k in q for k in ["login", "identity", "whoami", "user"]):
            return self._run_tsh(["whoami"], context)
        return self._run_tctl(["tsh", "status"], context)

    def execute(self, query: str, *args: Any, context: Optional[Dict[str, Any]] = None, **kwargs: Any) -> HarnessResult:
        if context is None:
            context = {}
        result = self.evaluate(query, context)
        try:
            self.observe(result)
        except Exception:
            pass
        return result

    def observe(self, result: HarnessResult) -> Dict[str, Any]:
        return {
            "event": result.event,
            "ok": result.ok,
            "tags": result.telemetry.tags,
            "error_class": result.telemetry.error_class,
        }

    def repair(self, result: HarnessResult) -> Optional[HarnessResult]:
        if result.ok:
            return None
        if result.telemetry.error_class == "prerequisite":
            return None
        return HarnessResult(ok=False, event="repair:manual", error="login required", telemetry=HarnessTelemetry(tags=["teleport", "repair"]))

    def shutdown(self) -> Dict[str, Any]:
        return {"ok": True, "event": "shutdown"}

    def _build_search_dirs(self, bin_dir: Optional[str | Path], profile: Optional[str]) -> List[str]:
        dirs: List[str] = []
        if bin_dir:
            dirs.append(str(Path(bin_dir).expanduser().resolve()))
        dirs.extend(["/usr/local/bin", "/opt/homebrew/bin", os.path.expanduser("~/.local/bin"), os.environ.get("PATH", "")])
        return dirs

    def _locate_binary(self, dirs: List[str], name: str) -> Optional[str]:
        for d in dirs:
            if d and Path(d, name).exists():
                return str(Path(d, name))
        return shutil.which(name)

    def _apply_detected_state(self, tctl: Optional[str], tsh: Optional[str], profile: Optional[str]) -> None:
        self.state.tctl = tctl
        self.state.tsh = tsh
        self.state.profile = profile or os.environ.get("TELEPORT_PROFILE")
        self.state.ok = bool(self.state.tctl and self.state.tsh)

    def _detect(self, bin_dir: Optional[str | Path], profile: Optional[str]) -> None:
        dirs = self._build_search_dirs(bin_dir, profile)
        tctl = self._locate_binary(dirs, "tctl")
        tsh = self._locate_binary(dirs, "tsh")
        self._apply_detected_state(tctl, tsh, profile)

    def _invoke(self, cmd: List[str], context: Dict[str, Any], timeout: int = 10) -> Dict[str, Any]:
        env = os.environ.copy()
        if self.state.profile:
            env["TELEPORT_PROFILE"] = str(self.state.profile)
        proxy = context.get("teleport_proxy") or os.environ.get("TELEPORT_PROXY")
        if proxy:
            env["TELEPORT_PROXY"] = str(proxy)
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
            raw = p.stdout.strip()
            data: Any = raw
            if raw.startswith("{") or raw.startswith("["):
                try:
                    data = json.loads(raw)
                except Exception:
                    pass
            return {"ok": p.returncode == 0, "code": p.returncode, "stdout": raw, "data": data, "returncode": p.returncode, "command": " ".join(cmd)}
        except FileNotFoundError as e:
            return {"ok": False, "code": 127, "stdout": "", "data": None, "error": str(e), "command": " ".join(cmd)}
        except subprocess.TimeoutExpired:
            return {"ok": False, "code": 124, "stdout": "", "data": None, "error": "timeout", "command": " ".join(cmd)}

    def _run_tctl(self, args: List[str], context: Dict[str, Any]) -> HarnessResult:
        cmd = [self.state.tctl, *args]
        out = self._invoke(cmd, context)
        payload = {"command": cmd, "result": out}
        telemetry = HarnessTelemetry(routing_confidence=0.0, tags=["teleport", "tctl"])
        if out.get("ok"):
            return HarnessResult(ok=True, event="tctl-ok", payload=payload, telemetry=telemetry)
        return HarnessResult(ok=False, event="tctl-failed", error=out.get("error") or out.get("stdout"), payload=payload, telemetry=HarnessTelemetry(error_class="external"))

    def _run_tsh(self, args: List[str], context: Dict[str, Any]) -> HarnessResult:
        cmd = [self.state.tsh, *args]
        out = self._invoke(cmd, context)
        payload = {"command": cmd, "result": out}
        telemetry = HarnessTelemetry(routing_confidence=0.0, tags=["teleport", "tsh"])
        if out.get("ok"):
            return HarnessResult(ok=True, event="tsh-ok", payload=payload, telemetry=telemetry)
        return HarnessResult(ok=False, event="tsh-failed", error=out.get("error") or out.get("stdout"), payload=payload, telemetry=HarnessTelemetry(error_class="external"))
