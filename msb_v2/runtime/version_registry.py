from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class VersionRecord:
    service: str
    version: str
    sha: str = ""
    since: str = ""


class VersionRegistry:
    def __init__(self) -> None:
        self._versions: Dict[str, VersionRecord] = {}

    def register(self, service: str, version: str, sha: str = "", since: str = "") -> None:
        self._versions[service] = VersionRecord(
            service=service, version=version, sha=sha, since=since
        )

    def get(self, service: str) -> VersionRecord | None:
        return self._versions.get(service)

    def all(self) -> Dict[str, VersionRecord]:
        return dict(self._versions)
