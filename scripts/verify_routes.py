from __future__ import annotations

import sys
from collections import defaultdict

from msb_v2.api.web import create_app, _ROUTER_REGISTRY
from starlette.routing import Mount, Route


def main() -> int:
    app = create_app()
    effective = []
    for route in app.routes:
        if isinstance(route, Mount):
            for child in getattr(route.app, "routes", []):
                if isinstance(child, Route):
                    effective.append(route.path + child.path)
        elif isinstance(route, Route):
            effective.append(route.path)

    by_path = defaultdict(list)
    for path in effective:
        by_path[path].append(path)

    dups = {path: hits for path, hits in by_path.items() if len(hits) > 1}
    if dups:
        print("Duplicate effective routes detected:")
        for path, hits in sorted(dups.items()):
            print(f"  {path} -> {len(hits)} mounts")
        return 1
    print(f"Route audit passed: {len(effective)} effective routes, 0 duplicates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
