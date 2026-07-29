"""
FastAPI wrapper exposing AI Ops Assistant & Autonomous AI Media Studio over HTTP & AWS Lambda.

Endpoints:
- GET  /health          - basic liveness check
- POST /ask             - RAG: answer a question grounded in ingested documents
- POST /agent           - Phase 2: run single tool-calling agent
- POST /pipeline        - Phase 3: run researcher->writer->reviewer pipeline
- POST /ingest          - Phase 5: ingest new files in data/docs/
- GET  /studio/trends   - Phase 5: fetch viral AI & tech video topics
- POST /studio/research - Phase 5: generate grounded research brief
- POST /studio/generate - Phase 5: trigger autonomous video production
- Mangum Handler        - AWS Lambda Serverless execution
"""

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from mangum import Mangum
from pydantic import BaseModel

from src.agents.multi_agent import run_pipeline
from src.agents.single_agent import run_agent
from src.api.studio_router import router as studio_router
from src.automation.scheduler import find_new_files, ingest_new_files
from src.rag.retrieve import answer_question

app = FastAPI(title="Personal AI Ops Assistant & Autonomous Media Studio")

# CORS — allow Next.js dev server and any localhost origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(studio_router)

# Mount video outputs directory for browser playback
os.makedirs("data/outputs", exist_ok=True)
app.mount("/data/outputs", StaticFiles(directory="data/outputs"), name="outputs")


class QuestionRequest(BaseModel):
    question: str
    k: int = 4


class TaskRequest(BaseModel):
    task: str


class AnswerResponse(BaseModel):
    answer: str


class IngestResponse(BaseModel):
    files_ingested: list[str]
    chunks_stored: int


@app.get("/")
def serve_root() -> dict:
    """API root — returns service info. Frontend runs separately on Next.js."""
    return {
        "title": "Autonomous AI Media Studio API",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict:
    """Basic health check endpoint."""
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask_endpoint(request: QuestionRequest) -> AnswerResponse:
    """Answer a question grounded in ingested documents."""
    if not request.question.strip():
        raise HTTPException(status_code=422, detail="question must not be empty")

    try:
        answer = answer_question(request.question, k=request.k)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {e}")

    return AnswerResponse(answer=answer)


@app.post("/agent", response_model=AnswerResponse)
def agent_endpoint(request: TaskRequest) -> AnswerResponse:
    """Run single tool-calling agent on a task."""
    if not request.task.strip():
        raise HTTPException(status_code=422, detail="task must not be empty")

    try:
        result = run_agent(request.task)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Agent run failed: {e}")

    return AnswerResponse(answer=result)


@app.post("/pipeline", response_model=AnswerResponse)
def pipeline_endpoint(request: TaskRequest) -> AnswerResponse:
    """Run researcher -> writer -> reviewer pipeline on a task."""
    if not request.task.strip():
        raise HTTPException(status_code=422, detail="task must not be empty")

    try:
        result = run_pipeline(request.task)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Pipeline run failed: {e}")

    return AnswerResponse(answer=result)


@app.post("/ingest", response_model=IngestResponse)
def ingest_endpoint() -> IngestResponse:
    """Ingest new files currently sitting in data/docs/."""
    new_files = find_new_files()
    try:
        stored = ingest_new_files(new_files)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

    return IngestResponse(files_ingested=new_files, chunks_stored=stored)


# AWS Lambda Serverless Handler
handler = Mangum(app)
