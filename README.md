# rag-knowledge-bot

> A company knowledge base chatbot — answers employee questions strictly from uploaded documents, never makes facts up.

![Python](https://img.shields.io/badge/python-3.12-3776ab?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-streaming-009688?logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-RAG-1c3c3c?logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector_store-f97316)
![Docker](https://img.shields.io/badge/Docker-compose-2496ed?logo=docker&logoColor=white)
[![KB Labs](https://img.shields.io/badge/infra-KB_Labs-6366f1)](https://kblabs.ru)

**Live demo:** [rag-demo.k-baranov.ru](https://rag-demo.k-baranov.ru)

---

## What it does

Drop company documents into `docs/` (`.txt`, `.md`, `.pdf`). On startup the app indexes them into a local ChromaDB vector store. Employees ask questions through a web chat — the bot retrieves the relevant chunks, feeds them to an LLM, and streams the answer back. If the answer isn't in the documents, it says so directly.

```
docs/ (txt · md · pdf)
      │
      ▼
  LangChain loader + splitter
      │
      ▼
  ChromaDB  ◀──── query embedding ◀──── user question
      │
      ▼  top-k chunks
  LLM (streaming)
      │
      ▼
  FastAPI  /api/ask  (SSE)
      │
      ▼
  Browser chat UI
```

---

## Stack

| Layer | Technology |
|-------|------------|
| LLM | OpenAI-compatible models via [KB Labs](https://kblabs.ru) |
| Embeddings | text-embedding-3-small via [KB Labs](https://kblabs.ru) |
| Vector store | ChromaDB (local, no external services) |
| RAG | LangChain |
| Backend | FastAPI + Server-Sent Events (streaming) |
| Frontend | Vanilla HTML/JS — no build step |
| Deployment | Docker + docker-compose |

---

## Quick start

```bash
git clone https://github.com/KirillBaranov/rag-knowledge-bot
cd rag-knowledge-bot

cp .env.example .env          # set OPENAI_API_KEY (or compatible endpoint)

# Put your company documents here:
cp your-docs/*.{md,pdf,txt} docs/

docker compose up -d
```

Open `http://localhost:8000` — the bot indexes documents on first startup.

**Adding documents:** drop a file into `docs/` and restart the container. No code changes, no re-deploy pipeline.

---

## Project structure

```
app/
├── config.py          # settings (API key, model, system prompt)
├── main.py            # FastAPI app — indexes docs on startup
├── rag/
│   ├── loader.py      # loads and splits documents into chunks
│   ├── embeddings.py  # embedding client (supports custom gateway + JWT auth)
│   ├── indexer.py     # builds / reuses ChromaDB vector store
│   └── chain.py       # RAG chain with async streaming
└── api/
    └── routes.py      # POST /api/ask — SSE streaming endpoint

static/
└── index.html         # chat UI

docs/                  # put company documents here
```

---

## Configuration

```env
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.kblabs.ru/llm/v1  # KB Labs Gateway (https://kblabs.ru) — used in this demo; any OpenAI-compatible endpoint works
MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
SYSTEM_PROMPT="Answer only from the provided documents. If the answer isn't there, say so."
CHROMA_PATH=data/chroma
DOCS_PATH=docs
```

The system prompt is the primary control knob — set the language, tone, and boundaries without touching code.

---

## Use case

**Context:** mid-size IT company, 80 employees. HR was answering the same 20–30 questions per week about vacation, sick leave, health insurance, and business travel — all of it already written in a 40-page PDF that nobody read.

**Solution:** RAG bot backed by internal HR documents. Deployed on the company VPS, accessed via browser. Adding new documents requires no developer involvement — drop a file, restart the container.

**Results:**
- HR workload on routine questions dropped ~70%
- Response time: seconds instead of waiting for HR to be available
- The bot correctly responds "I don't have information about that" for out-of-scope questions

**Delivery:** 7 days from brief to production.

---

## What a production version adds

- Authentication (login/password or SSO/LDAP)
- Role-based document visibility (HR sees everything; managers see a subset)
- Conversation history per user
- Document upload via admin UI (no container restart)
- Telegram interface alongside the web UI
- Usage analytics (most-asked questions, unanswered queries)

---

## Infrastructure

LLM inference and embeddings run on **[KB Labs](https://kblabs.ru)** — an infrastructure platform that puts every vendor behind one contract and one stable interface: LLM, embeddings, vector stores, cache, databases, event bus and more. Swap any vendor with a config line; service code never changes.

This project uses KB Labs for both embeddings and chat completions. The same platform backs all other products in this portfolio.

---

> Portfolio: [hire.k-baranov.ru](https://hire.k-baranov.ru) · Telegram: [@kirill_baranov](https://t.me/kirill_baranov)
