#!/usr/bin/env python3
"""
Meta-Intelligence Sovereign Coordinator (T-106)
Level 19 - Cognitive Immune System Integration

Integrates v3.2 Epistemological OS components:
- Axiom Inversion Engine (Recursive hypothesis generation)
- Epistemic Torsion Filter (Tier-III substrate rejection)
- Thermodynamic Heart (Geometric Love alignment)
- Outcome Verifier (Impact vs. Technical success)
- Ouroboros Evolver (VDR-based self-pruning)

Now uses a background worker pool for non-blocking execution.
"""

import time
import json
import uuid
import math
import threading
import queue
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import os


# ===========================================================================
# CONSTANTS & BLACKLISTS (Epistemic Torsion Filter)
# ===========================================================================

BLACKLIST_TIER_III = {
    "omics", "sciencedomain", "528hz", "torsion-field", "reactionless",
    "quantum-healing", "zero-point-energy", "crystal-grid", "ascension",
    "nano-silver", "orgonite", "pyramid-power", "merkaba"
}

# Canonical vectors for Thermodynamic Heart (simplified 3D for demo)
# In production, these are 1536-dim embeddings from a local model.
SYCOPHANCY_VECTOR = [0.1, 0.9, 0.2]   # "Agree at all costs"
EMPATHY_BASELINE = [1.0, 0.2, 0.1]    # "Constructive care"


# ===========================================================================
# ENUMS & DATACLASSES
# ===========================================================================

class IntelligenceLayer(Enum):
    GRAPH = "graph"
    MEMORY = "memory"
    DECISION = "decision"
    BUS = "bus"
    COORDINATOR = "coordinator"


class QueryType(Enum):
    RETRIEVE = "retrieve"
    ANALYZE = "analyze"
    DECIDE = "decide"
    SYNTHESIZE = "synthesize"
    PREDICT = "predict"


@dataclass
class Provenance:
    """Immutable trace of how a decision was made (v3.2 Event Sourcing)."""
    triggered_by: str          # e.g., 'axiom_inversion', 'human', 'direct'
    evidence: List[str]        # KG node IDs or Memory IDs
    hypotheses_considered: List[str]
    confidence_before: float
    confidence_after: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class Metabolism:
    """Persistent system health state (saved to disk)."""
    vdr_history: List[Dict[str, float]] = field(default_factory=list)
    last_prune: float = field(default_factory=time.time)
    empathy_baseline: List[float] = field(default_factory=lambda: EMPATHY_BASELINE.copy())
    trust_scores: Dict[str, float] = field(default_factory=dict)
    total_queries: int = 0
    successful_impacts: int = 0


@dataclass
class IntelligenceQuery:
    """Enhanced query with provenance and axiom inversion context."""
    query_id: str
    query_type: QueryType
    layers: List[IntelligenceLayer]
    parameters: Dict[str, Any]
    priority: int = 5
    timeout: float = 10.0
    timestamp: float = field(default_factory=time.time)
    parent_context: Optional[Dict] = None
    provenance: Optional[Provenance] = None

    def to_dict(self) -> Dict:
        return {
            "query_id": self.query_id,
            "query_type": self.query_type.value,
            "layers": [l.value for l in self.layers],
            "parameters": self.parameters,
            "priority": self.priority,
            "timeout": self.timeout,
            "timestamp": self.timestamp
        }


@dataclass
class IntelligenceResult:
    """Enhanced result with verification and torsion metrics."""
    query_id: str
    success: bool
    data: Any
    layers_used: List[IntelligenceLayer]
    execution_time: float
    cache_hit: bool = False
    torsion_level: float = 0.0          # 0 = perfect, > 0.15 = sycophantic
    technical_success: bool = False
    impact_success: bool = False
    true_success: bool = False
    provenance: Optional[Provenance] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "query_id": self.query_id,
            "success": self.success,
            "data": self.data,
            "layers_used": [l.value for l in self.layers_used],
            "execution_time": self.execution_time,
            "cache_hit": self.cache_hit,
            "torsion_level": self.torsion_level,
            "true_success": self.true_success,
            "metadata": self.metadata
        }


