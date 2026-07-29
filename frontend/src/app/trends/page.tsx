"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { RefreshCw, Clapperboard, ExternalLink, Search, Flame, Sparkles } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { useTrends } from "@/lib/queries";
import Link from "next/link";

export default function TrendsPage() {
  const [category, setCategory] = useState("AI technology news");
  const [searchQuery, setSearchQuery] = useState("");
  const { data, isLoading, refetch, isFetching } = useTrends(category);

  const categories = [
    { label: "🤖 AI Technology", value: "AI technology news" },
    { label: "🚀 Space Discoveries", value: "Space exploration discoveries" },
    { label: "🏛️ Ancient History", value: "Ancient history mysteries" },
    { label: "🦁 Wildlife Expeditions", value: "Wildlife documentary topics" },
    { label: "🎭 Comedy & Satire", value: "Comedy viral trends" },
    { label: "🇮🇳 India Breaking News", value: "India trending news" },
  ];

  const filteredTopics = (data?.topics || []).filter(
    (t) =>
      t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.snippet.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <DashboardShell>
      <motion.div
        className="space-y-6"
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">Viral Trend Hunter</h1>
              <Badge variant="outline" className="hidden sm:inline-flex gap-1 text-xs border-primary/20 text-primary">
                <Flame className="h-3 w-3 text-amber-500 fill-amber-500" /> Real-Time Search API
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              Discover breaking trends across tech, space, history, comedy, and wildlife to turn into viral documentary videos.
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => refetch()}
            disabled={isFetching}
            className="shrink-0"
          >
            <RefreshCw className={`mr-2 h-3.5 w-3.5 ${isFetching ? "animate-spin" : ""}`} />
            Refresh Stream
          </Button>
        </div>

        {/* Category Tabs */}
        <div className="flex flex-wrap gap-2">
          {categories.map((cat) => {
            const isActive = category === cat.value;
            return (
              <button
                key={cat.value}
                onClick={() => setCategory(cat.value)}
                className={`rounded-full border px-3.5 py-1.5 text-xs font-semibold transition-colors ${
                  isActive
                    ? "border-primary bg-primary text-primary-foreground shadow-sm"
                    : "border-border/80 bg-card text-muted-foreground hover:border-primary/40 hover:text-foreground"
                }`}
              >
                {cat.label}
              </button>
            );
          })}
        </div>

        {/* Search Input */}
        <div className="relative">
          <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Filter trends by keyword or topic title…"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 font-medium"
          />
        </div>

        {/* Trend Cards Grid */}
        {isLoading ? (
          <div className="grid gap-4 md:grid-cols-2">
            {Array.from({ length: 4 }).map((_, i) => (
              <Card key={i} className="border-border/70">
                <CardContent className="p-5 space-y-3">
                  <Skeleton className="h-5 w-3/4" />
                  <Skeleton className="h-3 w-full" />
                  <Skeleton className="h-3 w-2/3" />
                  <Skeleton className="h-9 w-36" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : filteredTopics.length === 0 ? (
          <Card className="border-border/70">
            <CardContent className="flex flex-col items-center justify-center py-16 text-center">
              <Search className="mb-4 h-10 w-10 text-muted-foreground/40" />
              <h3 className="text-base font-semibold">No matching trends found</h3>
              <p className="mt-1 text-xs text-muted-foreground max-w-sm">
                Try searching for a different keyword or switch to another category tab above.
              </p>
              <Button className="mt-4" size="sm" onClick={() => refetch()}>
                Refresh Trends Stream
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {filteredTopics.map((topic, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
              >
                <Card className="card-hover border-border/70 h-full flex flex-col justify-between">
                  <CardContent className="p-5 space-y-3">
                    <div className="flex items-start justify-between gap-3">
                      <h3 className="text-sm font-semibold leading-snug tracking-tight">
                        {topic.title}
                      </h3>
                      <Badge variant="secondary" className="shrink-0 text-[10px] font-mono bg-primary/10 text-primary border-primary/20">
                        #{i + 1} Viral
                      </Badge>
                    </div>

                    <p className="text-xs text-muted-foreground leading-relaxed line-clamp-3">
                      {topic.snippet}
                    </p>

                    <div className="pt-2 flex items-center justify-between">
                      <Link href={`/studio?topic=${encodeURIComponent(topic.title)}`}>
                        <Button size="sm" variant="default" className="shadow-xs text-xs font-semibold">
                          <Clapperboard className="mr-1.5 h-3.5 w-3.5" />
                          Produce Video
                        </Button>
                      </Link>

                      {topic.url && (
                        <a href={topic.url} target="_blank" rel="noopener noreferrer">
                          <Button size="sm" variant="ghost" className="text-xs text-muted-foreground">
                            <ExternalLink className="mr-1 h-3 w-3" /> Source
                          </Button>
                        </a>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>
    </DashboardShell>
  );
}
