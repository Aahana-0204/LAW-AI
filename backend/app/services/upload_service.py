import io
import os
import hashlib

import chromadb
from chromadb.utils import embedding_functions

from ..config import Config

_chroma_client = None
_user_collection = None


def _get_user_collection():
    global _chroma_client, _user_collection
    if _user_collection is not None:
        return _user_collection
    persist_dir = os.path.abspath(Config.CHROMA_PERSIST_DIR)
    os.makedirs(persist_dir, exist_ok=True)
    _chroma_client = chromadb.PersistentClient(path=persist_dir)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    _user_collection = _chroma_client.get_or_create_collection(
        name="user_documents",
        embedding_function=ef,
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
