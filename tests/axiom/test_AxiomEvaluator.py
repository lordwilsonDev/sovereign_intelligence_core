import json
from pathlib import Path
from cognitive_compiler.cognitive_compiler_Aie import AxiomEvaluator, Severity

DATASET = Path(__file__).resolve().parent.parent / 'axiom' / 'ground_truth_dataset.json'
EVAL = AxiomEvaluator()

class TestAxiomEvaluator:
    def test_dataset_integrity(self):
        with open(DATASET, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert len(data) >= 24
        ids = [c['id'] for c in data]
        assert len(ids) == len(set(ids))

    def test_evaluator_matches_expected_severity(self):
        with open(DATASET, 'r', encoding='utf-8') as f:
            data = json.load(f)

        mismatches = []
        for case in data:
            asg = case['asg']
            violations = EVAL.evaluate(asg, context={'context': 'production'})
            expected = case['expected_severity']
            if expected == 'PASS':
                actual_names = [v.axiom_id for v in violations]
                if actual_names:
                    mismatches.append(f"{case['id']}: expected PASS, got {actual_names}")
            else:
                actuals = {v.severity for v in violations}
                if expected not in actuals:
                    mismatches.append(f"{case['id']}: expected {expected}, got {actuals}")

        assert len(mismatches) == 0, f"{len(mismatches)} mismatches:\n" + "\n".join(mismatches)

    def test_repair_directives_populated_on_violations(self):
        with open(DATASET, 'r', encoding='utf-8') as f:
            data = json.load(f)
        directive_cases = [c for c in data if c['expected_severity'] not in ('PASS',)]
        total_directives = 0
        for case in directive_cases:
            viols = EVAL.evaluate(case['asg'], context={'context': 'production'})
            if not viols:
                continue
            total_directives += len(viols)
            directives = EVAL.render_repair_directives(viols)
            for d in directives:
                assert d['suggested_fix'], f"{case['id']} missing repair_hint"
                assert d['priority'] in (1, 2)
        assert total_directives > 0

    def test_contradiction_matrix_amplification(self):
        asg = {
            'init_bodies': ['URLSession.shared.dataTask(with: URL(string:"https://x")!).resume()'],
            'dlsyms': ['customSym'],
            'state_wrappers': [{ 'type': '@State', 'base': 'Foo' }],
            'ld_flags': '-Xlinker -other',
        }
        viols = EVAL.evaluate(asg, context={'context': 'production'})
        sevs = {v.severity for v in viols}
        assert Severity.CRITICAL in sevs

    def test_sovereign_decide_boundary(self):
        from sovereign_validator import _decide
        from cognitive_compiler.cognitive_compiler_Aie import Violation, Severity
        dummy = Violation('X', Severity.CRITICAL, '', '', '')
        assert _decide([dummy]) == 'BLOCK'
        assert _decide([]) == 'ALLOW'
