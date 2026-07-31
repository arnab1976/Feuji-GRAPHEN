"""ChromaDB vector store — persistent, local, no server required."""
from __future__ import annotations
import os
from loguru import logger
import chromadb  # type: ignore

from leaseguard.config import CHROMA_DB_PATH, CHROMA_COLLECTION
from leaseguard.intelligence.embedder import embed


class VectorStore:
    """
    Wraps ChromaDB PersistentClient.

    All embeddings are computed locally with sentence-transformers and stored
    to disk at CHROMA_DB_PATH — zero external API calls, fully private.
    """

    def __init__(
        self,
        db_path:    str | None = None,
        collection: str | None = None,
    ) -> None:
        path = db_path or CHROMA_DB_PATH
        name = collection or CHROMA_COLLECTION
        os.makedirs(path, exist_ok=True)
        self._client     = chromadb.PersistentClient(path=path)
        self._collection = self._client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )
        logger.debug(f"VectorStore  path={path}  collection={name}  docs={self._collection.count()}")

    # ── Write ──────────────────────────────────────────────────────────────

    def add_chunks(
        self,
        chunks:      list[str],
        lease_id:    str,
        source_file: str = "",
    ) -> int:
        """
        Embed *chunks* and add them to the collection.

        Returns the number of chunks actually added.
        """
        if not chunks:
            return 0
        # De-duplicate IDs (in case of re-ingest)
        ids      = [f"{lease_id}_{i}" for i in range(len(chunks))]
        existing = set(self._collection.get(ids=ids)["ids"])
        new_ids, new_chunks = zip(
            *[(id_, ch) for id_, ch in zip(ids, chunks) if id_ not in existing]
        ) if any(id_ not in existing for id_ in ids) else ([], [])

        if not new_ids:
            logger.debug(f"VectorStore: all {len(chunks)} chunks already indexed for {lease_id}")
            return 0

        embeddings = embed(list(new_chunks)).tolist()
        metadatas  = [
            {"lease_id": lease_id, "source": source_file, "chunk_idx": i}
            for i in range(len(new_chunks))
        ]
        self._collection.add(
            embeddings=embeddings,
            documents=list(new_chunks),
            metadatas=metadatas,
            ids=list(new_ids),
        )
        logger.debug(f"VectorStore: added {len(new_ids)} chunks for {lease_id}")
        return len(new_ids)

    # ── Read ───────────────────────────────────────────────────────────────

    def search(
        self,
        query:     str,
        n_results: int = 4,
        lease_id:  str | None = None,
    ) -> list[dict]:
        """
        Semantic search.

        If *lease_id* is given, restrict search to that lease's chunks only.
        Returns a list of dicts with keys: text, lease_id, source, score.
        """
        if self._collection.count() == 0:
            return []

        q_embedding = embed([query]).tolist()
        where       = {"lease_id": lease_id} if lease_id else None

        results = self._collection.query(
            query_embeddings=q_embedding,
            n_results=min(n_results, self._collection.count()),
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        out = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            out.append({
                "text":     doc,
                "lease_id": meta.get("lease_id", ""),
                "source":   meta.get("source",   ""),
                "score":    round(1.0 - dist, 4),  # cosine similarity
            })
        return out

    def count(self) -> int:
        return self._collection.count()

    def delete_lease(self, lease_id: str) -> None:
        """Remove all chunks belonging to *lease_id*."""
        self._collection.delete(where={"lease_id": lease_id})
        logger.info(f"VectorStore: deleted chunks for {lease_id}")
