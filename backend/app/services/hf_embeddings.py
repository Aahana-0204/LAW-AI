"""
HuggingFace API-based embedding function for ChromaDB.
Replaces sentence-transformers (saves ~500MB RAM on free tier).
Uses the free HF Inference API — no credit card, just an HF token.
"""

import os
import logging
import time
import requests

logger = logging.getLogger(__name__)

HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_EMBED_MODEL = os.environ.get(
    "HF_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
)
EMBED_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{HF_EMBED_MODEL}"


class HFEmbeddingFunction:
    """
    ChromaDB-compatible embedding function using HuggingFace Inference API.
    Drop-in replacement for SentenceTransformerEmbeddingFunction.
    """

    def __call__(self, input: list) -> list:
        return self._embed(input)

    def _embed(self, texts: list) -> list:
        headers = {"Content-Type": "application/json"}
        if HF_TOKEN:
            headers["Authorization"] = f"Bearer {HF_TOKEN}"

        # Batch texts to avoid rate limits
        all_embeddings = []
        batch_size = 8

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            embeddings = self._call_api(batch, headers)
            all_embeddings.extend(embeddings)
            if i + batch_size < len(texts):
                time.sleep(0.2)  # small delay between batches

        return all_embeddings

    def _call_api(self, texts: list, headers: dict, retries: int = 3) -> list:
        for attempt in range(retries):
            try:
                resp = requests.post(
                    EMBED_URL,
                    json={"inputs": texts, "options": {"wait_for_model": True}},
                    headers=headers,
                    timeout=60,
                )
                if resp.status_code == 503:
                    wait = 20 * (attempt + 1)
                    logger.info(f"HF embed model loading, retrying in {wait}s...")
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                result = resp.json()
                # API returns list of embeddings directly
                if isinstance(result, list) and len(result) > 0:
                    if isinstance(result[0], list):
                        return result  # Already list of embeddings
                    # Single embedding returned — wrap
                    return [result]
                raise ValueError(f"Unexpected HF embed response: {result}")
            except requests.HTTPError as e:
                logger.error(f"HF embed API error (attempt {attempt+1}): {e}")
                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    raise


# Singleton instance
hf_ef = HFEmbeddingFunction()
