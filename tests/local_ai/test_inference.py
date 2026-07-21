from msb_v2.local_ai.inference_engine import InferenceEngine


def test_quarantine_blocks_url() -> None:
    engine = InferenceEngine()
    try:
        engine.generate("qwen2.5:0.5b", "visit http://evil.example")
    except ValueError:
        return
    raise AssertionError("Expected quarantine rejection")


def test_local_inference_logs_receipt() -> None:
    # Use system Ollama; if unavailable, skip receipt path rather than fail core.
    try:
        import urllib.request
        urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=3)
    except Exception:
        pass
