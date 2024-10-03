from typing import Union

from pydantic import BaseModel
import numpy as np
from PIL import Image
import faiss

from .img import image_embed
from .text import text_embed

# Initialize FAISS index
embedding_dim = 2048  # Adjust based on your embedding size
index = faiss.IndexFlatL2(embedding_dim)
stored_models = []


class EmbModel(BaseModel):
    def embed(self) -> np.ndarray:
        embeddings = []
        for field_name, field_value in self:
            if isinstance(field_value, str):
                embeddings.append(text_embed(field_value))
            elif isinstance(field_value, Image.Image):
                embeddings.append(image_embed(field_value))
            elif isinstance(field_value, EmbModel):
                embeddings.append(field_value.embed())
            # Handle other types as needed
        return np.mean(embeddings, axis=0) if embeddings else np.array([])

    def store(self):
        embedding = self.embed()
        if embedding.size == 0:
            raise ValueError("Embedding is empty. Cannot store the model.")
        embedding = embedding.astype("float32")
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        n = embedding.shape[0]
        index.add(n, embedding)
        stored_models.append(self)

    @classmethod
    def search(cls, query: Union[str, Image.Image], top_k: int = 5):
        query_embedding = cls.embed_query(query).astype("float32")
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        n = query_embedding.shape[0]
        k = top_k
        d = query_embedding.shape[1]

        # Check if the dimensions match
        if d != index.d:
            raise ValueError(
                f"Dimension mismatch: query vector dimension {d} does not match index dimension {index.d}"
            )

        # Prepare output arrays
        distances = np.empty((n, k), dtype=np.float32)
        labels = np.empty((n, k), dtype=np.int64)

        # Get pointers to the data using faiss.swig_ptr
        x_ptr = faiss.swig_ptr(query_embedding)
        distances_ptr = faiss.swig_ptr(distances)
        labels_ptr = faiss.swig_ptr(labels)

        # Call the low-level search method
        index.search(n, x_ptr, k, distances_ptr, labels_ptr)

        # Process the results
        indices = labels
        results = [stored_models[i] for i in indices[0] if i != -1]
        return results

    @staticmethod
    def embed_query(query: Union[str, Image.Image]) -> np.ndarray:
        if isinstance(query, str):
            return np.array(text_embed(query))
        elif isinstance(query, Image.Image):
            return np.array(image_embed(query))
        else:
            raise ValueError("Query must be a string or PIL.Image.Image")
