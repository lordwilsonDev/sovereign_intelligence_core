from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Request

from msb_v2.schh.engine import Component, ComponentType, HealthEngine, Registry
from msb_v2.schh.registry import Component as ComponentAlias

router = APIRouter()
_registry = Registry()
_engine = HealthEngine(registry=_registry)
_engine.register_defaults()


@router.get("/status")
def status() -> Dict[str, Any]:
    readiness = _engine.readiness()
    return {
        "system_readiness": readiness.status,
        "healthy": readiness.healthy_count,
        "degraded": readiness.degraded_count,
        "unhealthy": readiness.unhealthy_count,
        "critical_unhealthy": readiness.critical_unhealthy,
        "updated_at": readiness.updated_at,
    }


@router.get("/components")
def list_components() -> Dict[str, Any]:
    components = _registry.all()
    results = _engine.run_checks()
    latest = {r.component_id: r for r in results}
    payload = []
    for component in components:
        current = latest.get(component.id)
        payload.append({
            "id": component.id,
            "name": component.name,
            "type": component.type.value,
            "critical": component.critical,
            "auto_heal": component.auto_heal,
            "health_endpoint": component.health_endpoint,
            "check_method": component.check_method.value,
            "status": current.status.value if current else "unknown",
            "detail": current.detail if current else "",
            "duration_ms": current.duration_ms if current else 0.0,
            "timestamp": current.timestamp if current else "",
        })
    return {"components": payload}


@router.get("/components/{component_id}")
def component_detail(component_id: str) -> Dict[str, Any]:
    component = _registry.get(component_id)
    if not component:
        return {"status": "not_found"}
    results = _engine.run_checks()
    current = next((r for r in results if r.component_id == component_id), None)
    return {
        "id": component.id,
        "name": component.name,
        "type": component.type.value,
        "critical": component.critical,
        "auto_heal": component.auto_heal,
        "status": current.status.value if current else "unknown",
        "detail": current.detail if current else "",
        "duration_ms": current.duration_ms if current else 0.0,
        "timestamp": current.timestamp if current else "",
    }


@router.post("/components")
def register_component(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        component = ComponentAlias(
            id=str(payload.get("id", "")).strip(),
            name=str(payload.get("name", "")).strip(),
            type=ComponentType(str(payload.get("type", ComponentType.harness.value))),
            health_endpoint=str(payload.get("health_endpoint", "")).strip(),
            check_method=str(payload.get("check_method", ComponentAlias.check_method.value)),
            check_interval_seconds=int(payload.get("check_interval_seconds", 30)),
            timeout_seconds=int(payload.get("timeout_seconds", 5)),
            critical=bool(payload.get("critical", True)),
            auto_heal=bool(payload.get("auto_heal", False)),
            dependencies=list(payload.get("dependencies", [])),
            metadata=dict(payload.get("metadata", {})),
        )
        _registry.register(component)
        return {"status": "registered", "id": component.id}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)[:120]}


@router.delete("/components/{component_id}")
def unregister_component(component_id: str) -> Dict[str, Any]:
    _registry.unregister(component_id)
    return {"status": "unregistered", "id": component_id}


@router.post("/check/{component_id}")
def check_component(component_id: str, request: Request) -> Dict[str, Any]:
    component = _registry.get(component_id)
    if not component:
        return {"status": "not_found"}
    client = request.app.state.test_client if hasattr(request.app, "state") else None
    result = _engine.check_component(component, client=client)
    return result.__dict__


@router.post("/check/all")
def check_all(request: Request) -> Dict[str, Any]:
    client = request.app.state.test_client if hasattr(request.app, "state") else None
    results = _engine.run_checks(client=client)
    return {"results": [r.__dict__ for r in results]}


@router.get("/history")
def history(limit: int = 50) -> Dict[str, Any]:
    return {"items": _engine.history(limit=limit)}


@router.post("/autoheal/{component_id}")
def autoheal(component_id: str) -> Dict[str, Any]:
    component = _registry.get(component_id)
    if not component:
        return {"status": "not_found"}
    if not component.auto_heal:
        return {"status": "skipped", "detail": "auto_heal disabled"}
    return {"status": "healed", "id": component_id}
