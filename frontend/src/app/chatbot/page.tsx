"use client";

import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Send, Bot, User, Sparkles, Copy, Check, ArrowRight } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { useAskQuestion } from "@/lib/queries";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

interface ChatMessage {
  id: string;
  sender: "user" | "bot";
  text: string;
  timestamp: Date;
}

const suggestedPrompts = [
  "Make a video about Indus Valley civilization engineering",
  "What are the latest discoveries in deep space black holes?",
  "Create a short documentary script on quantum computing",
  "Research ancient pyramid construction facts",
];

export default function ChatbotPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      sender: "bot",
      text: "Hello Creative Director! I am your AI Studio Producer. Ask me research questions, brainstorm script hooks, or type **\"make a video about X\"** to launch video production automatically.",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const askMutation = useAskQuestion();

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleCopyMessage = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    toast.success("Copied to clipboard!");
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleSend = async (textToSend?: string) => {
    const queryText = textToSend || input;
    if (!queryText.trim()) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: "user",
      text: queryText,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInput("");

    // Check if prompt is a video creation command
    if (queryText.toLowerCase().includes("make a video about") || queryText.toLowerCase().includes("create video on")) {
      const topic = queryText.replace(/make a video about|create video on/gi, "").trim();
      const botMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "bot",
        text: `Understood Producer! Redirecting you to the Video Studio to launch production for: "${topic}"...`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMsg]);
      setTimeout(() => {
        router.push(`/studio?topic=${encodeURIComponent(topic)}`);
      }, 1500);
      return;
    }

    try {
      const result = await askMutation.mutateAsync({ question: queryText, k: 3 });
      const botMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "bot",
        text: result.answer,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      const errMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "bot",
        text: `Apologies, I encountered a network error: ${err instanceof Error ? err.message : "Unknown error"}`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errMsg]);
    }
  };

  return (
    <DashboardShell>
      <motion.div
        className="flex h-[calc(100dvh-7.5rem)] flex-col space-y-4"
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">AI Studio Producer</h1>
            <p className="text-sm text-muted-foreground mt-0.5">
              Grounded research & creative assistant powered by ChromaDB RAG facts.
            </p>
          </div>
          <Badge variant="outline" className="hidden sm:inline-flex gap-1 font-mono text-xs border-primary/20 text-primary">
            <Sparkles className="h-3 w-3" /> Grounded RAG
          </Badge>
        </div>

        <Card className="flex flex-1 flex-col overflow-hidden border-border/70 card-hover">
          <ScrollArea className="flex-1 p-4 sm:p-6">
            <div className="space-y-5 max-w-4xl mx-auto">
              {messages.map((msg) => (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-3 group ${msg.sender === "user" ? "flex-row-reverse" : ""}`}
                >
                  <Avatar className="h-8 w-8 shrink-0 mt-0.5">
                    <AvatarFallback className={msg.sender === "bot" ? "bg-primary text-primary-foreground font-semibold" : "bg-secondary text-secondary-foreground"}>
                      {msg.sender === "bot" ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
                    </AvatarFallback>
                  </Avatar>
                  
                  <div className={`relative max-w-[80%] rounded-2xl px-4 py-3 text-xs sm:text-sm leading-relaxed ${
                    msg.sender === "user"
                      ? "bg-primary text-primary-foreground shadow-sm"
                      : "bg-secondary/60 border border-border/60 text-foreground"
                  }`}>
                    <p className="whitespace-pre-wrap">{msg.text}</p>
                    
                    {msg.sender === "bot" && (
                      <button
                        onClick={() => handleCopyMessage(msg.id, msg.text)}
                        className="absolute right-2 top-2 opacity-0 group-hover:opacity-100 transition-opacity p-1 rounded hover:bg-background/20"
                        title="Copy message"
                      >
                        {copiedId === msg.id ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5 text-muted-foreground" />}
                      </button>
                    )}
                  </div>
                </motion.div>
              ))}

              {askMutation.isPending && (
                <div className="flex gap-3">
                  <Avatar className="h-8 w-8 shrink-0">
                    <AvatarFallback className="bg-primary text-primary-foreground">
                      <Bot className="h-4 w-4" />
                    </AvatarFallback>
                  </Avatar>
                  <div className="space-y-2 rounded-2xl bg-secondary/60 border border-border/60 p-4">
                    <Skeleton className="h-3 w-48" />
                    <Skeleton className="h-3 w-32" />
                  </div>
                </div>
              )}

              <div ref={scrollRef} />
            </div>
          </ScrollArea>

          {/* Quick Suggestion Chips */}
          <div className="px-4 sm:px-6 pt-2 pb-1 border-t border-border/40 bg-secondary/20">
            <div className="flex flex-wrap gap-2 max-w-4xl mx-auto">
              {suggestedPrompts.map((p, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSend(p)}
                  className="inline-flex items-center gap-1.5 text-[11px] px-2.5 py-1 rounded-full bg-background border border-border/60 text-muted-foreground hover:text-foreground hover:border-primary/40 transition-colors"
                >
                  <span>{p}</span>
                  <ArrowRight className="h-2.5 w-2.5" />
                </button>
              ))}
            </div>
          </div>

          <CardContent className="p-4 sm:px-6 sm:py-4 border-t border-border/60">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex gap-2 max-w-4xl mx-auto"
            >
              <Input
                placeholder="Ask a question or type 'make a video about space black holes'…"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="flex-1 font-medium"
              />
              <Button type="submit" size="icon" disabled={askMutation.isPending || !input.trim()} className="shrink-0">
                <Send className="h-4 w-4" />
              </Button>
            </form>
          </CardContent>
        </Card>
      </motion.div>
    </DashboardShell>
  );
}
