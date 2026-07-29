# Personal AI Ops Assistant

A personal assistant that answers questions from your own documents (RAG),
completes multi-step tasks using AI agents, connects to tools via MCP,
and runs automated routines. Built layer by layer — see `CLAUDE.md` for
the full roadmap and current phase.

## Quickstart (Local Python)

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
py -m pip install -r requirements.txt
cp .env.example .env            # then add your GEMINI_API_KEY (free, get one at aistudio.google.com/app/apikey)
```

Run FastAPI server locally:
```bash
py -m uvicorn src.api.main:app --reload
```

---

## Docker Commands (Full Stack: Assistant + n8n)

### 1. Build & Start Containers (Background mode)
```bash
docker compose up -d --build
```
- **FastAPI Assistant API**: [http://localhost:8000](http://localhost:8000) (Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs))
- **n8n Automation UI**: [http://localhost:5678](http://localhost:5678)

### 2. View Running Containers & Status
```bash
docker compose ps
```

### 3. View Live Container Logs
- View logs for all services:
  ```bash
  docker compose logs -f
  ```
- View logs for a specific service:
  ```bash
  docker compose logs -f assistant
  docker compose logs -f n8n
  ```

### 4. Stop Containers (Keep Data)
```bash
docker compose stop
```

### 5. Tear Down Containers & Cleanup
- Stop and remove containers + networks:
  ```bash
  docker compose down
  ```
- Stop, remove containers, and purge persistent volumes (reset all n8n data):
  ```bash
  docker compose down -v
  ```

---

## Running Tests & Code Quality

```bash
# Run unit tests
py -m pytest tests/ -v

# Run code linter
py -m ruff check src/ tests/
```

---

## Project Structure

```
src/
  rag/          Phase 1 - document ingestion, embedding, retrieval
  agents/       Phase 2-3 - single agent, multi-agent (agentic AI)
  mcp/          Phase 4 - MCP servers + client
  automation/   Phase 5 - scheduled/event-triggered runs
  api/          Phase 6 - FastAPI HTTP wrapper
tests/          Mirrors src/ structure - unit tests for all phases
data/docs/      Drop your source documents here for ingestion
```