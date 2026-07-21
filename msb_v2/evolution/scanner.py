from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from msb_v2.evolution.memory import EvolutionMemory

from msb_v2.evolution.proposal import EvolutionProposal


class OuroborosScanner:
    def __init__(self, root: Path) -> None:
        self.root = root

    def scan(self) -> Dict[str, Any]:
        hotspots = self._complexity_hotspots()
        duplication = self._duplication_signals()
        dead = self._dead_symbols()
        return {
            "hotspots": hotspots,
            "duplication": duplication,
            "dead_symbols": dead,
            "proposal_count": len(hotspots) + len(duplication) + len(dead),
        }

    def _complexity_hotspots(self) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for path in self.root.rglob("*.py"):
            try:
                text = path.read_text(encoding="utf-8")
                tree = ast.parse(text)
            except Exception:
                continue
            funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            for func in funcs:
                loc = self._func_loc(text, func)
                complexity = self._cyclomatic(func)
                if complexity >= 10 or loc >= 120:
                    results.append(
                        {
                            "file": str(path.relative_to(self.root)),
                            "function": func.name,
                            "complexity": complexity,
                            "loc": loc,
                        }
                    )
        return results

    def _duplication_signals(self) -> List[Dict[str, Any]]:
        signals: List[Dict[str, Any]] = []
        buckets: Dict[str, List[str]] = {}
        for path in self.root.rglob("*.py"):
            try:
                text = path.read_text(encoding="utf-8")
                lines = [line.strip() for line in text.splitlines() if line.strip()]
            except Exception:
                continue
            for line in lines:
                if len(line) < 40:
                    continue
                digest = hashlib.md5(line.encode("utf-8")).hexdigest()
                buckets.setdefault(digest, []).append(str(path))
        for digest, files in buckets.items():
            if len(files) >= 2:
                signals.append({"digest": digest, "count": len(files), "files": files})
        return signals[:20]

    def _dead_symbols(self) -> List[Dict[str, Any]]:
        dead: List[Dict[str, Any]] = []
        for path in self.root.rglob("*.py"):
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            for line in text.splitlines():
                if line.strip().startswith("def ") or line.strip().startswith("class "):
                    symbol = line.strip().split("(")[0].split(" ")[-1]
                    if symbol.startswith("_"):
                        continue
                    usages = text.count(symbol)
                    if usages == 1:
                        dead.append({"file": str(path.relative_to(self.root)), "symbol": symbol})
        return dead[:20]

    def propose(self, proposal_id: str, title: str, affected_modules: List[str], rationale: str, risk: str = "medium", memory: Optional[EvolutionMemory] = None) -> EvolutionProposal:
        payload = {
            "proposal_id": proposal_id,
            "title": title,
            "affected_modules": affected_modules,
            "rationale": rationale,
            "risk": risk,
        }
        memory_fingerprint = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()
        memory_target = affected_modules[0] if affected_modules else ""
        if memory is not None:
            if memory.should_skip(memory_target, memory_fingerprint):
                return EvolutionProposal(
                    proposal_id=proposal_id,
                    title=title,
                    affected_modules=affected_modules,
                    rationale=rationale,
                    risk=risk,
                    status="skipped",
                    failure_reason="blocked_by_evolution_memory",
                    rollback_ref="evolution_memory",
                )
        scan = self.scan()
        rationale_text = f"{rationale}\n\nScanner findings:\n{json.dumps(scan, indent=2)}"
        proposal = EvolutionProposal(
            proposal_id=proposal_id,
            title=title,
            affected_modules=affected_modules,
            rationale=rationale_text,
            risk=risk,
        )
        proposal.fingerprint = memory_fingerprint
        proposal.target = memory_target
        return proposal

    @staticmethod
    def _func_loc(text: str, node: ast.AST) -> int:
        start = getattr(node, "lineno", 0)
        end = getattr(node, "end_lineno", start)
        return max(1, end - start + 1)

    @staticmethod
    def _cyclomatic(node: ast.AST) -> int:
        branches = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.Assert, ast.BoolOp)):
                branches += 1
        return branches


OuroborosScanner = OuroborosScanner
