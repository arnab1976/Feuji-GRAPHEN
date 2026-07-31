"""Sentence-transformer embeddings — lazy-loaded singleton, runs fully locally."""
from __future__ import annotations
import numpy as np
from loguru import logger
from leaseguard.config import EMBEDDING_MODEL

_model = None   # Singleton — loaded once on first call


def get_model():
    """Return the sentence-transformers model, loading it if necessary."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer  # type: ignore
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL} …")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("Embedding model ready")
    return _model


def embed(texts: list[str]) -> np.ndarray:
    """
    Embed a list of strings.

    Returns a 2-D float32 array of shape (len(texts), EMBEDDING_DIMENSION).
    """
    if not texts:
        return np.empty((0, 384), dtype=np.float32)
    return get_model().encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False,
        batch_size=32,
    )


def embed_one(text: str) -> np.ndarray:
    """Convenience wrapper for a single string → 1-D float32 array."""
    return embed([text])[0]
