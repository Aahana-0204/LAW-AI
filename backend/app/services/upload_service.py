"""
Document upload and query service.
Stores user documents in MongoDB (no ChromaDB dependency).
Uses BM25 search for querying uploaded documents.
"""

import io
import hashlib
import math
import re
from collections import Counter
from datetime import datetime

from ..config import Config


# ─── MongoDB lazy connection ──────────────────────────────────────────────────

_client = None
_db = None


def _get_db():
    global _client, _db
    if _db is not None:
        return _db
    from pymongo import MongoClient
    _client = MongoClient(
        Config.MONGO_URI,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=15000,
        maxPoolSize=1,
        tls=True,
        tlsAllowInvalidCertificates=True,
    )
    uri = Config.MONGO_URI or ""
    db_name = "lawai"
    if "/" in uri:
        part = uri.split("/")[-1].split("?")[0]
        if part:
            db_name = part
    _db = _client[db_name]
    return _db


def _docs_col():
    return _get_db()["user_documents"]


# ─── Text extraction ──────────────────────────────────────────────────────────

def _extract_text(file_bytes: bytes, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            return "\n\n".join(
                page.extract_text() or "" for page in reader.pages
            ).strip()
        except Exception as e:
            raise ValueError(f"Could not parse PDF: {e}")
    elif ext in ("docx", "doc"):
        try:
            from docx import Document
            doc = Document(io.BytesIO(file_bytes))
            return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except Exception as e:
            raise ValueError(f"Could not parse DOCX: {e}")
    elif ext == "txt":
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: .{ext}. Use PDF, DOCX, or TXT.")


def _chunk_text(text: str, chunk_size: int = 600, overlap: int = 100):
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i: i + chunk_size]))
        i += chunk_size - overlap
    return chunks


# ─── BM25 search over chunks ──────────────────────────────────────────────────

def _tokenize(text: str) -> list:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return [w for w in text.split() if len(w) > 2]


def _bm25_score(query_tokens, doc_tokens, avg_dl, k1=1.5, b=0.75):
    dl = len(doc_tokens)
    freq = Counter(doc_tokens)
    score = 0.0
    for term in query_tokens:
        tf = freq.get(term, 0)
        if tf == 0:
            continue
        idf = math.log(1 + 1 / (tf + 0.5))
        score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avg_dl))
    return score


def _search_chunks(chunks: list, query: str, n: int = 5) -> list:
    q_tokens = _tokenize(query)
    tokenized = [_tokenize(c["text"]) for c in chunks]
    avg_dl = sum(len(t) for t in tokenized) / max(len(tokenized), 1)
    scored = []
    for i, (chunk, tokens) in enumerate(zip(chunks, tokenized)):
        score = _bm25_score(q_tokens, tokens, avg_dl)
        if score > 0:
            scored.append((score, i))
    scored.sort(reverse=True)
    results = []
    max_score = scored[0][0] if scored else 1.0
    for score, idx in scored[:n]:
        c = chunks[idx]
        results.append({
            "text": c["text"],
            "chunk_index": c["chunk_index"],
            "relevance": round((score / max_score) * 100, 1),
        })
    return results


# ─── Public API ───────────────────────────────────────────────────────────────

def ingest_document(user_id: str, file_bytes: bytes, filename: str) -> dict:
    text = _extract_text(file_bytes, filename)
    if not text or len(text.strip()) < 50:
        raise ValueError("Document appears empty or unreadable.")

    doc_id = hashlib.md5(
        f"{user_id}:{filename}:{len(file_bytes)}".encode()
    ).hexdigest()[:16]

    chunks_text = _chunk_text(text)
    chunks = [
        {"chunk_index": i, "text": c}
        for i, c in enumerate(chunks_text)
    ]

    col = _docs_col()
    # Remove old version if exists
    col.delete_many({"doc_id": doc_id, "user_id": user_id})

    col.insert_one({
        "doc_id": doc_id,
        "user_id": user_id,
        "filename": filename,
        "chunks": chunks,
        "total_chunks": len(chunks),
        "char_count": len(text),
        "preview": text[:300] + "..." if len(text) > 300 else text,
        "uploaded_at": datetime.utcnow(),
    })

    return {
        "doc_id": doc_id,
        "filename": filename,
        "chunks": len(chunks),
        "chars": len(text),
        "preview": text[:300] + "..." if len(text) > 300 else text,
    }


