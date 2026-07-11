# ⚖️ LAWAI - AI Legal Assistant

LAWAI is a full-stack AI legal assistant focused on **Indian law**. It combines a Flask backend, a React + Vite frontend, a local ChromaDB vector store, local sentence-transformer embeddings, MongoDB-based user/chat storage, and **Google Gemini 1.5 Flash** for grounded legal responses with source attribution.

> **Important:** LAWAI provides legal information, not professional legal advice.

---

## ✨ Features

- **RAG-powered legal answers** over curated IPC, constitutional, civil, family, labour, corporate, property, and tax law content
- **Source attribution** with section/article titles, snippets, and relevance scoring
- **Domain-aware query routing** across 8 legal domains:
  - Criminal
  - Civil
  - Constitutional
  - Family
  - Property
  - Labour
  - Corporate
  - Tax
- **Expert Connect** flow for booking consultations with legal professionals
- **Authentication** with JWT-based login and registration
- **Chat history** persistence for signed-in users
- **Dark legal UI** with gold/amber accents
- **100% free-forever stack** using local embeddings + local vector DB + Gemini free tier

---

## 🧱 Tech Stack

### Frontend
- React 18
- Vite 5
- Tailwind CSS
- React Router
- Axios
- React Markdown

### Backend
- Python 3.12
- Flask
- Flask-CORS
- Flask-JWT-Extended
- PyMongo
- bcrypt
- python-dotenv

### AI / RAG
- Google Gemini 1.5 Flash via `google-generativeai`
- `sentence-transformers` with `all-MiniLM-L6-v2`
- ChromaDB (local persistent vector store)
- Custom RAG orchestration layer (no paid API dependency)

### Data
- MongoDB (local)
- Curated Indian legal corpus:
  - IPC sections
  - Constitutional articles
  - Civil / family / labour / corporate / tax references

---

## 📁 Project Structure

```text
LAW-AI/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── data/
│   │   └── corpus/
│   ├── scripts/
│   ├── .env.example
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 🚀 Setup Instructions

## 1) Clone the repository

```powershell
git clone <your-repo-url>
Set-Location LAW-AI
```

## 2) Backend setup

```powershell
Set-Location .\backend
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Update `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGO_URI=mongodb://localhost:27017/lawai
JWT_SECRET_KEY=your_super_secret_jwt_key_change_this
FLASK_ENV=development
FLASK_DEBUG=1
CHROMA_PERSIST_DIR=./chroma_db
CORPUS_DIR=./data/corpus
```

### Ingest the legal corpus

```powershell
python .\scripts\ingest_corpus.py
```

### Run the backend

```powershell
python .\main.py
```

Backend runs at: `http://localhost:5000`

---

## 3) Frontend setup

```powershell
Set-Location ..\frontend
npm install
npm run build
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 🔌 API Overview

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

### Chat
- `POST /api/chat/ask`
- `GET /api/chat/history/<session_id>`
- `GET /api/chat/sessions`

### Experts
- `GET /api/experts/`
- `POST /api/experts/book`

### Docs
- `GET /api/docs/domains`

### Health
- `GET /api/health`

---

## 🧠 How the RAG Flow Works

1. User submits a legal question
2. Backend classifies the likely legal domain
3. ChromaDB retrieves the most relevant legal passages
4. LAWAI sends the retrieved context to Gemini 1.5 Flash
5. The model returns a structured answer
6. UI displays the response along with source snippets and relevance scores

---

## 🖼️ Screenshots

> Add screenshots here after running the app locally.

- Landing page
- Chat interface with source citations
- Expert connect page
- Login / register flow

---

## 🌐 Live Demo

This project is currently configured for **local development**.  
You can deploy it later to a free-friendly environment after configuring MongoDB, the Gemini API key, and persistent storage for ChromaDB.

---

## 🛡️ Notes

- Uses the **Gemini free tier**
- Uses **local embeddings** to avoid paid embedding APIs
- Uses **local ChromaDB persistence**
- Uses **local MongoDB**
- Best suited for educational, portfolio, and prototype legal-assistant use cases

---

## 📄 License

MIT
