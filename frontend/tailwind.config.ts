import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: "#0B0F14",
          card:    "#111827",
          hover:   "#1F2937",
          deep:    "#070A0F",
        },
        clr: {
          green:  "#00C853",
          red:    "#FF5252",
          yellow: "#FFC107",
          blue:   "#2196F3",
          purple: "#8B5CF6",
          cyan:   "#06B6D4",
        },
        border: {
          DEFAULT: "#1F2937",
          subtle:  "#161D2A",
        },
      },
      fontFamily: {
        mono: ["'JetBrains Mono'", "'Fira Code'", "monospace"],
      },
      backgroundImage: {
        "grid-pattern": "linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px)",
      },
      backgroundSize: {
        "grid": "40px 40px",
      },
      animation: {
        "fade-up":   "fadeUp 0.45s ease forwards",
        "shimmer":   "shimmer 1.6s infinite",
        "pulse-dot": "pulseDot 1.5s ease infinite",
        "spin-slow": "spin 3s linear infinite",
      },
      keyframes: {
        fadeUp: {
          from: { opacity: "0", transform: "translateY(12px)" },
          to:   { opacity: "1", transform: "translateY(0)" },
        },
        shimmer: {
          "0%":   { backgroundPosition: "-400% 0" },
          "100%": { backgroundPosition:  "400% 0" },
        },
        pulseDot: {
          "0%,100%": { opacity: "1" },
          "50%":     { opacity: "0.3" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
