<div align="center">

<br/>

# ⚖️ LAWAI
### *Your AI-Powered Legal Companion for Indian Law*

<br/>

[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Free-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com/)

<br/>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![100% Free](https://img.shields.io/badge/Cost-100%25%20Free%20Forever-green?style=flat-square)](https://github.com/Aahana-0204/LAW-AI)
[![Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-4285F4?style=flat-square&logo=google&logoColor=white)](https://aistudio.google.com/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-orange?style=flat-square)](https://www.trychroma.com/)

<br/>

> **Get instant, cited answers on Indian law — IPC sections, constitutional rights, landmark case law, and more.**
> *Powered by RAG AI with full source attribution. 100% free, forever.*

<br/>

[🚀 **Quick Start**](#-quick-start) · [✨ **Features**](#-features) · [🏗️ **Architecture**](#️-architecture) · [📡 **API Docs**](#-api-reference) · [🤝 **Contribute**](#-contributing)

<br/>

---

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 AI & Intelligence
- **RAG Pipeline** — Retrieval-Augmented Generation over 35+ curated legal documents
- **Domain-Aware Routing** — Auto-detects Criminal, Civil, Constitutional, Family, Property, Labour, Corporate, or Tax law
- **Provenance-Based Answers** — Every response cites exact section numbers, article references, and case names
- **LRU Response Cache** — Instant replies for repeated queries
- **Retry Logic** — Graceful handling of API rate limits

</td>
<td width="50%">

### 🎨 User Experience
- **Stunning Dark UI** — Elegant dark theme with gold/amber accents
- **Chat Interface** — Copy answers, collapsible source citations, animated loading
- **Expert Connect** — Book consultations with 6+ verified lawyers
- **JWT Authentication** — Secure login with chat history persistence
- **Fully Responsive** — Works beautifully on mobile and desktop

</td>
</tr>
<tr>
<td>

### 📚 Legal Coverage
- **12 IPC Sections** — §302, §376, §420, §498A, §304B, §354, §307 and more
- **7 Constitutional Articles** — Art. 14, 19, 21, 32, 226, 44, 51A
- **8 Landmark SC Cases** — Maneka Gandhi, Kesavananda, Puttaswamy, Vishaka, Shah Bano and more
- **8 Civil/Family/Labour Domains** — Divorce, DV Act, Contracts, Consumer Protection, GST

</td>
<td>

### 🆓 100% Free Stack
- **Gemini 1.5 Flash** — 15 RPM, 1M tokens/day, no credit card
- **sentence-transformers** — Local embeddings, zero API cost
- **ChromaDB** — Local vector database, persists to disk
- **MongoDB** — Local or Atlas M0 free tier
- **No hidden costs** — Every dependency is free forever

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        LAWAI System                             │
│                                                                 │
│  ┌──────────────┐      ┌──────────────────────────────────┐    │
│  │   React UI   │ ───► │         Flask REST API            │    │
│  │  Vite 5      │      │   /api/chat  /api/auth            │    │
│  │  Tailwind    │      │   /api/experts  /api/docs         │    │
│  └──────────────┘      └──────────┬───────────────────────┘    │
│                                   │                             │
│                    ┌──────────────┼──────────────┐             │
│                    ▼              ▼              ▼             │
│             ┌────────────┐ ┌──────────┐ ┌───────────┐         │
│             │  ChromaDB  │ │  Gemini  │ │  MongoDB  │         │
│             │ (vectors)  │ │ 1.5 Flash│ │ (users +  │         │
│             │            │ │  (LLM)   │ │  chats)   │         │
│             └─────┬──────┘ └──────────┘ └───────────┘         │
│                   │                                             │
│             ┌─────▼──────────────────────────────┐            │
│             │      Legal Corpus (35+ docs)        │            │
│             │  IPC · Constitution · Cases ·       │            │
│             │  Civil · Family · Labour · Tax       │            │
│             └────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

### RAG Flow

```
User Query
    │
    ▼
Domain Classifier (keyword scoring → 8 legal domains)
    │
    ▼
ChromaDB Semantic Search (cosine similarity, top-5 docs)
    │
    ▼
Gemini 1.5 Flash (context + query → structured answer)
    │
    ▼
Response with Citations (section numbers + relevance scores)
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + Vite 5 | SPA with fast HMR |
| **Styling** | Tailwind CSS 3 | Dark gold theme |
| **Routing** | React Router 6 | SPA navigation |
| **HTTP** | Axios | API communication |
| **Markdown** | react-markdown | Formatted AI responses |
| **Backend** | Python 3.12 + Flask 3 | REST API server |
| **Auth** | Flask-JWT-Extended + bcrypt | Secure authentication |
| **LLM** | Google Gemini 1.5 Flash | AI text generation |
| **Embeddings** | sentence-transformers (MiniLM) | Local vector encoding |
| **Vector DB** | ChromaDB (persistent) | Semantic document search |
| **Database** | MongoDB + PyMongo | Users, chats, bookings |
| **Caching** | cachetools LRU | Response deduplication |

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version | Check |
|------|---------|-------|
| Python | 3.10+ | `python --version` |
| Node.js | 18+ | `node --version` |
| MongoDB | Any | `mongod --version` (optional) |

### 1️⃣ Clone

```bash
git clone https://github.com/Aahana-0204/LAW-AI.git
cd LAW-AI
```

### 2️⃣ Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# → Open .env and add your GEMINI_API_KEY
```

**Get your free Gemini API key:**
1. Visit [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with Google (no credit card required)
3. Click **"Create API Key"** and copy it into `.env`

```bash
# Ingest the legal corpus into ChromaDB (one-time)
python scripts/ingest_corpus.py

# Start the backend server
python main.py
# ✅ Running at http://localhost:5000
```

### 3️⃣ Frontend Setup

```bash
cd ../frontend

npm install
npm run dev
# ✅ Running at http://localhost:5173
```

**Open [http://localhost:5173](http://localhost:5173) and start asking legal questions!**

---

## 📡 API Reference

<details>
<summary><b>🔐 Authentication</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/auth/register` | Create account | No |
| `POST` | `/api/auth/login` | Login & get JWT | No |
| `GET` | `/api/auth/me` | Get current user | JWT |

**Register body:** `{ "name": "...", "email": "...", "password": "..." }`  
**Login body:** `{ "email": "...", "password": "..." }`

</details>

<details>
<summary><b>💬 Chat (RAG)</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/chat/ask` | Ask a legal question | Optional |
| `GET` | `/api/chat/history/<session_id>` | Get session messages | JWT |
| `GET` | `/api/chat/sessions` | List all sessions | JWT |

**Ask body:** `{ "query": "What is IPC Section 302?", "session_id": "uuid" }`

**Response:**
```json
{
  "answer": "## Legal Position\n...",
  "domain": "Criminal",
  "sources": [
    { "title": "IPC Section 302", "relevance": 94.2, "snippet": "..." }
  ],
  "session_id": "uuid"
}
```

</details>

<details>
<summary><b>👩‍⚖️ Experts</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/experts/` | List experts (filter by `?domain=`) | No |
| `POST` | `/api/experts/book` | Book consultation | JWT |

**Book body:** `{ "expert_id": "...", "date": "2024-12-25", "time_slot": "10:00 AM", "query_summary": "..." }`

</details>

<details>
<summary><b>📋 Misc</b></summary>

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/docs/domains` | List 8 legal domains |
| `GET` | `/api/health` | Health check |

</details>

---

## 📁 Project Structure

```
LAW-AI/
├── 📂 backend/
│   ├── 📂 app/
│   │   ├── 📂 models/          # user.py, chat.py, expert.py
│   │   ├── 📂 routes/          # auth.py, chat.py, expert.py, docs.py
│   │   ├── 📂 services/        # rag_service.py, domain_classifier.py
│   │   ├── 📂 utils/           # cache.py (LRU)
│   │   ├── __init__.py         # Flask app factory
│   │   └── config.py           # Environment config
│   ├── 📂 data/corpus/         # ipc_sections.py, constitutional_articles.py
│   │                           # civil_family_law.py, case_law.py
│   ├── 📂 scripts/
│   │   └── ingest_corpus.py    # One-time ChromaDB ingestion
│   ├── .env.example
│   ├── main.py                 # Entry point
│   └── requirements.txt
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   ├── layout/         # Navbar, ProtectedRoute
│   │   │   └── chat/           # Chat components
│   │   ├── 📂 context/         # AuthContext (JWT state)
│   │   ├── 📂 pages/           # HomePage, ChatPage, LoginPage
│   │   │                       # RegisterPage, ExpertsPage
│   │   ├── 📂 services/        # api.js (Axios instance)
│   │   ├── App.jsx             # Router + Toaster
│   │   └── index.css           # Tailwind + custom components
│   ├── vite.config.js          # API proxy to :5000
│   └── tailwind.config.js      # Dark gold theme
│
├── README.md
└── setup.md
```

---

## ⚖️ Legal Corpus

| Category | Documents | Coverage |
|----------|-----------|----------|
| 🔴 **IPC Sections** | 12 | §302 Murder, §376 Rape, §420 Fraud, §498A Cruelty, §304B Dowry, §354 Outraging Modesty, §307 Attempt to Murder, §406 Criminal Breach of Trust, §124A Sedition, §299 Culpable Homicide, §378 Theft, §320 Grievous Hurt |
| 🟣 **Constitutional Articles** | 7 | Art.14 Equality, Art.19 Six Freedoms, Art.21 Right to Life, Art.32 Remedies, Art.226 HC Writs, Art.44 UCC, Art.51A Duties |
| 🟢 **Civil & Family** | 8 | HMA §13 Divorce, DV Act 2005, Transfer of Property, Consumer Protection 2019, Indian Contract Act, Minimum Wages, Gratuity Act, GST Framework |
| 🔵 **Landmark Cases** | 8 | Maneka Gandhi (1978), Kesavananda (1973), Puttaswamy (2017), Vishaka (1997), Shah Bano (1985), Olga Tellis (1985), MC Mehta (1986+), Hussainara Khatoon (1979) |
| **Total** | **35+** | **8 Legal Domains** |

---

## 🌐 8 Legal Domains

| Domain | Emoji | Key Topics |
|--------|-------|------------|
| Criminal Law | ⚖️ | IPC, CrPC, bail, FIR, arrest, offenses |
| Civil Law | 📜 | Contracts, property disputes, torts |
| Constitutional | 🏛️ | Fundamental rights, PIL, writs |
| Family Law | 👨‍👩‍👧 | Divorce, custody, maintenance, dowry |
| Property Law | 🏠 | Land registration, tenancy, mortgage |
| Labour Law | 👷 | Employment, wages, PF, POSH Act |
| Corporate Law | 🏢 | Company law, SEBI, M&A, compliance |
| Tax Law | 💰 | Income Tax, GST, TDS, ITR |

---

## 🔒 Environment Variables

```env
# Required
GEMINI_API_KEY=          # From https://aistudio.google.com/app/apikey

# Optional (with defaults)
MONGO_URI=mongodb://localhost:27017/lawai
JWT_SECRET_KEY=change-this-in-production
FLASK_ENV=development
CHROMA_PERSIST_DIR=./chroma_db
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to help:

1. **Add more corpus** — Add IPC sections, case law, or new legal domains in `backend/data/corpus/`
2. **Improve UI** — Enhance the React frontend in `frontend/src/`
3. **Add features** — Document templates, legal news, multilingual support

```bash
# Fork → Clone → Create branch → Commit → Push → PR
git checkout -b feat/your-feature
git commit -m "feat: add ..."
git push origin feat/your-feature
```

---

## ⚠️ Disclaimer

> LAWAI provides **general legal information** for educational purposes only. It is **not a substitute for professional legal advice**. For specific legal matters, always consult a qualified and licensed lawyer. The information provided may not reflect the most recent legal developments.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for Indian legal empowerment**

*Making legal knowledge accessible to everyone, everywhere — completely free.*

<br/>

⭐ **Star this repo if you found it useful!** ⭐

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-Aahana--0204-181717?style=for-the-badge&logo=github)](https://github.com/Aahana-0204)

</div>
