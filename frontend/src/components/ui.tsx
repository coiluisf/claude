"use client";
import { confColor } from "@/lib/utils";

// ── Card ──────────────────────────────────────────────────────────────
export function Card({ children, className = "", glow }: { children: React.ReactNode; className?: string; glow?: "green"|"blue"|"red" }) {
  const glows: Record<string, string> = {
    green: "shadow-[0_0_20px_rgba(0,200,83,0.12)]",
    blue:  "shadow-[0_0_20px_rgba(33,150,243,0.12)]",
    red:   "shadow-[0_0_20px_rgba(255,82,82,0.12)]",
  };
  return (
    <div className={`bg-[#111827] border border-[#1F2937] rounded-xl ${glow ? glows[glow] : ""} ${className}`}>
      {children}
    </div>
  );
}

// ── Section title ─────────────────────────────────────────────────────
export function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-center gap-2 mb-4">
      <span className="text-[11px] font-bold tracking-widest uppercase text-[#9CA3AF]">{children}</span>
      <div className="flex-1 h-px bg-[#1F2937]" />
    </div>
  );
}

// ── KPI Card ──────────────────────────────────────────────────────────
export function KpiCard({ label, value, unit = "", delta, color = "#2196F3" }: {
  label: string; value: number; unit?: string; delta?: number; color?: string;
}) {
  return (
    <Card className="p-5 fade-up">
      <div className="text-[11px] text-[#9CA3AF] uppercase tracking-widest mb-2">{label}</div>
      <div className="text-3xl font-black" style={{ color }}>{value.toFixed(1)}<span className="text-lg font-semibold text-[#6B7280]">{unit}</span></div>
      {delta !== undefined && (
        <div className={`text-xs mt-1.5 font-semibold ${delta >= 0 ? "text-[#00C853]" : "text-[#FF5252]"}`}>
          {delta >= 0 ? "▲" : "▼"} {Math.abs(delta).toFixed(1)}{unit} vs ontem
        </div>
      )}
    </Card>
  );
}

// ── Probability block ─────────────────────────────────────────────────
export function ProbBlock({ label, prob, fairOdd, marketOdd, ev, color }: {
  label: string; prob: number; fairOdd: number; marketOdd?: number; ev?: number; color: string;
}) {
  const evPos = ev !== undefined && ev > 0;
  return (
    <div className="flex-1 rounded-xl border p-5 text-center" style={{ borderColor: color + "33", background: color + "0A" }}>
      <div className="text-xs text-[#9CA3AF] uppercase tracking-widest mb-2">{label}</div>
      <div className="text-4xl font-black mb-1" style={{ color }}>{prob.toFixed(1)}<span className="text-xl">%</span></div>
      <div className="text-xs text-[#6B7280] mt-1">Odd justa: <span className="text-white font-semibold">{fairOdd.toFixed(2)}</span></div>
      {marketOdd && <div className="text-xs text-[#6B7280]">Mercado: <span className="text-[#FFC107] font-semibold">{marketOdd.toFixed(2)}</span></div>}
      {ev !== undefined && (
        <div className={`text-xs font-bold mt-2 ${evPos ? "text-[#00C853]" : "text-[#FF5252]"}`}>
          EV: {ev > 0 ? "+" : ""}{ev.toFixed(1)}%
        </div>
      )}
    </div>
  );
}

// ── Bar ───────────────────────────────────────────────────────────────
export function Bar({ value, max = 100, color = "#2196F3", height = 6 }: {
  value: number; max?: number; color?: string; height?: number;
}) {
  const pct = Math.min(100, (value / Math.max(max, 0.01)) * 100);
  return (
    <div className="bg-[#1F2937] rounded-full overflow-hidden" style={{ height }}>
      <div className="h-full rounded-full transition-all duration-500" style={{ width: `${pct}%`, background: color }} />
    </div>
  );
}

// ── Stat row ──────────────────────────────────────────────────────────
export function StatRow({ label, hv, av, max }: { label: string; hv: number; av: number; max?: number }) {
  const mx = max ?? Math.max(hv, av, 1);
  const hPct = Math.min(100, (hv / mx) * 100);
  const aPct = Math.min(100, (av / mx) * 100);
  return (
    <div className="flex items-center gap-3 py-1.5">
      <div className="w-8 text-right text-sm font-semibold text-white">{hv}</div>
      <div className="flex-1 flex gap-1 items-center">
        <div className="flex-1 h-1.5 bg-[#1F2937] rounded-full overflow-hidden">
          <div className="h-full bg-[#2196F3] rounded-full ml-auto" style={{ width: `${hPct}%` }} />
        </div>
        <span className="text-[10px] text-[#4B5563] w-24 text-center leading-none">{label}</span>
        <div className="flex-1 h-1.5 bg-[#1F2937] rounded-full overflow-hidden">
          <div className="h-full bg-[#FF5252] rounded-full" style={{ width: `${aPct}%` }} />
        </div>
      </div>
      <div className="w-8 text-sm font-semibold text-white">{av}</div>
    </div>
  );
}

// ── Badge ─────────────────────────────────────────────────────────────
export function Badge({ children, color = "blue" }: { children: React.ReactNode; color?: "blue"|"green"|"red"|"yellow"|"purple" }) {
  const colors: Record<string, string> = {
    blue:   "bg-[#1a2a3a] text-[#2196F3] border-[#2196F333]",
    green:  "bg-[#1a2d1a] text-[#00C853] border-[#00C85333]",
    red:    "bg-[#2d1a1a] text-[#FF5252] border-[#FF525233]",
    yellow: "bg-[#2d2510] text-[#FFC107] border-[#FFC10733]",
    purple: "bg-[#1f1a2d] text-[#8B5CF6] border-[#8B5CF633]",
  };
  return (
    <span className={`inline-block text-[10px] font-semibold px-2 py-0.5 rounded-full border ${colors[color]}`}>
      {children}
    </span>
  );
}

// ── Confidence gauge ──────────────────────────────────────────────────
export function ConfGauge({ value, label }: { value: number; label?: string }) {
  const color = confColor(value);
  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs text-[#9CA3AF]">{label ?? "Confiança"}</span>
        <span className="text-sm font-bold" style={{ color }}>{value.toFixed(0)}/100</span>
      </div>
      <div className="h-2 bg-[#1F2937] rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${value}%`, background: color }} />
      </div>
    </div>
  );
}

// ── Alert card ────────────────────────────────────────────────────────
export function AlertCard({ icon, title, desc, time, color }: {
  icon: string; title: string; desc: string; time: string; color: "red"|"green"|"yellow"|"blue";
}) {
  const borders: Record<string, string> = {
    red:    "border-l-[#FF5252]", green: "border-l-[#00C853]",
    yellow: "border-l-[#FFC107]", blue:  "border-l-[#2196F3]",
  };
  return (
    <div className={`bg-[#111827] border border-[#1F2937] border-l-2 ${borders[color]} rounded-lg px-4 py-3 fade-up`}>
      <div className="flex items-start justify-between gap-2">
        <div>
          <div className="flex items-center gap-2 mb-0.5">
            <span>{icon}</span>
            <span className="text-sm font-semibold text-white">{title}</span>
          </div>
          <div className="text-xs text-[#9CA3AF]">{desc}</div>
        </div>
        <div className="text-[10px] text-[#4B5563] whitespace-nowrap flex-shrink-0">{time}</div>
      </div>
    </div>
  );
}

// ── Skeleton ──────────────────────────────────────────────────────────
export function Skeleton({ className = "" }: { className?: string }) {
  return <div className={`skeleton ${className}`} />;
}
