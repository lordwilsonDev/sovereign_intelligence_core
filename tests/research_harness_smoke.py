import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cognitive_compiler.research_harness_v1 import ResearchHarness

harness = ResearchHarness()
out = harness.execute("Why do some adaptive systems outperform static ones by ~25% under variable load?")
print("EXECUTED")
print("assumptions:", len(out['assumptions']))
print("evidence items:", len(out['evidence']))
print("hypotheses:", len(out['hypotheses']))
print("experiments:", len(out['experiments']))
print("risks:", len(out['risks']))
print("confidence:", out['overall_confidence'])
print("elapsed_s:", out['elapsed_s'])
