# Personal AI Ops Assistant & Autonomous AI Media Studio

## What this project is
An end-to-end **Autonomous AI Content & Media Production Studio** inspired by high-retention documentary channel styles (*Vox, Magnates Media, Dhruv Rathee, Manav Singh AI*):
1. **Trend Hunting & Research**: Ingests viral news/topics using web search & ChromaDB RAG.
2. **High-Retention Scriptwriter & Storyboarder**: LangGraph multi-agent flow producing intense narrative hooks, curiosity gaps, and dramatic scene pacing.
3. **100% Free Media Production Engine**:
   - **Voice**: Microsoft Edge Neural TTS (`edge-tts`) with word-by-word timestamped subtitles (`.srt`) and deep bass pitch tuning (`-8Hz`).
   - **Visuals**: Flux model image generation with cinematic prompt boosters (35mm lens, volumetric lighting, dark moody color grade, photorealistic 8k).
   - **Motion**: Dynamic Ken Burns camera zoom transformation on every keyframe image clip.
   - **Audio FX & BGM**: Ambient background music track synthesis + audio volume ducking under narration.
   - **Subtitles**: Styled caption overlay generator for Shorts & AniDoc Documentaries.
   - **Video Rendering**: `MoviePy v2` & `FFmpeg` 1080p rendering (9:16 Shorts & 16:9 AniDoc Documentaries).
4. **Luxury Vite React Frontend (`./frontend`)**:
   - Polished Web Application with Glassmorphic SSO Authentication.
   - Genre Chips: **Space Exploration**, **Ancient History**, **Satirical Comedy**, **Wildlife Expeditions**, **Trending News**.
   - AI Studio Producer Chatbot Assistant & Live Terminal Video Monitor.
5. **AWS Serverless & Docker**:
   - Serverless Framework `serverless.yml` + `mangum` adapter for single-command AWS Lambda & API Gateway deployment (`sls deploy`).
   - Docker containerization via Dockerfile (`ffmpeg` enabled) + `docker-compose.yml`.

---

## Current Phase Status

### **Phase 1: Free Media Production Suite** — `COMPLETED & TESTED`
- [x] `src/media/voice.py`: EdgeTTS neural voice synthesis with deep bass pitch & `.srt` subtitle generation.
- [x] `src/media/image_gen.py`: Flux model visual prompt generation with cinematic boosters & canvas fallback.
- [x] `src/media/renderer.py`: MoviePy v2 & FFmpeg video stitching engine with Ken Burns motion & subtitle cards.
- [x] `tests/test_media.py`: 100% unit test coverage for voice, image, and video assembly.

### **Phase 2: Storyboarder Agent & Autonomous Studio Flow** — `COMPLETED & TESTED`
- [x] `src/agents/storyboarder.py`: Vox/Magnates Media style scriptwriter agent for high-retention JSON storyboards.
- [x] `src/studio.py`: Full end-to-end pipeline (`create_video_from_topic`).
- [x] `tests/test_studio.py`: Full end-to-end integration test.

### **Phase 3: Trend Hunting & Grounded RAG Research** — `COMPLETED & TESTED`
- [x] `src/agents/trend_hunter.py`: Fetches trending news via DuckDuckGo API.
- [x] `src/rag/researcher.py`: NotebookLM-style grounded research brief synthesis combining local ChromaDB RAG + live web search.
- [x] `src/studio.py`: Updated pipeline integrating Step 1 Grounded Research into storyboarding.
- [x] `tests/test_phase3.py`: 100% unit test coverage passed.

### **Phase 4: Advanced FX, Subtitle Formatting & Audio Ducking** — `COMPLETED & TESTED`
- [x] `src/media/audio.py`: Ambient BGM synthesis + audio volume ducking under narration.
- [x] `src/media/subtitles.py`: Subtitle `.srt` parser & styled caption card overlay renderer.
- [x] `src/media/renderer.py`: Updated video renderer combining ducked BGM + voiceover.
- [x] `tests/test_phase4.py`: 100% unit test coverage passed.

### **Phase 5: Studio Web API & Vite React Luxury Frontend** — `COMPLETED & TESTED`
- [x] `frontend/`: Luxury Vite React web dashboard & AI Producer Chatbot interface.
- [x] `src/api/studio_router.py`: FastAPI endpoints for `/studio/generate`, `/studio/trends`, and `/studio/research`.
- [x] `tests/test_phase5.py`: 100% unit test coverage passed.

### **Phase 6: AWS Serverless & Production Deploy** — `COMPLETED & TESTED`
- [x] `serverless.yml`: AWS Lambda & API Gateway serverless configuration.
- [x] `Dockerfile` & `docker-compose.yml`: Containerized production deployment.
- [x] Full test suite passing 100% clean.

---

## Tech Stack (100% Free Focus)
- **Frontend**: Vite + React + Lucide Icons (in `./frontend`)
- **Backend API**: FastAPI + Mangum (AWS Lambda Ready)
- **LLM Engine**: Google Gemini API via `google-genai` SDK (`gemini-2.0-flash`)
- **TTS & Voiceover**: `edge-tts` (Microsoft Edge Neural Voices)
- **Video Assembly**: `moviepy` (v2.x) + `ffmpeg`
- **Vector DB**: ChromaDB (local at `./data/chroma`)
- **Serverless**: Serverless Framework (`sls deploy`) & Docker Compose

---

## How to Run & Test

### Start Vite React Frontend:
```bash
cd frontend
npm run dev
```

### Start FastAPI Backend Server:
```bash
.venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

### Run All Unit & Integration Tests:
```bash
.venv\Scripts\python.exe -m pytest tests/test_phase5.py tests/test_phase4.py tests/test_phase3.py tests/test_media.py tests/test_studio.py -v
```
