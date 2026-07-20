from __future__ import annotations

import sys

from msb_v2.api.web import create_app
from msb_v2.v3.contracts import lookup


def test_no_uncontracted_routes():
    doc_paths = {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}

    def collect_routes(app):
        routes = []
        for route in getattr(app, "routes", []):
            if hasattr(route, "app"):
                routes.extend(collect_routes(route.app))
            elif hasattr(route, "path") and hasattr(route, "methods"):
                routes.append(route)
        return routes

    app = create_app()
    routes = [route for route in collect_routes(app) if route.path not in doc_paths]
    missing = []
    for route in routes:
        methods = sorted(method.upper() for method in getattr(route, "methods", []) or [])
        for method in methods:
            if not method:
                continue
            if lookup(route.path, method) is None:
                missing.append((method, route.path))
    assert not missing, missing