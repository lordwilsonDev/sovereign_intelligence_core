from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Secret:
    key: str
    value: str


class SecretsLoader:
    def __init__(self, prefix: str = "MSB_SECRET_") -> None:
        self.prefix = prefix
        self._secrets: Dict[str, Secret] = {}

    def load_env(self) -> Dict[str, Secret]:
        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                secret_key = key[len(self.prefix) :].lower()
                self._secrets[secret_key] = Secret(key=secret_key, value=value)
        return dict(self._secrets)

    def get(self, key: str, default: str = "") -> Secret:
        return self._secrets.get(key, Secret(key=key, value=default))
