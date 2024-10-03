from enum import Enum

import numpy as np
from sentence_transformers import SentenceTransformer

from orcalib.rac.common import InputType


class EmbeddingModel(Enum):
    """Enum of embedding models for use with Memorysets"""

    # Format: hf model name, version, embedding dimension
    CLIP_BASE = "sentence-transformers/clip-ViT-L-14", 1, 768
    """CLIP-L14 embedding model"""

    GTE_BASE = "Alibaba-NLP/gte-base-en-v1.5", 1, 768
    """Alibaba GTE-Base v1.5 embedding model"""

    def __new__(cls, value, version, embedding_dim):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.version = version
        obj.embedding_dim = embedding_dim
        return obj

    def __init__(self, value, version, embedding_dim):
        self._value_ = value
        self.version = version
        self.embedding_dim = embedding_dim
        self.embedder = None

    def _get_embedding(self, data: InputType | list[InputType], show_progress_bar: bool = False) -> np.ndarray:
        if not isinstance(data, list):
            data = [data]
        if self.embedder is None:
            self.embedder = SentenceTransformer(self.value, trust_remote_code=True)
        # Automatically batches using size 32
        return self.embedder.encode(data, show_progress_bar=show_progress_bar, normalize_embeddings=True)  # type: ignore -- sentence transformer has not updated their typing
