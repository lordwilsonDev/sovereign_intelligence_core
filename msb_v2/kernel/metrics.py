"""Prometheus metrics for KB4 kernel invocations."""

from __future__ import annotations

from prometheus_client import Gauge

KB4_CYCLES_TOTAL = Gauge(
    "msb_kb4_cycles_total",
    "Total KB4 kernel run invocations",
)

KB4_MUTATIONS_TOTAL = Gauge(
    "msb_kb4_mutations_total",
    "Total KB4 mutation/Ouroboros events emitted",
)

KB4_VETOES_TOTAL = Gauge(
    "msb_kb4_vetoes_total",
    "Total high-risk intents vetoed by KB4",
)
