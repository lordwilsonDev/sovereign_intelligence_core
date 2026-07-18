from __future__ import annotations

import pytest

from msb_v2.planning.planner import create_plan, plan_from_json, plan_to_json, replan


def test_create_plan_weather() -> None:
    p = create_plan("What is the weather in Paris?")
    assert p.steps[0].tool == "weather_report"
    assert p.steps[0].parameters["city"] == ""


def test_create_plan_web_search() -> None:
    p = create_plan("search current Bitcoin price")
    assert p.steps[0].tool == "web_search"
    assert "Bitcoin" in p.steps[0].parameters["query"]


def test_create_plan_fallback() -> None:
    p = create_plan("unknown elaborate task with no keywords")
    assert p.steps[0].tool == "web_search"


def test_replan_after_search_failure() -> None:
    p = replan("retry search", [], {"tool": "web_search"}, "timeout")
    assert p.steps[0].tool == "web_search"


def test_plan_roundtrip() -> None:
    p = create_plan("open Spotify")
    data = plan_to_json(p)
    q = plan_from_json(data)
    assert q.goal == p.goal
    assert q.steps[0].tool == p.steps[0].tool
