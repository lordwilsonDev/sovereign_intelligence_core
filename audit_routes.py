import sys, traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from msb_v2.api.web import _ROUTER_REGISTRY, _load_routers

_load_routers()
app = FastAPI()
report = []

for idx, entry in enumerate(_ROUTER_REGISTRY):
    item = {
        "index": idx,
        "entry": repr(entry)[:200],
        "mount": "NOT_ATTEMPTED",
        "exception": None,
    }
    router_obj, prefix = entry
    item["entry"] = repr((type(router_obj).__name__, prefix))[:200]
    try:
        before = len(app.routes)
        app.include_router(router_obj, prefix=prefix)
        after = len(app.routes)
        item["mount"] = f"OK (+{after - before} routes)"
    except Exception as e:
        item["mount"] = "FAILED"
        item["exception"] = traceback.format_exc()
    report.append(item)

mounted = sum(1 for r in report if "OK" in r["mount"])
failed  = sum(1 for r in report if r["mount"] == "FAILED")
print(f"Registry entries: {len(_ROUTER_REGISTRY)} | Mounted: {mounted} | Failed: {failed}\n")
for r in report:
    if r["mount"] != "OK (+0 routes)" or "FAILED" in r["mount"]:
        print(f"[{r['index']}] {r['entry']}")
        print(f"  -> {r['mount']}")
        if r["exception"]:
            print(r["exception"][:300])
        print()
