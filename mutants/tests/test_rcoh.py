from msb_v2.engine.rcoh import (
    Assumption,
    Phase,
    RCOH,
    RCOHState,
)


def make_state(**overrides):
    return RCOHState(cycle_id="c1", **overrides)


def test_confidence_is_mean_of_assumptions():
    state = make_state(assumptions=[Assumption("a1", 0.6), Assumption("a2", 0.8)])
    rcoh = RCOH(state)
    rcoh.state.current_phase = Phase.CONFIDENCE
    rcoh.run()
    assert rcoh.state.confidence == 0.7


def test_inversion_populates_inversions():
    state = make_state(
        assumptions=[Assumption("local-only deployment is safer")]
    )
    rcoh = RCOH(state)
    rcoh.state.current_phase = Phase.INVERSION
    rcoh.run()
    assert state.assumptions[0].inversion == "not(local-only deployment is safer)"


def test_stop_when_confidence_above_threshold():
    state = make_state(
        assumptions=[Assumption("a1", 0.95)],
        confidence_threshold=0.8,
    )
    rcoh = RCOH(state)
    rcoh.state.current_phase = Phase.CONFIDENCE
    rcoh.run()
    assert rcoh.state.current_phase == Phase.DONE


def test_rcoh_runs_full_cycle():
    state = make_state()
    rcoh = RCOH(state)
    result = rcoh.run(max_iterations=20)
    assert result.current_phase == Phase.DONE
    assert result.iteration <= 15