def list_user_documents(user_id: str) -> list:
    col = _docs_col()
    docs = col.find(
        {"user_id": user_id},
        {"doc_id": 1, "filename": 1, "total_chunks": 1, "char_count": 1, "uploaded_at": 1}
    ).sort("uploaded_at", -1)
    result = []
    for d in docs:
        result.append({
            "doc_id": d["doc_id"],
            "filename": d["filename"],
            "total_chunks": d.get("total_chunks", 0),
            "char_count": d.get("char_count", 0),
        })
    return result


def delete_document(user_id: str, doc_id: str) -> bool:
    col = _docs_col()
    r = col.delete_many({"doc_id": doc_id, "user_id": user_id})
    return r.deleted_count > 0


def query_user_documents(user_id: str, query: str, doc_id: str = None) -> dict:
    col = _docs_col()
    filter_q = {"user_id": user_id}
    if doc_id:
        filter_q["doc_id"] = doc_id

    docs = list(col.find(filter_q))
    if not docs:
        return {
            "answer": "No documents uploaded yet. Please upload a document first.",
            "sources": []
        }

    # Search across all matching docs
    all_results = []
    for doc in docs:
        hits = _search_chunks(doc.get("chunks", []), query, n=3)
        for h in hits:
            h["filename"] = doc["filename"]
            h["doc_id"] = doc["doc_id"]
            all_results.append(h)

    # Sort by relevance, take top 5
    all_results.sort(key=lambda x: x["relevance"], reverse=True)
    top = all_results[:5]

    if not top:
        return {
            "answer": "No relevant content found in your documents for this query.",
            "sources": []
        }

    # Build answer from top chunks
    context_parts = []
    sources = []
    for r in top:
        context_parts.append(f"[From: {r['filename']}]\n{r['text']}")
        sources.append({
            "filename": r["filename"],
            "chunk": r["chunk_index"] + 1,
            "relevance": r["relevance"],
            "snippet": r["text"][:200] + "..." if len(r["text"]) > 200 else r["text"],
        })

    context = "\n\n---\n\n".join(context_parts)

    # Generate answer from template engine style
    answer = f"## 📄 Document Analysis\n\n"
    answer += f"**Query:** {query}\n\n"
    answer += f"**Relevant sections found in your document(s):**\n\n"
    for i, r in enumerate(top[:3], 1):
        answer += f"### {i}. From: {r['filename']} (Relevance: {r['relevance']}%)\n"
        answer += r["text"][:500] + ("..." if len(r["text"]) > 500 else "") + "\n\n"

    answer += "\n---\n> ⚠️ This analysis is based on the text extracted from your uploaded document. Always verify with the original document."

    return {"answer": answer, "sources": sources}


_chroma_client = None
_user_collection = None


def _get_user_collection():
    global _chroma_client, _user_collection
    if _user_collection is not None:
        return _user_collection
    persist_dir = os.path.abspath(Config.CHROMA_PERSIST_DIR)
    os.makedirs(persist_dir, exist_ok=True)
    _chroma_client = chromadb.PersistentClient(path=persist_dir)
    _user_collection = _chroma_client.get_or_create_collection(
        name="user_documents",
        embedding_function=hf_ef,
        metadata={"hnsw:space": "cosine"},
    )
    return _user_collection


def _extract_text(file_bytes: bytes, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            return "\n\n".join(
                page.extract_text() or "" for page in reader.pages
            ).strip()
        except Exception as e:
            raise ValueError(f"Could not parse PDF: {e}")
    elif ext in ("docx", "doc"):
        try:
            from docx import Document
            doc = Document(io.BytesIO(file_bytes))
            return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except Exception as e:
            raise ValueError(f"Could not parse DOCX: {e}")
    elif ext == "txt":
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: .{ext}. Use PDF, DOCX, or TXT.")


def _chunk_text(text: str, chunk_size: int = 600, overlap: int = 100):
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i: i + chunk_size]))
        i += chunk_size - overlap
    return chunks


