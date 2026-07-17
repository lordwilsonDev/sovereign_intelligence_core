from __future__ import annotations


from msb_v2.connectors.base import (
    BatchResult,
    ConnectorConfig,
    JiraConnector,
    SalesforceConnector,
    SAPConnector,
    SlackConnector,
    StubConnector,
    WorkdayConnector,
)


def test_stub_connector_write_and_read() -> None:
    cfg = ConnectorConfig(name="demo", settings={"mode": "stub"})
    connector = StubConnector(cfg)
    records = [{"id": "1", "value": "alpha"}, {"id": "2", "value": "beta"}]
    result = connector.write(records)
    assert isinstance(result, BatchResult)
    assert result.written == 2
    assert connector.validate() is True
    found = connector.read({"id": "1"})
    assert len(found) == 1
    assert found[0]["value"] == "alpha"


def test_stub_connector_partial_match() -> None:
    cfg = ConnectorConfig(name="partial")
    connector = StubConnector(cfg)
    connector.write([{"id": "1", "status": "active"}])
    assert len(connector.read({"status": "active"})) == 1
    assert len(connector.read({"status": "inactive"})) == 0


def test_subclass_is_stub() -> None:
    cfg = ConnectorConfig(name="sf")
    sf = SalesforceConnector(cfg)
    assert isinstance(sf, StubConnector)
    assert sf.validate() is True


def test_stub_connector_delete_returns_count() -> None:
    cfg = ConnectorConfig(name="delete-demo")
    connector = StubConnector(cfg)
    connector.write([{"id": "1"}, {"id": "2"}, {"id": "3"}])
    deleted = connector.delete(["1", "3"])
    assert deleted == 2
    assert len(connector.read({})) == 1
    assert connector.read({})[0]["id"] == "2"


def test_stub_connector_health_reports_counts() -> None:
    cfg = ConnectorConfig(name="health-demo")
    connector = StubConnector(cfg)
    connector.write([{"id": "1"}, {"id": "2"}])
    health = connector.health()
    assert health["status"] == "ok"
    assert health["connector"] == "health-demo"
    assert health["records"] == 2


def test_batch_result_contract() -> None:
    result = BatchResult(written=5, failed=1, errors=("timeout",))
    assert result.written == 5
    assert result.failed == 1
    assert len(result.errors) == 1


def test_all_connector_subclasses_construct() -> None:
    cfgs = [
        ConnectorConfig("sf"),
        ConnectorConfig("sap"),
        ConnectorConfig("workday"),
        ConnectorConfig("jira"),
        ConnectorConfig("slack"),
    ]
    connectors = [
        SalesforceConnector,
        SAPConnector,
        WorkdayConnector,
        JiraConnector,
        SlackConnector,
    ]
    for cfg, cls in zip(cfgs, connectors):
        instance = cls(cfg)
        assert instance.validate() is True
        assert instance.health()["status"] == "ok"


def test_read_empty_returns_empty_list() -> None:
    cfg = ConnectorConfig(name="empty")
    connector = StubConnector(cfg)
    assert connector.read({"any": "query"}) == []
