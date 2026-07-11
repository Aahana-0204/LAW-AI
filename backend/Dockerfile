FROM python:3.11-slim

WORKDIR /app

# System deps for llama-cpp-python compilation + sentence-transformers
RUN apt-get update && apt-get install -y \
    gcc g++ cmake make git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install llama-cpp-python pre-built CPU wheel (faster than compiling)
RUN pip install --no-cache-dir \
    "llama-cpp-python==0.2.90" \
    --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu \
    || pip install --no-cache-dir "llama-cpp-python==0.2.90"

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Create necessary directories
RUN mkdir -p chroma_db data/corpus

# HuggingFace Spaces uses port 7860
EXPOSE 7860

# Environment defaults for cloud deployment
ENV LLM_BACKEND=local
ENV LLM_MODEL_REPO=Qwen/Qwen2.5-3B-Instruct-GGUF
ENV LLM_MODEL_FILE=qwen2.5-3b-instruct-q4_k_m.gguf
ENV LLM_THREADS=2
ENV LLM_N_CTX=4096
ENV PORT=7860
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV CHROMA_PERSIST_DIR=/app/chroma_db
ENV CORPUS_DIR=/app/data/corpus

CMD ["bash", "startup.sh"]
