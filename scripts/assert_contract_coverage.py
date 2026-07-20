from __future__ import annotations

import sys
from typing import Any

from msb_v2.api.web import create_app
from msb_v2.v3.contracts import lookup, all_contracts


def route_key(route: Any) -> tuple[str, str]:
    path = getattr(route, 'path', '')
    methods = sorted(method.upper() for method in getattr(route, 'methods', []) or [])
    return path, ','.join(methods)


def collect_routes(app: Any) -> list[Any]:
    routes: list[Any] = []
    for route in getattr(app, 'routes', []):
        if hasattr(route, 'app'):
            routes.extend(collect_routes(route.app))
        elif hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append(route)
    return routes


def main() -> int:
    app = create_app()
    doc_paths = {'/openapi.json', '/docs', '/docs/oauth2-redirect', '/redoc'}
    routes = [route for route in collect_routes(app) if route_key(route)[0] not in doc_paths]
    missing = []
    for route in routes:
        path, methods = route_key(route)
        if not methods:
            continue
        for method in methods.split(','):
            if lookup(path, method) is None:
                missing.append((path, method))
    if missing:
        print('Uncontracted routes detected:')
        for path, method in missing:
            print(f'  {method} {path}')
        print(f'Total: {len(missing)} uncontracted route(s); registered contracts: {len(all_contracts())}')
        return 1
    print(f'Contract coverage passed: {len(routes)} routes, {len(all_contracts())} contracts, 0 uncovered')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
