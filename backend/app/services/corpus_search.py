"""
Lightweight keyword-based corpus searcher with direct section lookup.
Zero dependencies, zero API calls, instant startup.
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
        ipc    = importlib.import_module("data.corpus.ipc_sections")
        crpc   = importlib.import_module("data.corpus.crpc_sections")
        const  = importlib.import_module("data.corpus.constitutional_articles")
        civil  = importlib.import_module("data.corpus.civil_family_law")
        special = importlib.import_module("data.corpus.special_laws")
        case   = importlib.import_module("data.corpus.case_law")
        _corpus = (
            ipc.IPC_CORPUS
            + crpc.CRPC_CORPUS
            + const.CONSTITUTIONAL_CORPUS
            + civil.CIVIL_FAMILY_CORPUS
            + special.SPECIAL_LAWS_CORPUS
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


def _extract_section_refs(query: str) -> list:
    """
    Extract explicit section/article references from query.
    Returns list of (act, number) tuples.
    e.g. "IPC 302" → [("ipc", "302")]
         "Article 21" → [("article", "21")]
    """
    q = query.lower()
    refs = []
    patterns = [
        (r'\bipc\s+(?:section\s+)?(\d+[a-z]*)\b', 'ipc'),
        (r'\bcrpc\s+(?:section\s+)?(\d+[a-z]*)\b', 'crpc'),
        (r'\bcpc\s+(?:section\s+)?(\d+[a-z]*)\b', 'cpc'),
        (r'\barticle\s+(\d+[a-z]*)\b', 'article'),
        (r'\bsection\s+(\d+[a-z]*)\b', 'section'),
    ]
    for pat, act in patterns:
        for m in re.finditer(pat, q):
            refs.append((act, m.group(1)))
    return refs


def _direct_section_lookup(query: str, corpus: list) -> list:
    """
    Find corpus docs that exactly match section/article references in the query.
    Returns matched docs (may be multiple if multiple refs found).
    """
    refs = _extract_section_refs(query)
    if not refs:
        return []

    matched = []
    seen_ids = set()
    for act, num in refs:
        for doc in corpus:
            doc_id = doc.get("id", "")
            if doc_id in seen_ids:
                continue
            title_lower = doc.get("title", "").lower()
            section_lower = doc.get("section", "").lower()

            # Check title and section field for match
            hit = False
            if act == 'article':
                hit = (f"article {num}" in title_lower or f"article {num}" in section_lower)
            else:
                hit = (
                    f"section {num}" in title_lower
                    or f"section {num}" in section_lower
                    or (act != 'section' and act in title_lower and num in title_lower)
                )

            if hit:
                matched.append(doc)
                seen_ids.add(doc_id)

    return matched


def _make_result(doc: dict, relevance: float) -> dict:
    content = doc["content"]
    return {
        "title": doc.get("title", "Legal Document"),
        "section": doc.get("section", ""),
        "domain": doc.get("domain", "General"),
        "relevance": relevance,
        "snippet": content[:250] + "..." if len(content) > 250 else content,
        "content": content,
    }


def search_corpus(query: str, n_results: int = 5) -> list:
    """
    Search the legal corpus.
    Priority: 1) direct section/article number lookup, 2) BM25 keyword search.
    Returns list of dicts with title, section, domain, relevance, snippet, content.
    """
    corpus = _get_corpus()
    if not corpus:
        return []

    # ── Step 1: Try direct section number lookup ──────────────────────────
    direct_hits = _direct_section_lookup(query, corpus)
    if direct_hits:
        results = [_make_result(doc, 100.0) for doc in direct_hits[:n_results]]
        # Fill remaining slots with BM25 results (different docs)
        if len(results) < n_results:
            used_titles = {r["title"] for r in results}
            bm25_extra = _bm25_search(query, corpus, n_results * 2)
            for r in bm25_extra:
                if r["title"] not in used_titles and len(results) < n_results:
                    r["relevance"] = min(r["relevance"], 85.0)  # cap so direct hits stay #1
                    results.append(r)
        return results

    # ── Step 2: BM25 keyword search ───────────────────────────────────────
    return _bm25_search(query, corpus, n_results)


def _bm25_search(query: str, corpus: list, n_results: int) -> list:
    """Pure BM25 search with title-boost for section references."""
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    refs = _extract_section_refs(query)
    ref_numbers = {num for _, num in refs}

    tokenized = [_tokenize(d["content"]) for d in corpus]
    avg_dl = sum(len(t) for t in tokenized) / max(len(tokenized), 1)

    scored = []
    for i, (doc, tokens) in enumerate(zip(corpus, tokenized)):
        score = _bm25_score(query_tokens, tokens, avg_dl)
        # Boost if section number appears in doc title/section field
        title_lower = doc.get("title", "").lower()
        if any(num in title_lower for num in ref_numbers):
            score *= 3.0
        if score > 0:
            scored.append((score, i))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:n_results]
    if not top:
        return []

    results = []
    max_score = top[0][0]
    for score, idx in top:
        doc = corpus[idx]
        relevance = round((score / max_score) * 100, 1)
        if relevance < 25:
            continue
        results.append(_make_result(doc, relevance))
    return results