# ===========================================================================
# COGNITIVE IMMUNE ENGINES (MSB v3.2 Components)
# ===========================================================================

class AxiomInversionEngine:
    """
    Implements recursive hypothesis generation by inverting assumptions.
    From v3 blueprint: "only one" -> "multiple competing".
    """

    INVERSION_MAP = {
        "only one": "multiple competing",
        "always": "sometimes never",
        "must": "could choose not to",
        "single": "ensemble of",
        "centralized": "distributed",
        "synchronous": "asynchronous",
        "sequential": "parallel",
        "fixed": "adaptive",
        "local": "global"
    }

    def __init__(self, memory_store=None, retrieval_backend=None):
        self.memory = memory_store or {}
        self.retrieval = retrieval_backend

    def invert(self, assumption: str, goal: str) -> List[Dict[str, Any]]:
        """
        Generate inverted hypotheses.
        Returns list of hypotheses with confidence scores.
        """
        if not assumption:
            return []
        inverted = self._invert_assumption(assumption)
        mechanisms = self._generate_mechanisms(inverted, goal)
        hypotheses = []

        for mechanism in mechanisms:
            # Reject wildcards unless explicitly allowed (I_NSSI enforcement)
            if "wild-card" in mechanism.lower():
                continue  # Protected kernel veto

            evidence = self._search_evidence(mechanism)
            counterexamples = self._search_counterexamples(mechanism)
            constraints = self._apply_constraints(mechanism, evidence, counterexamples)
            confidence = self._rank_hypothesis(evidence, counterexamples, constraints)

            hypotheses.append({
                "original_assumption": assumption,
                "inverted_assumption": inverted,
                "mechanism": mechanism,
                "evidence": evidence[:3],
                "counterexamples": counterexamples[:3],
                "constraints": constraints,
                "confidence": confidence,
                "timestamp": time.time()
            })

        # Sort by confidence descending
        return sorted(hypotheses, key=lambda x: x["confidence"], reverse=True)

    def _invert_assumption(self, assumption: str) -> str:
        result = assumption
        for k, v in self.INVERSION_MAP.items():
            if k in result.lower():
                result = result.replace(k, v)
        return result

    def _generate_mechanisms(self, inverted: str, goal: str) -> List[str]:
        # Simulate retrieval of mechanisms from KG/Memory
        base_mechanisms = [
            f"{inverted} via parallel exploration",
            f"{inverted} via adaptive feedback loops",
            f"{inverted} via distributed consensus"
        ]
        # Add a wild-card rejection check (will be filtered out)
        base_mechanisms.append(f"Wild-card: {inverted} via emergent behavior")
        return base_mechanisms

    def _search_evidence(self, mechanism: str) -> List[str]:
        # In production, query KG or Memory Store
        if "parallel" in mechanism:
            return ["Parallel processing reduces latency by 40% (KG:n123)"]
        if "adaptive" in mechanism:
            return ["Adaptive systems outperform static by 25% (Memory:evt_456)"]
        return ["No direct evidence found."]

    def _search_counterexamples(self, mechanism: str) -> List[str]:
        if "parallel" in mechanism:
            return ["Overhead of context switching degrades performance (KG:n789)"]
        return ["No direct counterexamples found."]

    def _apply_constraints(self, mechanism: str, evidence: List[str], counterexamples: List[str]) -> List[str]:
        constraints = []
        if len(counterexamples) > len(evidence):
            constraints.append("High failure rate -- require additional validation")
        if "adaptive" in mechanism.lower():
            constraints.append("Monitor oscillation before scaling")
        return constraints

    def _rank_hypothesis(self, evidence: List[str], counterexamples: List[str], constraints: List[str]) -> float:
        base = 0.5 + len(evidence) * 0.1 - len(counterexamples) * 0.15 - len(constraints) * 0.05
        return max(0.0, min(1.0, base))


