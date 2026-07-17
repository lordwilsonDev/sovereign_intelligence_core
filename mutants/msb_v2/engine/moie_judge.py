from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Sequence

from msb_v2.engine.moie_types import Claim, DebateRound
from msb_v2.engine.rcoh_persistence import RCOHPersistence


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁJudgeǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁJudgeǁsynthesize__mutmut: MutantDict = {}  # type: ignore
mutants_xǁJudgeǁ_claim_to_dict__mutmut: MutantDict = {}  # type: ignore
mutants_xǁJudgeǁ_build_consensus__mutmut: MutantDict = {}  # type: ignore


class Judge:
    """Synthesize broadcast debate transcript into validated judgment."""

    @_mutmut_mutated(mutants_xǁJudgeǁ__init____mutmut)
    def __init__(self, persistence: RCOHPersistence | None = None) -> None:
        self._persistence = persistence

    def xǁJudgeǁ__init____mutmut_orig(self, persistence: RCOHPersistence | None = None) -> None:
        self._persistence = persistence

    def xǁJudgeǁ__init____mutmut_1(self, persistence: RCOHPersistence | None = None) -> None:
        self._persistence = None

    @_mutmut_mutated(mutants_xǁJudgeǁsynthesize__mutmut)
    def synthesize(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_orig(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_1(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = None
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_2(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(None)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_3(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "XX\nXX".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_4(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = None
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_5(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" - hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_6(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "XXsha256:XX" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_7(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "SHA256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_8(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(None).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_9(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode(None)).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_10(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("XXutf-8XX")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_11(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("UTF-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_12(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = None
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_13(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = None
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_14(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = None

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_15(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = None
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_16(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] = 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_17(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] -= 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_18(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(None, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_19(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, None)[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_20(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_21(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, )[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_22(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 2

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_23(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = None
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_24(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(None, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_25(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, None)
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_26(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_27(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, )
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_28(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = None
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_29(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get(None, 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_30(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", None)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_31(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get(0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_32(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", )
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_33(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("XXsupportXX", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_34(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("SUPPORT", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_35(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 1)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_36(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = None
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_37(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get(None, 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_38(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", None)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_39(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get(0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_40(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", )
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_41(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("XXrejectXX", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_42(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("REJECT", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_43(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 1)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_44(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = None
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_45(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get(None, 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_46(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", None)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_47(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get(0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_48(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", )
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_49(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("XXrefineXX", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_50(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("REFINE", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_51(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 1)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_52(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject or support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_53(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support >= reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_54(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support > refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_55(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(None)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_56(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = None
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_57(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "XXvalidatedXX"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_58(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "VALIDATED"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_59(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support or reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_60(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject > support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_61(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject > refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_62(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(None)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_63(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = None
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_64(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "XXrejectedXX"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_65(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "REJECTED"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_66(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(None)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_67(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = None

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_68(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "XXinconclusiveXX"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_69(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "INCONCLUSIVE"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_70(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = None
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_71(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(None)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_72(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = None
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_73(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(None)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_74(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(2)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_75(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[1][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_76(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][1] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_77(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "XXinconclusiveXX"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_78(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "INCONCLUSIVE"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_79(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = None

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_80(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "XXhighXX" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_81(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "HIGH" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_82(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) > len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_83(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) / 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_84(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 3 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_85(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("XXmediumXX" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_86(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("MEDIUM" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_87(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "XXlowXX")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_88(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "LOW")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_89(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = None

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_90(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "XXqueryXX": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_91(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "QUERY": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_92(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "XXclaimsXX": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_93(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "CLAIMS": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_94(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(None) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_95(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "XXtranscript_hashXX": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_96(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "TRANSCRIPT_HASH": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_97(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "XXvalidatedXX": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_98(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "VALIDATED": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_99(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "XXrejectedXX": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_100(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "REJECTED": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_101(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "XXinconclusiveXX": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_102(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "INCONCLUSIVE": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_103(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "XXconsensus_statementXX": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_104(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "CONSENSUS_STATEMENT": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_105(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(None, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_106(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, None, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_107(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, None),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_108(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_109(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_110(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, ),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_111(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "XXanomaly_scoreXX": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_112(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "ANOMALY_SCORE": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_113(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round(None, 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_114(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), None),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_115(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round(4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_116(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), ),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_117(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) * max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_118(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 - len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_119(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) / 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_120(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 1.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_121(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) / 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_122(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 1.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_123(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(None, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_124(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, None), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_125(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_126(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, ), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_127(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(2, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_128(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 5),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_129(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "XXbreakthrough_potentialXX": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_130(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "BREAKTHROUGH_POTENTIAL": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_131(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "XXtimestampXX": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_132(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "TIMESTAMP": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_133(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(None).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_134(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_135(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact(None, f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_136(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", None, judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_137(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", None)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_138(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact(f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_139(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_140(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", )
        return judgment

    def xǁJudgeǁsynthesize__mutmut_141(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("XXmoieXX", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_142(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("MOIE", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    def xǁJudgeǁsynthesize__mutmut_143(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:51]}/judgment", judgment)
        return judgment

    @staticmethod
    @_mutmut_mutated(mutants_xǁJudgeǁ_claim_to_dict__mutmut)
    def _claim_to_dict(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "text": claim.text,
            "source": claim.source,
            "inversion_of": claim.inversion_of,
            "scores": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_orig(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "text": claim.text,
            "source": claim.source,
            "inversion_of": claim.inversion_of,
            "scores": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_1(claim: Claim) -> Dict[str, Any]:
        return {
            "XXidXX": claim.id,
            "text": claim.text,
            "source": claim.source,
            "inversion_of": claim.inversion_of,
            "scores": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_2(claim: Claim) -> Dict[str, Any]:
        return {
            "ID": claim.id,
            "text": claim.text,
            "source": claim.source,
            "inversion_of": claim.inversion_of,
            "scores": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_3(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "XXtextXX": claim.text,
            "source": claim.source,
            "inversion_of": claim.inversion_of,
            "scores": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_4(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "TEXT": claim.text,
            "source": claim.source,
            "inversion_of": claim.inversion_of,
            "scores": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_5(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "text": claim.text,
            "XXsourceXX": claim.source,
            "inversion_of": claim.inversion_of,
            "scores": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_6(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "text": claim.text,
            "SOURCE": claim.source,
            "inversion_of": claim.inversion_of,
            "scores": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_7(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "text": claim.text,
            "source": claim.source,
            "XXinversion_ofXX": claim.inversion_of,
            "scores": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_8(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "text": claim.text,
            "source": claim.source,
            "INVERSION_OF": claim.inversion_of,
            "scores": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_9(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "text": claim.text,
            "source": claim.source,
            "inversion_of": claim.inversion_of,
            "XXscoresXX": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_10(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "text": claim.text,
            "source": claim.source,
            "inversion_of": claim.inversion_of,
            "SCORES": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_11(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "text": claim.text,
            "source": claim.source,
            "inversion_of": claim.inversion_of,
            "scores": claim.scores,
            "XXstatusXX": claim.status,
        }

    @staticmethod
    def xǁJudgeǁ_claim_to_dict__mutmut_12(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "text": claim.text,
            "source": claim.source,
            "inversion_of": claim.inversion_of,
            "scores": claim.scores,
            "STATUS": claim.status,
        }

    @staticmethod
    @_mutmut_mutated(mutants_xǁJudgeǁ_build_consensus__mutmut)
    def _build_consensus(debate: DebateRound, validated: Sequence[str], dominant: str) -> str:
        validated_texts = [c.text for c in debate.claims if c.id in validated]
        if validated_texts:
            return f"Validated inversions ({len(validated_texts)} of {len(debate.claims)}): " + "; ".join(validated_texts)
        return f"No validated claims after {len(debate.nodes)}-node broadcast; dominant stance={dominant}."

    @staticmethod
    def xǁJudgeǁ_build_consensus__mutmut_orig(debate: DebateRound, validated: Sequence[str], dominant: str) -> str:
        validated_texts = [c.text for c in debate.claims if c.id in validated]
        if validated_texts:
            return f"Validated inversions ({len(validated_texts)} of {len(debate.claims)}): " + "; ".join(validated_texts)
        return f"No validated claims after {len(debate.nodes)}-node broadcast; dominant stance={dominant}."

    @staticmethod
    def xǁJudgeǁ_build_consensus__mutmut_1(debate: DebateRound, validated: Sequence[str], dominant: str) -> str:
        validated_texts = None
        if validated_texts:
            return f"Validated inversions ({len(validated_texts)} of {len(debate.claims)}): " + "; ".join(validated_texts)
        return f"No validated claims after {len(debate.nodes)}-node broadcast; dominant stance={dominant}."

    @staticmethod
    def xǁJudgeǁ_build_consensus__mutmut_2(debate: DebateRound, validated: Sequence[str], dominant: str) -> str:
        validated_texts = [c.text for c in debate.claims if c.id not in validated]
        if validated_texts:
            return f"Validated inversions ({len(validated_texts)} of {len(debate.claims)}): " + "; ".join(validated_texts)
        return f"No validated claims after {len(debate.nodes)}-node broadcast; dominant stance={dominant}."

    @staticmethod
    def xǁJudgeǁ_build_consensus__mutmut_3(debate: DebateRound, validated: Sequence[str], dominant: str) -> str:
        validated_texts = [c.text for c in debate.claims if c.id in validated]
        if validated_texts:
            return f"Validated inversions ({len(validated_texts)} of {len(debate.claims)}): " - "; ".join(validated_texts)
        return f"No validated claims after {len(debate.nodes)}-node broadcast; dominant stance={dominant}."

    @staticmethod
    def xǁJudgeǁ_build_consensus__mutmut_4(debate: DebateRound, validated: Sequence[str], dominant: str) -> str:
        validated_texts = [c.text for c in debate.claims if c.id in validated]
        if validated_texts:
            return f"Validated inversions ({len(validated_texts)} of {len(debate.claims)}): " + "; ".join(None)
        return f"No validated claims after {len(debate.nodes)}-node broadcast; dominant stance={dominant}."

    @staticmethod
    def xǁJudgeǁ_build_consensus__mutmut_5(debate: DebateRound, validated: Sequence[str], dominant: str) -> str:
        validated_texts = [c.text for c in debate.claims if c.id in validated]
        if validated_texts:
            return f"Validated inversions ({len(validated_texts)} of {len(debate.claims)}): " + "XX; XX".join(validated_texts)
        return f"No validated claims after {len(debate.nodes)}-node broadcast; dominant stance={dominant}."

mutants_xǁJudgeǁ__init____mutmut['_mutmut_orig'] = Judge.xǁJudgeǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁJudgeǁ__init____mutmut['xǁJudgeǁ__init____mutmut_1'] = Judge.xǁJudgeǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁJudgeǁsynthesize__mutmut['_mutmut_orig'] = Judge.xǁJudgeǁsynthesize__mutmut_orig # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_1'] = Judge.xǁJudgeǁsynthesize__mutmut_1 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_2'] = Judge.xǁJudgeǁsynthesize__mutmut_2 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_3'] = Judge.xǁJudgeǁsynthesize__mutmut_3 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_4'] = Judge.xǁJudgeǁsynthesize__mutmut_4 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_5'] = Judge.xǁJudgeǁsynthesize__mutmut_5 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_6'] = Judge.xǁJudgeǁsynthesize__mutmut_6 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_7'] = Judge.xǁJudgeǁsynthesize__mutmut_7 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_8'] = Judge.xǁJudgeǁsynthesize__mutmut_8 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_9'] = Judge.xǁJudgeǁsynthesize__mutmut_9 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_10'] = Judge.xǁJudgeǁsynthesize__mutmut_10 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_11'] = Judge.xǁJudgeǁsynthesize__mutmut_11 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_12'] = Judge.xǁJudgeǁsynthesize__mutmut_12 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_13'] = Judge.xǁJudgeǁsynthesize__mutmut_13 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_14'] = Judge.xǁJudgeǁsynthesize__mutmut_14 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_15'] = Judge.xǁJudgeǁsynthesize__mutmut_15 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_16'] = Judge.xǁJudgeǁsynthesize__mutmut_16 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_17'] = Judge.xǁJudgeǁsynthesize__mutmut_17 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_18'] = Judge.xǁJudgeǁsynthesize__mutmut_18 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_19'] = Judge.xǁJudgeǁsynthesize__mutmut_19 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_20'] = Judge.xǁJudgeǁsynthesize__mutmut_20 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_21'] = Judge.xǁJudgeǁsynthesize__mutmut_21 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_22'] = Judge.xǁJudgeǁsynthesize__mutmut_22 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_23'] = Judge.xǁJudgeǁsynthesize__mutmut_23 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_24'] = Judge.xǁJudgeǁsynthesize__mutmut_24 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_25'] = Judge.xǁJudgeǁsynthesize__mutmut_25 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_26'] = Judge.xǁJudgeǁsynthesize__mutmut_26 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_27'] = Judge.xǁJudgeǁsynthesize__mutmut_27 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_28'] = Judge.xǁJudgeǁsynthesize__mutmut_28 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_29'] = Judge.xǁJudgeǁsynthesize__mutmut_29 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_30'] = Judge.xǁJudgeǁsynthesize__mutmut_30 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_31'] = Judge.xǁJudgeǁsynthesize__mutmut_31 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_32'] = Judge.xǁJudgeǁsynthesize__mutmut_32 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_33'] = Judge.xǁJudgeǁsynthesize__mutmut_33 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_34'] = Judge.xǁJudgeǁsynthesize__mutmut_34 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_35'] = Judge.xǁJudgeǁsynthesize__mutmut_35 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_36'] = Judge.xǁJudgeǁsynthesize__mutmut_36 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_37'] = Judge.xǁJudgeǁsynthesize__mutmut_37 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_38'] = Judge.xǁJudgeǁsynthesize__mutmut_38 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_39'] = Judge.xǁJudgeǁsynthesize__mutmut_39 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_40'] = Judge.xǁJudgeǁsynthesize__mutmut_40 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_41'] = Judge.xǁJudgeǁsynthesize__mutmut_41 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_42'] = Judge.xǁJudgeǁsynthesize__mutmut_42 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_43'] = Judge.xǁJudgeǁsynthesize__mutmut_43 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_44'] = Judge.xǁJudgeǁsynthesize__mutmut_44 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_45'] = Judge.xǁJudgeǁsynthesize__mutmut_45 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_46'] = Judge.xǁJudgeǁsynthesize__mutmut_46 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_47'] = Judge.xǁJudgeǁsynthesize__mutmut_47 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_48'] = Judge.xǁJudgeǁsynthesize__mutmut_48 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_49'] = Judge.xǁJudgeǁsynthesize__mutmut_49 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_50'] = Judge.xǁJudgeǁsynthesize__mutmut_50 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_51'] = Judge.xǁJudgeǁsynthesize__mutmut_51 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_52'] = Judge.xǁJudgeǁsynthesize__mutmut_52 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_53'] = Judge.xǁJudgeǁsynthesize__mutmut_53 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_54'] = Judge.xǁJudgeǁsynthesize__mutmut_54 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_55'] = Judge.xǁJudgeǁsynthesize__mutmut_55 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_56'] = Judge.xǁJudgeǁsynthesize__mutmut_56 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_57'] = Judge.xǁJudgeǁsynthesize__mutmut_57 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_58'] = Judge.xǁJudgeǁsynthesize__mutmut_58 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_59'] = Judge.xǁJudgeǁsynthesize__mutmut_59 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_60'] = Judge.xǁJudgeǁsynthesize__mutmut_60 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_61'] = Judge.xǁJudgeǁsynthesize__mutmut_61 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_62'] = Judge.xǁJudgeǁsynthesize__mutmut_62 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_63'] = Judge.xǁJudgeǁsynthesize__mutmut_63 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_64'] = Judge.xǁJudgeǁsynthesize__mutmut_64 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_65'] = Judge.xǁJudgeǁsynthesize__mutmut_65 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_66'] = Judge.xǁJudgeǁsynthesize__mutmut_66 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_67'] = Judge.xǁJudgeǁsynthesize__mutmut_67 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_68'] = Judge.xǁJudgeǁsynthesize__mutmut_68 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_69'] = Judge.xǁJudgeǁsynthesize__mutmut_69 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_70'] = Judge.xǁJudgeǁsynthesize__mutmut_70 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_71'] = Judge.xǁJudgeǁsynthesize__mutmut_71 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_72'] = Judge.xǁJudgeǁsynthesize__mutmut_72 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_73'] = Judge.xǁJudgeǁsynthesize__mutmut_73 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_74'] = Judge.xǁJudgeǁsynthesize__mutmut_74 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_75'] = Judge.xǁJudgeǁsynthesize__mutmut_75 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_76'] = Judge.xǁJudgeǁsynthesize__mutmut_76 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_77'] = Judge.xǁJudgeǁsynthesize__mutmut_77 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_78'] = Judge.xǁJudgeǁsynthesize__mutmut_78 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_79'] = Judge.xǁJudgeǁsynthesize__mutmut_79 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_80'] = Judge.xǁJudgeǁsynthesize__mutmut_80 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_81'] = Judge.xǁJudgeǁsynthesize__mutmut_81 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_82'] = Judge.xǁJudgeǁsynthesize__mutmut_82 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_83'] = Judge.xǁJudgeǁsynthesize__mutmut_83 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_84'] = Judge.xǁJudgeǁsynthesize__mutmut_84 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_85'] = Judge.xǁJudgeǁsynthesize__mutmut_85 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_86'] = Judge.xǁJudgeǁsynthesize__mutmut_86 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_87'] = Judge.xǁJudgeǁsynthesize__mutmut_87 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_88'] = Judge.xǁJudgeǁsynthesize__mutmut_88 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_89'] = Judge.xǁJudgeǁsynthesize__mutmut_89 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_90'] = Judge.xǁJudgeǁsynthesize__mutmut_90 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_91'] = Judge.xǁJudgeǁsynthesize__mutmut_91 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_92'] = Judge.xǁJudgeǁsynthesize__mutmut_92 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_93'] = Judge.xǁJudgeǁsynthesize__mutmut_93 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_94'] = Judge.xǁJudgeǁsynthesize__mutmut_94 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_95'] = Judge.xǁJudgeǁsynthesize__mutmut_95 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_96'] = Judge.xǁJudgeǁsynthesize__mutmut_96 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_97'] = Judge.xǁJudgeǁsynthesize__mutmut_97 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_98'] = Judge.xǁJudgeǁsynthesize__mutmut_98 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_99'] = Judge.xǁJudgeǁsynthesize__mutmut_99 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_100'] = Judge.xǁJudgeǁsynthesize__mutmut_100 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_101'] = Judge.xǁJudgeǁsynthesize__mutmut_101 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_102'] = Judge.xǁJudgeǁsynthesize__mutmut_102 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_103'] = Judge.xǁJudgeǁsynthesize__mutmut_103 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_104'] = Judge.xǁJudgeǁsynthesize__mutmut_104 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_105'] = Judge.xǁJudgeǁsynthesize__mutmut_105 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_106'] = Judge.xǁJudgeǁsynthesize__mutmut_106 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_107'] = Judge.xǁJudgeǁsynthesize__mutmut_107 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_108'] = Judge.xǁJudgeǁsynthesize__mutmut_108 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_109'] = Judge.xǁJudgeǁsynthesize__mutmut_109 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_110'] = Judge.xǁJudgeǁsynthesize__mutmut_110 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_111'] = Judge.xǁJudgeǁsynthesize__mutmut_111 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_112'] = Judge.xǁJudgeǁsynthesize__mutmut_112 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_113'] = Judge.xǁJudgeǁsynthesize__mutmut_113 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_114'] = Judge.xǁJudgeǁsynthesize__mutmut_114 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_115'] = Judge.xǁJudgeǁsynthesize__mutmut_115 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_116'] = Judge.xǁJudgeǁsynthesize__mutmut_116 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_117'] = Judge.xǁJudgeǁsynthesize__mutmut_117 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_118'] = Judge.xǁJudgeǁsynthesize__mutmut_118 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_119'] = Judge.xǁJudgeǁsynthesize__mutmut_119 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_120'] = Judge.xǁJudgeǁsynthesize__mutmut_120 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_121'] = Judge.xǁJudgeǁsynthesize__mutmut_121 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_122'] = Judge.xǁJudgeǁsynthesize__mutmut_122 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_123'] = Judge.xǁJudgeǁsynthesize__mutmut_123 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_124'] = Judge.xǁJudgeǁsynthesize__mutmut_124 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_125'] = Judge.xǁJudgeǁsynthesize__mutmut_125 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_126'] = Judge.xǁJudgeǁsynthesize__mutmut_126 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_127'] = Judge.xǁJudgeǁsynthesize__mutmut_127 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_128'] = Judge.xǁJudgeǁsynthesize__mutmut_128 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_129'] = Judge.xǁJudgeǁsynthesize__mutmut_129 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_130'] = Judge.xǁJudgeǁsynthesize__mutmut_130 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_131'] = Judge.xǁJudgeǁsynthesize__mutmut_131 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_132'] = Judge.xǁJudgeǁsynthesize__mutmut_132 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_133'] = Judge.xǁJudgeǁsynthesize__mutmut_133 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_134'] = Judge.xǁJudgeǁsynthesize__mutmut_134 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_135'] = Judge.xǁJudgeǁsynthesize__mutmut_135 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_136'] = Judge.xǁJudgeǁsynthesize__mutmut_136 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_137'] = Judge.xǁJudgeǁsynthesize__mutmut_137 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_138'] = Judge.xǁJudgeǁsynthesize__mutmut_138 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_139'] = Judge.xǁJudgeǁsynthesize__mutmut_139 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_140'] = Judge.xǁJudgeǁsynthesize__mutmut_140 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_141'] = Judge.xǁJudgeǁsynthesize__mutmut_141 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_142'] = Judge.xǁJudgeǁsynthesize__mutmut_142 # type: ignore # mutmut generated
mutants_xǁJudgeǁsynthesize__mutmut['xǁJudgeǁsynthesize__mutmut_143'] = Judge.xǁJudgeǁsynthesize__mutmut_143 # type: ignore # mutmut generated

mutants_xǁJudgeǁ_claim_to_dict__mutmut['_mutmut_orig'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_orig # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_1'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_1 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_2'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_2 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_3'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_3 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_4'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_4 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_5'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_5 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_6'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_6 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_7'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_7 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_8'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_8 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_9'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_9 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_10'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_10 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_11'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_11 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_claim_to_dict__mutmut['xǁJudgeǁ_claim_to_dict__mutmut_12'] = Judge.xǁJudgeǁ_claim_to_dict__mutmut_12 # type: ignore # mutmut generated

mutants_xǁJudgeǁ_build_consensus__mutmut['_mutmut_orig'] = Judge.xǁJudgeǁ_build_consensus__mutmut_orig # type: ignore # mutmut generated
mutants_xǁJudgeǁ_build_consensus__mutmut['xǁJudgeǁ_build_consensus__mutmut_1'] = Judge.xǁJudgeǁ_build_consensus__mutmut_1 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_build_consensus__mutmut['xǁJudgeǁ_build_consensus__mutmut_2'] = Judge.xǁJudgeǁ_build_consensus__mutmut_2 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_build_consensus__mutmut['xǁJudgeǁ_build_consensus__mutmut_3'] = Judge.xǁJudgeǁ_build_consensus__mutmut_3 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_build_consensus__mutmut['xǁJudgeǁ_build_consensus__mutmut_4'] = Judge.xǁJudgeǁ_build_consensus__mutmut_4 # type: ignore # mutmut generated
mutants_xǁJudgeǁ_build_consensus__mutmut['xǁJudgeǁ_build_consensus__mutmut_5'] = Judge.xǁJudgeǁ_build_consensus__mutmut_5 # type: ignore # mutmut generated
