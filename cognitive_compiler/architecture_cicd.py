from __future__ import annotations

import copy
import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


class ArchitectureVersion:
    def __init__(self, version_id: str, prompt_templates: Dict[str, str], metadata: Dict[str, Any]):
        self.id = version_id
        self.prompt_templates = prompt_templates
        self.metadata = metadata
        self.deployed_at = datetime.utcnow()


class ArchitectureCICD:
    def __init__(self, baseline_prompts: Dict[str,str]) -> None:
        self.versions: Dict[str, ArchitectureVersion] = {}
        self.active_version_id: Optional[str] = None
        self.canary_version_id: Optional[str] = None
        self.canary_traffic: float = 0.0
        self.test_results: Dict[str, list] = defaultdict(list)
        self._commit_baseline(baseline_prompts)

    def _generate_version_id(self, prompts: Dict[str, str]) -> str:
        content = json.dumps(prompts, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:12]

    def _commit_baseline(self, prompts: Dict[str, str]) -> None:
        vid = self._generate_version_id(prompts)
        self.versions[vid] = ArchitectureVersion(vid, copy.deepcopy(prompts), {"type": "baseline"})
        self.active_version_id = vid

    def propose_candidate(self, new_prompts: Dict[str, str], change_description: str) -> str:
        vid = self._generate_version_id(new_prompts)
        self.versions[vid] = ArchitectureVersion(vid, copy.deepcopy(new_prompts), {"description": change_description, "type": "candidate"})
        return vid

    def start_canary(self, candidate_version_id: str, traffic_percent: float = 0.1) -> None:
        if candidate_version_id not in self.versions:
            raise ValueError("Candidate version not found")
        self.canary_version_id = candidate_version_id
        self.canary_traffic = float(traffic_percent)

    def resolve_canary(self, decision: str) -> None:
        if decision == "promote" and self.canary_version_id:
            self.active_version_id = self.canary_version_id
        self.canary_version_id = None
        self.canary_traffic = 0.0

    def get_active_prompts(self) -> Dict[str, str]:
        if not self.active_version_id or self.active_version_id not in self.versions:
            return {}
        return copy.deepcopy(self.versions[self.active_version_id].prompt_templates)

    def record_test_result(self, version_id: str, benchmark_name: str, score: float) -> None:
        self.test_results[version_id].append({"benchmark": benchmark_name, "score": float(score), "timestamp": datetime.utcnow().isoformat()})

    def should_rollback(self, degradation_threshold: float = 0.1) -> bool:
        if not self.canary_version_id:
            return False
        active_scores = [r["score"] for r in self.test_results.get(self.active_version_id, [])]
        canary_scores = [r["score"] for r in self.test_results.get(self.canary_version_id, [])]
        if not active_scores or not canary_scores:
            return False
        active_avg = sum(active_scores) / len(active_scores)
        canary_avg = sum(canary_scores) / len(canary_scores)
        return active_avg - canary_avg > degradation_threshold
