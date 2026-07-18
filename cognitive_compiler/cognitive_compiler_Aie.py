import json, re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable

SCHEMA_PATH = Path(__file__).with_name('axiom_schema.nano')

class Severity(str):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'

@dataclass(frozen=True)
class Violation:
    axiom_id: str
    severity: str
    message: str
    offending_node: str
    repair_hint: str
    context: dict = None  # type: ignore[assignment]

    def __post_init__(self):
        if self.context is None:
            object.__setattr__(self, 'context', {})

class AxiomEvaluator:
    def __init__(self, schema_path: str | None = None):
        with open(schema_path or SCHEMA_PATH, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)
        self.axioms = {a['id']: a for a in self.schema.get('axioms', [])}

    def evaluate(self, asg: dict[str, Any], context: dict | None = None) -> list[Violation]:
        ctx = context or {}
        context_name = ctx.get('context', 'production')
        results: list[Violation] = []

        # Delegate to specialized checkers
        results.extend(self._check_idempotency(asg, context_name))
        results.extend(self._check_symbolic_stability(asg, context_name))
        results.extend(self._check_observability(asg, context_name))
        results.extend(self._check_config_integrity(asg, context_name))

        # Contradiction amplification
        failing_ids = frozenset(v.axiom_id for v in results)
        if {'IDEMPOTENCY', 'OBSERVABILITY'}.issubset(failing_ids):
            results = [replace(v, severity=Severity.CRITICAL) if v.severity != Severity.CRITICAL else v for v in results]
        if {'SYMBOLIC_STABILITY', 'CONFIG_INTEGRITY'}.issubset(failing_ids):
            results = [replace(v, severity=Severity.CRITICAL) if v.severity != Severity.CRITICAL else v for v in results]

        return results

    def _severity_for(self, axiom_id: str, context_name: str) -> str:
        axiom = self.axioms.get(axiom_id, {})
        return axiom.get('severity', 'MEDIUM')

    def _weight(self, axiom: dict, context: str) -> float:
        weights = axiom.get('context_weights', {})
        if context == 'hot_reload':
            return float(weights.get('hot_reload', weights.get('production', 1.0)))
        return float(weights.get('production', 1.0))

    def _check_idempotency(self, asg, context_name) -> Iterable[Violation]:
        axiom = self.axioms.get('IDEMPOTENCY', {})
        weight = self._weight(axiom, context_name)
        sev = self._severity_for('IDEMPOTENCY', context_name)
        for node in asg.get('init_bodies', []):
            if re.search(r'NetworkRequest|FileIO|UserDefaults|URLSession|FileManager', str(node), re.IGNORECASE):
                yield Violation(
                    axiom_id='IDEMPOTENCY', severity=sev,
                    message=f'Network/FileIO/UserDefaults in init: {node}', offending_node=str(node),
                    repair_hint=axiom.get('repair_hint', ''), context={'weight': weight},
                )

    def _check_symbolic_stability(self, asg, context_name) -> Iterable[Violation]:
        axiom = self.axioms.get('SYMBOLIC_STABILITY', {})
        sev = self._severity_for('SYMBOLIC_STABILITY', context_name)
        for sym in asg.get('dlsyms', []):
            sym = str(sym)
            if not re.match(r'^_\$s.*', sym):
                yield Violation(
                    axiom_id='SYMBOLIC_STABILITY', severity=sev,
                    message=f'Non-mangled dylib symbol: {sym}', offending_node=sym,
                    repair_hint=axiom.get('repair_hint', ''), context={},
                )

    def _check_observability(self, asg, context_name) -> Iterable[Violation]:
        axiom = self.axioms.get('OBSERVABILITY', {})
        sev = self._severity_for('OBSERVABILITY', context_name)
        for wrap in asg.get('state_wrappers', []):
            base = (wrap or {}).get('base', '')
            if wrap.get('type') == '@State' and base not in ('StateObject', 'ObservedObject'):
                yield Violation(
                    axiom_id='OBSERVABILITY', severity=sev,
                    message=f'Raw @State without observable wrapper: {wrap}', offending_node=json.dumps(wrap),
                    repair_hint=axiom.get('repair_hint', ''), context={},
                )

    def _check_config_integrity(self, asg, context_name) -> Iterable[Violation]:
        axiom = self.axioms.get('CONFIG_INTEGRITY', {})
        sev = self._severity_for('CONFIG_INTEGRITY', context_name)
        ld_flags = str(asg.get('ld_flags') or '')
        only_default = ld_flags in ('', '-Xlinker -interposable')
        if '-Xlinker' not in ld_flags or '-interposable' not in ld_flags:
            yield Violation(
                axiom_id='CONFIG_INTEGRITY', severity=sev,
                message='OTHER_LDFLAGS missing -Xlinker -interposable',
                offending_node=ld_flags, repair_hint=axiom.get('repair_hint', ''), context={},
            )

    def render_repair_directives(self, violations: list[Violation]) -> list[dict[str, Any]]:
        return [
            {
                'violated_axiom': v.axiom_id,
                'offending_node': v.offending_node,
                'suggested_fix': v.repair_hint,
                'priority': 1 if v.severity == Severity.CRITICAL else 2,
            }
            for v in violations
        ]
