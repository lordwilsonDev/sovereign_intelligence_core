"""In-process model metadata registry with usage metrics and access control."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


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
    last_error: str = ""
    inference_failed: bool = False

    @property
    def average_latency_ms(self) -> float:
        return self.total_latency_ms / self.calls if self.calls else 0.0


class ModelRegistry:
    def __init__(self) -> None:
        self._models: dict[tuple[str, str], ModelRecord] = {}
        self._metrics: dict[tuple[str, str], ModelMetrics] = {}

    def register(self, model: ModelRecord) -> None:
        key = (model.id, model.version)
        self._models[key] = model
        self._metrics.setdefault(key, ModelMetrics())

    def get(self, model_id: str, version: str, *, role: str | None = None) -> ModelRecord:
        key = (model_id, version)
        try:
            model = self._models[key]
        except KeyError as error:
            raise KeyError(f"Unknown model: {model_id}@{version}") from error
        if model.allowed_roles and role not in model.allowed_roles:
            raise PermissionError(f"Role {role!r} cannot access {model_id}@{version}")
        return model

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

    def metrics_for(self, model_id: str, version: str, *, role: str | None = None) -> ModelMetrics:
        self.get(model_id, version, role=role)
        return self._metrics[(model_id, version)]


default_registry = ModelRegistry()
default_registry.register(ModelRecord("deepseek-v4-flash", "latest", "deepseek", "chat", input_cost_per_1k=0.0, output_cost_per_1k=0.0))
default_registry.register(ModelRecord("claude", "latest", "anthropic", "chat", input_cost_per_1k=0.003, output_cost_per_1k=0.003))
default_registry.register(ModelRecord("local", "latest", "local", "local", input_cost_per_1k=0.0, output_cost_per_1k=0.0))
