from __future__ import annotations

import sys
from pathlib import Path

import pytest

from msb_v2.api.main import _parse_args, run
from msb_v2.transport.tls import write_self_signed_cert


def test_parse_args_defaults() -> None:
    assert _parse_args([]) == {"cert": None, "key": None}


def test_parse_args_reads_flags() -> None:
    assert _parse_args(["--cert=/a/cert.pem", "--key=/a/key.pem"]) == {"cert": "/a/cert.pem", "key": "/a/key.pem"}


def test_run_returns_http_when_no_tls(tmp_path: str, monkeypatch: "pytest.MonkeyPatch") -> None:
    called = {}

    class FakeUvicorn:
        def run(self, application, **kwargs):  # noqa: A003
            called["application"] = application
            called["kwargs"] = kwargs

    monkeypatch.setitem(sys.modules, "uvicorn", FakeUvicorn())
    result = run(host="127.0.0.1", port=8080, reload=True)
    assert result == "http://127.0.0.1:8080"
    assert called["kwargs"]["port"] == 8080
    assert called["kwargs"]["reload"] is True


def test_run_returns_tls_when_cert_provided(tmp_path: str, monkeypatch: "pytest.MonkeyPatch") -> None:
    called = {}

    class FakeUvicorn:
        def run(self, application, **kwargs):  # noqa: A003
            called["application"] = application
            called["kwargs"] = kwargs

    monkeypatch.setitem(sys.modules, "uvicorn", FakeUvicorn())
    cert = str(Path(tmp_path) / "server.crt")
    key = str(Path(tmp_path) / "server.key")
    write_self_signed_cert(cert, key)
    result = run(cert=cert, key=key, host="127.0.0.1", port=8443)
    assert result == "tls://127.0.0.1:8443"
    assert called["kwargs"]["ssl_certfile"] in {cert, str(Path(cert).resolve())}
    assert called["kwargs"]["ssl_keyfile"] in {key, str(Path(key).resolve())}
