from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import List, Dict


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class RetrieverInterface(ABC):
    @abstractmethod
    async def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        pass
mutants_xǁBM25Retrieverǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁBM25Retrieverǁretrieve__mutmut: MutantDict = {}  # type: ignore
mutants_xǁBM25Retrieverǁ_tokenize__mutmut: MutantDict = {}  # type: ignore
mutants_xǁBM25Retrieverǁ_term_freq__mutmut: MutantDict = {}  # type: ignore
mutants_xǁBM25Retrieverǁ_idf__mutmut: MutantDict = {}  # type: ignore


class BM25Retriever(RetrieverInterface):
    @_mutmut_mutated(mutants_xǁBM25Retrieverǁ__init____mutmut)
    def __init__(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_orig(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_1(self, documents: List[str] | None = None) -> None:
        self.documents = None
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_2(self, documents: List[str] | None = None) -> None:
        self.documents = documents and []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_3(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = None
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_4(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(None) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_5(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = None
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_6(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(None) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_7(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = None
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_8(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) * max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_9(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(None) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_10(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(None, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_11(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, None)
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_12(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_13(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, )
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_14(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(2, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_15(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = None
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_16(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 2.2
        self._b = 0.75
    def xǁBM25Retrieverǁ__init____mutmut_17(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = None
    def xǁBM25Retrieverǁ__init____mutmut_18(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 1.75

    @_mutmut_mutated(mutants_xǁBM25Retrieverǁretrieve__mutmut)
    async def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_orig(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_1(self, query: str, top_k: int = 4) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_2(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = None
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_3(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(None)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_4(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = None
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_5(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(None)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_6(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = None
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_7(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(None):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_8(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = None
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_9(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 1.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_10(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = None
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_11(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = None
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_12(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(None, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_13(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, None)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_14(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_15(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, )
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_16(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 1)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_17(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = None
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_18(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(None)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_19(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = None
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_20(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf / (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_21(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 - 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_22(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 2.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_23(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = None
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_24(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf - self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_25(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 / (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_26(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b - self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_27(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 + self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_28(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (2.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_29(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len * max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_30(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b / doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_31(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(None, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_32(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, None))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_33(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_34(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, ))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_35(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(2.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_36(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score = qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_37(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score -= qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_38(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator * max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_39(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf / numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_40(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf / idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_41(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(None, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_42(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, None)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_43(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(1e-9)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_44(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, )
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_45(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1.000000001)
            scores.append((score, idx))
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_46(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append(None)
        scores.sort(reverse=True)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_47(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=None)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    async def xǁBM25Retrieverǁretrieve__mutmut_48(self, query: str, top_k: int = 3) -> List[str]:
        q_tokens = self._tokenize(query)
        q_freq = self._term_freq(q_tokens)
        scores = []
        for idx, tokens in enumerate(self._tokenized):
            score = 0.0
            doc_len = len(tokens)
            for term, qf in q_freq.items():
                tf = self._freqs[idx].get(term, 0)
                idf = self._idf(term)
                numerator = tf * (self._k1 + 1.0)
                denominator = tf + self._k1 * (1.0 - self._b + self._b * doc_len / max(1.0, self._avg_len))
                score += qf * idf * numerator / max(denominator, 1e-9)
            scores.append((score, idx))
        scores.sort(reverse=False)
        return [self.documents[idx] for _, idx in scores[:top_k]]

    @staticmethod
    @_mutmut_mutated(mutants_xǁBM25Retrieverǁ_tokenize__mutmut)
    def _tokenize(text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+", text.lower())

    @staticmethod
    def xǁBM25Retrieverǁ_tokenize__mutmut_orig(text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+", text.lower())

    @staticmethod
    def xǁBM25Retrieverǁ_tokenize__mutmut_1(text: str) -> List[str]:
        return re.findall(None, text.lower())

    @staticmethod
    def xǁBM25Retrieverǁ_tokenize__mutmut_2(text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+", None)

    @staticmethod
    def xǁBM25Retrieverǁ_tokenize__mutmut_3(text: str) -> List[str]:
        return re.findall(text.lower())

    @staticmethod
    def xǁBM25Retrieverǁ_tokenize__mutmut_4(text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+", )

    @staticmethod
    def xǁBM25Retrieverǁ_tokenize__mutmut_5(text: str) -> List[str]:
        return re.findall(r"XX[a-z0-9]+XX", text.lower())

    @staticmethod
    def xǁBM25Retrieverǁ_tokenize__mutmut_6(text: str) -> List[str]:
        return re.findall(r"[A-Z0-9]+", text.lower())

    @staticmethod
    def xǁBM25Retrieverǁ_tokenize__mutmut_7(text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+", text.upper())

    @staticmethod
    @_mutmut_mutated(mutants_xǁBM25Retrieverǁ_term_freq__mutmut)
    def _term_freq(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        return freq

    @staticmethod
    def xǁBM25Retrieverǁ_term_freq__mutmut_orig(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        return freq

    @staticmethod
    def xǁBM25Retrieverǁ_term_freq__mutmut_1(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = None
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        return freq

    @staticmethod
    def xǁBM25Retrieverǁ_term_freq__mutmut_2(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = {}
        for t in tokens:
            freq[t] = None
        return freq

    @staticmethod
    def xǁBM25Retrieverǁ_term_freq__mutmut_3(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) - 1
        return freq

    @staticmethod
    def xǁBM25Retrieverǁ_term_freq__mutmut_4(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(None, 0) + 1
        return freq

    @staticmethod
    def xǁBM25Retrieverǁ_term_freq__mutmut_5(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(t, None) + 1
        return freq

    @staticmethod
    def xǁBM25Retrieverǁ_term_freq__mutmut_6(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(0) + 1
        return freq

    @staticmethod
    def xǁBM25Retrieverǁ_term_freq__mutmut_7(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(t, ) + 1
        return freq

    @staticmethod
    def xǁBM25Retrieverǁ_term_freq__mutmut_8(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(t, 1) + 1
        return freq

    @staticmethod
    def xǁBM25Retrieverǁ_term_freq__mutmut_9(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 2
        return freq

    @_mutmut_mutated(mutants_xǁBM25Retrieverǁ_idf__mutmut)
    def _idf(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_orig(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_1(self, term: str) -> float:
        n = None
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_2(self, term: str) -> float:
        n = len(self._tokenized)
        df = None
        return max(0.0, (n - df + 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_3(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(None)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_4(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(2 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_5(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term not in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_6(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(None, (n - df + 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_7(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, None)

    def xǁBM25Retrieverǁ_idf__mutmut_8(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max((n - df + 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_9(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, )

    def xǁBM25Retrieverǁ_idf__mutmut_10(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(1.0, (n - df + 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_11(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, 1e-9) - 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_12(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) * max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_13(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df - 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_14(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n + df + 0.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_15(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 1.5) / max(df + 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_16(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(None, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_17(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, None) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_18(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_19(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, ) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_20(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df - 0.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_21(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 1.5, 1e-9) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_22(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, 1.000000001) + 1.0)

    def xǁBM25Retrieverǁ_idf__mutmut_23(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, 1e-9) + 2.0)

mutants_xǁBM25Retrieverǁ__init____mutmut['_mutmut_orig'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_1'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_2'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_3'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_4'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_5'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_6'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_7'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_7 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_8'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_8 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_9'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_9 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_10'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_10 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_11'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_11 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_12'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_12 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_13'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_13 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_14'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_14 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_15'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_15 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_16'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_16 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_17'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_17 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ__init____mutmut['xǁBM25Retrieverǁ__init____mutmut_18'] = BM25Retriever.xǁBM25Retrieverǁ__init____mutmut_18 # type: ignore # mutmut generated

mutants_xǁBM25Retrieverǁretrieve__mutmut['_mutmut_orig'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_orig # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_1'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_1 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_2'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_2 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_3'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_3 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_4'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_4 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_5'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_5 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_6'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_6 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_7'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_7 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_8'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_8 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_9'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_9 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_10'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_10 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_11'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_11 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_12'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_12 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_13'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_13 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_14'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_14 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_15'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_15 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_16'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_16 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_17'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_17 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_18'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_18 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_19'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_19 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_20'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_20 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_21'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_21 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_22'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_22 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_23'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_23 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_24'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_24 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_25'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_25 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_26'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_26 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_27'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_27 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_28'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_28 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_29'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_29 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_30'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_30 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_31'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_31 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_32'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_32 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_33'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_33 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_34'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_34 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_35'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_35 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_36'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_36 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_37'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_37 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_38'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_38 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_39'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_39 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_40'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_40 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_41'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_41 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_42'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_42 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_43'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_43 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_44'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_44 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_45'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_45 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_46'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_46 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_47'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_47 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁretrieve__mutmut['xǁBM25Retrieverǁretrieve__mutmut_48'] = BM25Retriever.xǁBM25Retrieverǁretrieve__mutmut_48 # type: ignore # mutmut generated

mutants_xǁBM25Retrieverǁ_tokenize__mutmut['_mutmut_orig'] = BM25Retriever.xǁBM25Retrieverǁ_tokenize__mutmut_orig # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_tokenize__mutmut['xǁBM25Retrieverǁ_tokenize__mutmut_1'] = BM25Retriever.xǁBM25Retrieverǁ_tokenize__mutmut_1 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_tokenize__mutmut['xǁBM25Retrieverǁ_tokenize__mutmut_2'] = BM25Retriever.xǁBM25Retrieverǁ_tokenize__mutmut_2 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_tokenize__mutmut['xǁBM25Retrieverǁ_tokenize__mutmut_3'] = BM25Retriever.xǁBM25Retrieverǁ_tokenize__mutmut_3 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_tokenize__mutmut['xǁBM25Retrieverǁ_tokenize__mutmut_4'] = BM25Retriever.xǁBM25Retrieverǁ_tokenize__mutmut_4 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_tokenize__mutmut['xǁBM25Retrieverǁ_tokenize__mutmut_5'] = BM25Retriever.xǁBM25Retrieverǁ_tokenize__mutmut_5 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_tokenize__mutmut['xǁBM25Retrieverǁ_tokenize__mutmut_6'] = BM25Retriever.xǁBM25Retrieverǁ_tokenize__mutmut_6 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_tokenize__mutmut['xǁBM25Retrieverǁ_tokenize__mutmut_7'] = BM25Retriever.xǁBM25Retrieverǁ_tokenize__mutmut_7 # type: ignore # mutmut generated

mutants_xǁBM25Retrieverǁ_term_freq__mutmut['_mutmut_orig'] = BM25Retriever.xǁBM25Retrieverǁ_term_freq__mutmut_orig # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_term_freq__mutmut['xǁBM25Retrieverǁ_term_freq__mutmut_1'] = BM25Retriever.xǁBM25Retrieverǁ_term_freq__mutmut_1 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_term_freq__mutmut['xǁBM25Retrieverǁ_term_freq__mutmut_2'] = BM25Retriever.xǁBM25Retrieverǁ_term_freq__mutmut_2 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_term_freq__mutmut['xǁBM25Retrieverǁ_term_freq__mutmut_3'] = BM25Retriever.xǁBM25Retrieverǁ_term_freq__mutmut_3 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_term_freq__mutmut['xǁBM25Retrieverǁ_term_freq__mutmut_4'] = BM25Retriever.xǁBM25Retrieverǁ_term_freq__mutmut_4 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_term_freq__mutmut['xǁBM25Retrieverǁ_term_freq__mutmut_5'] = BM25Retriever.xǁBM25Retrieverǁ_term_freq__mutmut_5 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_term_freq__mutmut['xǁBM25Retrieverǁ_term_freq__mutmut_6'] = BM25Retriever.xǁBM25Retrieverǁ_term_freq__mutmut_6 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_term_freq__mutmut['xǁBM25Retrieverǁ_term_freq__mutmut_7'] = BM25Retriever.xǁBM25Retrieverǁ_term_freq__mutmut_7 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_term_freq__mutmut['xǁBM25Retrieverǁ_term_freq__mutmut_8'] = BM25Retriever.xǁBM25Retrieverǁ_term_freq__mutmut_8 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_term_freq__mutmut['xǁBM25Retrieverǁ_term_freq__mutmut_9'] = BM25Retriever.xǁBM25Retrieverǁ_term_freq__mutmut_9 # type: ignore # mutmut generated

mutants_xǁBM25Retrieverǁ_idf__mutmut['_mutmut_orig'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_orig # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_1'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_1 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_2'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_2 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_3'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_3 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_4'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_4 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_5'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_5 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_6'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_6 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_7'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_7 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_8'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_8 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_9'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_9 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_10'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_10 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_11'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_11 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_12'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_12 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_13'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_13 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_14'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_14 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_15'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_15 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_16'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_16 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_17'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_17 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_18'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_18 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_19'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_19 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_20'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_20 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_21'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_21 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_22'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_22 # type: ignore # mutmut generated
mutants_xǁBM25Retrieverǁ_idf__mutmut['xǁBM25Retrieverǁ_idf__mutmut_23'] = BM25Retriever.xǁBM25Retrieverǁ_idf__mutmut_23 # type: ignore # mutmut generated
