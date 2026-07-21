from pathlib import Path
from msb_v2.local_ai.model_manager import ModelManager


def test_list_models() -> None:
    manager = ModelManager()
    models = manager.list_models()
    assert isinstance(models, list)


def test_record_use_persists_manifest() -> None:
    manager = ModelManager()
    manager.record_use("test-model")
    assert manager._manifest.get("test-model", {}).get("last_used_at") is not None
    assert Path(manager._manifest_path).exists()
