"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Clapperboard,
  MessageSquare,
  TrendingUp,
  Workflow,
  Settings,
  Zap,
  LogOut,
  Moon,
  Sun,
} from "lucide-react";
import { useTheme } from "next-themes";
import { useState, useEffect } from "react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarSeparator,
} from "@/components/ui/sidebar";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useHealth } from "@/lib/queries";

const navItems = [
  { title: "Dashboard", href: "/", icon: LayoutDashboard },
  { title: "Video Studio", href: "/studio", icon: Clapperboard },
  { title: "AI Chatbot", href: "/chatbot", icon: MessageSquare },
  { title: "Trend Hunter", href: "/trends", icon: TrendingUp },
  { title: "Pipeline", href: "/pipeline", icon: Workflow },
  { title: "Settings", href: "/settings", icon: Settings },
];

const categories = [
  { label: "🚀 Space", href: "/studio?genre=space" },
  { label: "🏛️ History", href: "/studio?genre=history" },
  { label: "🎭 Comedy", href: "/studio?genre=comedy" },
  { label: "🦁 Wildlife", href: "/studio?genre=wildlife" },
  { label: "🔥 Trending", href: "/trends" },
];

export function AppSidebar() {
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();
  const { data: health } = useHealth();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <Sidebar collapsible="icon" variant="sidebar" className="border-r border-border">
      <SidebarHeader className="p-4">
        <Link href="/" className="flex items-center gap-3 group-data-[collapsible=icon]:justify-center">
          <div className="flex h-9 w-9 items-center justify-center rounded-md bg-primary text-primary-foreground font-bold shadow-xs">
            <Zap className="h-5 w-5 fill-current" />
          </div>
          <div className="flex flex-col group-data-[collapsible=icon]:hidden">
            <span className="text-sm font-bold tracking-tight text-foreground">AI Media Studio</span>
            <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <span className={`h-1.5 w-1.5 rounded-full ${health?.status === "ok" ? "bg-emerald-500 shadow-[0_0_6px_#10b981]" : "bg-amber-500"}`} />
              {health?.status === "ok" ? "Engine Online" : "Connecting…"}
            </span>
          </div>
        </Link>
      </SidebarHeader>

      <SidebarSeparator />

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="text-xs uppercase font-semibold text-muted-foreground">Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navItems.map((item) => {
                const isActive = item.href === "/"
                  ? pathname === "/"
                  : pathname.startsWith(item.href);

                return (
                  <SidebarMenuItem key={item.href}>
                    <Link href={item.href} className="w-full">
                      <SidebarMenuButton isActive={isActive} tooltip={item.title} className="font-medium text-xs">
                        <item.icon className="h-4 w-4" />
                        <span>{item.title}</span>
                      </SidebarMenuButton>
                    </Link>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarSeparator />

        <SidebarGroup>
          <SidebarGroupLabel className="text-xs uppercase font-semibold text-muted-foreground">Categories</SidebarGroupLabel>
          <SidebarGroupContent>
            <div className="flex flex-wrap gap-1.5 px-2 group-data-[collapsible=icon]:hidden">
              {categories.map((cat) => (
                <Link key={cat.label} href={cat.href}>
                  <Badge
                    variant="outline"
                    className="cursor-pointer text-[11px] font-medium border-border bg-secondary text-secondary-foreground hover:bg-primary hover:text-primary-foreground transition-all"
                  >
                    {cat.label}
                  </Badge>
                </Link>
              ))}
            </div>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="p-2">
        <SidebarSeparator className="mb-2" />
        <div className="flex items-center justify-between px-2 group-data-[collapsible=icon]:flex-col">
          <Button
            variant="outline"
            size="sm"
            className="h-8 text-xs font-semibold border-border gap-2 text-foreground"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          >
            {mounted && theme === "dark" ? (
              <>
                <Moon className="h-3.5 w-3.5" /> Dark Mode
              </>
            ) : (
              <>
                <Sun className="h-3.5 w-3.5" /> Light Mode
              </>
            )}
          </Button>
        </div>
        <SidebarSeparator className="my-2" />
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton className="w-full">
              <Avatar className="h-6 w-6">
                <AvatarFallback className="text-[10px] bg-primary text-primary-foreground font-bold">AP</AvatarFallback>
              </Avatar>
              <div className="flex flex-col text-left group-data-[collapsible=icon]:hidden">
                <span className="text-xs font-semibold text-foreground">AI Producer</span>
                <span className="text-[10px] text-muted-foreground">Lead Director</span>
              </div>
              <LogOut className="ml-auto h-3.5 w-3.5 text-muted-foreground group-data-[collapsible=icon]:hidden" />
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
