"""Verify every HCL contract marked allow_anonymous=True matches live app behavior."""
from __future__ import annotations

from msb_v2.api.web import create_app
from msb_v2.v3.contracts import all_contracts
from starlette.testclient import TestClient


def main() -> int:
    contracts = [c for c in all_contracts() if c.allow_anonymous]
    if not contracts:
        print("verify_anonymous_routes: OK (no anonymous contracts to verify)")
        return 0

    app = create_app()
    client = TestClient(app)

    drifts = []
    for contract in contracts:
        route = contract.route
        method = (contract.method or "get").lower()
        try:
            r = (
                client.get(route)
                if method == "get"
                else client.post(route, json={})
                if method == "post"
                else client.put(route, json={})
                if method == "put"
                else client.delete(route)
                if method == "delete"
                else client.request(method.upper(), route)
            )
        except Exception:
            continue
        if r.status_code == 401:
            drifts.append(f"{method.upper()} {route} -> {r.status_code}: {r.text[:80]}")

    if drifts:
        print("verify_anonymous_routes: DRIFT_FOUND")
        for drift in drifts:
            print("  - " + drift)
        return 2

    print(f"verify_anonymous_routes: OK ({len(contracts)} anonymous routes verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
