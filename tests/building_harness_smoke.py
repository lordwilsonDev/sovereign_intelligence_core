import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cognitive_compiler.building_harness_v1 import BuildingHarness

harness = BuildingHarness()
out = harness.execute(
    goal="Design a REST API that stores user state and must scale to 10k RPS within 6 months.",
    constraints=["budget: 2 engineers", "must be observable"]
)
print("EXECUTED")
print("reqs:", len(out['requirements']))
print("concepts:", len(out['concepts']))
print("risks:", len(out['risks']))
print("confidence:", out['plan']['confidence'])
print("elapsed_s:", out['elapsed_s'])
