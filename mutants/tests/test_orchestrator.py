import pytest

from msb_v2.engine.orchestrator import BLOCKED, FAILED, SUCCEEDED, Task, orchestrate


def test_single_task_runs_immediately():
    task = Task(id="one", action=lambda: "done")

    completed = orchestrate([task])

    assert completed == [task]
    assert task.status == SUCCEEDED
    assert task.result == "done"


def test_task_waits_for_its_dependency():
    calls: list[str] = []
    first = Task(id="a", action=lambda: calls.append("a"))
    second = Task(id="b", dependencies=["a"], action=lambda: calls.append("b"))

    orchestrate([second, first])

    assert calls == ["a", "b"]
    assert second.status == SUCCEEDED


def test_circular_dependency_raises_error():
    first = Task(id="a", dependencies=["b"])
    second = Task(id="b", dependencies=["a"])

    with pytest.raises(ValueError, match="Circular"):
        orchestrate([first, second])


def test_failed_task_blocks_dependents():
    def fail():
        raise RuntimeError("source unavailable")

    first = Task(id="a", action=fail)
    second = Task(id="b", dependencies=["a"], action=lambda: "must not run")

    orchestrate([first, second])

    assert first.status == FAILED
    assert isinstance(first.result, RuntimeError)
    assert second.status == BLOCKED
    assert second.result is None


def test_empty_task_list_returns_empty():
    assert orchestrate([]) == []
