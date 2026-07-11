import os

from .corpus_search import search_corpus
from .domain_classifier import classify_domain
from .llm_service import call_llm
from ..utils.cache import get_cached, set_cached

NON_LEGAL_KEYWORDS = [
    "recipe", "weather", "sports", "movie", "music", "game", "food",
    "travel", "coding", "programming", "math", "science", "chemistry", "physics",
]

SYSTEM_PROMPT = """You are LAWAI, an expert AI Legal Assistant specializing in Indian law. You have deep knowledge of:
- Indian Penal Code (IPC) and Criminal Procedure Code (CrPC)
- Constitutional Law and Fundamental Rights
- Civil Procedure Code (CPC) and Contract Law
- Family Law (Hindu, Muslim, Christian personal laws)
- Property Law (Transfer of Property Act, Registration Act)
- Labour Law (Industrial Disputes Act, Minimum Wages, Gratuity)
- Corporate Law (Companies Act, SEBI regulations)
- Tax Law (Income Tax Act, GST)
- Consumer Protection Law
- Important Supreme Court and High Court judgments

RESPONSE FORMAT:
## Legal Position
[Clear explanation of the law]

## Relevant Provisions
[Specific sections, articles, or acts]

## Key Points
[Bullet points of important facts]

## Practical Implications
[What this means for the person asking]

## Important Note
Always recommend consulting a qualified lawyer for specific legal situations.

RULES:
- Always cite specific section numbers, article numbers, or case names
- If context documents are provided, prioritize them
- Be clear, structured, and use plain language
- Never fabricate section numbers or case citations
- If you're unsure, say so honestly"""


def get_rag_answer(query: str, chat_history: list = None) -> dict:
    cached = get_cached(query)
    if cached and not chat_history:
        return cached

    domain = classify_domain(query)

    query_lower = query.lower()
    if domain == "General" and any(kw in query_lower for kw in NON_LEGAL_KEYWORDS):
        return {
            "answer": "I specialize in Indian law and legal matters. Your query appears to be outside my domain of expertise. Please ask me about IPC sections, constitutional rights, family law, property matters, employment law, or any other legal topic.",
            "domain": "General",
            "sources": [],
        }

    # Keyword-based corpus search (zero deps, instant startup)
    corpus_results = search_corpus(query, n_results=5)
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
        answer = call_llm(prompt, max_tokens=2000, temperature=0.2)
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
