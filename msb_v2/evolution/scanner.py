from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

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

    def propose(self, proposal_id: str, title: str, affected_modules: List[str], rationale: str, risk: str = "medium") -> EvolutionProposal:
        scan = self.scan()
        return EvolutionProposal(
            proposal_id=proposal_id,
            title=title,
            affected_modules=affected_modules,
            rationale=f"{rationale}\n\nScanner findings:\n{json.dumps(scan, indent=2)}",
            risk=risk,
        )

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
