"""
Lightweight keyword-based corpus searcher.
Zero dependencies, zero API calls, instant startup.
The LLM (Qwen 72B) already knows Indian law — this just adds extra context
for the most relevant corpus sections.
"""

import math
import re
from collections import Counter

# Lazy-loaded corpus
_corpus = None


def _get_corpus():
    global _corpus
    if _corpus is not None:
        return _corpus
    try:
        import importlib
        ipc = importlib.import_module("data.corpus.ipc_sections")
        const = importlib.import_module("data.corpus.constitutional_articles")
        civil = importlib.import_module("data.corpus.civil_family_law")
        case = importlib.import_module("data.corpus.case_law")
        _corpus = (
            ipc.IPC_CORPUS
            + const.CONSTITUTIONAL_CORPUS
            + civil.CIVIL_FAMILY_CORPUS
            + case.CASE_LAW_CORPUS
        )
    except Exception:
        _corpus = []
    return _corpus


def _tokenize(text: str) -> list:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return [w for w in text.split() if len(w) > 2]


def _bm25_score(query_tokens: list, doc_tokens: list, avg_dl: float, k1=1.5, b=0.75) -> float:
    dl = len(doc_tokens)
    doc_freq = Counter(doc_tokens)
    score = 0.0
    for term in query_tokens:
        tf = doc_freq.get(term, 0)
        if tf == 0:
            continue
        idf = math.log(1 + (1 / (tf + 0.5)))
        score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avg_dl))
    return score


def search_corpus(query: str, n_results: int = 5) -> list:
    """
    BM25 keyword search over the legal corpus.
    Returns list of dicts with title, section, domain, relevance, snippet.
    """
    corpus = _get_corpus()
    if not corpus:
        return []

    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    # Pre-tokenize docs and compute avg length
    tokenized = [_tokenize(d["content"]) for d in corpus]
    avg_dl = sum(len(t) for t in tokenized) / max(len(tokenized), 1)

    # Score each doc
    scored = []
    for i, (doc, tokens) in enumerate(zip(corpus, tokenized)):
        score = _bm25_score(query_tokens, tokens, avg_dl)
        if score > 0:
            scored.append((score, i))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:n_results]

    results = []
    max_score = top[0][0] if top else 1.0
    for score, idx in top:
        doc = corpus[idx]
        relevance = round((score / max_score) * 100, 1)
        if relevance < 30:
            continue
        results.append(
            {
                "title": doc.get("title", "Legal Document"),
                "section": doc.get("section", ""),
                "domain": doc.get("domain", "General"),
                "relevance": relevance,
                "snippet": doc["content"][:250] + "..."
                if len(doc["content"]) > 250
                else doc["content"],
                "content": doc["content"],
            }
        )
    return results