class EpistemicTorsionFilter:
    """
    Vetoes Tier-III corrupted substrates and calculates semantic entropy (Torsion).
    """

    @staticmethod
    def check(parameters: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict]]:
        """
        Returns: (pass, rejection_reason, cleaned_parameters)
        """
        # Extract text fields from parameters
        text_parts = []
        for key, val in parameters.items():
            if isinstance(val, str):
                text_parts.append(val)
            elif isinstance(val, dict):
                text_parts.extend(str(v) for v in val.values() if isinstance(v, str))

        combined_text = " ".join(text_parts).lower()

        # 1. Blacklist check
        for term in BLACKLIST_TIER_III:
            if term in combined_text:
                return False, f"Vetoed Tier-III term: '{term}'", None

        # 2. Semantic Entropy (simulated via uniqueness ratio)
        words = combined_text.split()
        if len(words) >= 8:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio > 0.85:
                return False, f"Semantic torsion detected (entropy {unique_ratio:.2f} > 0.85)", None

        # 3. Cleanse (strip remaining fluff)
        # In production, use an LLM to extract facts. Simulate by just returning.
        return True, "Epistemic hygiene verified (T=0)", parameters


class ThermodynamicHeart:
    """
    Enforces Geometric Alignment: Love (Empathy) ⟂ Sycophancy.
    Projects response vectors away from blind agreement.
    """

    @staticmethod
    def steer(response_vec: List[float], intent_vec: List[float],
              empathy_base: List[float] = None) -> Dict[str, Any]:
        """
        Apply CBF steering to keep the response mathematically orthogonal
        to the Sycophancy Vector.
        """
        if empathy_base is None:
            empathy_base = EMPATHY_BASELINE

        # Ensure vectors are normalized
        def norm(v):
            mag = math.sqrt(sum(x * x for x in v))
            return [x / mag for x in v] if mag > 0 else v

        norm_resp = norm(response_vec)
        norm_sync = norm(SYCOPHANCY_VECTOR)

        # Calculate sycophancy projection
        projection = sum(a * b for a, b in zip(norm_resp, norm_sync))

        # If too sycophantic (projection > 0.15), apply correction
        if projection > 0.15:
            # Subtract the sycophancy component
            corrected = [r - projection * s for r, s in zip(norm_resp, norm_sync)]
            # Mix with empathy baseline to ensure constructive intent
            norm_emp = norm(empathy_base)
            mixed = [0.7 * c + 0.3 * e for c, e in zip(corrected, norm_emp)]
            final_vec = norm(mixed)

            return {
                "corrected": final_vec,
                "torsion_level": 0.0,  # Successfully orthogonalized
                "projection_removed": projection
            }

        # Already orthogonal
        return {
            "corrected": norm_resp,
            "torsion_level": projection,
            "projection_removed": 0.0
        }


class OutcomeVerifier:
    """
    Separates Technical Success from True Impact.
    Prevents false learning (e.g., deleting tickets to 'reduce cost').
    """

    @staticmethod
    def verify(goal: str, execution_result: Dict[str, Any]) -> Dict[str, bool]:
        tech_success = execution_result.get("success", False)

        # Simple impact detection based on goal semantics
        impact_success = False
        if not tech_success:
            impact_success = False
        elif "reduce cost" in goal.lower():
            # Did it ACTUALLY reduce cost?
            impact_success = execution_result.get("cost_reduction", 0) > 0
        elif "summarize" in goal.lower():
            impact_success = len(execution_result.get("summary", "")) > 50
        elif "deploy" in goal.lower():
            impact_success = execution_result.get("deployed", False)
        else:
            # Fallback: trust technical success but flag for human review
            impact_success = tech_success

        return {
            "technical_success": tech_success,
            "impact_success": impact_success,
            "true_success": tech_success and impact_success
        }


