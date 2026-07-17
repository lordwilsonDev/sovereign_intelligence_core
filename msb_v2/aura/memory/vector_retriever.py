"""
Vector retriever stub.

Week 5 swap target: replace BM25Retriever with this implementation
when ChromaDB or pgvector is available in the runtime environment.

This stub preserves the RetrieverInterface while making vector semantics
explicit. It intentionally fails closed if dependencies are missing so
misconfiguration is obvious.
"""

from __future__ import annotations

from typing import List

from msb_v2.aura.memory.retriever import RetrieverInterface


class VectorRetriever(RetrieverInterface):
    def __init__(self, documents: List[str] | None = None, provider: str = "chroma") -> None:
        self.documents = documents or []
        self.provider = provider
        self._ready = False

    async def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        if not self._ready:
            raise RuntimeError("VectorRetriever is not initialized. Call `build_index()` first.")
        return self.documents[:top_k]

    def build_index(self) -> None:
        raise RuntimeError(
            "VectorRetriever index build is not implemented. "
            "Install and configure ChromaDB or pgvector, then replace this stub."
        )
