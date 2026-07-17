from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ConnectorConfig:
    name: str
    settings: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BatchResult:
    written: int
    failed: int = 0
    errors: tuple[str, ...] = ()


class AILConnector(ABC):
    def __init__(self, config: ConnectorConfig) -> None:
        self.config = config

    @abstractmethod
    def read(self, query: dict[str, Any]) -> list[dict[str, Any]]: ...

    @abstractmethod
    def write(self, records: list[dict[str, Any]]) -> BatchResult: ...

    @abstractmethod
    def delete(self, record_ids: list[str]) -> int: ...

    @abstractmethod
    def validate(self) -> bool: ...

    @abstractmethod
    def health(self) -> dict[str, Any]: ...

    def connect(self) -> None:
        return None


class StubConnector(AILConnector):
    """Credential-free placeholder for Salesforce, SAP, Workday, Jira, or Slack."""

    def __init__(self, config: ConnectorConfig) -> None:
        super().__init__(config)
        self.records: list[dict[str, Any]] = []

    def read(self, query: dict[str, Any]) -> list[dict[str, Any]]:
        if not query:
            return list(self.records)
        return [
            record
            for record in self.records
            if all(record.get(key) == value for key, value in query.items())
        ]

    def write(self, records: list[dict[str, Any]]) -> BatchResult:
        self.records.extend(records)
        return BatchResult(written=len(records))

    def delete(self, record_ids: list[str]) -> int:
        before = len(self.records)
        self.records = [
            record for record in self.records if record.get("id") not in record_ids
        ]
        return before - len(self.records)

    def validate(self) -> bool:
        return True

    def health(self) -> dict[str, Any]:
        return {
            "connector": self.config.name,
            "status": "ok",
            "records": len(self.records),
        }


class SalesforceConnector(StubConnector):
    pass


class SAPConnector(StubConnector):
    pass


class WorkdayConnector(StubConnector):
    pass


class JiraConnector(StubConnector):
    pass


class SlackConnector(StubConnector):
    pass
