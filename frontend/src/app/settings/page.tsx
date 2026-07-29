"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Moon, Sun, Monitor } from "lucide-react";
import { useTheme } from "next-themes";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { DashboardShell } from "@/components/layout/dashboard-shell";

export default function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const themes = [
    { value: "light", label: "Light", icon: Sun },
    { value: "dark", label: "Dark Mode", icon: Moon },
    { value: "system", label: "System Theme", icon: Monitor },
  ];

  return (
    <DashboardShell>
      <motion.div
        className="space-y-6 max-w-4xl"
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">System Settings</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Manage UI appearance, backend API connections, model configurations, and environment specs.
          </p>
        </div>

        <Tabs defaultValue="general" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 sm:w-auto">
            <TabsTrigger value="general">Appearance</TabsTrigger>
            <TabsTrigger value="api">API Config</TabsTrigger>
            <TabsTrigger value="models">Models</TabsTrigger>
            <TabsTrigger value="about">About</TabsTrigger>
          </TabsList>

          {/* GENERAL TAB */}
          <TabsContent value="general">
            <Card className="border-border/70 card-hover">
              <CardHeader>
                <CardTitle className="text-base font-semibold">Appearance & Theme</CardTitle>
                <CardDescription className="text-xs">Customize dashboard theme palette and dark mode defaults</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Select Interface Theme</Label>
                  <div className="flex flex-wrap gap-3 pt-1">
                    {themes.map((t) => {
                      const isActive = mounted && theme === t.value;
                      return (
                        <Button
                          key={t.value}
                          variant={isActive ? "default" : "outline"}
                          size="sm"
                          onClick={() => setTheme(t.value)}
                          className="gap-2 font-medium"
                        >
                          <t.icon className="h-4 w-4" />
                          {t.label}
                        </Button>
                      );
                    })}
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* API CONFIG TAB */}
          <TabsContent value="api">
            <Card className="border-border/70 card-hover">
              <CardHeader>
                <CardTitle className="text-base font-semibold">Backend API Endpoints</CardTitle>
                <CardDescription className="text-xs">Configure FastAPI host address and API access keys</CardDescription>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="space-y-2">
                  <Label htmlFor="api-url" className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    FastAPI Backend Base URL
                  </Label>
                  <Input
                    id="api-url"
                    defaultValue="http://127.0.0.1:8000"
                    placeholder="http://127.0.0.1:8000"
                    className="font-mono text-xs"
                  />
                </div>
                <Separator />
                <div className="space-y-2">
                  <Label htmlFor="gemini-key" className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    Google Gemini API Key
                  </Label>
                  <Input
                    id="gemini-key"
                    type="password"
                    defaultValue="••••••••••••••••••••••••"
                    placeholder="AIza…"
                    className="font-mono text-xs"
                  />
                  <p className="text-[11px] text-muted-foreground">
                    Configured via environment variable <code className="text-primary font-mono">GEMINI_API_KEY</code> in root <code className="font-mono">.env</code>.
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* MODELS TAB */}
          <TabsContent value="models">
            <Card className="border-border/70 card-hover">
              <CardHeader>
                <CardTitle className="text-base font-semibold font-sans">Configured AI & Media Engines</CardTitle>
                <CardDescription className="text-xs">Sub-system models utilized across autonomous pipeline steps</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {[
                  { name: "Scriptwriter & Research Briefs", model: "Gemini 2.0 Flash", provider: "Google DeepMind" },
                  { name: "YouTube SEO Metadata Generator", model: "Gemini 2.0 Flash Lite", provider: "Google DeepMind" },
                  { name: "Visual Keyframe Generator", model: "Flux Schnell Model", provider: "Pollinations AI" },
                  { name: "Deep Bass Neural Narration", model: "en-US-ChristopherNeural (-8Hz Pitch)", provider: "Microsoft Edge TTS" },
                  { name: "Audio Ducking & Video Assembly", model: "MoviePy v2 + FFmpeg Engine", provider: "Local Runtime" },
                  { name: "Vector Fact Database", model: "ChromaDB Local Collection", provider: "Local Persistent DB" },
                ].map((item, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-3.5 rounded-lg border border-border/60 bg-secondary/30"
                  >
                    <div>
                      <p className="text-xs font-semibold">{item.name}</p>
                      <p className="text-[11px] text-muted-foreground">{item.provider}</p>
                    </div>
                    <Badge variant="secondary" className="font-mono text-[10px] bg-primary/10 text-primary border-primary/20">
                      {item.model}
                    </Badge>
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          {/* ABOUT TAB */}
          <TabsContent value="about">
            <Card className="border-border/70 card-hover">
              <CardHeader>
                <CardTitle className="text-base font-semibold">Autonomous AI Media Studio Pro</CardTitle>
                <CardDescription className="text-xs">Enterprise SaaS architecture overview</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4 text-xs leading-relaxed text-muted-foreground">
                <p>
                  Built inspired by high-retention documentary channel production workflows (Vox, Magnates Media). Automatically converts breaking trend topics into grounded research briefs, high-retention 9:16 Shorts or 16:9 AniDoc documentaries with burned-in captions, dynamic Ken Burns motion transforms, and ducked background audio.
                </p>
                <Separator />
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  <div className="p-3 rounded-lg border border-border/50 bg-secondary/30">
                    <span className="text-[10px] font-semibold text-muted-foreground uppercase">Frontend</span>
                    <p className="text-xs font-semibold text-foreground mt-0.5">Next.js 15 App Router</p>
                  </div>
                  <div className="p-3 rounded-lg border border-border/50 bg-secondary/30">
                    <span className="text-[10px] font-semibold text-muted-foreground uppercase">Backend Engine</span>
                    <p className="text-xs font-semibold text-foreground mt-0.5">FastAPI + Mangum</p>
                  </div>
                  <div className="p-3 rounded-lg border border-border/50 bg-secondary/30">
                    <span className="text-[10px] font-semibold text-muted-foreground uppercase">Serverless</span>
                    <p className="text-xs font-semibold text-foreground mt-0.5">AWS Lambda Ready</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </motion.div>
    </DashboardShell>
  );
}
