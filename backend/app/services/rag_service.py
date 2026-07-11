import os

import chromadb

from ..config import Config
from .domain_classifier import classify_domain
from .llm_service import call_llm
from .hf_embeddings import hf_ef
from ..utils.cache import get_cached, set_cached

_chroma_client = None
_collection = None


def _get_collection():
    global _chroma_client, _collection
    if _collection is not None:
        return _collection
    persist_dir = os.path.abspath(Config.CHROMA_PERSIST_DIR)
    os.makedirs(persist_dir, exist_ok=True)
    _chroma_client = chromadb.PersistentClient(path=persist_dir)
    _collection = _chroma_client.get_or_create_collection(
        name="lawai_corpus",
        embedding_function=hf_ef,
        metadata={"hnsw:space": "cosine"},
    )
    return _collection


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

    collection = _get_collection()
    sources = []
    context = ""

    if collection.count() > 0:
        results = collection.query(
            query_texts=[query],
            n_results=min(5, collection.count()),
            include=["documents", "metadatas", "distances"],
        )
        docs = results["documents"][0] if results["documents"] else []
        metas = results["metadatas"][0] if results["metadatas"] else []
        dists = results["distances"][0] if results["distances"] else []

        context_parts = []
        for doc, meta, dist in zip(docs, metas, dists):
            relevance = round((1 - dist) * 100, 1)
            if relevance > 40:
                sources.append(
                    {
                        "title": meta.get("title", "Legal Document"),
                        "section": meta.get("section", ""),
                        "domain": meta.get("domain", domain),
                        "relevance": relevance,
                        "snippet": doc[:250] + "..." if len(doc) > 250 else doc,
                    }
                )
                context_parts.append(f"### {meta.get('title', '')}\n{doc}")
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
