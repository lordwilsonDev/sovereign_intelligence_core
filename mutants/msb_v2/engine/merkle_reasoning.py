from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


@dataclass
class MerkleStep:
    step_id: str
    step_type: str
    payload: dict[str, Any]
    prev_hash: str = ""
    step_hash: str = ""
    timestamp: str = ""
mutants_xǁMerkleReasoningChainǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁMerkleReasoningChainǁappend__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut: MutantDict = {}  # type: ignore
mutants_xǁMerkleReasoningChainǁverify__mutmut: MutantDict = {}  # type: ignore


class MerkleReasoningChain:
    @_mutmut_mutated(mutants_xǁMerkleReasoningChainǁ__init____mutmut)
    def __init__(self) -> None:
        self.chain: list[MerkleStep] = []
        self._root_hash = ""
    def xǁMerkleReasoningChainǁ__init____mutmut_orig(self) -> None:
        self.chain: list[MerkleStep] = []
        self._root_hash = ""
    def xǁMerkleReasoningChainǁ__init____mutmut_1(self) -> None:
        self.chain: list[MerkleStep] = None
        self._root_hash = ""
    def xǁMerkleReasoningChainǁ__init____mutmut_2(self) -> None:
        self.chain: list[MerkleStep] = []
        self._root_hash = None
    def xǁMerkleReasoningChainǁ__init____mutmut_3(self) -> None:
        self.chain: list[MerkleStep] = []
        self._root_hash = "XXXX"

    @_mutmut_mutated(mutants_xǁMerkleReasoningChainǁappend__mutmut)
    def append(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_orig(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_1(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = None
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_2(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = None
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_3(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps(None)
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_4(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"XXstep_typeXX": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_5(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"STEP_TYPE": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_6(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "XXpayloadXX": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_7(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "PAYLOAD": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_8(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "XXprevXX": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_9(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "PREV": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_10(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = None
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_11(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(None).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_12(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode(None)).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_13(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("XXutf-8XX")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_14(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("UTF-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_15(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = None
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_16(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=None,
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_17(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=None,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_18(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=None,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_19(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=None,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_20(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=None,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_21(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=None,
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_22(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_23(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_24(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_25(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_26(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_27(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_28(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain) - 1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_29(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+2}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_30(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(None).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_31(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(None)
        self._root_hash = step_hash
        return step

    def xǁMerkleReasoningChainǁappend__mutmut_32(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = None
        return step

    def root_hash(self) -> str:
        return self._root_hash

    @_mutmut_mutated(mutants_xǁMerkleReasoningChainǁsnapshot__mutmut)
    def snapshot(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_orig(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_1(self, label: str) -> dict[str, Any]:
        return {
            "XXlabelXX": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_2(self, label: str) -> dict[str, Any]:
        return {
            "LABEL": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_3(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "XXrootXX": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_4(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "ROOT": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_5(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "XXlenXX": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_6(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "LEN": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_7(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "XXstepsXX": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_8(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "STEPS": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_9(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "XXstep_idXX": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_10(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "STEP_ID": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_11(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "XXstep_typeXX": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_12(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "STEP_TYPE": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_13(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "XXprev_hashXX": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_14(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "PREV_HASH": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_15(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "XXstep_hashXX": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_16(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "STEP_HASH": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_17(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "XXtsXX": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def xǁMerkleReasoningChainǁsnapshot__mutmut_18(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "TS": s.timestamp,
                }
                for s in self.chain
            ],
        }

    @_mutmut_mutated(mutants_xǁMerkleReasoningChainǁverify__mutmut)
    def verify(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_orig(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_1(self) -> bool:
        expected = None
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_2(self) -> bool:
        expected = "XXXX"
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_3(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = None
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_4(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps(None)
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_5(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"XXstep_typeXX": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_6(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"STEP_TYPE": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_7(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "XXpayloadXX": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_8(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "PAYLOAD": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_9(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "XXprevXX": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_10(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "PREV": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_11(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = None
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_12(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(None).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_13(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode(None)).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_14(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("XXutf-8XX")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_15(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("UTF-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_16(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash == calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_17(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return True
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_18(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected or expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_19(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash == expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_20(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected == "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_21(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "XXXX":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_22(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return True
            expected = s.step_hash
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_23(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = None
        self._root_hash = expected
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_24(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = None
        return True

    def xǁMerkleReasoningChainǁverify__mutmut_25(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return False

mutants_xǁMerkleReasoningChainǁ__init____mutmut['_mutmut_orig'] = MerkleReasoningChain.xǁMerkleReasoningChainǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁ__init____mutmut['xǁMerkleReasoningChainǁ__init____mutmut_1'] = MerkleReasoningChain.xǁMerkleReasoningChainǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁ__init____mutmut['xǁMerkleReasoningChainǁ__init____mutmut_2'] = MerkleReasoningChain.xǁMerkleReasoningChainǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁ__init____mutmut['xǁMerkleReasoningChainǁ__init____mutmut_3'] = MerkleReasoningChain.xǁMerkleReasoningChainǁ__init____mutmut_3 # type: ignore # mutmut generated

mutants_xǁMerkleReasoningChainǁappend__mutmut['_mutmut_orig'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_1'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_2'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_3'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_4'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_5'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_6'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_7'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_8'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_9'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_10'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_11'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_12'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_13'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_14'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_15'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_16'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_17'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_17 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_18'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_18 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_19'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_19 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_20'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_20 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_21'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_21 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_22'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_22 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_23'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_23 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_24'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_24 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_25'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_25 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_26'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_26 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_27'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_27 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_28'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_28 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_29'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_29 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_30'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_30 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_31'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_31 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁappend__mutmut['xǁMerkleReasoningChainǁappend__mutmut_32'] = MerkleReasoningChain.xǁMerkleReasoningChainǁappend__mutmut_32 # type: ignore # mutmut generated

mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['_mutmut_orig'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_1'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_2'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_3'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_4'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_5'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_6'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_7'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_8'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_9'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_10'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_11'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_12'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_13'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_14'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_15'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_16'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_17'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_17 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁsnapshot__mutmut['xǁMerkleReasoningChainǁsnapshot__mutmut_18'] = MerkleReasoningChain.xǁMerkleReasoningChainǁsnapshot__mutmut_18 # type: ignore # mutmut generated

mutants_xǁMerkleReasoningChainǁverify__mutmut['_mutmut_orig'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_orig # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_1'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_1 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_2'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_2 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_3'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_3 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_4'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_4 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_5'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_5 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_6'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_6 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_7'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_7 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_8'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_8 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_9'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_9 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_10'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_10 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_11'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_11 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_12'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_12 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_13'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_13 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_14'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_14 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_15'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_15 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_16'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_16 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_17'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_17 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_18'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_18 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_19'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_19 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_20'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_20 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_21'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_21 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_22'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_22 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_23'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_23 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_24'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_24 # type: ignore # mutmut generated
mutants_xǁMerkleReasoningChainǁverify__mutmut['xǁMerkleReasoningChainǁverify__mutmut_25'] = MerkleReasoningChain.xǁMerkleReasoningChainǁverify__mutmut_25 # type: ignore # mutmut generated
mutants_x_json_dumps__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_json_dumps__mutmut)
def json_dumps(obj: Any) -> str:
    import json
    return json.dumps(obj, sort_keys=True, default=str)


def x_json_dumps__mutmut_orig(obj: Any) -> str:
    import json
    return json.dumps(obj, sort_keys=True, default=str)


def x_json_dumps__mutmut_1(obj: Any) -> str:
    import json
    return json.dumps(None, sort_keys=True, default=str)


def x_json_dumps__mutmut_2(obj: Any) -> str:
    import json
    return json.dumps(obj, sort_keys=None, default=str)


def x_json_dumps__mutmut_3(obj: Any) -> str:
    import json
    return json.dumps(obj, sort_keys=True, default=None)


def x_json_dumps__mutmut_4(obj: Any) -> str:
    import json
    return json.dumps(sort_keys=True, default=str)


def x_json_dumps__mutmut_5(obj: Any) -> str:
    import json
    return json.dumps(obj, default=str)


def x_json_dumps__mutmut_6(obj: Any) -> str:
    import json
    return json.dumps(obj, sort_keys=True, )


def x_json_dumps__mutmut_7(obj: Any) -> str:
    import json
    return json.dumps(obj, sort_keys=False, default=str)

mutants_x_json_dumps__mutmut['_mutmut_orig'] = x_json_dumps__mutmut_orig # type: ignore # mutmut generated
mutants_x_json_dumps__mutmut['x_json_dumps__mutmut_1'] = x_json_dumps__mutmut_1 # type: ignore # mutmut generated
mutants_x_json_dumps__mutmut['x_json_dumps__mutmut_2'] = x_json_dumps__mutmut_2 # type: ignore # mutmut generated
mutants_x_json_dumps__mutmut['x_json_dumps__mutmut_3'] = x_json_dumps__mutmut_3 # type: ignore # mutmut generated
mutants_x_json_dumps__mutmut['x_json_dumps__mutmut_4'] = x_json_dumps__mutmut_4 # type: ignore # mutmut generated
mutants_x_json_dumps__mutmut['x_json_dumps__mutmut_5'] = x_json_dumps__mutmut_5 # type: ignore # mutmut generated
mutants_x_json_dumps__mutmut['x_json_dumps__mutmut_6'] = x_json_dumps__mutmut_6 # type: ignore # mutmut generated
mutants_x_json_dumps__mutmut['x_json_dumps__mutmut_7'] = x_json_dumps__mutmut_7 # type: ignore # mutmut generated
