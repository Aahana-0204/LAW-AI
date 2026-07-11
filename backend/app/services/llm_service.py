"""
Unified LLM caller.

LLM_BACKEND env var:
  "ollama"   (default) — uses local Ollama server (local dev)
  "hf_api"             — uses HuggingFace Serverless Inference API (free, cloud)

For cloud (HuggingFace Spaces), set:
  LLM_BACKEND=hf_api
  HF_TOKEN=hf_...           (your HuggingFace token)
  HF_MODEL=Qwen/Qwen2.5-72B-Instruct  (or any free model)
"""

import logging
import os
import time

logger = logging.getLogger(__name__)

LLM_BACKEND = os.environ.get("LLM_BACKEND", "ollama")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")

# HF Inference Serverless API settings
HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_MODEL = os.environ.get("HF_MODEL", "Qwen/Qwen2.5-72B-Instruct")


def _call_hf_api(prompt: str, max_tokens: int = 2000, temperature: float = 0.2) -> str:
    """Use HuggingFace Serverless Inference API — free with any HF account."""
    import requests

    headers = {"Content-Type": "application/json"}
    if HF_TOKEN:
        headers["Authorization"] = f"Bearer {HF_TOKEN}"

    # Use the chat completions endpoint (OpenAI-compatible)
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}/v1/chat/completions"
    payload = {
        "model": HF_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are LAWAI, an expert AI legal assistant specializing in Indian law. "
                    "Provide accurate, helpful legal information based on Indian legal framework. "
                    "Always mention consulting a qualified lawyer for specific legal advice."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    for attempt in range(3):
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=120)
            if resp.status_code == 503:
                # Model loading — wait and retry
                wait = min(20 * (attempt + 1), 60)
                logger.info(f"HF model loading, retrying in {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                logger.error(f"HF API error: {e}")
                raise


def call_llm(prompt: str, max_tokens: int = 2000, temperature: float = 0.2) -> str:
    """Call the configured LLM backend. Returns the generated text."""

    if LLM_BACKEND == "hf_api":
        return _call_hf_api(prompt, max_tokens, temperature)

    # Ollama (default for local dev)
    import requests
    for attempt in range(3):
        try:
            resp = requests.post(
                f"{OLLAMA_BASE}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": temperature, "num_predict": max_tokens},
                },
                timeout=180,
            )
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
            else:
                raise
