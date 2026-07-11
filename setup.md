# LAWAI Setup Guide

## Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB (optional — needed for chat history and auth)

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/Aahana-0204/LAW-AI.git
cd LAW-AI
```

### 2. Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY (free from https://aistudio.google.com/app/apikey)

pip install -r requirements.txt
python scripts/ingest_corpus.py  # One-time corpus setup
python main.py  # Starts on http://localhost:5000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev  # Starts on http://localhost:5173
```

## Getting Your Free Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into your `backend/.env` file

**Free tier limits:** 15 requests/minute, 1 million tokens/day — more than enough!

## MongoDB Setup (Optional)

Without MongoDB, LAWAI works in **guest mode** (no chat history, no auth).

**Option A — Local MongoDB:**
- Install [MongoDB Community](https://www.mongodb.com/try/download/community)
- Default URI: `mongodb://localhost:27017/lawai`

**Option B — MongoDB Atlas (Free Cloud):**
- Create free M0 cluster at [atlas.mongodb.com](https://www.mongodb.com/atlas)
- Get connection string and set as `MONGO_URI` in `.env`

## Architecture

```
Frontend (React/Vite) → Flask API → Gemini 1.5 Flash (LLM)
                                 → ChromaDB (Vector Search)
                                 → MongoDB (User Data)
```

## Project Structure

```
LAW-AI/
├── backend/
│   ├── app/
│   │   ├── models/       # MongoDB models (User)
│   │   ├── routes/       # API endpoints (auth, chat)
│   │   ├── services/     # RAG service, domain classifier
│   │   └── utils/        # Cache, helpers
│   ├── data/corpus/      # Legal corpus (IPC, Constitutional, Case Law)
│   ├── scripts/          # Corpus ingestion script
│   └── main.py           # Flask entry point
├── frontend/
│   ├── src/
│   │   ├── pages/        # React pages (Home, Chat, Experts)
│   │   ├── components/   # Reusable components (Navbar)
│   │   ├── context/      # Auth context
│   │   └── services/     # API service layer
│   └── index.html
└── setup.md              # This file
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `GEMINI_API_KEY` error | Ensure `.env` file exists with valid key |
| ChromaDB errors | Delete `chroma_db/` folder and re-run ingestion |
| MongoDB connection failed | Start MongoDB service or remove MONGO_URI for guest mode |
| Frontend can't reach backend | Ensure backend runs on port 5000 and CORS is configured |
| `sentence-transformers` slow first run | First run downloads ~90MB model — subsequent runs are cached |
