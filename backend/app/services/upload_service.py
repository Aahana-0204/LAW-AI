import io
import hashlib
import math
import re
from collections import Counter
from datetime import datetime

from ..config import Config

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


def _extract_text(file_bytes, filename):
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            return "\n\n".join(page.extract_text() or "" for page in reader.pages).strip()
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


def _chunk_text(text, chunk_size=600, overlap=100):
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i: i + chunk_size]))
        i += chunk_size - overlap
    return chunks


def _tokenize(text):
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


def _search_chunks(chunks, query, n=5):
    q_tokens = _tokenize(query)
    if not q_tokens:
        return []
    tokenized = [_tokenize(c["text"]) for c in chunks]
    avg_dl = sum(len(t) for t in tokenized) / max(len(tokenized), 1)
    scored = []
    for i, (chunk, tokens) in enumerate(zip(chunks, tokenized)):
        score = _bm25_score(q_tokens, tokens, avg_dl)
        if score > 0:
            scored.append((score, i))
    scored.sort(reverse=True)
    if not scored:
        return []
    max_score = scored[0][0]
    results = []
    for score, idx in scored[:n]:
        c = chunks[idx]
        results.append({
            "text": c["text"],
            "chunk_index": c["chunk_index"],
            "relevance": round((score / max_score) * 100, 1),
        })
    return results


def ingest_document(user_id, file_bytes, filename):
    text = _extract_text(file_bytes, filename)
    if not text or len(text.strip()) < 50:
        raise ValueError("Document appears empty or unreadable.")
    doc_id = hashlib.md5(f"{user_id}:{filename}:{len(file_bytes)}".encode()).hexdigest()[:16]
    chunks_text = _chunk_text(text)
    chunks = [{"chunk_index": i, "text": c} for i, c in enumerate(chunks_text)]
    col = _docs_col()
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
    return {"doc_id": doc_id, "filename": filename, "chunks": len(chunks), "chars": len(text)}


def list_user_documents(user_id):
    col = _docs_col()
    try:
        docs = col.find(
            {"user_id": user_id},
            {"doc_id": 1, "filename": 1, "total_chunks": 1, "char_count": 1}
        ).sort("uploaded_at", -1)
        return [{
            "doc_id": d["doc_id"],
            "filename": d["filename"],
            "total_chunks": d.get("total_chunks", 0),
            "char_count": d.get("char_count", 0),
        } for d in docs]
    except Exception:
        return []


def delete_document(user_id, doc_id):
    col = _docs_col()
    r = col.delete_many({"doc_id": doc_id, "user_id": user_id})
    return r.deleted_count > 0


def query_user_documents(user_id, query, doc_id=None):
    col = _docs_col()
    filter_q = {"user_id": user_id}
    if doc_id:
        filter_q["doc_id"] = doc_id
    try:
        docs = list(col.find(filter_q))
    except Exception as e:
        return {"answer": f"Database error: {e}", "sources": []}
    if not docs:
        return {
            "answer": "No documents uploaded yet. Upload a PDF, DOCX, or TXT file first.",
            "sources": []
        }
    all_results = []
    for doc in docs:
        hits = _search_chunks(doc.get("chunks", []), query, n=3)
        for h in hits:
            h["filename"] = doc["filename"]
            h["doc_id"] = doc["doc_id"]
            all_results.append(h)
    all_results.sort(key=lambda x: x["relevance"], reverse=True)
    top = all_results[:5]
    if not top:
        return {
            "answer": "No relevant content found. Try rephrasing your question.",
            "sources": []
        }
    sources = [{
        "filename": r["filename"],
        "chunk": r["chunk_index"] + 1,
        "relevance": r["relevance"],
        "snippet": r["text"][:200] + "..." if len(r["text"]) > 200 else r["text"],
    } for r in top]
    answer = "## Document Analysis\n\n"
    answer += f"**Query:** {query}\n\n"
    answer += "**Relevant sections found:**\n\n"
    for i, r in enumerate(top[:3], 1):
        answer += f"### {i}. {r['filename']} (Relevance: {r['relevance']}%)\n"
        answer += r["text"][:500] + ("..." if len(r["text"]) > 500 else "") + "\n\n"
    answer += "\n---\nNote: Always verify with the original document."
    return {"answer": answer, "sources": sources}
