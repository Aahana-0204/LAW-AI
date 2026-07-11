import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
)

import chromadb

from app.services.hf_embeddings import hf_ef

from data.corpus.civil_family_law import CIVIL_FAMILY_CORPUS
from data.corpus.constitutional_articles import CONSTITUTIONAL_CORPUS
from data.corpus.ipc_sections import IPC_CORPUS
from data.corpus.case_law import CASE_LAW_CORPUS


def ingest():
    persist_dir = os.path.abspath(os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"))
    os.makedirs(persist_dir, exist_ok=True)

    print(f"Initializing ChromaDB at {persist_dir}")
    client = chromadb.PersistentClient(path=persist_dir)

    try:
        client.delete_collection("lawai_corpus")
        print("Deleted existing collection")
    except Exception:
        pass

    collection = client.create_collection(
        name="lawai_corpus",
        embedding_function=hf_ef,
        metadata={"hnsw:space": "cosine"},
    )

    all_corpus = IPC_CORPUS + CONSTITUTIONAL_CORPUS + CIVIL_FAMILY_CORPUS + CASE_LAW_CORPUS

    ids = [doc["id"] for doc in all_corpus]
    docs = [doc["content"] for doc in all_corpus]
    metas = [
        {
            "title": doc["title"],
            "section": doc["section"],
            "domain": doc["domain"],
        }
        for doc in all_corpus
    ]

    batch_size = 10
    for i in range(0, len(all_corpus), batch_size):
        collection.add(
            documents=docs[i : i + batch_size],
            metadatas=metas[i : i + batch_size],
            ids=ids[i : i + batch_size],
        )
        print(
            f"Ingested batch {i // batch_size + 1}: "
            f"{min(i + batch_size, len(all_corpus))}/{len(all_corpus)}"
        )

    print(f"\nTotal documents ingested: {collection.count()}")
    print("Corpus ingestion complete!")


if __name__ == "__main__":
    ingest()
