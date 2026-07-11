"""
Unified LLM caller.

LLM_BACKEND env var:
  "ollama"   — uses local Ollama server (local dev)
  "hf_api"   — uses HuggingFace InferenceClient via router.huggingface.co (free, cloud)
"""

import logging
import os
import time

logger = logging.getLogger(__name__)

LLM_BACKEND = os.environ.get("LLM_BACKEND", "ollama")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")

HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_MODEL = os.environ.get("HF_MODEL", "Qwen/Qwen2.5-72B-Instruct")

_hf_client = None


def _get_hf_client():
    global _hf_client
    if _hf_client is not None:
        return _hf_client
    from huggingface_hub import InferenceClient

    # provider="hf-inference" routes via router.huggingface.co (new infra, better DNS)
    try:
        _hf_client = InferenceClient(
            provider="hf-inference",
            api_key=HF_TOKEN or None,
        )
    except TypeError:
        # Older huggingface_hub without provider param
        _hf_client = InferenceClient(token=HF_TOKEN or None)
    return _hf_client


SYSTEM_MSG = (
    "You are LAWAI, an expert AI legal assistant specializing in Indian law. "
    "Provide accurate, structured legal information based on the Indian legal framework. "
    "Always recommend consulting a qualified lawyer for specific legal advice."
)


def _call_hf_api(prompt: str, max_tokens: int = 2000, temperature: float = 0.2) -> str:
    client = _get_hf_client()
    messages = [
        {"role": "system", "content": SYSTEM_MSG},
        {"role": "user", "content": prompt},
    ]
    for attempt in range(3):
        try:
            resp = client.chat_completion(
                model=HF_MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            err = str(e)
            logger.warning(f"HF API attempt {attempt+1}: {err[:200]}")
            if "503" in err or "loading" in err.lower():
                time.sleep(20)
            elif attempt < 2:
                time.sleep(3)
            else:
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
