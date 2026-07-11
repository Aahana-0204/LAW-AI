import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
)

import chromadb
from chromadb.utils import embedding_functions

from data.corpus.civil_family_law import CIVIL_FAMILY_CORPUS
from data.corpus.constitutional_articles import CONSTITUTIONAL_CORPUS
from data.corpus.ipc_sections import IPC_CORPUS


def ingest():
    persist_dir = os.path.abspath(os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"))
    os.makedirs(persist_dir, exist_ok=True)

    print(f"Initializing ChromaDB at {persist_dir}")
    client = chromadb.PersistentClient(path=persist_dir)

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    try:
        client.delete_collection("lawai_corpus")
        print("Deleted existing collection")
    except Exception:
        pass

    collection = client.create_collection(
        name="lawai_corpus",
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"},
    )

    all_corpus = IPC_CORPUS + CONSTITUTIONAL_CORPUS + CIVIL_FAMILY_CORPUS

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

    collection.add(documents=docs, metadatas=metas, ids=ids)
    print(f"Ingested {len(all_corpus)} legal documents into ChromaDB")
    print(f"Collection count: {collection.count()}")


if __name__ == "__main__":
    ingest()
