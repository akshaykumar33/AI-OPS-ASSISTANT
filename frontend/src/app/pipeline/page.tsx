"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Play, Loader2, Workflow, Sparkles, CheckCircle2, AlertCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { useRunPipeline } from "@/lib/queries";
import { toast } from "sonner";

interface PipelineRun {
  id: string;
  task: string;
  result: string;
  timestamp: Date;
  status: "success" | "error";
}

export default function PipelinePage() {
  const [task, setTask] = useState("");
  const [runs, setRuns] = useState<PipelineRun[]>([]);
  const pipelineMutation = useRunPipeline();

  const handleRun = async () => {
    if (!task.trim()) return;

    try {
      const result = await pipelineMutation.mutateAsync(task);
      setRuns((prev) => [
        {
          id: Date.now().toString(),
          task,
          result: result.answer,
          timestamp: new Date(),
          status: "success",
        },
        ...prev,
      ]);
      toast.success("Pipeline Run Completed!");
      setTask("");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Pipeline run failed";
      setRuns((prev) => [
        {
          id: Date.now().toString(),
          task,
          result: message,
          timestamp: new Date(),
          status: "error",
        },
        ...prev,
      ]);
      toast.error("Pipeline Run Failed", { description: message });
    }
  };

  return (
    <DashboardShell>
      <motion.div
        className="space-y-6"
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">Multi-Agent Pipeline</h1>
            <p className="text-sm text-muted-foreground mt-1">
              Trigger autonomous Researcher → Writer → Reviewer agent workflows.
            </p>
          </div>
          <Badge variant="outline" className="hidden sm:inline-flex gap-1 text-xs border-primary/20 text-primary">
            <Workflow className="h-3 w-3" /> LangGraph Architecture
          </Badge>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Submit Task Card */}
          <Card className="border-border/70 card-hover">
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">Submit Research Task</CardTitle>
              <CardDescription className="text-xs">
                Enter an objective to run through the multi-agent editorial review pipeline.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="pipeline-task" className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Task Specification
                </Label>
                <Textarea
                  id="pipeline-task"
                  placeholder="e.g. Research the deepest hydrothermal vent discoveries and outline a 3-act video documentary script…"
                  value={task}
                  onChange={(e) => setTask(e.target.value)}
                  rows={6}
                  className="font-medium leading-relaxed"
                />
              </div>
              <Button
                onClick={handleRun}
                disabled={pipelineMutation.isPending || !task.trim()}
                className="w-full h-10 font-semibold shadow-sm"
              >
                {pipelineMutation.isPending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Executing Multi-Agent Flow…
                  </>
                ) : (
                  <>
                    <Play className="mr-2 h-4 w-4 fill-current" />
                    Run Pipeline Task
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Run History Card */}
          <Card className="border-border/70 card-hover flex flex-col">
            <CardHeader className="pb-3 flex flex-row items-center justify-between space-y-0">
              <div>
                <CardTitle className="text-base font-semibold">Execution Log</CardTitle>
                <CardDescription className="text-xs">History of completed pipeline runs</CardDescription>
              </div>
              <Badge variant="secondary" className="text-xs font-mono">{runs.length} Runs</Badge>
            </CardHeader>
            <CardContent className="flex-1">
              {runs.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-16 text-center">
                  <Workflow className="mb-3 h-10 w-10 text-muted-foreground/30" />
                  <p className="text-sm font-medium">No pipeline executions yet</p>
                  <p className="text-xs text-muted-foreground mt-1 max-w-xs">
                    Submit a task on the left to trigger the researcher, writer, and reviewer agents.
                  </p>
                </div>
              ) : (
                <ScrollArea className="h-[340px] pr-2">
                  <div className="space-y-4">
                    {runs.map((run) => (
                      <div
                        key={run.id}
                        className="rounded-lg border border-border/70 bg-secondary/30 p-4 text-xs space-y-2"
                      >
                        <div className="flex items-center justify-between">
                          <span className="flex items-center gap-1.5 font-semibold">
                            {run.status === "success" ? (
                              <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                            ) : (
                              <AlertCircle className="h-4 w-4 text-rose-500" />
                            )}
                            {run.status === "success" ? "Pipeline Success" : "Pipeline Failed"}
                          </span>
                          <span className="text-[10px] font-mono text-muted-foreground">
                            {run.timestamp.toLocaleTimeString()}
                          </span>
                        </div>
                        <p className="font-semibold text-foreground">{run.task}</p>
                        <div className="p-3 rounded bg-zinc-950 text-zinc-300 font-mono text-[11px] leading-relaxed max-h-[160px] overflow-y-auto">
                          {run.result}
                        </div>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              )}
            </CardContent>
          </Card>
        </div>
      </motion.div>
    </DashboardShell>
  );
}
