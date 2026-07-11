#!/bin/bash
set -e

echo "============================================"
echo "  LAWAI Backend Starting..."
echo "============================================"

# Ingest legal corpus into ChromaDB if not already done
echo "Checking legal corpus..."
python - <<'PY'
import sys, os
os.chdir("/app")
sys.path.insert(0, "/app")

import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
try:
    col = client.get_collection("lawai_corpus")
    count = col.count()
    if count > 0:
        print(f"Corpus already ingested: {count} documents. Skipping.")
        sys.exit(0)
except Exception:
    pass

print("Ingesting legal corpus into ChromaDB...")
import subprocess
r = subprocess.run(["python", "scripts/ingest_corpus.py"], capture_output=True, text=True)
print(r.stdout[-500:] if r.stdout else "")
if r.returncode != 0:
    print("Warning during ingest:", r.stderr[-300:])
else:
    print("Corpus ingested successfully!")
PY

PORT="${PORT:-7860}"
echo "Starting gunicorn on port $PORT ..."
exec gunicorn \
    --workers 1 \
    --bind "0.0.0.0:${PORT}" \
    --timeout 300 \
    --keep-alive 5 \
    --preload \
    main:app
