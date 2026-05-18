import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    // INTERNAL_API_URL → Docker internal URL (e.g. http://api:8000)
    // NEXT_PUBLIC_API_URL → Vercel: public URL of the web service (https://<host>/_/web)
    const api = (
      process.env.INTERNAL_API_URL ??
      process.env.NEXT_PUBLIC_API_URL ??
      "http://localhost:8000"
    ).trim();
    return [
      {
        source: "/api-proxy/:path*",
        destination: `${api}/:path*`,
      },
    ];
  },
};

export default nextConfig;
