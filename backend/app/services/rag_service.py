import os

from .corpus_search import search_corpus
from .domain_classifier import classify_domain
from .llm_service import call_llm
from ..utils.cache import get_cached, set_cached

# Words that strongly suggest legal intent
LEGAL_INTENT_WORDS = {
    "law", "legal", "ipc", "section", "act", "court", "judge", "lawyer",
    "advocate", "rights", "crime", "criminal", "civil", "constitution",
    "article", "petition", "case", "fir", "bail", "arrest", "police",
    "property", "contract", "divorce", "marriage", "custody", "maintenance",
    "tax", "gst", "company", "employment", "labour", "worker", "salary",
    "rent", "tenant", "landlord", "consumer", "cheque", "fraud", "theft",
    "murder", "assault", "rape", "sentence", "punishment", "tribunal",
    "affidavit", "notary", "deed", "registration", "will", "succession",
    "shareholder", "director", "sebi", "pf", "gratuity", "termination",
    "harassment", "defamation", "negligence", "damages", "injunction",
    "supreme court", "high court", "district court", "magistrate", "pil",
    "fundamental right", "writ", "habeas corpus", "mandamus", "crpc", "cpc",
    "hindu", "muslim", "christian", "personal law", "dowry", "adoption",
}

OUT_OF_DOMAIN_REPLY = (
    "🚫 **Outside My Domain**\n\n"
    "I am LAWAI — an AI assistant specializing **exclusively in Indian law**.\n\n"
    "I cannot answer questions about cricket, sports, weather, cooking, entertainment, "
    "science, technology, or other non-legal topics.\n\n"
    "**Ask me about:**\n"
    "- 🔴 IPC sections & criminal law\n"
    "- 📜 Constitutional rights (Articles 12–35)\n"
    "- 👨‍👩‍👧 Family law (divorce, custody, maintenance)\n"
    "- 🏠 Property & rent disputes\n"
    "- 💼 Employment & labour law\n"
    "- 🏢 Company law & compliance\n"
    "- 💰 Tax law (GST, Income Tax)\n"
    "- 👥 Consumer rights & protection"
)


def _has_legal_intent(query: str) -> bool:
    """Check if query has any legal intent keywords."""
    q = query.lower()
    return any(word in q for word in LEGAL_INTENT_WORDS)


def _is_out_of_domain(query: str, domain: str, corpus_results: list) -> bool:
    """
    Return True if query is clearly out of legal domain.
    Uses two checks:
    1. Domain is General AND no legal intent words detected
    2. Best corpus relevance is below minimum threshold (weak match)
    """
    # If classified into a specific legal domain, allow it
    if domain != "General":
        return False

    # General domain: only allow if legal intent words present
    if not _has_legal_intent(query):
        return True

    # Even with intent words, if corpus relevance is too low, likely off-topic
    if corpus_results and corpus_results[0]["relevance"] < 25:
        return True

    return False


def get_rag_answer(query: str, chat_history: list = None) -> dict:
    cached = get_cached(query)
    if cached and not chat_history:
        return cached

    domain = classify_domain(query)

    # Keyword-based corpus search (zero deps, instant startup)
    corpus_results = search_corpus(query, n_results=5)

    # ── Out-of-domain guard ─────────────────────────────────────────────────
    if _is_out_of_domain(query, domain, corpus_results):
        return {
            "answer": OUT_OF_DOMAIN_REPLY,
            "domain": "Out of Scope",
            "sources": [],
        }
    # ────────────────────────────────────────────────────────────────────────

    sources = [
        {
            "title": r["title"],
            "section": r["section"],
            "domain": r["domain"],
            "relevance": r["relevance"],
            "snippet": r["snippet"],
        }
        for r in corpus_results
    ]
    context_parts = [f"### {r['title']}\n{r['content']}" for r in corpus_results]
    context = "\n\n---\n\n".join(context_parts)

    history_text = ""
    if chat_history:
        recent = chat_history[-4:]
        for msg in recent:
            role = "User" if msg["role"] == "user" else "LAWAI"
            history_text += f"**{role}:** {msg['content'][:300]}\n\n"

    prompt = f"""{SYSTEM_PROMPT}

**Detected Legal Domain:** {domain}

**Retrieved Legal Context:**
{context if context else "No specific corpus matches found. Answer from comprehensive legal knowledge."}

{"**Conversation History:**" + chr(10) + history_text if history_text else ""}

**User Query:** {query}

Provide a comprehensive, accurate legal response following the format above:"""

    try:
        answer = call_llm(
            prompt, max_tokens=2000, temperature=0.2,
            domain=domain, corpus_results=corpus_results
        )
    except Exception as e:
        answer = (
            "I apologize, I'm temporarily unable to process your query. "
            f"Please try again in a moment. (Error: {type(e).__name__})"
        )

    result = {"answer": answer, "domain": domain, "sources": sources}
    if not chat_history:
        set_cached(query, result)
    return result


def is_domain_relevant(query: str) -> bool:
    domain = classify_domain(query)
    return domain != "General"