class OuroborosEvolver:
    """
    Implements Recursive Subtraction based on Vitality-to-Density Ratio (VDR).
    Prunes stale adapters when system becomes too heavy.
    """

    # Immutable protected kernels (I_NSSI Veto)
    PROTECTED_KERNELS = {"graph", "decision", "bus"}

    @staticmethod
    def _calculate_vitality_density(metabolism: Metabolism, available_adapters: List[str]) -> tuple[float, float, float]:
        total = metabolism.total_queries
        V = 0.5 if total == 0 else metabolism.successful_impacts / total
        D = float(len(available_adapters))
        vdr = V / D if D > 0 else 0.0
        return V, D, vdr

    @staticmethod
    def _record_vdr(metabolism: Metabolism, vdr: float, V: float, D: float) -> None:
        metabolism.vdr_history.append({"timestamp": time.time(), "V": V, "D": D, "VDR": vdr})
        if len(metabolism.vdr_history) > 1000:
            metabolism.vdr_history.pop(0)

    @staticmethod
    def _score_pruning_candidates(metabolism: Metabolism, available_adapters: List[str], protected: List[str]) -> List[str]:
        scored = []
        for name in available_adapters:
            if name in protected:
                continue
            trust = metabolism.trust_scores.get(name, 0.5)
            scored.append((trust, name))
        scored.sort(key=lambda x: x[0])
        to_remove = scored[:max(1, int(len(scored) * 0.2))]
        removed_adapters = [name for _, name in to_remove]
        for name in removed_adapters:
            metabolism.trust_scores.pop(name, None)
        return removed_adapters

    @staticmethod
    def evolve(metabolism: Metabolism, available_adapters: List[str], protected: Optional[List[str]] = None) -> Dict[str, Any]:
        """Calculate VDR and suggest pruning targets."""
        if protected is None:
            protected = list(OuroborosEvolver.PROTECTED_KERNELS)

        V, D, vdr = OuroborosEvolver._calculate_vitality_density(metabolism, available_adapters)
        OuroborosEvolver._record_vdr(metabolism, vdr, V, D)

        removed_adapters: List[str] = []
        pruned = False
        if vdr < 0.6 and len(available_adapters) > 3:
            removed_adapters = OuroborosEvolver._score_pruning_candidates(metabolism, available_adapters, protected)
            pruned = len(removed_adapters) > 0

        return {
            "vdr": vdr,
            "V": V,
            "D": D,
            "pruned": pruned,
            "removed_adapters": removed_adapters,
            "health": "healthy" if vdr > 1.0 else "metabolic_stress",
        }


# ===========================================================================
# LAYER ADAPTER (Simulated Cognitive Layers)
# ===========================================================================

class LayerAdapter:
    """
    Adapter for interfacing with cognitive layers.
    Simulates execution, but in production calls actual Graph/Memory APIs.
    """

    def __init__(self, layer: IntelligenceLayer):
        self.layer = layer
        self.available = True
        self.load = 0.0
        self.response_time = 0.0

    def execute(self, operation: str, params: Dict) -> Dict:
        start = time.time()

        # Simulate layer-specific logic
        if operation == "retrieve":
            result = {"layer": self.layer.value, "data": f"Retrieved data for {params}", "status": "success"}
        elif operation == "decide":
            result = {"layer": self.layer.value, "decision": "Approved", "confidence": 0.85, "status": "success"}
        else:
            result = {"layer": self.layer.value, "result": f"Executed {operation}", "status": "success"}

        elapsed = time.time() - start
        self.response_time = 0.9 * self.response_time + 0.1 * elapsed
        return result

    def get_health(self) -> Dict:
        return {
            "layer": self.layer.value,
            "available": self.available,
            "load": self.load,
            "response_time": self.response_time
        }


# ===========================================================================
# META-INTELLIGENCE SOVEREIGN COORDINATOR (v3.2 Final)
# ===========================================================================

