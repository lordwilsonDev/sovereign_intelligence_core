"""Cross-node task executor — runs submitted tasks and produces signed receipts."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


class MeshTaskExecutor:
    """Picks up queued mesh tasks, runs them through the local kernel, and stores signed results."""

    def __init__(self, node_identity: Any, task_store: Dict[str, Dict[str, Any]]) -> None:
        self._node = node_identity
        self._tasks = task_store

    def execute(self, task_id: str) -> Dict[str, Any]:
        """Run the task and return a signed UIM-style receipt."""
        task = self._tasks.get(task_id)
        if not task:
            return {"error": "task not found"}

        if task.get("status") not in {"queued", "processing"}:
            return {"error": "task is not queued", "current_status": task.get("status")}

        task["status"] = "processing"
        task.pop("error", None)

        try:
            result = self._run_intent(task.get("intent") or "")
        except Exception as exc:
            task["status"] = "failed"
            task["error"] = str(exc)
            return task

        receipt = {
            "task_id": task_id,
            "result": result,
            "executed_by": getattr(self._node, "node_id", None),
            "signature": self._sign(result),
        }
        task["status"] = "completed"
        task["result"] = receipt
        return task

    def _run_intent(self, intent: str) -> Dict[str, Any]:
        try:
            from msb_v2.kernel.kb4 import KB4Kernel
            kernel = KB4Kernel()
            kb4 = kernel.run(intent)
            try:
                return json.loads(kb4.json()) if hasattr(kb4, "json") else kb4.to_dict()
            except Exception:
                return dict(getattr(kb4, "__dict__", {"result": str(kb4)}))
        except Exception:
            pass
        try:
            from cognitive_compiler.harness_dispatcher_v1 import HarnessDispatcher
            dispatcher = HarnessDispatcher()
            return dispatcher.dispatch(intent, {})
        except Exception as exc:
            return {"status": "error", "message": str(exc), "query": intent}

    def _sign(self, data: Any) -> str:
        payload = json.dumps(data, sort_keys=True, default=str).encode()
        return hashlib.sha256(payload + str(getattr(self._node, "node_id", "") or "").encode()).hexdigest()
