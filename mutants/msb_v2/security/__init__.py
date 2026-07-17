from .guardrails import GuardrailResult, Guardrails

__all__ = ["GuardrailResult", "Guardrails"]


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
