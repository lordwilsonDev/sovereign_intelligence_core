from .registry import ModelMetrics, ModelRecord, ModelRegistry

__all__ = ["ModelMetrics", "ModelRecord", "ModelRegistry"]


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
