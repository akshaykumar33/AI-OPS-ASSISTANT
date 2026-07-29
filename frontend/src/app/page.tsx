"use client";

import { motion } from "framer-motion";
import {
  Clapperboard,
  TrendingUp,
  FileText,
  Workflow,
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  Sparkles,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { ScrollArea } from "@/components/ui/scroll-area";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { useHealth } from "@/lib/queries";
import Link from "next/link";
import {
  Area,
  AreaChart,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip as RechartsTooltip,
} from "recharts";

const fadeInUp = {
  initial: { opacity: 0, y: 15 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.3, ease: "easeOut" },
};

const stagger = {
  animate: { transition: { staggerChildren: 0.08 } },
};

const kpiCards = [
  {
    title: "Videos Produced",
    value: "24",
    change: "+12%",
    trend: "up" as const,
    icon: Clapperboard,
    desc: "Autonomous AI media rendered",
  },
  {
    title: "Trends Tracked",
    value: "156",
    change: "+8%",
    trend: "up" as const,
    icon: TrendingUp,
    desc: "DuckDuckGo viral topic queries",
  },
  {
    title: "RAG Documents",
    value: "42",
    change: "+3",
    trend: "up" as const,
    icon: FileText,
    desc: "ChromaDB vector embeddings",
  },
  {
    title: "Pipeline Runs",
    value: "89",
    change: "-2%",
    trend: "down" as const,
    icon: Workflow,
    desc: "Researcher → Writer → Reviewer",
  },
];

const chartData = [
  { day: "Mon", videos: 3, trends: 20 },
  { day: "Tue", videos: 5, trends: 35 },
  { day: "Wed", videos: 2, trends: 28 },
  { day: "Thu", videos: 7, trends: 42 },
  { day: "Fri", videos: 4, trends: 31 },
  { day: "Sat", videos: 6, trends: 38 },
  { day: "Sun", videos: 8, trends: 45 },
];

const recentActivity = [
  { text: "Video generated: 'Ancient Indus Valley Engineering'", time: "2 min ago", type: "success" },
  { text: "Trend alert: Space exploration breakthrough discovery", time: "15 min ago", type: "info" },
  { text: "Pipeline completed: researcher → writer → reviewer", time: "1h ago", type: "success" },
  { text: "RAG ingestion: 3 new research documents indexed", time: "3h ago", type: "info" },
  { text: "Comedy video rendered: 'Silicon Valley Satire'", time: "5h ago", type: "success" },
];

export default function DashboardPage() {
  const { data: health, isLoading } = useHealth();

  return (
    <DashboardShell>
      <motion.div
        className="space-y-8"
        variants={stagger}
        initial="initial"
        animate="animate"
      >
        {/* Page Header */}
        <motion.div variants={fadeInUp} className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">Executive Dashboard</h1>
              <Badge variant="outline" className="hidden sm:inline-flex gap-1 text-xs font-normal border-primary/20 bg-primary/5 text-primary">
                <Sparkles className="h-3 w-3" /> Autonomous Studio v1.0
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground">
              Real-time monitoring of AI content creation, viral trend tracking, and multi-agent workflows.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <Link href="/studio">
              <Button className="shadow-sm">
                <Clapperboard className="mr-2 h-4 w-4" />
                Launch Production
              </Button>
            </Link>
          </div>
        </motion.div>

        {/* KPI Cards */}
        <motion.div
          className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4"
          variants={stagger}
        >
          {kpiCards.map((kpi) => (
            <motion.div key={kpi.title} variants={fadeInUp}>
              <Card className="card-hover relative overflow-hidden border-border/70">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    {kpi.title}
                  </CardTitle>
                  <div className="p-2 rounded-md bg-secondary/60 text-secondary-foreground">
                    <kpi.icon className="h-4 w-4" />
                  </div>
                </CardHeader>
                <CardContent className="space-y-1">
                  <div className="text-3xl font-extrabold tracking-tight">{kpi.value}</div>
                  <div className="flex items-center justify-between pt-1">
                    <span className="text-xs text-muted-foreground">{kpi.desc}</span>
                    <div className="flex items-center gap-0.5 text-xs font-semibold">
                      {kpi.trend === "up" ? (
                        <span className="inline-flex items-center text-emerald-500 bg-emerald-500/10 px-1.5 py-0.5 rounded text-[11px]">
                          <ArrowUpRight className="h-3 w-3 mr-0.5" />
                          {kpi.change}
                        </span>
                      ) : (
                        <span className="inline-flex items-center text-rose-500 bg-rose-500/10 px-1.5 py-0.5 rounded text-[11px]">
                          <ArrowDownRight className="h-3 w-3 mr-0.5" />
                          {kpi.change}
                        </span>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* Chart + Activity Section */}
        <div className="grid gap-6 lg:grid-cols-7">
          <motion.div className="lg:col-span-4 min-w-0" variants={fadeInUp}>
            <Card className="h-full border-border/70">
              <CardHeader className="pb-2">
                <CardTitle className="text-base font-semibold flex items-center justify-between">
                  <span>Production & Tracking Volume</span>
                  <Badge variant="secondary" className="text-[11px] font-normal">Last 7 Days</Badge>
                </CardTitle>
                <CardDescription className="text-xs">
                  Daily comparison of rendered videos and analyzed viral trends
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-4">
                <div className="h-[280px] w-full min-w-0">
                  <ResponsiveContainer width="100%" height={280} minWidth={0}>
                    <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                      <defs>
                        <linearGradient id="colorVideos" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="var(--color-primary)" stopOpacity={0.4} />
                          <stop offset="95%" stopColor="var(--color-primary)" stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <XAxis
                        dataKey="day"
                        tickLine={false}
                        axisLine={false}
                        className="text-xs font-mono text-muted-foreground"
                      />
                      <YAxis tickLine={false} axisLine={false} className="text-xs font-mono text-muted-foreground" />
                      <RechartsTooltip
                        contentStyle={{
                          backgroundColor: "var(--color-card)",
                          borderColor: "var(--color-border)",
                          borderRadius: "8px",
                          fontSize: "12px",
                          boxShadow: "0 10px 15px -3px rgba(0,0,0,0.1)",
                        }}
                      />
                      <Area
                        type="monotone"
                        dataKey="videos"
                        stroke="var(--color-primary)"
                        strokeWidth={2.5}
                        fill="url(#colorVideos)"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div className="lg:col-span-3 min-w-0" variants={fadeInUp}>
            <Card className="h-full border-border/70 flex flex-col">
              <CardHeader className="pb-3 flex flex-row items-center justify-between space-y-0">
                <div>
                  <CardTitle className="text-base font-semibold">Live System Events</CardTitle>
                  <CardDescription className="text-xs">Real-time asynchronous job feed</CardDescription>
                </div>
                <Activity className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent className="flex-1">
                <ScrollArea className="h-[260px] pr-3">
                  <div className="space-y-4">
                    {recentActivity.map((item, i) => (
                      <div key={i} className="flex items-start gap-3 group">
                        <div
                          className={`mt-1.5 h-2 w-2 shrink-0 rounded-full ${
                            item.type === "success"
                              ? "bg-emerald-500 shadow-[0_0_8px_theme(colors.emerald.500)]"
                              : "bg-sky-500 shadow-[0_0_8px_theme(colors.sky.500)]"
                          }`}
                        />
                        <div className="flex-1 space-y-1">
                          <p className="text-xs font-medium leading-snug group-hover:text-primary transition-colors">
                            {item.text}
                          </p>
                          <p className="text-[11px] text-muted-foreground font-mono">
                            {item.time}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Quick Actions & Status */}
        <motion.div variants={fadeInUp} className="grid gap-6 md:grid-cols-3">
          <Card className="md:col-span-2 border-border/70">
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">Studio Quick Launch</CardTitle>
              <CardDescription className="text-xs">Shortcut to start tasks across studio modules</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-3">
                <Link href="/studio">
                  <Button variant="default" size="sm">
                    <Clapperboard className="mr-2 h-4 w-4" />
                    Produce Video
                  </Button>
                </Link>
                <Link href="/trends">
                  <Button variant="secondary" size="sm">
                    <TrendingUp className="mr-2 h-4 w-4" />
                    Fetch Viral Trends
                  </Button>
                </Link>
                <Link href="/chatbot">
                  <Button variant="outline" size="sm">
                    Ask AI Assistant
                  </Button>
                </Link>
                <Link href="/pipeline">
                  <Button variant="ghost" size="sm">
                    <Workflow className="mr-2 h-4 w-4" />
                    Multi-Agent Pipeline
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          <Card className="border-border/70 flex flex-col justify-between">
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">System Health</CardTitle>
              <CardDescription className="text-xs">API server status monitoring</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between p-3 rounded-lg bg-secondary/40 border border-border/50">
                <div className="flex items-center gap-2.5">
                  <span
                    className={`h-2.5 w-2.5 rounded-full ${
                      health?.status === "ok"
                        ? "bg-emerald-500 shadow-[0_0_8px_theme(colors.emerald.500)]"
                        : "bg-amber-500 animate-pulse"
                    }`}
                  />
                  <span className="text-xs font-semibold">FastAPI Engine</span>
                </div>
                {isLoading ? (
                  <Skeleton className="h-4 w-16" />
                ) : health?.status === "ok" ? (
                  <Badge variant="secondary" className="text-[10px] font-mono bg-emerald-500/10 text-emerald-500 hover:bg-emerald-500/20">
                    ONLINE
                  </Badge>
                ) : (
                  <Badge variant="destructive" className="text-[10px] font-mono">
                    OFFLINE
                  </Badge>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>
    </DashboardShell>
  );
}
