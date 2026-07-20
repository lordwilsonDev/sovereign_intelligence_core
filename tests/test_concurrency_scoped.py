from __future__ import annotations

import threading

import pytest

from msb_v2.concurrency.cancellable import CancellableOutput, Cancelled, Done, bind, cancel, done, fmap, is_cancelled
from msb_v2.concurrency.task_scope import ScopeCancelled, SquadErrorFusion, TaskScope


def test_cancellable_bind_propagates_cancelled():
    c = cancel(reason="policy")
    result = bind(c, lambda _x: done("ok"))
    assert is_cancelled(result)
    assert result.reason == "policy"


def test_cancellable_fmap_preserves_value():
    d = done(5)
    result = fmap(d, lambda x: x + 1)
    assert isinstance(result, Done)
    assert result.value == 6


def test_task_scope_cancel_children():
    scope = TaskScope(name="q")
    started = threading.Event()
    released = threading.Event()

    def task():
        started.set()
        released.wait(timeout=1)
        return 1

    child = scope.spawn("t1", task)
    started.wait(timeout=1)
    scope.cancel()
    child.wait(timeout=1)
    assert child.cancelled


def test_task_scope_results_ok():
    scope = TaskScope(name="q")
    children = [
        scope.spawn("a", lambda: done(1)),
        scope.spawn("b", lambda: done(2)),
    ]
    result = scope.results()
    assert isinstance(result, Done)
    assert result.value == {"a": 1, "b": 2}


def test_squad_error_fusion_metadata():
    fusion = SquadErrorFusion(scope="s1")
    fusion.add("t1", ValueError("v1"))
    d = fusion.to_dict()
    assert d["scope"] == "s1"
    assert d["count"] == 1
    assert d["tasks"][0]["task_id"] == "t1"
