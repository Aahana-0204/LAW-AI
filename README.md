<div align="center">

<br/>

# ⚖️ LAWAI
### *AI-Powered Legal Assistant for Indian Law*

<br/>

[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com/atlas)

<br/>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-frontend--lilac--five--64.vercel.app-gold?style=for-the-badge)](https://frontend-lilac-five-64.vercel.app)
[![Backend API](https://img.shields.io/badge/⚡_Backend_API-backend--zeta--one--95.vercel.app-blue?style=for-the-badge)](https://backend-zeta-one-95.vercel.app/api/health)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![100% Free Forever](https://img.shields.io/badge/Cost-100%25%20Free%20Forever-brightgreen?style=flat-square)](https://github.com/Aahana-0204/LAW-AI)

<br/>

> **Chat with Indian law · Analyze your legal documents · Generate professional legal docs — all for free, forever.**
> *Powered by BM25 RAG + Knowledge-Grounded Response Engine. No paid API keys. No billing. No limits.*

<br/>

### 🌐 Live Deployment

| Service | URL |
|---|---|
| 🖥️ **Frontend** | https://frontend-lilac-five-64.vercel.app |
| ⚙️ **Backend API** | https://backend-zeta-one-95.vercel.app |
| 💚 **Health Check** | https://backend-zeta-one-95.vercel.app/api/health |

<br/>

[🚀 **Quick Start**](#-quick-start) · [✨ **Features**](#-features) · [🏗️ **Architecture**](#️-architecture) · [📡 **API Docs**](#-api-reference) · [🔄 **RAG Pipeline**](#-rag-pipeline)

<br/>

---

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 AI Legal Chat
- **RAG Pipeline** — BM25 retrieval over 72 curated Indian legal documents
- **Direct Section Lookup** — "IPC 302" → exact match (100% accurate)
- **Domain-Aware Routing** — Auto-detects Criminal, Civil, Constitutional, Family, Property, Labour, Corporate, Tax law
- **Intent Detection** — Understands punishment / procedure / rights / definition queries
- **Step-by-Step Guides** — FIR, bail, divorce, cheque bounce, consumer complaint
- **Hallucination Guard** — Blocks out-of-domain queries (cricket, weather, etc.)
- **Chat History** — Saved to MongoDB when logged in

</td>
<td width="50%">

### 📄 Document Upload & Analysis
- **Upload Your Docs** — PDF, DOCX, or TXT legal files
- **AI-Powered Q&A** — Ask questions about your own contracts, notices, agreements
- **Multi-Doc Search** — Query across all your documents
- **Secure Storage** — Per-user document isolation

</td>
</tr>
<tr>
<td>

### ⚖️ Legal Document Generator
- **10 Complete Templates** — Rental Agreement, NDA, Employment Contract, Legal Notice, Affidavit, Power of Attorney, FIR Complaint, Consumer Complaint, RTI Application, Will & Testament
- **Field Substitution** — Fill in details → get a complete professional document instantly
- **Custom Prompts** — Describe any document in plain English
- **Indian Law Standards** — All docs reference correct Indian statutes, signature blocks, witness blocks, disclaimers
- **Copy & Download** — Export as `.txt` in one click

</td>
<td>

### 🆓 100% Free Tech Stack
- **No LLM API needed** — Knowledge-Grounded Response Engine (no OpenAI, no Groq, no Gemini)
- **BM25 Search** — Zero-dependency keyword retrieval
- **MongoDB Atlas M0** — Free database tier
- **Vercel Free Tier** — Both frontend and backend deployed free
- **No hidden costs** — Works 100% on free tiers forever

</td>
</tr>
<tr>
<td>

### 🎨 Beautiful UI
- **Dark Gold Theme** — Elegant dark UI with gold/amber accents
- **Animated Chat** — Typing indicators, copy button, collapsible sources
- **Fully Responsive** — Mobile and desktop optimized
- **Hot Toast Notifications** — Clean success/error feedback

</td>
<td>

### 📚 Legal Coverage
- **72 Legal Documents** — IPC, Constitution, Family, Case Law
- **8 Legal Domains** — Criminal, Constitutional, Civil, Family, Property, Labour, Corporate, Tax
- **Landmark SC Cases** — Maneka Gandhi, Kesavananda, Puttaswamy, Vishaka, Shah Bano…
- **Procedure Guides** — 8 step-by-step legal how-to guides

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              LAWAI System                               │
│                                                                         │
│  ┌─────────────────────┐         ┌──────────────────────────────────┐  │
│  │  React 18 Frontend  │ ──────► │      Flask 3 REST API             │  │
│  │  Vite + Tailwind    │         │  /api/chat  /api/auth             │  │
│  │  Vercel (Free)      │         │  /api/docs  /api/generate         │  │
│  │                     │         │  /api/experts  /api/health        │  │
│  │  Pages:             │         │  Vercel Serverless (Free)         │  │
│  │  ├── / Home         │         └──────────────┬───────────────────┘  │
│  │  ├── /chat          │                         │                      │
│  │  ├── /documents     │          ┌──────────────┼──────────┐           │
│  │  ├── /generate      │          ▼              ▼          ▼           │
│  │  ├── /experts       │     ┌─────────┐  ┌──────────┐ ┌────────┐      │
│  │  ├── /login         │     │  BM25   │  │Template  │ │MongoDB │      │
│  │  └── /register      │     │ Search  │  │ Engine   │ │ Atlas  │      │
│  └─────────────────────┘     │ (RAG)   │  │(Generate)│ │  M0    │      │
│                               └────┬────┘  └──────────┘ └────────┘      │
│                                    │                                     │
│                      ┌─────────────┴──────────────────┐                 │
│                      │     Legal Corpus (72 docs)      │                 │
│                      │  IPC · Constitution · Cases ·   │                 │
│                      │  Civil · Family · Labour · Tax  │                 │
│                      └─────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 RAG Pipeline

> **RAG = Retrieval Augmented Generation**
> Retrieve relevant legal documents first → generate answer FROM those documents → prevents hallucination

```
User Query: "What is punishment for IPC 302?"
         │
         ▼
┌─────────────────────────┐
│   Domain Classifier     │ → "Criminal"
│   (keyword matching)    │   (8 legal domains)
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Out-of-Domain Guard   │ → "cricket score?" → BLOCKED ❌
│   (hallucination guard) │ → "IPC 302?"      → ALLOWED ✅
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│      RETRIEVAL          │
│                         │
│  Stage 1: Direct Lookup │ → "IPC 302" → regex extracts section number
│  (exact section match)  │   → finds "IPC Section 302" → relevance: 100%
│                         │
│  Stage 2: BM25 Search   │ → tokenize → score 72 docs → top 5 results
│  (keyword ranking)      │   → 3× boost if section number in title
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│      GENERATION         │
│                         │
│  Intent Detection:      │
│  "punishment" queries   │ → extract punishment sentences from doc
│  "procedure" queries    │ → return step-by-step guide
│  "definition" queries   │ → show full section content
│  "rights" queries       │ → extract rights-related sentences
│                         │
│  Template Engine        │ → format structured markdown answer
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Structured Response    │ → ## ⚖️ IPC Section 302...
│  + Sources cited        │ → sources: [{title, relevance}]
│  + Domain label         │ → domain: "Criminal"
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│  MongoDB Save           │ → chats collection (if logged in)
│  (chat history)         │ → user_id, session_id, timestamp
└─────────────────────────┘
```

### Why BM25 instead of Vector Embeddings?

| | Vector DB (ChromaDB) | BM25 (Our Approach) |
|---|---|---|
| **Accuracy for exact sections** | May miss "IPC 302" exactly | Direct lookup = 100% |
| **Setup** | 600MB+ dependencies | Zero dependencies |
| **Startup time** | 10-30 seconds | Instant |
| **Vercel compatible** | ❌ Too heavy | ✅ Works perfectly |
| **Cost** | Paid embedding API or heavy local model | Free forever |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | React 18 + Vite 5 | SPA with fast HMR |
| **Styling** | Tailwind CSS 3 | Dark gold custom theme |
| **Routing** | React Router 6 | SPA navigation |
| **HTTP Client** | Axios + JWT interceptor | API communication with auto auth |
| **Backend** | Python 3.12 + Flask 3 | REST API server |
| **Auth** | Flask-JWT-Extended + bcrypt | Secure JWT authentication |
| **RAG Retrieval** | Custom BM25 (zero deps) | Keyword search over legal corpus |
| **Generation** | Template Engine (zero deps) | Intent-aware answer synthesis |
| **Document Gen** | Pure Python templates | 10 complete Indian legal documents |
| **Database** | MongoDB Atlas M0 + PyMongo | Users, chats, experts |
| **Caching** | cachetools LRU | Response deduplication |
| **Deployment** | Vercel (frontend + backend) | 100% free hosting |

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version | Install |
|---|---|---|
| Python | 3.10+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| MongoDB | Optional | [MongoDB Atlas](https://mongodb.com/atlas) free M0 |

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
# Edit .env and set MONGO_URI (optional) and JWT_SECRET_KEY

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

**Open [http://localhost:5173](http://localhost:5173) — LAWAI is live!**

---

## 📡 API Reference

Base URL (Production): `https://backend-zeta-one-95.vercel.app`

<details>
<summary><b>🔐 Authentication</b></summary>

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/api/auth/register` | Create account | No |
| `POST` | `/api/auth/login` | Login & get JWT | No |
| `GET` | `/api/auth/me` | Get current user | JWT |

**Register:**
```json
{ "name": "Aahana Shukla", "email": "user@example.com", "password": "yourpassword" }
```

</details>

<details>
<summary><b>💬 Chat (RAG)</b></summary>

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/api/chat/ask` | Ask a legal question | Optional |
| `GET` | `/api/chat/history/<session_id>` | Get session messages | JWT |
| `GET` | `/api/chat/sessions` | List all sessions | JWT |

**Request:**
```json
{ "query": "What is IPC Section 302?", "session_id": "uuid-optional" }
```

**Response:**
```json
{
  "answer": "## ⚖️ IPC Section 302 - Punishment for Murder\n\nWhoever commits murder...",
  "domain": "Criminal",
  "sources": [
    { "title": "IPC Section 302", "relevance": 100.0, "section": "Section 302" }
  ],
  "session_id": "9ad2731b-dae8-4c8e-aaa1-4a17dfc16dda"
}
```

</details>

<details>
<summary><b>📄 Document Upload & Analysis</b></summary>

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/api/docs/upload` | Upload PDF/DOCX/TXT | Optional |
| `GET` | `/api/docs/documents` | List your documents | Optional |
| `DELETE` | `/api/docs/documents/<doc_id>` | Delete a document | Optional |
| `POST` | `/api/docs/query` | Ask AI about your docs | Optional |

**Upload:** `multipart/form-data` with `file` field

</details>

<details>
<summary><b>⚖️ Document Generator</b></summary>

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/api/generate/templates` | List 10 legal templates | No |
| `POST` | `/api/generate/document` | Generate legal document | Optional |

**Template-based request:**
```json
{
  "template_id": "rental_agreement",
  "fields": {
    "landlord_name": "Rahul Sharma",
    "tenant_name": "Priya Patel",
    "property_address": "123 MG Road, Mumbai",
    "rent_amount": "25000",
    "duration": "11 months",
    "city": "Mumbai"
  }
}
```

**Custom prompt request:**
```json
{
  "template_id": "custom",
  "custom_prompt": "Generate a rental agreement for a 2BHK flat in Delhi..."
}
```

</details>

<details>
<summary><b>🔍 Debug & Health</b></summary>

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/debug/db` | MongoDB connection status |

</details>

---

## 📁 Project Structure

```
LAW-AI/
├── 📂 backend/
│   ├── 📂 api/
│   │   └── index.py               # Vercel WSGI entry point
│   ├── 📂 app/
│   │   ├── 📂 models/
│   │   │   ├── user.py            # MongoDB users (lazy connection)
│   │   │   ├── chat.py            # MongoDB chats
│   │   │   └── expert.py          # MongoDB experts
│   │   ├── 📂 routes/
│   │   │   ├── auth.py            # Register, Login, Me
│   │   │   ├── chat.py            # Ask, History, Sessions
│   │   │   ├── docs.py            # Document query
│   │   │   ├── upload.py          # File upload
│   │   │   ├── generate.py        # Document generation
│   │   │   └── expert.py          # Experts & booking
│   │   ├── 📂 services/
│   │   │   ├── rag_service.py         # ← Main RAG pipeline
│   │   │   ├── corpus_search.py       # ← BM25 + Direct section lookup
│   │   │   ├── domain_classifier.py   # ← 8-domain legal classifier
│   │   │   ├── template_engine.py     # ← Intent-aware answer generator
│   │   │   ├── doc_generator_service.py # ← 10 legal document templates
│   │   │   └── upload_service.py      # ← Document upload handler
│   │   ├── 📂 utils/
│   │   │   └── cache.py               # LRU response cache
│   │   ├── __init__.py                # Flask app factory
│   │   └── config.py                  # Environment config
│   ├── 📂 data/corpus/
│   │   ├── ipc_sections.py            # IPC 302, 376, 420, 498A...
│   │   ├── constitutional_articles.py # Article 14, 19, 21, 32...
│   │   ├── civil_family_law.py        # HMA, DV Act, Consumer...
│   │   └── case_law.py                # Landmark SC judgments
│   ├── vercel.json                    # Vercel deployment config
│   ├── .python-version                # Python 3.12
│   ├── requirements.txt
│   └── main.py
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 components/layout/
│   │   │   └── Navbar.jsx
│   │   ├── 📂 context/
│   │   │   └── AuthContext.jsx        # JWT auth state
│   │   ├── 📂 pages/
│   │   │   ├── HomePage.jsx           # Landing page
│   │   │   ├── ChatPage.jsx           # AI legal chat
│   │   │   ├── UploadPage.jsx         # Document upload & analysis
│   │   │   ├── GeneratePage.jsx       # Legal document generator
│   │   │   ├── ExpertsPage.jsx        # Find lawyers
│   │   │   ├── LoginPage.jsx
│   │   │   └── RegisterPage.jsx
│   │   ├── 📂 services/
│   │   │   └── api.js                 # Axios + JWT interceptor
│   │   ├── App.jsx
│   │   └── index.css                  # Tailwind + dark gold theme
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md
```

---

## 📚 Legal Corpus (72 Documents)

| Category | Count | Coverage |
|---|---|---|
| 🔴 **IPC Sections** | 20+ | §34, §120B, §124A, §141, §191, §299, §300, §302, §304, §304B, §307, §319, §320, §323, §325, §326, §354, §363, §375, §376... |
| 🟣 **Constitutional Articles** | 8 | Art.14 Equality · Art.19 Six Freedoms · Art.21 Right to Life · Art.22 Arrest · Art.32 Remedies · Art.39A Legal Aid · Art.44 UCC · Art.51A Duties |
| 🟢 **Civil & Family Law** | 20+ | HMA Divorce · DV Act 2005 · Transfer of Property · Consumer Protection 2019 · Contract Act · Minimum Wages · Gratuity · GST · RTI · NI Act §138 |
| 🔵 **Landmark SC Cases** | 10+ | Maneka Gandhi · Kesavananda · Puttaswamy · Vishaka · Shah Bano · Olga Tellis · MC Mehta · Hussainara Khatoon · K.M. Nanavati · Bachan Singh |

---

## 📋 Document Templates

| Template | Key Indian Law |
|---|---|
| 🏠 Rental Agreement | Transfer of Property Act, 1882; Rent Control Acts |
| 🔒 Non-Disclosure Agreement | Indian Contract Act, 1872 |
| 💼 Employment Contract | Industrial Disputes Act, 1947; Shops & Establishments Act |
| 📮 Legal Notice | CPC Order XXI; specific applicable statutes |
| ✍️ Affidavit | Oaths Act, 1969; Indian Evidence Act, 1872 |
| ⚖️ Power of Attorney | Powers of Attorney Act, 1882 |
| 🚔 FIR / Police Complaint | CrPC Section 154; Bharatiya Nagarik Suraksha Sanhita |
| 🛒 Consumer Complaint | Consumer Protection Act, 2019 |
| 📋 RTI Application | Right to Information Act, 2005 |
| 📜 Last Will & Testament | Indian Succession Act, 1925 |

---

## 🔒 Environment Variables

```env
# MongoDB (required for auth & chat history)
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/lawai

# Auth (change in production!)
JWT_SECRET_KEY=your-secret-key-here

# LLM Backend (default: template — no API key needed)
# Options: template | groq | gemini | ollama | hf_api
LLM_BACKEND=template

# Optional: Enable real LLM (get free key from console.groq.com)
# GROQ_API_KEY=gsk_xxxx
# LLM_BACKEND=groq

# Optional: Google Gemini (free at aistudio.google.com)
# GEMINI_API_KEY=xxxx
# LLM_BACKEND=gemini

# Optional: Local Ollama
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=mistral
# LLM_BACKEND=ollama

# Flask
FLASK_ENV=production
FLASK_DEBUG=0

# CORS (add your frontend URL)
CORS_ORIGINS=https://frontend-lilac-five-64.vercel.app,http://localhost:5173
```

---

## 🚀 Deployment (Vercel — Free)

### Backend

```bash
cd backend
npm i -g vercel
vercel --prod
# Set env vars in Vercel dashboard or via CLI
```

### Frontend

```bash
cd frontend
# Set VITE_API_URL=https://your-backend.vercel.app in Vercel env vars
vercel --prod
```

### MongoDB Atlas (Free M0)

1. Create free cluster at [cloud.mongodb.com](https://cloud.mongodb.com)
2. Network Access → Add IP → `0.0.0.0/0` (allow all)
3. Create database user
4. Copy connection string → set as `MONGO_URI` in Vercel

---

## ⚠️ Disclaimer

> LAWAI provides **general legal information** for educational purposes only. It is **not a substitute for professional legal advice**. For specific legal matters, always consult a qualified advocate registered with the Bar Council of India. AI-generated documents should be reviewed by a lawyer before use.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ for Indian legal empowerment**

*Making legal knowledge accessible to everyone — completely free, forever.*

<br/>

⭐ **Star this repo if you found it useful!** ⭐

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-Aahana--0204-181717?style=for-the-badge&logo=github)](https://github.com/Aahana-0204)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Visit_Now-gold?style=for-the-badge)](https://frontend-lilac-five-64.vercel.app)

</div>

<br/>

[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Mistral_7B-FF6600?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com/)

<br/>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![100% Free Forever](https://img.shields.io/badge/Cost-100%25%20Free%20Forever-brightgreen?style=flat-square&logo=opensourceinitiative)](https://github.com/Aahana-0204/LAW-AI)
[![No API Key](https://img.shields.io/badge/API%20Key-Not%20Required-success?style=flat-square)](https://ollama.com/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-orange?style=flat-square)](https://www.trychroma.com/)
[![Offline](https://img.shields.io/badge/Runs-100%25%20Offline-blueviolet?style=flat-square)](https://ollama.com/)

<br/>

> **Chat with Indian law · Analyze your legal documents · Generate professional legal docs — all for free, forever.**
> *Powered by local Mistral 7B via Ollama + RAG. No API keys. No billing. No limits.*

<br/>

[🚀 **Quick Start**](#-quick-start) · [✨ **Features**](#-features) · [🏗️ **Architecture**](#️-architecture) · [📡 **API Docs**](#-api-reference) · [🤝 **Contribute**](#-contributing)

<br/>

---

</div>

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 AI Legal Chat
- **RAG Pipeline** — Retrieval-Augmented Generation over 35+ curated legal documents
- **Domain-Aware Routing** — Auto-detects Criminal, Civil, Constitutional, Family, Property, Labour, Corporate, or Tax law
- **Cited Answers** — Every response references exact section numbers, article references, and landmark case names
- **LRU Response Cache** — Instant replies for repeated queries
- **Conversation History** — Context-aware multi-turn chat

</td>
<td width="50%">

### 📄 Document Upload & Analysis *(New!)*
- **Upload Your Docs** — Drag & drop PDF, DOCX, or TXT legal files (up to 10 MB)
- **Vector Indexing** — Documents chunked and indexed into ChromaDB
- **AI-Powered Q&A** — Ask questions about your own contracts, notices, agreements
- **Multi-Doc Search** — Query across all your documents or focus on one
- **Instant Delete** — Remove documents anytime

</td>
</tr>
<tr>
<td>

### ⚖️ Legal Document Generator *(New!)*
- **10 Ready Templates** — Rental Agreement, NDA, Employment Contract, Legal Notice, Affidavit, Power of Attorney, FIR Complaint, Consumer Complaint, RTI Application, Will & Testament
- **Custom Prompts** — Describe any document in plain English
- **Indian Law Standards** — All docs reference applicable Indian statutes
- **Copy & Download** — Export as `.txt` in one click
- **Complete Drafts** — Signature blocks, numbered clauses, disclaimers

</td>
<td>

### 🆓 100% Free Tech Stack
- **Ollama + Mistral 7B** — Local LLM, no API key, no rate limits, runs offline
- **sentence-transformers** — Local embeddings (all-MiniLM-L6-v2)
- **ChromaDB** — Local persistent vector database
- **No hidden costs** — Every dependency is free forever
- **MongoDB Optional** — Falls back gracefully without it

</td>
</tr>
<tr>
<td>

### 🎨 Beautiful UI
- **Dark Gold Theme** — Elegant dark UI with gold/amber accents
- **Animated Chat** — Typing dots, copy button, collapsible sources
- **Drag & Drop Upload** — Visual upload zone with live feedback
- **Fully Responsive** — Mobile and desktop optimized
- **Hot Toast Notifications** — Clean success/error feedback

</td>
<td>

### 📚 Legal Coverage
- **12 IPC Sections** — §302, §376, §420, §498A, §304B and more
- **7 Constitutional Articles** — Art. 14, 19, 21, 32, 226, 44, 51A
- **8 Landmark SC Cases** — Maneka Gandhi, Kesavananda, Puttaswamy, Vishaka, Shah Bano…
- **8 Civil/Family/Labour Domains** — Divorce, DV Act, Consumer Protection, GST

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                           LAWAI System                               │
│                                                                      │
│  ┌───────────────────┐        ┌───────────────────────────────────┐  │
│  │    React 18 UI    │  ────► │         Flask 3 REST API           │  │
│  │  Vite + Tailwind  │        │  /api/chat  /api/auth              │  │
│  │                   │        │  /api/docs  /api/generate          │  │
│  │  Pages:           │        │  /api/experts  /api/health         │  │
│  │  ├── / Home       │        └────────────┬──────────────────────┘  │
│  │  ├── /chat        │                     │                         │
│  │  ├── /documents   │      ┌──────────────┼────────────┐            │
│  │  ├── /generate    │      ▼              ▼            ▼            │
│  │  └── /experts     │  ┌────────┐  ┌──────────┐ ┌──────────┐       │
│  └───────────────────┘  │Chroma  │  │  Ollama  │ │ MongoDB  │       │
│                          │  DB   │  │ Mistral  │ │(optional)│       │
│                          │(RAG + │  │   7B     │ │          │       │
│                          │ User  │  │ (local)  │ │          │       │
│                          │ Docs) │  └──────────┘ └──────────┘       │
│                          └───┬───┘                                   │
│                              │                                       │
│              ┌───────────────┴──────────────────┐                   │
│              │         Legal Corpus (35+ docs)   │                   │
│              │  IPC · Constitution · Cases ·     │                   │
│              │  Civil · Family · Labour · Tax    │                   │
│              │                    +              │                   │
│              │      User Uploaded Documents      │                   │
│              │   (PDF · DOCX · TXT — per user)   │                   │
│              └──────────────────────────────────┘                   │
└──────────────────────────────────────────────────────────────────────┘
```

### RAG Flow

```
User Query
    │
    ▼
Domain Classifier  ──►  8 Legal Domains (Criminal / Civil / Constitutional…)
    │
    ▼
ChromaDB Semantic Search  ──►  cosine similarity, top-5 chunks
    │
    ▼
Ollama Mistral 7B  ──►  context + structured prompt → formatted answer
    │
    ▼
Response with Citations  ──►  section numbers + relevance scores
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + Vite 5 | SPA with fast HMR |
| **Styling** | Tailwind CSS 3 | Dark gold custom theme |
| **Routing** | React Router 6 | SPA navigation |
| **HTTP** | Axios | API communication |
| **Backend** | Python 3.12 + Flask 3 | REST API server |
| **Auth** | Flask-JWT-Extended + bcrypt | Secure JWT authentication |
| **LLM** | Ollama + Mistral 7B (local) | AI text generation — free, offline |
| **Embeddings** | sentence-transformers MiniLM | Local vector encoding |
| **Vector DB** | ChromaDB (persistent) | Semantic search for corpus + user docs |
| **Database** | MongoDB + PyMongo | Users, chats, bookings (optional) |
| **Caching** | cachetools LRU | Response deduplication |
| **File Parsing** | pypdf + python-docx | PDF and DOCX extraction |

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.10+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| Ollama | Any | [ollama.com](https://ollama.com) |

### 1️⃣ Clone

```bash
git clone https://github.com/Aahana-0204/LAW-AI.git
cd LAW-AI
```

### 2️⃣ Install Ollama & Pull Model

```bash
# Download Ollama from https://ollama.com and install
# Then pull the Mistral model (one-time, ~4 GB):
ollama pull mistral

# Start Ollama server
ollama serve
```

### 3️⃣ Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment (no API key needed!)
cp .env.example .env
# .env is ready to use — no changes required for local dev

# Ingest legal corpus into ChromaDB (one-time)
python scripts/ingest_corpus.py

# Start the backend server
python main.py
# ✅ Running at http://localhost:5000
```

### 4️⃣ Frontend Setup

```bash
cd ../frontend

npm install
npm run dev
# ✅ Running at http://localhost:5173
```

**Open [http://localhost:5173](http://localhost:5173) — LAWAI is live!**

---

## 📡 API Reference

<details>
<summary><b>🔐 Authentication</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/auth/register` | Create account | No |
| `POST` | `/api/auth/login` | Login & get JWT | No |
| `GET` | `/api/auth/me` | Get current user | JWT |

**Register:** `{ "name": "...", "email": "...", "password": "..." }`

</details>

<details>
<summary><b>💬 Chat (RAG)</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/chat/ask` | Ask a legal question | Optional |
| `GET` | `/api/chat/history/<session_id>` | Get session messages | JWT |
| `GET` | `/api/chat/sessions` | List all sessions | JWT |

**Request:**
```json
{ "query": "What is IPC Section 302?", "session_id": "uuid" }
```
**Response:**
```json
{
  "answer": "## Legal Position\n...",
  "domain": "Criminal",
  "sources": [{ "title": "IPC Section 302", "relevance": 94.2, "snippet": "..." }],
  "session_id": "uuid"
}
```

</details>

<details>
<summary><b>📄 Document Upload & Analysis (New!)</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/docs/upload` | Upload PDF/DOCX/TXT | Optional |
| `GET` | `/api/docs/documents` | List your documents | Optional |
| `DELETE` | `/api/docs/documents/<doc_id>` | Delete a document | Optional |
| `POST` | `/api/docs/query` | Ask AI about your docs | Optional |

**Upload:** `multipart/form-data` with `file` field

**Query:**
```json
{ "query": "What are the termination clauses?", "doc_id": "optional-filter" }
```

</details>

<details>
<summary><b>⚖️ Document Generator (New!)</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/generate/templates` | List 10 legal templates | No |
| `POST` | `/api/generate/document` | Generate legal document | Optional |

**Template-based:**
```json
{
  "template_id": "rental_agreement",
  "fields": {
    "landlord_name": "Rahul Sharma",
    "tenant_name": "Priya Patel",
    "property_address": "123 MG Road, Mumbai",
    "rent_amount": "25000",
    "duration": "11 months",
    "city": "Mumbai"
  }
}
```
**Custom prompt:**
```json
{
  "template_id": "custom",
  "custom_prompt": "Generate an NDA between two tech startups..."
}
```

</details>

<details>
<summary><b>👩‍⚖️ Experts & Misc</b></summary>

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/experts/` | List experts (`?domain=`) | No |
| `POST` | `/api/experts/book` | Book consultation | JWT |
| `GET` | `/api/docs/domains` | List 8 legal domains | No |
| `GET` | `/api/health` | Health check | No |

</details>

---

## 📁 Project Structure

```
LAW-AI/
├── 📂 backend/
│   ├── 📂 app/
│   │   ├── 📂 models/             # user.py, chat.py, expert.py
│   │   ├── 📂 routes/             # auth.py, chat.py, expert.py
│   │   │                          # docs.py, upload.py, generate.py
│   │   ├── 📂 services/           # rag_service.py
│   │   │                          # upload_service.py  ← Document RAG
│   │   │                          # doc_generator_service.py  ← Generator
│   │   │                          # domain_classifier.py
│   │   ├── 📂 utils/              # cache.py (LRU)
│   │   ├── __init__.py            # Flask app factory
│   │   └── config.py              # Environment config
│   ├── 📂 data/corpus/            # ipc_sections.py
│   │                              # constitutional_articles.py
│   │                              # civil_family_law.py, case_law.py
│   ├── 📂 scripts/
│   │   └── ingest_corpus.py       # One-time ChromaDB ingestion
│   ├── .env.example
│   ├── main.py
│   └── requirements.txt
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 components/layout/  # Navbar.jsx
│   │   ├── 📂 context/            # AuthContext.jsx
│   │   ├── 📂 pages/
│   │   │   ├── HomePage.jsx       # Landing page
│   │   │   ├── ChatPage.jsx       # AI legal chat
│   │   │   ├── UploadPage.jsx     # ← Document upload & analysis
│   │   │   ├── GeneratePage.jsx   # ← Legal document generator
│   │   │   ├── ExpertsPage.jsx    # Find lawyers
│   │   │   ├── LoginPage.jsx
│   │   │   └── RegisterPage.jsx
│   │   ├── 📂 services/           # api.js (Axios)
│   │   ├── App.jsx                # Router + Toaster
│   │   └── index.css              # Tailwind + custom components
│   ├── vite.config.js             # API proxy → :5000
│   └── tailwind.config.js         # Dark gold theme config
│
├── README.md
└── setup.md
```

---

## ⚖️ Legal Corpus

| Category | Count | Coverage |
|----------|-------|----------|
| 🔴 **IPC Sections** | 12 | §302 Murder · §376 Rape · §420 Fraud · §498A Cruelty · §304B Dowry · §354 · §307 · §406 · §124A Sedition · §299 · §378 Theft · §320 |
| 🟣 **Constitutional Articles** | 7 | Art.14 Equality · Art.19 Six Freedoms · Art.21 Right to Life · Art.32 · Art.226 HC Writs · Art.44 UCC · Art.51A |
| 🟢 **Civil & Family** | 8 | HMA §13 Divorce · DV Act 2005 · Transfer of Property · Consumer Protection 2019 · Contract Act · Minimum Wages · Gratuity · GST |
| 🔵 **Landmark SC Cases** | 8 | Maneka Gandhi (1978) · Kesavananda (1973) · Puttaswamy (2017) · Vishaka (1997) · Shah Bano (1985) · Olga Tellis · MC Mehta · Hussainara Khatoon |
| **Total** | **35+** | **8 Legal Domains** |

---

## 📋 Document Templates

| # | Template | Indian Law Reference |
|---|----------|---------------------|
| 1 | 🏠 Rental Agreement | Transfer of Property Act, 1882 |
| 2 | 🔒 Non-Disclosure Agreement | Indian Contract Act, 1872 |
| 3 | 💼 Employment Contract | Industrial Disputes Act, 1947 |
| 4 | 📮 Legal Notice | CPC Order XXI / specific statutes |
| 5 | ✍️ Affidavit | Oaths Act, 1969 |
| 6 | ⚖️ Power of Attorney | Powers of Attorney Act, 1882 |
| 7 | 🚔 FIR / Police Complaint | CrPC Section 154 |
| 8 | 🛒 Consumer Complaint | Consumer Protection Act, 2019 |
| 9 | 📋 RTI Application | Right to Information Act, 2005 |
| 10 | 📜 Last Will & Testament | Indian Succession Act, 1925 |

---

## 🔒 Environment Variables

```env
# LLM (Ollama — no API key needed!)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Database (optional — app runs without it)
MONGO_URI=mongodb://localhost:27017/lawai

# Auth
JWT_SECRET_KEY=change-this-in-production

# Storage
CHROMA_PERSIST_DIR=./chroma_db
CORPUS_DIR=./data/corpus

# Flask
FLASK_ENV=development
FLASK_DEBUG=1
```

---

## 🤝 Contributing

Contributions are welcome!

1. **Add more corpus** — Add IPC sections, case law, or legal domains in `backend/data/corpus/`
2. **Improve UI** — Enhance pages in `frontend/src/pages/`
3. **Add templates** — New document templates in `backend/app/services/doc_generator_service.py`
4. **Bug fixes** — Open an issue or submit a PR

```bash
git checkout -b feat/your-feature
git commit -m "feat: add ..."
git push origin feat/your-feature
# → Open a Pull Request
```

---

## ⚠️ Disclaimer

> LAWAI provides **general legal information** for educational purposes only. It is **not a substitute for professional legal advice**. For specific legal matters, always consult a qualified and licensed advocate. AI-generated documents should be reviewed by a lawyer before use.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ for Indian legal empowerment**

*Making legal knowledge accessible to everyone — completely free, forever.*

<br/>

⭐ **Star this repo if you found it useful!** ⭐

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-Aahana--0204-181717?style=for-the-badge&logo=github)](https://github.com/Aahana-0204)

</div>
