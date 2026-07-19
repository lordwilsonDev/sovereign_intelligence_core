from __future__ import annotations

from pathlib import Path

from msb_v2.transport.tls import resolve_tls_paths, write_self_signed_cert


def test_write_self_signed_cert_creates_files(tmp_path: str) -> None:
    cert = str(Path(tmp_path) / "server.crt")
    key = str(Path(tmp_path) / "server.key")
    out = write_self_signed_cert(cert, key, common_name="localhost", days=1)
    assert Path(out["cert_path"]).exists()
    assert Path(out["key_path"]).exists()
    assert Path(out["cert_path"]).stat().st_size > 0
    assert Path(out["key_path"]).stat().st_size > 0


def test_resolve_tls_paths_returns_none_when_missing() -> None:
    assert resolve_tls_paths(None, None) is None
    assert resolve_tls_paths("/x/cert.pem", None) is None
    assert resolve_tls_paths("/x/cert.pem", "/x/key.pem") is None


def test_resolve_tls_paths_returns_pair_when_present(tmp_path: str) -> None:
    cert = str(Path(tmp_path) / "tls.crt")
    key = str(Path(tmp_path) / "tls.key")
    write_self_signed_cert(cert, key)
    assert resolve_tls_paths(cert, key) == (cert, key)
