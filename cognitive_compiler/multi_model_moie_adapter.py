from __future__ import annotations

from Cognitive_compiler.multi_model_moie import LLMBackend, MoIEExpertConfig, MultiModelMoIEOrchestrator


class MultiModelMoIEAdapter:
    def __init__(self, critic_backend: LLMBackend = None, scout_backend: LLMBackend = None, synthesizer_backend: LLMBackend = None, default_backend: LLMBackend = None):
        critic = critic_backend or default_backend
        scout = scout_backend or default_backend
        synthesizer = synthesizer_backend or default_backend
        if critic is None or scout is None or synthesizer is None:
            raise ValueError("multi-model MoIE requires LLMBackends for critic/scout/synthesizer")
        self.orchestrator = MultiModelMoIEOrchestrator({
            "critic": MoIEExpertConfig(role="critic", backend=critic),
            "scout": MoIEExpertConfig(role="scout", backend=scout),
            "synthesizer": MoIEExpertConfig(role="synthesizer", backend=synthesizer),
        })

    def run(self, problem: str, context: str) -> dict:
        return self.orchestrator.run_dialectic(problem, context)
