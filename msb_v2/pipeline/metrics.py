"""Prometheus metrics for sovereign pipeline stages."""

from __future__ import annotations

from prometheus_client import Gauge

PIPELINE_SAS_AVERAGE = Gauge(
    "msb_pipeline_sas_average",
    "Average Sovereignty Autonomy Score for pipeline artifacts",
    ["stage"],
)

PIPELINE_FTS_AVERAGE = Gauge(
    "msb_pipeline_fts_average",
    "Average Falsification Theatricality Score for pipeline artifacts",
    ["stage"],
)

PIPELINE_DECISIONS_TOTAL = Gauge(
    "msb_pipeline_decisions_total",
    "Total pipeline sovereignty gate decisions",
    ["verdict"],
)