def ingest_document(user_id: str, file_bytes: bytes, filename: str) -> dict:
    text = _extract_text(file_bytes, filename)
    if not text or len(text.strip()) < 50:
        raise ValueError("Document appears empty or unreadable.")

    doc_id = hashlib.md5(
        f"{user_id}:{filename}:{len(file_bytes)}".encode()
    ).hexdigest()[:16]
    chunks = _chunk_text(text)
    collection = _get_user_collection()

    try:
        existing = collection.get(where={"doc_id": doc_id})
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
    except Exception:
        pass

    ids, documents, metadatas = [], [], []
    for i, chunk in enumerate(chunks):
        ids.append(f"{doc_id}_chunk_{i}")
        documents.append(chunk)
        metadatas.append({
            "user_id": user_id,
            "doc_id": doc_id,
            "filename": filename,
            "chunk_index": i,
            "total_chunks": len(chunks),
        })

    for start in range(0, len(ids), 20):
        collection.add(
            ids=ids[start: start + 20],
            documents=documents[start: start + 20],
            metadatas=metadatas[start: start + 20],
        )

    return {
        "doc_id": doc_id,
        "filename": filename,
        "chunks": len(chunks),
        "chars": len(text),
        "preview": text[:300] + "..." if len(text) > 300 else text,
    }


def list_user_documents(user_id: str) -> list:
    collection = _get_user_collection()
    try:
        results = collection.get(where={"user_id": user_id})
        seen = {}
        for meta in results["metadatas"] or []:
            did = meta.get("doc_id", "")
            if did not in seen:
                seen[did] = {
                    "doc_id": did,
                    "filename": meta.get("filename", ""),
                    "total_chunks": meta.get("total_chunks", 0),
                }
        return list(seen.values())
    except Exception:
        return []


def delete_document(user_id: str, doc_id: str) -> bool:
    collection = _get_user_collection()
    try:
        results = collection.get(where={"doc_id": doc_id, "user_id": user_id})
        if results["ids"]:
            collection.delete(ids=results["ids"])
            return True
        return False
    except Exception:
        return False


def query_user_documents(user_id: str, query: str, doc_id: str = None) -> dict:
    from .llm_service import call_llm

    collection = _get_user_collection()
    where_filter = {"user_id": user_id}
    if doc_id:
        where_filter = {"$and": [{"user_id": user_id}, {"doc_id": doc_id}]}

    try:
        total = collection.count()
        if total == 0:
            return {"answer": "No documents uploaded yet. Please upload a document first.", "sources": []}

        results = collection.query(
            query_texts=[query],
            n_results=min(5, total),
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )
    except Exception as e:
        return {"answer": f"Query error: {e}", "sources": []}

    docs = results["documents"][0] if results["documents"] else []
    metas = results["metadatas"][0] if results["metadatas"] else []
    dists = results["distances"][0] if results["distances"] else []

    context_parts, sources = [], []
    for doc, meta, dist in zip(docs, metas, dists):
        relevance = round((1 - dist) * 100, 1)
        sources.append({
            "filename": meta.get("filename", ""),
            "chunk": meta.get("chunk_index", 0) + 1,
            "relevance": relevance,
            "snippet": doc[:200] + "..." if len(doc) > 200 else doc,
        })
        context_parts.append(f"[From: {meta.get('filename', '')}]\n{doc}")

    context = "\n\n---\n\n".join(context_parts)
    prompt = f"""You are LAWAI, an expert AI Legal Assistant. Analyze the provided legal document excerpts and answer the user's question accurately.

DOCUMENT EXCERPTS:
{context}

USER QUESTION: {query}

Provide a clear, structured answer based on the documents. Highlight important legal clauses or provisions found. If documents don't contain relevant information, say so clearly."""

    try:
        answer = call_llm(prompt, max_tokens=1500, temperature=0.1)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        return {"answer": f"Error: {type(e).__name__}. LLM unavailable.", "sources": sources}
