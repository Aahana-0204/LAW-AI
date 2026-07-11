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
