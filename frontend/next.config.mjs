/** @type {import("next").NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "https://wezzyw-agentic-research-system.hf.space/api/:path*",
      },
    ]
  },
};
export default nextConfig;
