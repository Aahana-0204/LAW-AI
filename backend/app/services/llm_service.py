"""
Unified LLM caller.

LLM_BACKEND env var:
  "ollama"  (default) — uses local Ollama server (for local dev)
  "local"             — uses llama-cpp-python with GGUF model (for cloud / no-API deploy)

For cloud (HuggingFace Spaces), set:
  LLM_BACKEND=local
  LLM_MODEL_REPO=Qwen/Qwen2.5-3B-Instruct-GGUF
  LLM_MODEL_FILE=qwen2.5-3b-instruct-q4_k_m.gguf
"""

import logging
import os
import time

logger = logging.getLogger(__name__)

LLM_BACKEND = os.environ.get("LLM_BACKEND", "ollama")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")

# Local GGUF model (used when LLM_BACKEND=local)
MODEL_REPO = os.environ.get("LLM_MODEL_REPO", "Qwen/Qwen2.5-3B-Instruct-GGUF")
MODEL_FILE = os.environ.get("LLM_MODEL_FILE", "qwen2.5-3b-instruct-q4_k_m.gguf")
N_THREADS = int(os.environ.get("LLM_THREADS", "2"))
N_CTX = int(os.environ.get("LLM_N_CTX", "4096"))

_local_llm = None


def _get_local_llm():
    global _local_llm
    if _local_llm is not None:
        return _local_llm
    from huggingface_hub import hf_hub_download
    from llama_cpp import Llama

    logger.info(f"Downloading model {MODEL_FILE} from {MODEL_REPO} ...")
    model_path = hf_hub_download(repo_id=MODEL_REPO, filename=MODEL_FILE)
    logger.info(f"Loading model from {model_path}")
    _local_llm = Llama(
        model_path=model_path,
        n_ctx=N_CTX,
        n_threads=N_THREADS,
        verbose=False,
    )
    logger.info("Model ready.")
    return _local_llm


def call_llm(prompt: str, max_tokens: int = 2000, temperature: float = 0.2) -> str:
    """Call the configured LLM backend. Returns the generated text."""

    if LLM_BACKEND == "local":
        try:
            llm = _get_local_llm()
            output = llm.create_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return output["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.error(f"Local LLM error: {e}")
            raise

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
                timeout=120,
            )
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
            else:
                raise
