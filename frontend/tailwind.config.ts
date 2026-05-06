import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      boxShadow: {
        glow: "0 0 0 1px rgba(255,255,255,0.15), 0 20px 80px rgba(59,130,246,0.25)"
      }
    }
  },
  plugins: []
};

export default config;
