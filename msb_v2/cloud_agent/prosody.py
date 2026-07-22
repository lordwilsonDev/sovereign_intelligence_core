from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class CognitiveState:
    fatigue: float = 0.0
    frustration: float = 0.0
    urgency: float = 0.0
    features: Dict[str, Any] = field(default_factory=dict)

    def summary(self) -> str:
        return f"FATIGUE {self.fatigue:.2f}, FRUSTRATION {self.frustration:.2f}, URGENCY {self.urgency:.2f}"


_DEFAULT_BASELINE_PATH = Path("/Users/lordwilson/msb-v2/msb_v2/cloud_agent/voiceprint_baseline.json")


def _default_baseline() -> Dict[str, Any]:
    return {
        "fatigue_baseline": 0.2,
        "frustration_baseline": 0.1,
        "urgency_baseline": 0.1,
        "speech_rate": 1.0,
        "pitch_variance": 1.0,
        "pause_frequency": 0.1,
    }


class VoiceprintStore:
    def __init__(self, path: Optional[Path] = None) -> None:
        self._path = path or _DEFAULT_BASELINE_PATH
        self._baseline = self._load()

    def _load(self) -> Dict[str, Any]:
        if self._path.exists():
            try:
                return json.loads(self._path.read_text())
            except Exception:
                return _default_baseline()
        return _default_baseline()

    def persist(self) -> None:
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(json.dumps(self._baseline, indent=2))
        except Exception:
            pass

    def reset(self) -> Dict[str, Any]:
        self._baseline = _default_baseline()
        self.persist()
        return self._baseline

    def update(self, samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not samples:
            return self._baseline
        for key in ["fatigue_baseline", "frustration_baseline", "urgency_baseline", "speech_rate", "pitch_variance", "pause_frequency"]:
            vals = [float(s.get(key, 0.0)) for s in samples if key in s]
            if vals:
                self._baseline[key] = sum(vals) / len(vals)
        self.persist()
        return self._baseline

    def baseline(self) -> Dict[str, Any]:
        return dict(self._baseline)


class ProsodyAnalyzer:
    def __init__(self, store: Optional[VoiceprintStore] = None) -> None:
        self._store = store or VoiceprintStore()

    def analyze(self, voice_features: Optional[Dict[str, Any]] = None) -> CognitiveState:
        baseline = self._store.baseline()
        features = voice_features or {}

        fatigue = float(features.get("fatigue", baseline.get("fatigue_baseline", 0.2)))
        frustration = float(features.get("frustration", baseline.get("frustration_baseline", 0.1)))
        urgency = float(features.get("urgency", baseline.get("urgency_baseline", 0.1)))

        return CognitiveState(
            fatigue=max(0.0, min(1.0, fatigue)),
            frustration=max(0.0, min(1.0, frustration)),
            urgency=max(0.0, min(1.0, urgency)),
            features=dict(features),
        )

    @staticmethod
    def extract_features_from_pcm(pcm_bytes: bytes) -> Dict[str, Any]:
        length = len(pcm_bytes or b"")
        return {
            "pcm_length": length,
            "speech_rate": 1.0,
            "pitch_variance": 1.0,
            "pause_frequency": 0.1,
            "fatigue": 0.2,
            "frustration": 0.1,
            "urgency": 0.1,
        }
