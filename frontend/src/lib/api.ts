const API_BASE = "";

// ─── Types ────────────────────────────────────────────────────────────────────

export interface HealthResponse {
  status: string;
}

export interface AnswerResponse {
  answer: string;
}

export interface IngestResponse {
  files_ingested: string[];
  chunks_stored: number;
}

export interface TrendTopic {
  title: string;
  snippet: string;
  source?: string;
  url?: string;
}

export interface TrendsResponse {
  status: string;
  category: string;
  topics: TrendTopic[];
}

export interface ResearchBrief {
  topic: string;
  summary: string;
  key_facts: string[];
  sources: string[];
}

export interface YouTubeMetadata {
  title: string;
  description: string;
  tags: string[];
  thumbnail_prompt: string;
}

export interface VideoGenerationResult {
  status: string;
  topic: string;
  video_path: string;
  youtube_metadata?: YouTubeMetadata;
}

export interface StudioVideoRequest {
  topic: string;
  format_type: "short" | "documentary";
  language: string;
  enable_research: boolean;
}

// ─── Fetch Helper ─────────────────────────────────────────────────────────────

async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `API error ${res.status}`);
  }

  return res.json();
}

// ─── Endpoints ────────────────────────────────────────────────────────────────

export function getHealth() {
  return apiFetch<HealthResponse>("/api/health");
}

export function askQuestion(question: string, k = 3) {
  return apiFetch<AnswerResponse>("/api/ask", {
    method: "POST",
    body: JSON.stringify({ question, k }),
  });
}

export function runAgent(task: string) {
  return apiFetch<AnswerResponse>("/api/agent", {
    method: "POST",
    body: JSON.stringify({ task }),
  });
}

export function runPipeline(task: string) {
  return apiFetch<AnswerResponse>("/api/pipeline", {
    method: "POST",
    body: JSON.stringify({ task }),
  });
}

export function ingestFiles() {
  return apiFetch<IngestResponse>("/api/ingest", { method: "POST" });
}

export function getStudioTrends(category = "AI technology news", maxResults = 8) {
  return apiFetch<TrendsResponse>(
    `/api/studio/trends?category=${encodeURIComponent(category)}&max_results=${maxResults}`
  );
}

export function generateResearch(topic: string) {
  return apiFetch<ResearchBrief>("/api/studio/research", {
    method: "POST",
    body: JSON.stringify({ topic }),
  });
}

export function generateVideo(req: StudioVideoRequest) {
  return apiFetch<VideoGenerationResult>("/api/studio/generate", {
    method: "POST",
    body: JSON.stringify(req),
  });
}
