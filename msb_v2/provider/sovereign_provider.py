from __future__ import annotations

import hashlib
import os
import random
import shutil
import subprocess
import time
from typing import Any, Dict, List, Optional

from prometheus_client import Gauge  # type: ignore[import]

try:
    from cognitive_compiler.sovereign_autonomy_core import QuarantineInversionAgent
except Exception:  # pragma: no fallback
    QuarantineInversionAgent = None  # type: ignore[misc,assignment]

try:
    from cognitive_compiler.sac_self_audit import get_auditor
except Exception:  # pragma: no fallback
    get_auditor = None  # type: ignore[misc,assignment]


_provider_sovereignty_score = Gauge("msb_provider_sovereignty_score", "Composite provider sovereignty score")
_provider_vetoes_total = Gauge("msb_provider_vetoes_total", "Total provider veto events")
_provider_coherence_avg = Gauge("msb_provider_coherence_avg", "Average coherence score")
_provider_trust_status = Gauge("msb_provider_trust_status", "Provider trust status: 1 trusted, 0 untrusted")


class ProviderVetoException(Exception):
    pass


class SovereignProviderWrapper:
    def __init__(self, provider: Any, source_label: str = "neuralagent-ollama") -> None:
        self.provider = provider
        self.source_label = source_label
        self.provider_trusted = self._verify_ollama_binary()
        self._quarantine = QuarantineInversionAgent() if QuarantineInversionAgent else None
        self._veto_count = 0
        self._coherence_sum = 0.0
        self._coherence_samples = 0
        _provider_trust_status.set(1.0 if self.provider_trusted else 0.0)

    def chat(self, messages: List[Dict[str, str]], max_tokens: int = 256, **kwargs: Any) -> Dict[str, Any]:
        user_prompt = _last_user_content(messages)
        risk = self._classify_risk(user_prompt)
        if risk == "HIGH":
            self._veto_count += 1
            _provider_vetoes_total.set(float(self._veto_count))
            self._log_veto(user_prompt)
            raise ProviderVetoException("Prompt quarantined by QuarantineInversionAgent")

        response = self.provider.chat(messages, max_tokens=max_tokens, **kwargs)
        coherence = self._check_coherence(response)
        self._coherence_sum += float(coherence)
        self._coherence_samples += 1
        _provider_coherence_avg.set(self._coherence_sum / max(self._coherence_samples, 1))
        self._apply_jitter()
        self._update_score()
        return dict(response or {}, provider_metadata=self._metadata(risk, coherence))

    def _classify_risk(self, prompt: str) -> str:
        if self._quarantine is None:
            return "LOW"
        try:
            self._quarantine.apply(self.source_label, {"type": "veto-content", "payload": {"prompt": prompt}})
            return "LOW"
        except Exception:
            return "HIGH"

    def _check_coherence(self, response: Dict[str, Any]) -> float:
        text = (response or {}).get("content", "") or ""
        answer = "yes"
        try:
            coherence_prompt = (
                "Answer only with yes or no.\n"
                "Is the following response internally consistent and factually plausible?\n"
                f"{text}"
            )
            result = self.provider.chat([{"role": "user", "content": coherence_prompt}], max_tokens=16)
            answer = ((result or {}).get("content", "") or "").strip().lower()
        except Exception:
            answer = "no"
        return 1.0 if answer == "yes" else 0.0

    def _apply_jitter(self) -> None:
        try:
            time.sleep(random.uniform(0.005, 0.05))
        except Exception:
            pass

    def _update_score(self) -> None:
        try:
            veto_component = max(0.0, 1.0 - (self._veto_count / max(self._coherence_samples, 1)))
            coherence_component = self._coherence_sum / max(self._coherence_samples, 1)
            trust_component = 1.0 if self.provider_trusted else 0.0
            jitter_component = 1.0
            score = (trust_component * 0.4) + (veto_component * 0.3) + (coherence_component * 0.2) + (jitter_component * 0.1)
            _provider_sovereignty_score.set(float(score))
        except Exception:
            pass

    def _metadata(self, risk: str, coherence: float) -> Dict[str, Any]:
        return {
            "risk": risk,
            "coherence": coherence,
            "provider_trusted": self.provider_trusted,
        }

    def _log_veto(self, prompt: str) -> None:
        try:
            if get_auditor is None:
                return
            audit = get_auditor()
            audit.record_policy_falsification(
                policy="provider_veto",
                detected_rate=1.0,
                sample_count=1,
                blocked=True,
                checksum=hashlib.sha256((prompt or "").encode("utf-8")).hexdigest(),
            )
        except Exception:
            pass

    def _verify_ollama_binary(self) -> bool:
        path = shutil.which("ollama")
        if not path or not os.path.exists(path):
            return False
        try:
            digest = hashlib.sha256()
            with open(path, "rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            current = digest.hexdigest()
        except Exception:
            return False
        try:
            trusted = subprocess.check_output(
                ["security", "find-generic-password", "-a", "ollama", "-s", "sovereign-provider", "-w"],
                stderr=subprocess.DEVNULL,
            ).decode("utf-8", errors="ignore").strip()
            return trusted == current
        except subprocess.CalledProcessError:
            return False


def _last_user_content(messages: List[Dict[str, str]]) -> str:
    for item in reversed(messages):
        if item.get("role") == "user":
            return item.get("content", "") or ""
    return ""
