import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cognitive_compiler.harness_dispatcher_v1 import HarnessDispatcher


def test_dispatch_routes_sovereign_finetune_scan():
    dispatcher = HarnessDispatcher.__new__(HarnessDispatcher)
    decision = type("D", (), {
        "primary": "sovereign-finetune",
        "secondary": None,
        "order": "single",
        "confidence": 0.95,
        "justification": "test",
    })()
    temperature = type("T", (), {
        "score": 0.1,
        "logic_loop_failures": 0,
        "uncertainty_spike": 0.0,
    })()
    meta = type("M", (), {
        "execute": lambda self, query, context: type("R", (), {
            "decision": self.decision,
            "rerouted": False,
            "elapsed_s": 0.01,
            "temperature": self.temperature,
        })(),
        "decision": decision,
        "temperature": temperature,
    })()
    dispatcher.meta = meta
    dispatcher.research = None
    dispatcher.building = None
    dispatcher.finetune = type("F", (), {
        "scan_documents": lambda self: {
            "source_hash": "abc",
            "documents": [],
            "total_tokens": 1,
            "recommendation": "proceed",
            "assumption_risks": [],
            "failure_patterns": [],
        },
        "jobs": {},
        "reports": {},
    })()
    dispatcher.verifier = type("V", (), {
        "verify": lambda self, result, context: type("V2", (), {"ok": True, "issues": [], "risk": 0.0})(),
    })()
    dispatcher.coordinator = type("C", (), {
        "query": lambda self, **kwargs: type("Q", (), {"to_dict": lambda self: {}})(),
    })()
    result = dispatcher.dispatch("sovereign fine-tune scan", context={"preferred_harness": "sovereign-finetune"})
    assert result["routing"]["primary"] == "sovereign-finetune"
    assert isinstance(result["primary_output"], dict)
    assert result["primary_output"]["source_hash"] == "abc"


def test_dispatch_routes_sovereign_finetune_distill():
    dispatcher = HarnessDispatcher.__new__(HarnessDispatcher)
    decision = type("D", (), {
        "primary": "sovereign-finetune",
        "secondary": None,
        "order": "single",
        "confidence": 0.95,
        "justification": "test",
    })()
    temperature = type("T", (), {
        "score": 0.1,
        "logic_loop_failures": 0,
        "uncertainty_spike": 0.0,
    })()
    meta = type("M", (), {
        "execute": lambda self, query, context: type("R", (), {
            "decision": self.decision,
            "rerouted": False,
            "elapsed_s": 0.01,
            "temperature": self.temperature,
        })(),
        "decision": decision,
        "temperature": temperature,
    })()
    dispatcher.meta = meta
    dispatcher.research = None
    dispatcher.building = None
    dispatcher.finetune = type("F", (), {
        "synthesize_pairs": lambda self, max_pairs=64: [
            {"instruction": "i", "output": "o", "chunk_index": 0, "source_path": "", "grounded": True}
        ],
        "validate_pairs": lambda self: {"failure_rate": 0.0, "inspected_count": 1, "passed": 1, "failures": 0, "action": "proceed"},
        "privacy_boundary": "local-only",
        "repo_path": "/tmp",
    })()
    dispatcher.verifier = type("V", (), {
        "verify": lambda self, result, context: type("V2", (), {"ok": True, "issues": [], "risk": 0.0})(),
    })()
    dispatcher.coordinator = type("C", (), {
        "query": lambda self, **kwargs: type("Q", (), {"to_dict": lambda self: {}})(),
    })()
    result = dispatcher.dispatch("distill dataset", context={"preferred_harness": "sovereign-finetune", "finetune_action": "distill", "max_pairs": 1})
    assert result["routing"]["primary"] == "sovereign-finetune"
    assert result["primary_output"]["action"] == "distill"
    assert result["primary_output"]["pairs"] == 1


def test_dispatch_routes_sovereign_finetune_train():
    dispatcher = HarnessDispatcher.__new__(HarnessDispatcher)
    decision = type("D", (), {
        "primary": "sovereign-finetune",
        "secondary": None,
        "order": "single",
        "confidence": 0.95,
        "justification": "test",
    })()
    temperature = type("T", (), {
        "score": 0.1,
        "logic_loop_failures": 0,
        "uncertainty_spike": 0.0,
    })()
    meta = type("M", (), {
        "execute": lambda self, query, context: type("R", (), {
            "decision": self.decision,
            "rerouted": False,
            "elapsed_s": 0.01,
            "temperature": self.temperature,
        })(),
        "decision": decision,
        "temperature": temperature,
    })()
    dispatcher.meta = meta
    dispatcher.research = None
    dispatcher.building = None
    dispatcher.finetune = type("F", (), {
        "scan_documents": lambda self: None,
        "synthesize_pairs": lambda self: None,
        "create_training_job": lambda self, base_model: type("J", (), {
            "job_id": "job-1",
            "status": "completed",
            "dataset_size": 1,
        })(),
        "validate_baseline_coherence": lambda self: {"status": "baseline_ready"},
        "run_post_training_validation": lambda self, job_id: type("R", (), {
            "model_name": "sovereign-local-base-job-1",
            "validation_passed": True,
            "coherence_score": 0.8,
            "confidence_score": 0.75,
            "recommendation": "suitable_for_domain_routing",
            "falsification_condition": "rollback",
        })(),
        "privacy_boundary": "local-only",
        "repo_path": "/tmp",
    })()
    dispatcher.verifier = type("V", (), {
        "verify": lambda self, result, context: type("V2", (), {"ok": True, "issues": [], "risk": 0.0})(),
    })()
    dispatcher.coordinator = type("C", (), {
        "query": lambda self, **kwargs: type("Q", (), {"to_dict": lambda self: {}})(),
    })()
    result = dispatcher.dispatch("train model", context={"preferred_harness": "sovereign-finetune", "finetune_action": "train", "base_model": "local-base"})
    assert result["routing"]["primary"] == "sovereign-finetune"
    assert result["primary_output"]["action"] == "train"
    assert result["primary_output"]["job_id"] == "job-1"
    assert result["primary_output"]["integration_report"]["coherence_score"] == 0.8