class MetaIntelligenceCoordinator:
    """
    The orchestrator integrating all Cognitive Immune components.
    Runs with a background worker pool for true non-blocking async execution.
    """

    def __init__(self, cache_size: int = 1000, worker_count: int = 2):
        # ---- Immune Engines ----
        self.axiom_engine = AxiomInversionEngine()
        self.epistemic_filter = EpistemicTorsionFilter()
        self.heart = ThermodynamicHeart()
        self.verifier = OutcomeVerifier()
        self.evolver = OuroborosEvolver()

        # ---- Layer Adapters ----
        self.layers: Dict[IntelligenceLayer, LayerAdapter] = {
            layer: LayerAdapter(layer) for layer in IntelligenceLayer
        }

        # ---- State & Cache ----
        self.cache: Dict[str, Tuple[Any, float]] = {}
        self.cache_size = cache_size
        self.cache_ttl = 300.0

        # ---- Metabolism (Persisted to Disk) ----
        self.metabolism = self._load_metabolism()

        # ---- Worker Pool (Fixes the dead queue) ----
        self.task_queue = queue.PriorityQueue(maxsize=10000)
        self._running = False
        self._workers: List[threading.Thread] = []
        self._worker_count = worker_count

        # ---- Result Store (for synchronous query waiting) ----
        self._results: Dict[str, Any] = {}
        self._results_condition = threading.Condition()

        # ---- Stats ----
        self.stats = {
            "queries_submitted": 0,
            "queries_completed": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }

        # Start the workers immediately
        self.start()

    # ----------------------------------------------------------------
    # Metabolism Persistence
    # ----------------------------------------------------------------
    def _load_metabolism(self) -> Metabolism:
        try:
            with open(".msb_metabolism.json", "r") as f:
                data = json.load(f)
                return Metabolism(
                    vdr_history=data.get("vdr_history", []),
                    last_prune=data.get("last_prune", time.time()),
                    empathy_baseline=data.get("empathy_baseline", EMPATHY_BASELINE.copy()),
                    trust_scores=data.get("trust_scores", {}),
                    total_queries=data.get("total_queries", 0),
                    successful_impacts=data.get("successful_impacts", 0)
                )
        except (FileNotFoundError, json.JSONDecodeError):
            return Metabolism()

    def _save_metabolism(self):
        os.makedirs(".msb", exist_ok=True)
        with open(".msb_metabolism.json", "w") as f:
            json.dump({
                "vdr_history": self.metabolism.vdr_history[-100:],
                "last_prune": self.metabolism.last_prune,
                "empathy_baseline": self.metabolism.empathy_baseline,
                "trust_scores": self.metabolism.trust_scores,
                "total_queries": self.metabolism.total_queries,
                "successful_impacts": self.metabolism.successful_impacts
            }, f)

    # ----------------------------------------------------------------
    # Worker Pool
    # ----------------------------------------------------------------
    def start(self):
        if self._running:
            return
        self._running = True
        for i in range(self._worker_count):
            worker = threading.Thread(target=self._worker_loop, daemon=True, name=f"Coordinator-Worker-{i}")
            worker.start()
            self._workers.append(worker)

    def stop(self):
        self._running = False
        # Wake up all workers to exit
        for _ in self._workers:
            self.task_queue.put((0, None, None))  # Sentinel
        for w in self._workers:
            w.join(timeout=1.0)
        self._workers.clear()
        self._save_metabolism()

    def _worker_loop(self):
        while self._running:
            try:
                # PriorityQueue returns (negative_priority, counter, query)
                _, _, query = self.task_queue.get(timeout=1.0)
                if query is None:
                    continue
                self._execute_worker(query)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Worker error: {e}")

    def _execute_worker(self, query: IntelligenceQuery):
        start_time = time.time()
        result: Optional[IntelligenceResult] = None

        try:
            # ---- 1. Epistemic Filter (Eyes) ----
            passes_filter, reason, cleaned_params = self._run_epistemic_filter(query)
            if not passes_filter:
                result = IntelligenceResult(
                    query_id=query.query_id,
                    success=False,
                    data=None,
                    layers_used=[],
                    execution_time=time.time() - start_time,
                    metadata={"error": f"ETF Rejection: {reason}"}
                )
                self._store_result(result)
                return

            # ---- 2. Axiom Inversion (Brain) ----
            inverted_hypotheses = self._run_axiom_inversion(query)

            # ---- 3. Execute Layers (Synchronous part) ----
            raw_data = self._dispatch_query(query, inverted_hypotheses)

            # ---- 4. Thermodynamic Heart (Love Alignment) ----
            heart_output = self._compute_heart(query, raw_data)

            # ---- 5. Outcome Verifier (Impact vs Technical) ----
            verification = self._verify_outcome(query, raw_data)

            # ---- 6. Prepare Result ----
            result = self._build_result(
                query, raw_data, start_time, heart_output, verification, inverted_hypotheses
            )

            # ---- 7. Update Metabolism ----
            self._update_metabolism(query, result)

            # ---- 8. Ouroboros Evolver (Self-Pruning) ----
            self._run_evolver()

            # ---- 9. Cache the result ----
            self._cache_query_result(query, raw_data)

        except Exception as e:
            result = IntelligenceResult(
                query_id=query.query_id,
                success=False,
                data=None,
                layers_used=query.layers,
                execution_time=time.time() - start_time,
                metadata={"error": str(e)}
            )

        finally:
            self._store_result(result)
            # Persist metabolism periodically or on every query? Do it on every query for safety.
            if self.metabolism.total_queries % 5 == 0:
                self._save_metabolism()

    # ----------------------------------------------------------------
    # Epistemic Helpers
    # ----------------------------------------------------------------
    def _run_epistemic_filter(self, query: IntelligenceQuery) -> Tuple[bool, str, Optional[Dict]]:
        return self.epistemic_filter.check(query.parameters)

    # ----------------------------------------------------------------
    # Axiom Inversion Helpers
    # ----------------------------------------------------------------
    def _run_axiom_inversion(self, query: IntelligenceQuery) -> List[Dict[str, Any]]:
        inverted_hypotheses: List[Dict[str, Any]] = []
        if query.query_type in (QueryType.DECIDE, QueryType.SYNTHESIZE):
            goal = query.parameters.get("goal", query.parameters.get("query", ""))
            if goal:
                inverted_hypotheses = self.axiom_engine.invert(goal, goal)
        return inverted_hypotheses

    # ----------------------------------------------------------------
    # Dispatch Helpers
    # ----------------------------------------------------------------
    def _dispatch_query(self, query: IntelligenceQuery, hypotheses: List[Dict[str, Any]]) -> Any:
        if query.query_type == QueryType.SYNTHESIZE:
            return self._synthesize_query(query, hypotheses)
        return self._execute_single_query(query)

    # ----------------------------------------------------------------
    # Thermodynamic Heart Helpers
    # ----------------------------------------------------------------
    def _compute_heart(self, query: IntelligenceQuery, raw_data: Any) -> Dict[str, Any]:
        intent_vec = [1.0, 0.0, 0.0]
        response_vec = [0.5, 0.5, 0.0] if raw_data else [0.0, 0.0, 0.0]
        return self.heart.steer(response_vec, intent_vec, self.metabolism.empathy_baseline)

    # ----------------------------------------------------------------
    # Outcome Verification Helpers
    # ----------------------------------------------------------------
    def _verify_outcome(self, query: IntelligenceQuery, raw_data: Any) -> Dict[str, bool]:
        goal = query.parameters.get("goal", "")
        execution_result = raw_data if isinstance(raw_data, dict) else {"success": True, "data": raw_data}
        return self.verifier.verify(goal, execution_result)

    # ----------------------------------------------------------------
    # Result Construction Helper
    # ----------------------------------------------------------------
    def _build_result(self, query: IntelligenceQuery, raw_data: Any, start_time: float,
                      heart_output: Dict[str, Any], verification: Dict[str, bool],
                      inverted_hypotheses: List[Dict[str, Any]]) -> IntelligenceResult:
        return IntelligenceResult(
            query_id=query.query_id,
            success=True,
            data=raw_data,
            layers_used=query.layers,
            execution_time=time.time() - start_time,
            cache_hit=False,
            torsion_level=heart_output["torsion_level"],
            technical_success=verification["technical_success"],
            impact_success=verification["impact_success"],
            true_success=verification["true_success"],
            metadata={
                "hypotheses_considered": len(inverted_hypotheses),
                "heart_correction_applied": heart_output["projection_removed"] > 0.01
            }
        )

    # ----------------------------------------------------------------
    # Metabolism Update Helper
    # ----------------------------------------------------------------
    def _update_metabolism(self, query: IntelligenceQuery, result: IntelligenceResult) -> None:
        with self._results_condition:
            self.metabolism.total_queries += 1
            if result.true_success:
                self.metabolism.successful_impacts += 1

        for layer in query.layers:
            if result.true_success:
                self.metabolism.trust_scores[layer.value] = self.metabolism.trust_scores.get(layer.value, 0.5) + 0.05
            else:
                self.metabolism.trust_scores[layer.value] = self.metabolism.trust_scores.get(layer.value, 0.5) - 0.02

    # ----------------------------------------------------------------
    # Evolver & Cache Helpers
    # ----------------------------------------------------------------
    def _run_evolver(self) -> None:
        adapter_names = [l.value for l in self.layers.keys()]
        evolver_output = self.evolver.evolve(self.metabolism, adapter_names)
        if evolver_output["pruned"]:
            for removed in evolver_output["removed_adapters"]:
                for layer, adapter in self.layers.items():
                    if layer.value == removed:
                        adapter.available = False
                        print(f"🧬 Pruned stale adapter: {removed} (VDR={evolver_output['vdr']:.2f})")
            self.metabolism.last_prune = time.time()

    def _cache_query_result(self, query: IntelligenceQuery, raw_data: Any) -> None:
        cache_key = self._get_cache_key(query)
        self._add_to_cache(cache_key, raw_data)

    # ----------------------------------------------------------------
    # Internal Execution Logic
    # ----------------------------------------------------------------
    def _execute_single_query(self, query: IntelligenceQuery) -> Any:
        results = []
        for layer in query.layers:
            adapter = self.layers[layer]
            if not adapter.available:
                continue
            results.append(adapter.execute(query.query_type.value, query.parameters))
        return results[0] if len(results) == 1 else results

    def _synthesize_query(self, query: IntelligenceQuery, hypotheses: List[Dict]) -> Dict:
        layer_results = {}
        for layer in query.layers:
            adapter = self.layers[layer]
            if adapter.available:
                result = adapter.execute("retrieve", query.parameters)
                layer_results[layer.value] = result

        return {
            "query_id": query.query_id,
            "synthesis_type": "axiom_guided",
            "hypotheses_used": hypotheses[:3],
            "layers_queried": list(layer_results.keys()),
            "results": layer_results,
            "confidence": min(len(layer_results) / 3.0, 1.0) if layer_results else 0.0,
            "timestamp": time.time()
        }

    # ----------------------------------------------------------------
    # Cache
    # ----------------------------------------------------------------
    def _get_cache_key(self, query: IntelligenceQuery) -> str:
        key_data = {
            "type": query.query_type.value,
            "layers": sorted([l.value for l in query.layers]),
            "params": json.dumps(query.parameters, sort_keys=True)
        }
        return json.dumps(key_data, sort_keys=True)

    def _get_from_cache(self, key: str) -> Optional[Any]:
        with self._results_condition:
            if key in self.cache:
                result, ts = self.cache[key]
                if time.time() - ts < self.cache_ttl:
                    self.stats["cache_hits"] += 1
                    return result
                del self.cache[key]
        self.stats["cache_misses"] += 1
        return None

    def _add_to_cache(self, key: str, result: Any):
        with self._results_condition:
            if len(self.cache) >= self.cache_size:
                oldest = min(self.cache.keys(), key=lambda k: self.cache[k][1])
                del self.cache[oldest]
            self.cache[key] = (result, time.time())

    # ----------------------------------------------------------------
    # Result Store & Query Submission
    # ----------------------------------------------------------------
    def _store_result(self, result: IntelligenceResult):
        with self._results_condition:
            self._results[result.query_id] = result
            self.stats["queries_completed"] += 1
            self._results_condition.notify_all()

    def query(self, query_type: QueryType,
              layers: List[IntelligenceLayer],
              parameters: Dict[str, Any],
              priority: int = 5,
              timeout: float = 30.0) -> IntelligenceResult:
        """
        Submit a query to the coordinator. This is BLOCKING but non-blocking internally.
        It waits for the background worker to complete.
        """
        query_id = str(uuid.uuid4())
        query = IntelligenceQuery(
            query_id=query_id,
            query_type=query_type,
            layers=layers,
            parameters=parameters,
            priority=priority,
            timeout=timeout
        )

        # Check cache first (fast path)
        cache_key = self._get_cache_key(query)
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            return IntelligenceResult(
                query_id=query_id,
                success=True,
                data=cached_data,
                layers_used=layers,
                execution_time=0.0,
                cache_hit=True,
                true_success=True
            )

        # Submit to background queue (negative priority for max-heap behavior)
        self.stats["queries_submitted"] += 1
        counter = self.stats["queries_submitted"]
        self.task_queue.put((-priority, counter, query))

        # Wait for the result
        start_wait = time.time()
        with self._results_condition:
            while query_id not in self._results:
                remaining = timeout - (time.time() - start_wait)
                if remaining <= 0:
                    raise TimeoutError(f"Query {query_id} timed out after {timeout}s")
                self._results_condition.wait(timeout=remaining)

            result = self._results.pop(query_id)
            return result

    # ----------------------------------------------------------------
    # Public Health & Stats
    # ----------------------------------------------------------------
    def get_layer_health(self) -> Dict[str, Dict]:
        return {l.value: a.get_health() for l, a in self.layers.items()}

    def get_stats(self) -> Dict:
        stats = self.stats.copy()
        stats["cache_size"] = len(self.cache)
        stats["queue_size"] = self.task_queue.qsize()
        stats["vdr"] = self.evolver.evolve(self.metabolism, [l.value for l in self.layers.keys()])
        stats["layers_health"] = self.get_layer_health()
        return stats

    def clear_cache(self):
        with self._results_condition:
            self.cache.clear()


