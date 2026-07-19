from __future__ import annotations

import time

from msb_v2.agent.sovereign_agent_runtime import LoveGateway, AgentProfile, SovereignAgentRuntime


def test_love_gateway_quarantines_by_type() -> None:
    gw = LoveGateway()
    result = gw.quarantine({"type": "injection_attempt"}, "epistemic_risk")
    assert result["quarantined"] is True
    assert len(gw.recent(limit=5)) == 1


def test_runtime_submit_queue_depth() -> None:
    runtime = SovereignAgentRuntime(profile=AgentProfile(profile_id="p", display_name="P", memory_partition="m"))
    first = runtime.submit({"type": "msg", "content": "hello"})
    second = runtime.submit({"type": "ignore"})
    assert first["accepted"] is True
    assert first["queue_depth"] == 1
    assert second["quarantined"] is True
    runtime.start()
    time.sleep(0.05)
    runtime.stop()
    assert runtime.state()["processed_count"] == 1
