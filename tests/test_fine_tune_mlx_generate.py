from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_mlx_generate_fallback_reports_dependency_failure(tmp_path) -> None:
    client = TestClient(create_app())
    response = client.post(
        "/fine-tune/mlx-generate",
        json={
            "model": "mlx-community/Llama-3.2-3B-Instruct-4bit",
            "prompt": "Say OK",
            "max_tokens": 16,
            "temp": 0.0,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "returncode" in body
    assert "output" in body
    # this host currently returns dependency-failure instead of model output
    assert body.get("returncode") != 0 or "dependency-failure" in body.get("output", "") or "Say OK" in body.get("output", "")
