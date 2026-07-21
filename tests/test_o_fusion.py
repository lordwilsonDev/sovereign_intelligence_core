import asyncio
import pytest

from o_fusion import Scope, FusionPolicy, FusedError


async def ok(value, delay=0.01):
    await asyncio.sleep(delay)
    return value


async def fail(exc: Exception, delay=0.01):
    await asyncio.sleep(delay)
    raise exc


# ---------- AGGREGATE ----------

@pytest.mark.asyncio
async def test_aggregate_collects_all_failures_when_not_cancelling():
    with pytest.raises(ExceptionGroup) as exc_info:
        async with Scope(policy=FusionPolicy.AGGREGATE, cancel_on_error=False) as scope:
            scope.spawn(fail(ValueError("a"), 0.01), name="a")
            scope.spawn(fail(TypeError("b"), 0.02), name="b")
            scope.spawn(ok(1, 0.03), name="c")

    eg = exc_info.value
    assert len(eg.exceptions) == 2
    types = {type(e) for e in eg.exceptions}
    assert types == {ValueError, TypeError}


@pytest.mark.asyncio
async def test_aggregate_with_cancellation_only_collects_survivors():
    with pytest.raises(ExceptionGroup) as exc_info:
        async with Scope(policy=FusionPolicy.AGGREGATE) as scope:
            scope.spawn(fail(ValueError("fast"), 0.01), name="a")
            scope.spawn(fail(TypeError("slow"), 0.5), name="b")

    eg = exc_info.value
    assert len(eg.exceptions) == 1
    assert isinstance(eg.exceptions[0], ValueError)


@pytest.mark.asyncio
async def test_aggregate_no_failures_no_raise():
    results = []
    async with Scope(policy=FusionPolicy.AGGREGATE) as scope:
        scope.spawn(ok(1), name="a")
        scope.spawn(ok(2), name="b")
    assert True


@pytest.mark.asyncio
async def test_aggregate_catchable_with_except_star():
    caught_value_errors = []
    caught_type_errors = []
    try:
        async with Scope(policy=FusionPolicy.AGGREGATE) as scope:
            scope.spawn(fail(ValueError("a")), name="a")
            scope.spawn(fail(TypeError("b")), name="b")
    except* ValueError as eg:
        caught_value_errors.extend(eg.exceptions)
    except* TypeError as eg:
        caught_type_errors.extend(eg.exceptions)

    assert len(caught_value_errors) == 1
    assert len(caught_type_errors) == 1


# ---------- FIRST_WINS ----------

@pytest.mark.asyncio
async def test_first_wins_propagates_earliest_and_suppresses_rest():
    with pytest.raises(ValueError) as exc_info:
        async with Scope(policy=FusionPolicy.FIRST_WINS, cancel_on_error=False) as scope:
            scope.spawn(fail(ValueError("first"), delay=0.01), name="a")
            scope.spawn(fail(TypeError("second"), delay=0.05), name="b")

    primary = exc_info.value
    assert str(primary) == "first"
    assert len(primary.__suppressed__) == 1
    assert isinstance(primary.__suppressed__[0], TypeError)


# ---------- TREE ----------

@pytest.mark.asyncio
async def test_tree_preserves_which_task_failed():
    with pytest.raises(FusedError) as exc_info:
        async with Scope(policy=FusionPolicy.TREE) as scope:
            scope.spawn(fail(ValueError("bad-a")), name="worker-a")
            scope.spawn(fail(TypeError("bad-b")), name="worker-b")
            scope.spawn(ok(1), name="worker-c")

    err = exc_info.value
    assert set(err.tree.keys()) == {"worker-a", "worker-b"}
    assert isinstance(err.tree["worker-a"], ValueError)
    assert isinstance(err.tree["worker-b"], TypeError)


# ---------- Cancellation propagation (structured concurrency invariant) ----------

@pytest.mark.asyncio
async def test_sibling_is_cancelled_on_first_failure():
    cancelled_flag = {"cancelled": False}

    async def slow_worker():
        try:
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            cancelled_flag["cancelled"] = True
            raise

    with pytest.raises(ExceptionGroup):
        async with Scope(policy=FusionPolicy.AGGREGATE) as scope:
            scope.spawn(fail(ValueError("early failure"), delay=0.01), name="failer")
            scope.spawn(slow_worker(), name="slow")

    assert cancelled_flag["cancelled"] is True


# ---------- Body-level failure also triggers fusion ----------

@pytest.mark.asyncio
async def test_body_exception_is_fused_with_child_exceptions():
    with pytest.raises(ExceptionGroup) as exc_info:
        async with Scope(policy=FusionPolicy.AGGREGATE) as scope:
            scope.spawn(fail(ValueError("child"), delay=0.001), name="a")
            await asyncio.sleep(0.05)  # give the child time to fail first
            raise RuntimeError("body blew up")

    eg = exc_info.value
    types = {type(e) for e in eg.exceptions}
    assert RuntimeError in types
    assert ValueError in types
