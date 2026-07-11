import os

import chromadb
import google.generativeai as genai
from chromadb.utils import embedding_functions

from ..config import Config
from .domain_classifier import classify_domain

genai.configure(api_key=Config.GEMINI_API_KEY)

_chroma_client = None
_collection = None
_embedding_function = None


def _get_collection():
    global _chroma_client, _collection, _embedding_function
    if _collection is not None:
        return _collection
    persist_dir = os.path.abspath(Config.CHROMA_PERSIST_DIR)
    os.makedirs(persist_dir, exist_ok=True)
    _chroma_client = chromadb.PersistentClient(path=persist_dir)
    _embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    _collection = _chroma_client.get_or_create_collection(
        name="lawai_corpus",
        embedding_function=_embedding_function,
        metadata={"hnsw:space": "cosine"},
    )
    return _collection


SYSTEM_PROMPT = """You are LAWAI, an expert AI Legal Assistant specializing in Indian law.
You provide accurate, helpful legal information based on IPC sections, constitutional articles, case law, and other legal provisions.

RULES:
1. Always cite specific sections, articles, or case names from the provided context
2. If the context doesn't contain relevant information, say so honestly
3. Never give advice on matters outside Indian law
4. Always recommend consulting a qualified lawyer for specific legal situations
5. Be clear, structured, and use simple language

Format your response with:
- Clear explanation of the legal position
- Relevant sections/articles cited
- Practical implications
- Recommendation to consult a lawyer for specific cases"""


def get_rag_answer(query: str, chat_history: list = None) -> dict:
    domain = classify_domain(query)
    collection = _get_collection()

    if collection.count() == 0:
        context = ""
        sources = []
    else:
        results = collection.query(
            query_texts=[query],
            n_results=min(5, collection.count()),
            include=["documents", "metadatas", "distances"],
        )
        docs = results["documents"][0] if results["documents"] else []
        metas = results["metadatas"][0] if results["metadatas"] else []
        dists = results["distances"][0] if results["distances"] else []

        sources = []
        context_parts = []
        for doc, meta, dist in zip(docs, metas, dists):
            relevance = round((1 - dist) * 100, 1)
            if relevance > 30:
                sources.append(
                    {
                        "title": meta.get("title", "Legal Document"),
                        "section": meta.get("section", ""),
                        "domain": meta.get("domain", domain),
                        "relevance": relevance,
                        "snippet": doc[:200] + "..." if len(doc) > 200 else doc,
                    }
                )
                context_parts.append(f"[{meta.get('title', '')}]\n{doc}")
        context = "\n\n---\n\n".join(context_parts)

    history_text = ""
    if chat_history:
        for msg in chat_history[-4:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"

    prompt = f"""{SYSTEM_PROMPT}

Domain detected: {domain}

Legal Context:
{context if context else "No specific corpus entries found. Answering from general legal knowledge."}

{f"Conversation history:{chr(10)}{history_text}" if history_text else ""}

User Query: {query}

Provide a comprehensive, accurate legal response:"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=1500,
            ),
        )
        answer = response.text
    except Exception as exc:
        answer = (
            "I apologize, I'm unable to process your query at the moment. "
            f"Please try again. Error: {str(exc)}"
        )

    return {
        "answer": answer,
        "domain": domain,
        "sources": sources,
    }


def is_domain_relevant(query: str) -> bool:
    domain = classify_domain(query)
    return domain != "General"
