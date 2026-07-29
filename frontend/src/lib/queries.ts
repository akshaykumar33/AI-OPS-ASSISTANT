"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import {
  askQuestion,
  generateResearch,
  generateVideo,
  getHealth,
  getStudioTrends,
  ingestFiles,
  runAgent,
  runPipeline,
  type StudioVideoRequest,
} from "./api";

// ─── Queries ──────────────────────────────────────────────────────────────────

export function useHealth() {
  return useQuery({
    queryKey: ["health"],
    queryFn: getHealth,
    refetchInterval: 30_000,
    retry: 1,
  });
}

export function useTrends(category?: string) {
  return useQuery({
    queryKey: ["trends", category],
    queryFn: () => getStudioTrends(category),
    staleTime: 60_000,
  });
}

// ─── Mutations ────────────────────────────────────────────────────────────────

export function useAskQuestion() {
  return useMutation({
    mutationFn: ({ question, k }: { question: string; k?: number }) =>
      askQuestion(question, k),
  });
}

export function useRunAgent() {
  return useMutation({
    mutationFn: (task: string) => runAgent(task),
  });
}

export function useRunPipeline() {
  return useMutation({
    mutationFn: (task: string) => runPipeline(task),
  });
}

export function useIngestFiles() {
  return useMutation({
    mutationFn: ingestFiles,
  });
}

export function useGenerateResearch() {
  return useMutation({
    mutationFn: (topic: string) => generateResearch(topic),
  });
}

export function useGenerateVideo() {
  return useMutation({
    mutationFn: (req: StudioVideoRequest) => generateVideo(req),
  });
}
