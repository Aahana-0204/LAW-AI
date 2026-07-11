"""
Unified LLM caller.

LLM_BACKEND env var:
  "template" — built-in template engine, zero deps (DEFAULT for cloud)
  "ollama"   — local Ollama server (local dev)
  "groq"     — Groq API, free tier (Llama 3.3 70B)
  "gemini"   — Google Gemini Flash, free tier
  "hf_api"   — HuggingFace InferenceClient
"""

import logging
import os
import time

logger = logging.getLogger(__name__)

LLM_BACKEND = os.environ.get("LLM_BACKEND", "template")
OLLAMA_BASE = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
HF_TOKEN = os.environ.get("HF_TOKEN", "")
HF_MODEL = os.environ.get("HF_MODEL", "Qwen/Qwen2.5-72B-Instruct")

SYSTEM_MSG = (
    "You are LAWAI, an expert AI legal assistant specializing in Indian law. "
    "Provide accurate, structured legal information. Cite specific sections, acts, and articles. "
    "Always recommend consulting a qualified advocate for specific legal situations."
)


def _call_template(prompt: str, domain: str = None, corpus_results: list = None) -> str:
    from .template_engine import generate_template_response
    from .domain_classifier import classify_domain

    if domain is None:
        domain = classify_domain(prompt)
    if corpus_results is None:
        from .corpus_search import search_corpus
        corpus_results = search_corpus(prompt, n_results=5)
    return generate_template_response(prompt, domain, corpus_results)


def _call_groq(prompt: str, max_tokens: int, temperature: float) -> str:
    import requests
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json={
            "model": GROQ_MODEL,
            "messages": [{"role": "system", "content": SYSTEM_MSG}, {"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def _call_gemini(prompt: str, max_tokens: int, temperature: float) -> str:
    import requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    resp = requests.post(
        url,
        json={
            "contents": [{"parts": [{"text": f"{SYSTEM_MSG}\n\n{prompt}"}]}],
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": temperature},
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def _call_hf_api(prompt: str, max_tokens: int, temperature: float) -> str:
    from huggingface_hub import InferenceClient
    try:
        client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN or None)
    except TypeError:
        client = InferenceClient(token=HF_TOKEN or None)
    resp = client.chat_completion(
        model=HF_MODEL,
        messages=[{"role": "system", "content": SYSTEM_MSG}, {"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content.strip()


def call_llm(
    prompt: str,
    max_tokens: int = 2000,
    temperature: float = 0.2,
    domain: str = None,
    corpus_results: list = None,
) -> str:
    """Call the configured LLM backend. Returns the generated text."""
    backend = LLM_BACKEND

    for attempt in range(2):
        try:
            if backend == "template":
                return _call_template(prompt, domain=domain, corpus_results=corpus_results)
            elif backend == "groq":
                return _call_groq(prompt, max_tokens, temperature)
            elif backend == "gemini":
                return _call_gemini(prompt, max_tokens, temperature)
            elif backend == "hf_api":
                return _call_hf_api(prompt, max_tokens, temperature)
            else:  # ollama
                import requests
                resp = requests.post(
                    f"{OLLAMA_BASE}/api/generate",
                    json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False,
                          "options": {"temperature": temperature, "num_predict": max_tokens}},
                    timeout=180,
                )
                resp.raise_for_status()
                return resp.json().get("response", "").strip()
        except Exception as e:
            logger.warning(f"LLM attempt {attempt+1} ({backend}): {str(e)[:150]}")
            if attempt == 0:
                time.sleep(1)
            else:
                # Last resort: use template engine
                logger.info("Falling back to template engine")
                return _call_template(prompt, domain=domain, corpus_results=corpus_results)
