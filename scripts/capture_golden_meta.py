import json, sys
sys.path.insert(0, '/Users/lordwilson/msb-v2')
from cognitive_compiler.meta_router_v2 import MetaRoutingHarness

router = MetaRoutingHarness()
golden = []

scenarios = [
    {"primary": "desktop", "secondary": "building", "query": "open app and build api"},
    {"primary": "building", "secondary": "desktop", "query": "architect system and click UI"},
    {"primary": "desktop", "secondary": "research", "query": "launch browser and study market"},
    {"primary": "research", "secondary": "desktop", "query": "investigate and open app"},
    {"primary": "desktop", "secondary": "complex_reasoning", "query": "automate UI and ethics strategy"},
    {"primary": "research", "secondary": "complex_reasoning", "query": "hypothesis and paradox"},
    {"primary": "building", "secondary": "complex_reasoning", "query": "plan system and concept"},
    {"primary": "desktop", "secondary": "telegram", "query": "screenshot and send widget"},
    {"primary": "telegram", "secondary": "desktop", "query": "chart and launch app"},
    {"primary": "telegram", "secondary": "research", "query": "html and experiment"},
    {"primary": "research", "secondary": "telegram", "query": "study and send webapp"},
    {"primary": "telegram", "secondary": "building", "query": "recipe and design api"},
    {"primary": "building", "secondary": "telegram", "query": "build system and send html"},
    {"primary": "code", "secondary": "data", "query": "generate code and analyze csv"},
    {"primary": "career", "secondary": "building", "query": "cv and build system"},
    {"primary": "telegram", "secondary": "career", "query": "telegram artifact and evaluate offer"},
    {"primary": "career", "secondary": "telegram", "query": "scan job and send widget"},
    {"primary": "backend", "secondary": "frontend", "query": "design microservice and dashboard"},
]

for s in scenarios:
    order = router._determine_order(s["primary"], s["secondary"], s["query"])
    golden.append({"input": s, "output": order})

with open('/Users/lordwilson/msb-v2/golden_meta.json', 'w') as f:
    json.dump(golden, f, indent=2)
print(f"Captured {len(golden)} golden samples.")
