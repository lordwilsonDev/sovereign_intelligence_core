from __future__ import annotations

import pytest

from msb_v2.api.middleware import set_local_bypass


@pytest.fixture(autouse=True)
def local_auth_bypass() -> None:
    set_local_bypass(True)
    yield
    set_local_bypass(None)