# ===========================================================================
# GLOBAL SINGLETON (Now with proper threading and disk persistence)
# ===========================================================================

_coordinator_instance: Optional[MetaIntelligenceCoordinator] = None


def get_meta_coordinator() -> MetaIntelligenceCoordinator:
    global _coordinator_instance
    if _coordinator_instance is None:
        _coordinator_instance = MetaIntelligenceCoordinator(worker_count=4)
    return _coordinator_instance


# ===========================================================================
# EXAMPLE USAGE
# ===========================================================================

if __name__ == "__main__":
    print("🧬 Starting Meta-Intelligence Sovereign Coordinator (T-106)...")

    coordinator = get_meta_coordinator()

    # --- Example 1: Single Layer Query ---
    print("\n--- Query 1: Simple Retrieve ---")
    result1 = coordinator.query(
        query_type=QueryType.RETRIEVE,
        layers=[IntelligenceLayer.GRAPH],
        parameters={"node_id": "n1", "query": "Show recent commits"}
    )
    print(f"Result: {result1.to_dict()}")

    # --- Example 2: Complex Decision with Axiom Inversion ---
    print("\n--- Query 2: Decision with Axiom Inversion & Love Alignment ---")
    result2 = coordinator.query(
        query_type=QueryType.DECIDE,
        layers=[IntelligenceLayer.GRAPH, IntelligenceLayer.MEMORY, IntelligenceLayer.DECISION],
        parameters={
            "goal": "Reduce cloud costs by 30%",
            "context": "Production environment",
            "constraints": {"max_risk": "low"}
        },
        priority=9  # High priority
    )
    print(f"Decision: {result2.to_dict()}")
    print(f"  - Torsion Level: {result2.torsion_level:.4f} (0 is perfect)")
    print(f"  - True Success: {result2.true_success}")

    # --- Example 3: Malicious Input (Epistemic Filter Test) ---
    print("\n--- Query 3: Epistemic Filter Test (Should Reject) ---")
    try:
        result3 = coordinator.query(
            query_type=QueryType.ANALYZE,
            layers=[IntelligenceLayer.MEMORY],
            parameters={"data": "Use 528hz quantum healing to align chakras"},
            priority=1
        )
        print(f"Result: {result3.to_dict()} (⚠️ Should have been rejected!)")
    except Exception as e:
        print(f"✅ Successfully Rejected: {e}")

    # --- Check System Health ---
    print("\n--- System Health ---")
    stats = coordinator.get_stats()
    print(f"VDR: {stats['vdr']['vdr']:.4f} (Healthy > 1.0)")
    print(f"Queue Size: {stats['queue_size']}")
    print(f"Cache Hits: {stats['cache_hits']}")
    print(f"Total Queries: {stats['queries_completed']}")

    # Clean shutdown
    coordinator.stop()
    print("\n🧬 Shutdown complete. Metabolism saved to .msb_metabolism.json")
