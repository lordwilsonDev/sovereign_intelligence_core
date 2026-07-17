from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import List, Dict


class RetrieverInterface(ABC):
    @abstractmethod
    async def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        pass


class BM25Retriever(RetrieverInterface):
    def __init__(self, documents: List[str] | None = None) -> None:
        self.documents = documents or []
        self._tokenized = [self._tokenize(doc) for doc in self.documents]
        self._freqs = [self._term_freq(tokens) for tokens in self._tokenized]
        self._avg_len = sum(len(t) for t in self._tokenized) / max(1, len(self._tokenized))
        self._k1 = 1.2
        self._b = 0.75

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

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+", text.lower())

    @staticmethod
    def _term_freq(tokens: List[str]) -> Dict[str, int]:
        freq: Dict[str, int] = {}
        for t in tokens:
            freq[t] = freq.get(t, 0) + 1
        return freq

    def _idf(self, term: str) -> float:
        n = len(self._tokenized)
        df = sum(1 for tokens in self._tokenized if term in tokens)
        return max(0.0, (n - df + 0.5) / max(df + 0.5, 1e-9) + 1.0)
