# AI Ops Assistant & Autonomous Media Studio 🚀🎬

An enterprise-grade, full-stack autonomous AI content production studio & personal AI Ops assistant. Built with **Next.js 15 (App Router)**, **React 19**, **FastAPI**, **ChromaDB RAG**, **Google Gemini**, **Google Imagen 3**, **EdgeTTS**, **MoviePy v2**, and **AWS Lambda**.

---

## 🌟 Key Features

* **📽️ Autonomous AI Media Studio**: Automatically converts trending topics into high-retention 9:16 Shorts or 16:9 AniDoc documentaries with deep-bass voiceover, burnt-in SRT captions, and dynamic Ken Burns visual transforms.
* **🔥 Real-Time Viral Trend Hunter**: Fetches breaking viral topics across AI News, Space, Ancient History, Wildlife, and Comedy via DuckDuckGo API.
* **🧠 Grounded RAG Vector Search**: ChromaDB vector store + Google Gemini 2.0 Flash for grounded research briefs and document Q&A.
* **⚡ Multi-Agent Pipeline**: Researcher → Writer → Reviewer workflow orchestration using LangGraph / LangChain abstractions.
* **🎨 Enterprise SaaS UI**: High-contrast monochromatic Next.js 15 App Router frontend with `shadcn/ui`, TanStack Query, Framer Motion, and Recharts.
* **☁️ AWS Lambda & Serverless Ready**: Configured with `Mangum` ASGI adapter and `serverless.yml` for zero-management serverless deployment.

---

## 🏗️ Architecture Stack

```
AI-OPS-ASSISTANT/
├── frontend/             # Next.js 15 (App Router), TypeScript, Tailwind CSS, shadcn/ui
│   ├── src/app/          # Dashboard, Studio, Chatbot, Trends, Pipeline, Settings
│   └── src/lib/          # Typed API Client & TanStack Query Hooks
├── src/                  # FastAPI Backend Engine
│   ├── agents/           # Single & Multi-Agent Editorial Workflows
│   ├── api/              # FastAPI Router & Mangum Lambda Handler
│   ├── media/            # ImageGen (Imagen 3 / FLUX.2), Voice (EdgeTTS), Video Renderer
│   ├── rag/              # ChromaDB Ingestion & Vector Retrieval
│   └── studio.py         # Autonomous Media Studio End-to-End Orchestrator
├── tests/                # Pytest Test Suite (13/13 passing)
├── docker-compose.yml    # Full-Stack Docker Containerization
└── serverless.yml        # AWS Lambda Infrastructure Configuration
```

---

## 🚀 Quickstart Guide

### 1. Backend Setup (FastAPI & Python)

```bash
# Clone the repository
git clone https://github.com/akshaykumar33/AI-OPS-ASSISTANT.git
cd AI-OPS-ASSISTANT

# Create virtual environment & install dependencies
python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY (from https://aistudio.google.com/app/apikey)

# Launch FastAPI Backend Server
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload
```

FastAPI Documentation available at: **`http://127.0.0.1:8000/docs`**

---

### 2. Frontend Setup (Next.js 15 App Router)

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Next.js Development Server
npm run dev
```

Next.js Frontend available at: **`http://localhost:3000`**

---

## 🐳 Docker Deployment (Full Stack + n8n)

```bash
# Build and launch containers in background
docker compose up -d --build

# Services running:
# - FastAPI Assistant API: http://localhost:8000
# - n8n Workflow Automation: http://localhost:5678
```

---

## 🧪 Testing & Code Quality

```bash
# Run backend test suite (13 tests)
python -m pytest tests/ -v

# Run code linter
python -m ruff check src/ tests/

# Build Next.js production bundle
cd frontend && npm run build
```

---

## ⚡ Serverless Deployment (AWS Lambda)

Deploy backend to AWS Lambda with Serverless Framework:

```bash
npm install -g serverless
serverless deploy
```

---

## 📄 License
MIT License. Created by [Akshay Kumar](https://github.com/akshaykumar33).