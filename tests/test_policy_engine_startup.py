from __future__ import annotations

import time


def test_policy_engine_startup_thread():
    from msb_v2.api.web import create_app

    if getattr(create_app, "_policy_engine_started", False):
        return

    create_app()
    time.sleep(0.2)
    assert getattr(create_app, "_policy_engine_started", False) is True
