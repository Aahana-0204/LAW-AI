FROM python:3.11-slim

WORKDIR /app

# Minimal system deps (no C++ compiler needed anymore)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Create necessary directories
RUN mkdir -p chroma_db data/corpus

# HuggingFace Spaces uses port 7860
EXPOSE 7860

# Environment defaults for cloud deployment
ENV LLM_BACKEND=hf_api
ENV HF_MODEL=Qwen/Qwen2.5-72B-Instruct
ENV PORT=7860
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV CHROMA_PERSIST_DIR=/app/chroma_db
ENV CORPUS_DIR=/app/data/corpus

CMD ["bash", "startup.sh"]
