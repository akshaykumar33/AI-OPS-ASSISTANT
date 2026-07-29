"use client";

import { useState, useRef, useEffect, Suspense } from "react";
import { motion } from "framer-motion";
import {
  Rocket,
  Landmark,
  Drama,
  PawPrint,
  Flame,
  Copy,
  Check,
  Play,
  Sparkles,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Progress } from "@/components/ui/progress";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { useGenerateVideo } from "@/lib/queries";
import { useSearchParams } from "next/navigation";
import { toast } from "sonner";

const genres = [
  { id: "space", label: "Space & Cosmic", icon: Rocket, prefix: "Deep Space Secret: " },
  { id: "history", label: "Ancient History", icon: Landmark, prefix: "Ancient Secret of " },
  { id: "comedy", label: "Comedy & Parody", icon: Drama, prefix: "The Hilarious Truth About " },
  { id: "wildlife", label: "Wildlife Expeditions", icon: PawPrint, prefix: "Wild Nature Discovery: " },
  { id: "trending", label: "Trending News", icon: Flame, prefix: "Breaking Update: " },
];

function StudioContent() {
  const searchParams = useSearchParams();
  const genreParam = searchParams.get("genre");
  const topicParam = searchParams.get("topic");

  const [activeGenre, setActiveGenre] = useState("space");
  const [topic, setTopic] = useState("The 4,000 Year Old Ancient Genius of Indus Valley Engineering");
  const [formatType, setFormatType] = useState<"short" | "documentary">("short");
  const [language, setLanguage] = useState("en");
  const [enableResearch, setEnableResearch] = useState(true);
  const [copiedLogs, setCopiedLogs] = useState(false);
  const [logs, setLogs] = useState<string[]>([
    "[System] Autonomous AI Studio Engine Ready.",
    "[System] Connected to EdgeTTS & Flux Visual Synthesis pipelines.",
  ]);
  const logEndRef = useRef<HTMLDivElement>(null);

  const generateMutation = useGenerateVideo();

  useEffect(() => {
    if (genreParam) {
      const found = genres.find((g) => g.id === genreParam);
      if (found) {
        setActiveGenre(found.id);
        setTopic(`${found.prefix}Exploration and breakthroughs`);
      }
    }
    if (topicParam) {
      setTopic(topicParam);
    }
  }, [genreParam, topicParam]);

  const addLog = (msg: string) => {
    setLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);
  };

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const handleSelectGenre = (genreObj: (typeof genres)[0]) => {
    setActiveGenre(genreObj.id);
    const cleanedTopic = topic.replace(/^(Deep Space Secret: |Ancient Secret of |The Hilarious Truth About |Wild Nature Discovery: |Breaking Update: )/, "");
    setTopic(`${genreObj.prefix}${cleanedTopic}`);
  };

  const handleCopyLogs = () => {
    navigator.clipboard.writeText(logs.join("\n"));
    setCopiedLogs(true);
    toast.success("Logs copied to clipboard!");
    setTimeout(() => setCopiedLogs(false), 2000);
  };

  const handleGenerate = async () => {
    if (!topic.trim()) return;
    addLog(`Initiating autonomous pipeline for: "${topic}"`);
    addLog(`Genre: ${activeGenre.toUpperCase()} | Format: ${formatType.toUpperCase()} | Language: ${language}`);

    try {
      const result = await generateMutation.mutateAsync({
        topic,
        format_type: formatType,
        language,
        enable_research: enableResearch,
      });

      addLog(`✅ SUCCESS — Video Rendered: ${result.video_path}`);
      if (result.youtube_metadata) {
        addLog(`YouTube Title: ${result.youtube_metadata.title}`);
      }
      toast.success("Video Masterpiece Rendered!", {
        description: result.video_path,
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : "Pipeline failed";
      addLog(`❌ Error: ${message}`);
      toast.error("Video Generation Failed", { description: message });
    }
  };

  return (
    <motion.div
      className="space-y-8"
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">Autonomous Media Studio</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Produce high-retention 9:16 Shorts or 16:9 AniDoc Documentaries powered by Deep Bass Voiceover & Ken Burns Motion.
        </p>
      </div>

      {/* Genre Selector Bar */}
      <div className="flex flex-wrap gap-2.5">
        {genres.map((g) => {
          const isActive = activeGenre === g.id;
          return (
            <motion.button
              key={g.id}
              onClick={() => handleSelectGenre(g)}
              className={`inline-flex items-center gap-2 rounded-full border px-4 py-2 text-xs font-bold transition-all ${
                isActive
                  ? "border-primary bg-primary text-primary-foreground shadow-sm"
                  : "border-border bg-card text-muted-foreground hover:border-primary/50 hover:text-foreground"
              }`}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <g.icon className="h-3.5 w-3.5" />
              {g.label}
            </motion.button>
          );
        })}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Form Controls Card */}
        <Card className="border-border card-hover">
          <CardHeader className="pb-4 border-b border-border/80">
            <CardTitle className="text-base font-bold flex items-center justify-between text-foreground">
              <span>Production Configurator</span>
              <Badge variant="outline" className="text-[10px] font-mono border-border bg-secondary text-secondary-foreground">FastAPI Engine</Badge>
            </CardTitle>
            <CardDescription className="text-xs text-muted-foreground">
              Configure topic titles, media aspect ratios, narration voice, and grounded research.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5 pt-5">
            <div className="space-y-2">
              <Label htmlFor="topic" className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                Video Topic or News Title
              </Label>
              <Input
                id="topic"
                placeholder="e.g. The 4,000 Year Old Ancient Genius of Indus Valley Engineering"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="font-medium"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                  Format Aspect Ratio
                </Label>
                <Select value={formatType} onValueChange={(v) => v && setFormatType(v as "short" | "documentary")}>
                  <SelectTrigger className="w-full">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="short">📱 9:16 Viral Shorts (30-50s)</SelectItem>
                    <SelectItem value="documentary">📺 16:9 AniDoc (60-120s)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                  Script Language
                </Label>
                <Select value={language} onValueChange={(v) => v && setLanguage(v)}>
                  <SelectTrigger className="w-full">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="en">🇬🇧 English</SelectItem>
                    <SelectItem value="hi">🇮🇳 Hindi (हिंदी)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="flex items-center justify-between rounded-lg border border-border bg-secondary/40 p-3.5">
              <div className="space-y-0.5">
                <p className="text-xs font-bold text-foreground">Grounded RAG Research</p>
                <p className="text-[11px] text-muted-foreground">
                  Integrates local ChromaDB vectors + live web search facts
                </p>
              </div>
              <Switch
                checked={enableResearch}
                onCheckedChange={setEnableResearch}
              />
            </div>

            <Button
              onClick={handleGenerate}
              disabled={generateMutation.isPending || !topic.trim()}
              className="w-full h-11 text-sm font-bold shadow-md"
            >
              {generateMutation.isPending ? (
                <>
                  <Sparkles className="mr-2 h-4 w-4 animate-spin" />
                  Rendering Masterpiece…
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4 fill-current" />
                  Launch Video Production
                </>
              )}
            </Button>

            {generateMutation.isPending && (
              <div className="space-y-2 pt-1">
                <div className="flex justify-between text-xs text-muted-foreground font-mono">
                  <span>Synthesizing Audio & Frames…</span>
                  <span>35%</span>
                </div>
                <Progress value={35} className="h-1.5" />
              </div>
            )}
          </CardContent>
        </Card>

        {/* Live Studio Monitor Card */}
        <Card className="border-border card-hover flex flex-col">
          <CardHeader className="pb-3 flex flex-row items-center justify-between space-y-0 border-b border-border/80">
            <div>
              <CardTitle className="text-base font-bold text-foreground">Live Studio Monitor</CardTitle>
              <CardDescription className="text-xs text-muted-foreground">Real-time pipeline logs & preview player</CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="icon" className="h-7 w-7 text-muted-foreground hover:text-foreground" onClick={handleCopyLogs} title="Copy logs">
                {copiedLogs ? <Check className="h-3.5 w-3.5 text-emerald-500" /> : <Copy className="h-3.5 w-3.5" />}
              </Button>
              <Badge
                variant={
                  generateMutation.isPending
                    ? "default"
                    : generateMutation.isSuccess
                      ? "secondary"
                      : "outline"
                }
                className="text-[10px] font-mono"
              >
                {generateMutation.isPending
                  ? "Rendering"
                  : generateMutation.isSuccess
                    ? "Completed"
                    : "Idle"}
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="flex-1 space-y-4 pt-4">
            <ScrollArea className="h-[280px] rounded-lg border border-border bg-black p-4 font-mono text-[11px] text-zinc-300">
              {logs.map((log, i) => (
                <div key={i} className="mb-1 leading-relaxed">
                  {log}
                </div>
              ))}
              <div ref={logEndRef} />
            </ScrollArea>

            {generateMutation.isSuccess && generateMutation.data?.video_path && (
              <div className="space-y-3 pt-2">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Rendered Masterpiece</h4>
                  <Badge variant="outline" className="text-[10px] bg-emerald-500/10 text-emerald-500 border-emerald-500/20">1080p MP4 Ready</Badge>
                </div>
                <video
                  controls
                  className="w-full rounded-lg border border-border shadow-md bg-black max-h-[220px]"
                  src={generateMutation.data.video_path}
                />
                {generateMutation.data.youtube_metadata && (
                  <div className="rounded-lg border border-border bg-secondary/50 p-3 text-xs space-y-1.5">
                    <p className="font-semibold text-foreground">
                      <strong className="text-muted-foreground">YouTube Title:</strong> {generateMutation.data.youtube_metadata.title}
                    </p>
                    <p className="text-muted-foreground">
                      <strong>Tags:</strong> {generateMutation.data.youtube_metadata.tags?.join(", ")}
                    </p>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </motion.div>
  );
}

export default function StudioPage() {
  return (
    <DashboardShell>
      <Suspense fallback={<div className="text-foreground p-4 font-mono text-xs">Loading Studio Engine...</div>}>
        <StudioContent />
      </Suspense>
    </DashboardShell>
  );
}
