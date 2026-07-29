import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: "/api/health", destination: "http://127.0.0.1:8000/health" },
      { source: "/api/ask", destination: "http://127.0.0.1:8000/ask" },
      { source: "/api/agent", destination: "http://127.0.0.1:8000/agent" },
      { source: "/api/pipeline", destination: "http://127.0.0.1:8000/pipeline" },
      { source: "/api/ingest", destination: "http://127.0.0.1:8000/ingest" },
      { source: "/api/studio/:path*", destination: "http://127.0.0.1:8000/studio/:path*" },
    ];
  },
};

export default nextConfig;
