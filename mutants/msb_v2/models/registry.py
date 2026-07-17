"""In-process model metadata registry with usage metrics and access control."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


@dataclass(frozen=True)
class ModelRecord:
    id: str
    version: str
    provider: str
    model_type: str
    allowed_roles: frozenset[str] = frozenset()
    input_cost_per_1k: float = 0.0
    output_cost_per_1k: float = 0.0


@dataclass
class ModelMetrics:
    calls: int = 0
    total_latency_ms: float = 0.0
    total_cost: float = 0.0
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def average_latency_ms(self) -> float:
        return self.total_latency_ms / self.calls if self.calls else 0.0
mutants_xǁModelRegistryǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁModelRegistryǁregister__mutmut: MutantDict = {}  # type: ignore
mutants_xǁModelRegistryǁget__mutmut: MutantDict = {}  # type: ignore
mutants_xǁModelRegistryǁrecord_usage__mutmut: MutantDict = {}  # type: ignore
mutants_xǁModelRegistryǁmetrics_for__mutmut: MutantDict = {}  # type: ignore


class ModelRegistry:
    @_mutmut_mutated(mutants_xǁModelRegistryǁ__init____mutmut)
    def __init__(self) -> None:
        self._models: dict[tuple[str, str], ModelRecord] = {}
        self._metrics: dict[tuple[str, str], ModelMetrics] = {}
    def xǁModelRegistryǁ__init____mutmut_orig(self) -> None:
        self._models: dict[tuple[str, str], ModelRecord] = {}
        self._metrics: dict[tuple[str, str], ModelMetrics] = {}
    def xǁModelRegistryǁ__init____mutmut_1(self) -> None:
        self._models: dict[tuple[str, str], ModelRecord] = None
        self._metrics: dict[tuple[str, str], ModelMetrics] = {}
    def xǁModelRegistryǁ__init____mutmut_2(self) -> None:
        self._models: dict[tuple[str, str], ModelRecord] = {}
        self._metrics: dict[tuple[str, str], ModelMetrics] = None

    @_mutmut_mutated(mutants_xǁModelRegistryǁregister__mutmut)
    def register(self, model: ModelRecord) -> None:
        key = (model.id, model.version)
        self._models[key] = model
        self._metrics.setdefault(key, ModelMetrics())

    def xǁModelRegistryǁregister__mutmut_orig(self, model: ModelRecord) -> None:
        key = (model.id, model.version)
        self._models[key] = model
        self._metrics.setdefault(key, ModelMetrics())

    def xǁModelRegistryǁregister__mutmut_1(self, model: ModelRecord) -> None:
        key = None
        self._models[key] = model
        self._metrics.setdefault(key, ModelMetrics())

    def xǁModelRegistryǁregister__mutmut_2(self, model: ModelRecord) -> None:
        key = (model.id, model.version)
        self._models[key] = None
        self._metrics.setdefault(key, ModelMetrics())

    def xǁModelRegistryǁregister__mutmut_3(self, model: ModelRecord) -> None:
        key = (model.id, model.version)
        self._models[key] = model
        self._metrics.setdefault(None, ModelMetrics())

    def xǁModelRegistryǁregister__mutmut_4(self, model: ModelRecord) -> None:
        key = (model.id, model.version)
        self._models[key] = model
        self._metrics.setdefault(key, None)

    def xǁModelRegistryǁregister__mutmut_5(self, model: ModelRecord) -> None:
        key = (model.id, model.version)
        self._models[key] = model
        self._metrics.setdefault(ModelMetrics())

    def xǁModelRegistryǁregister__mutmut_6(self, model: ModelRecord) -> None:
        key = (model.id, model.version)
        self._models[key] = model
        self._metrics.setdefault(key, )

    @_mutmut_mutated(mutants_xǁModelRegistryǁget__mutmut)
    def get(self, model_id: str, version: str, *, role: str | None = None) -> ModelRecord:
        key = (model_id, version)
        try:
            model = self._models[key]
        except KeyError as error:
            raise KeyError(f"Unknown model: {model_id}@{version}") from error
        if model.allowed_roles and role not in model.allowed_roles:
            raise PermissionError(f"Role {role!r} cannot access {model_id}@{version}")
        return model

    def xǁModelRegistryǁget__mutmut_orig(self, model_id: str, version: str, *, role: str | None = None) -> ModelRecord:
        key = (model_id, version)
        try:
            model = self._models[key]
        except KeyError as error:
            raise KeyError(f"Unknown model: {model_id}@{version}") from error
        if model.allowed_roles and role not in model.allowed_roles:
            raise PermissionError(f"Role {role!r} cannot access {model_id}@{version}")
        return model

    def xǁModelRegistryǁget__mutmut_1(self, model_id: str, version: str, *, role: str | None = None) -> ModelRecord:
        key = None
        try:
            model = self._models[key]
        except KeyError as error:
            raise KeyError(f"Unknown model: {model_id}@{version}") from error
        if model.allowed_roles and role not in model.allowed_roles:
            raise PermissionError(f"Role {role!r} cannot access {model_id}@{version}")
        return model

    def xǁModelRegistryǁget__mutmut_2(self, model_id: str, version: str, *, role: str | None = None) -> ModelRecord:
        key = (model_id, version)
        try:
            model = None
        except KeyError as error:
            raise KeyError(f"Unknown model: {model_id}@{version}") from error
        if model.allowed_roles and role not in model.allowed_roles:
            raise PermissionError(f"Role {role!r} cannot access {model_id}@{version}")
        return model

    def xǁModelRegistryǁget__mutmut_3(self, model_id: str, version: str, *, role: str | None = None) -> ModelRecord:
        key = (model_id, version)
        try:
            model = self._models[key]
        except KeyError as error:
            raise KeyError(None) from error
        if model.allowed_roles and role not in model.allowed_roles:
            raise PermissionError(f"Role {role!r} cannot access {model_id}@{version}")
        return model

    def xǁModelRegistryǁget__mutmut_4(self, model_id: str, version: str, *, role: str | None = None) -> ModelRecord:
        key = (model_id, version)
        try:
            model = self._models[key]
        except KeyError as error:
            raise KeyError(f"Unknown model: {model_id}@{version}") from error
        if model.allowed_roles or role not in model.allowed_roles:
            raise PermissionError(f"Role {role!r} cannot access {model_id}@{version}")
        return model

    def xǁModelRegistryǁget__mutmut_5(self, model_id: str, version: str, *, role: str | None = None) -> ModelRecord:
        key = (model_id, version)
        try:
            model = self._models[key]
        except KeyError as error:
            raise KeyError(f"Unknown model: {model_id}@{version}") from error
        if model.allowed_roles and role in model.allowed_roles:
            raise PermissionError(f"Role {role!r} cannot access {model_id}@{version}")
        return model

    def xǁModelRegistryǁget__mutmut_6(self, model_id: str, version: str, *, role: str | None = None) -> ModelRecord:
        key = (model_id, version)
        try:
            model = self._models[key]
        except KeyError as error:
            raise KeyError(f"Unknown model: {model_id}@{version}") from error
        if model.allowed_roles and role not in model.allowed_roles:
            raise PermissionError(None)
        return model

    @_mutmut_mutated(mutants_xǁModelRegistryǁrecord_usage__mutmut)
    def record_usage(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_orig(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_1(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 1,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_2(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 1,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_3(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = None
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_4(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(None, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_5(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, None, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_6(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=None)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_7(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_8(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_9(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, )
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_10(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = None
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_11(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls = 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_12(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls -= 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_13(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 2
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_14(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms = latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_15(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms -= latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_16(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost = (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_17(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost -= (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_18(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) / model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_19(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens * 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_20(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1001) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_21(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost = (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_22(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost -= (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_23(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) / model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_24(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens * 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_25(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1001) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(timezone.utc)
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_26(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = None
        return metrics

    def xǁModelRegistryǁrecord_usage__mutmut_27(
        self,
        model_id: str,
        version: str,
        *,
        latency_ms: float,
        input_tokens: int = 0,
        output_tokens: int = 0,
        role: str | None = None,
    ) -> ModelMetrics:
        model = self.get(model_id, version, role=role)
        metrics = self._metrics[(model_id, version)]
        metrics.calls += 1
        metrics.total_latency_ms += latency_ms
        metrics.total_cost += (input_tokens / 1000) * model.input_cost_per_1k
        metrics.total_cost += (output_tokens / 1000) * model.output_cost_per_1k
        metrics.updated_at = datetime.now(None)
        return metrics

    @_mutmut_mutated(mutants_xǁModelRegistryǁmetrics_for__mutmut)
    def metrics_for(self, model_id: str, version: str, *, role: str | None = None) -> ModelMetrics:
        self.get(model_id, version, role=role)
        return self._metrics[(model_id, version)]

    def xǁModelRegistryǁmetrics_for__mutmut_orig(self, model_id: str, version: str, *, role: str | None = None) -> ModelMetrics:
        self.get(model_id, version, role=role)
        return self._metrics[(model_id, version)]

    def xǁModelRegistryǁmetrics_for__mutmut_1(self, model_id: str, version: str, *, role: str | None = None) -> ModelMetrics:
        self.get(None, version, role=role)
        return self._metrics[(model_id, version)]

    def xǁModelRegistryǁmetrics_for__mutmut_2(self, model_id: str, version: str, *, role: str | None = None) -> ModelMetrics:
        self.get(model_id, None, role=role)
        return self._metrics[(model_id, version)]

    def xǁModelRegistryǁmetrics_for__mutmut_3(self, model_id: str, version: str, *, role: str | None = None) -> ModelMetrics:
        self.get(model_id, version, role=None)
        return self._metrics[(model_id, version)]

    def xǁModelRegistryǁmetrics_for__mutmut_4(self, model_id: str, version: str, *, role: str | None = None) -> ModelMetrics:
        self.get(version, role=role)
        return self._metrics[(model_id, version)]

    def xǁModelRegistryǁmetrics_for__mutmut_5(self, model_id: str, version: str, *, role: str | None = None) -> ModelMetrics:
        self.get(model_id, role=role)
        return self._metrics[(model_id, version)]

    def xǁModelRegistryǁmetrics_for__mutmut_6(self, model_id: str, version: str, *, role: str | None = None) -> ModelMetrics:
        self.get(model_id, version, )
        return self._metrics[(model_id, version)]

mutants_xǁModelRegistryǁ__init____mutmut['_mutmut_orig'] = ModelRegistry.xǁModelRegistryǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁModelRegistryǁ__init____mutmut['xǁModelRegistryǁ__init____mutmut_1'] = ModelRegistry.xǁModelRegistryǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁ__init____mutmut['xǁModelRegistryǁ__init____mutmut_2'] = ModelRegistry.xǁModelRegistryǁ__init____mutmut_2 # type: ignore # mutmut generated

mutants_xǁModelRegistryǁregister__mutmut['_mutmut_orig'] = ModelRegistry.xǁModelRegistryǁregister__mutmut_orig # type: ignore # mutmut generated
mutants_xǁModelRegistryǁregister__mutmut['xǁModelRegistryǁregister__mutmut_1'] = ModelRegistry.xǁModelRegistryǁregister__mutmut_1 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁregister__mutmut['xǁModelRegistryǁregister__mutmut_2'] = ModelRegistry.xǁModelRegistryǁregister__mutmut_2 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁregister__mutmut['xǁModelRegistryǁregister__mutmut_3'] = ModelRegistry.xǁModelRegistryǁregister__mutmut_3 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁregister__mutmut['xǁModelRegistryǁregister__mutmut_4'] = ModelRegistry.xǁModelRegistryǁregister__mutmut_4 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁregister__mutmut['xǁModelRegistryǁregister__mutmut_5'] = ModelRegistry.xǁModelRegistryǁregister__mutmut_5 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁregister__mutmut['xǁModelRegistryǁregister__mutmut_6'] = ModelRegistry.xǁModelRegistryǁregister__mutmut_6 # type: ignore # mutmut generated

mutants_xǁModelRegistryǁget__mutmut['_mutmut_orig'] = ModelRegistry.xǁModelRegistryǁget__mutmut_orig # type: ignore # mutmut generated
mutants_xǁModelRegistryǁget__mutmut['xǁModelRegistryǁget__mutmut_1'] = ModelRegistry.xǁModelRegistryǁget__mutmut_1 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁget__mutmut['xǁModelRegistryǁget__mutmut_2'] = ModelRegistry.xǁModelRegistryǁget__mutmut_2 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁget__mutmut['xǁModelRegistryǁget__mutmut_3'] = ModelRegistry.xǁModelRegistryǁget__mutmut_3 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁget__mutmut['xǁModelRegistryǁget__mutmut_4'] = ModelRegistry.xǁModelRegistryǁget__mutmut_4 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁget__mutmut['xǁModelRegistryǁget__mutmut_5'] = ModelRegistry.xǁModelRegistryǁget__mutmut_5 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁget__mutmut['xǁModelRegistryǁget__mutmut_6'] = ModelRegistry.xǁModelRegistryǁget__mutmut_6 # type: ignore # mutmut generated

mutants_xǁModelRegistryǁrecord_usage__mutmut['_mutmut_orig'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_orig # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_1'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_1 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_2'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_2 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_3'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_3 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_4'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_4 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_5'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_5 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_6'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_6 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_7'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_7 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_8'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_8 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_9'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_9 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_10'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_10 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_11'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_11 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_12'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_12 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_13'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_13 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_14'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_14 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_15'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_15 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_16'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_16 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_17'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_17 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_18'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_18 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_19'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_19 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_20'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_20 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_21'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_21 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_22'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_22 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_23'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_23 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_24'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_24 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_25'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_25 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_26'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_26 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁrecord_usage__mutmut['xǁModelRegistryǁrecord_usage__mutmut_27'] = ModelRegistry.xǁModelRegistryǁrecord_usage__mutmut_27 # type: ignore # mutmut generated

mutants_xǁModelRegistryǁmetrics_for__mutmut['_mutmut_orig'] = ModelRegistry.xǁModelRegistryǁmetrics_for__mutmut_orig # type: ignore # mutmut generated
mutants_xǁModelRegistryǁmetrics_for__mutmut['xǁModelRegistryǁmetrics_for__mutmut_1'] = ModelRegistry.xǁModelRegistryǁmetrics_for__mutmut_1 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁmetrics_for__mutmut['xǁModelRegistryǁmetrics_for__mutmut_2'] = ModelRegistry.xǁModelRegistryǁmetrics_for__mutmut_2 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁmetrics_for__mutmut['xǁModelRegistryǁmetrics_for__mutmut_3'] = ModelRegistry.xǁModelRegistryǁmetrics_for__mutmut_3 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁmetrics_for__mutmut['xǁModelRegistryǁmetrics_for__mutmut_4'] = ModelRegistry.xǁModelRegistryǁmetrics_for__mutmut_4 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁmetrics_for__mutmut['xǁModelRegistryǁmetrics_for__mutmut_5'] = ModelRegistry.xǁModelRegistryǁmetrics_for__mutmut_5 # type: ignore # mutmut generated
mutants_xǁModelRegistryǁmetrics_for__mutmut['xǁModelRegistryǁmetrics_for__mutmut_6'] = ModelRegistry.xǁModelRegistryǁmetrics_for__mutmut_6 # type: ignore # mutmut generated
