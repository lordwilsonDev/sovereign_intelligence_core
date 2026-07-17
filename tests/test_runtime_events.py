from __future__ import annotations

from msb_v2.runtime.events import Event, EventBus


def test_event_bus_publish_and_receive() -> None:
    received = []

    def handler(event: Event) -> None:
        received.append(event)

    bus = EventBus()
    bus.subscribe("ingest", handler)
    bus.publish("ingest", {"record_id": "1"})
    assert len(received) == 1
    assert received[0].topic == "ingest"
    assert received[0].payload["record_id"] == "1"


def test_event_bus_multiple_subscribers() -> None:
    a, b = [], []

    bus = EventBus()
    bus.subscribe("metrics", lambda e: a.append(e))
    bus.subscribe("metrics", lambda e: b.append(e))
    bus.publish("metrics", {"cpu": 0.5})
    assert len(a) == 1
    assert len(b) == 1


def test_event_bus_topic_isolation() -> None:
    received = []
    bus = EventBus()
    bus.subscribe("alpha", lambda e: received.append(e))
    bus.publish("beta")
    assert received == []


def test_event_bus_empty_payload() -> None:
    received = []
    bus = EventBus()
    bus.subscribe("ping", lambda e: received.append(e))
    bus.publish("ping")
    assert received[0].payload == {}
