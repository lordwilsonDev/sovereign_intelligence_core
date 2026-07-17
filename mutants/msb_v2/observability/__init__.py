from .tracing import TraceEvent, Tracer

__all__ = ["TraceEvent", "Tracer"]


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
