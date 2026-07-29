"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import {
  LayoutDashboard,
  Clapperboard,
  MessageSquare,
  TrendingUp,
  Workflow,
  Settings,
} from "lucide-react";
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command";

const quickActions = [
  { title: "Dashboard", href: "/", icon: LayoutDashboard, group: "Navigate" },
  { title: "Video Studio", href: "/studio", icon: Clapperboard, group: "Navigate" },
  { title: "AI Chatbot", href: "/chatbot", icon: MessageSquare, group: "Navigate" },
  { title: "Trend Hunter", href: "/trends", icon: TrendingUp, group: "Navigate" },
  { title: "Pipeline", href: "/pipeline", icon: Workflow, group: "Navigate" },
  { title: "Settings", href: "/settings", icon: Settings, group: "Navigate" },
];

export function CommandPalette({
  open,
  onOpenChange,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}) {
  const router = useRouter();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        onOpenChange(!open);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, [open, onOpenChange]);

  return (
    <CommandDialog open={open} onOpenChange={onOpenChange}>
      <CommandInput placeholder="Type a command or search…" />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>

        <CommandGroup heading="Navigate">
          {quickActions
            .filter((a) => a.group === "Navigate")
            .map((action) => (
              <CommandItem
                key={action.href}
                onSelect={() => {
                  router.push(action.href);
                  onOpenChange(false);
                }}
              >
                <action.icon className="mr-2 h-4 w-4" />
                <span>{action.title}</span>
              </CommandItem>
            ))}
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
