"use client";
import { useState } from "react";
import { Card, SectionTitle, ProbBlock, Bar, StatRow, Badge, ConfGauge } from "@/components/ui";
import { mockMatches, mockScenarios, mockOddsHistory } from "@/lib/mock";
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, BarChart as ReBarChart, Bar as ReBar, CartesianGrid
} from "recharts";

const MODELS = [
  { name: "Monte Carlo",        weight: 30, home: 48.3, draw: 26.1, away: 25.6 },
  { name: "Poisson",            weight: 25, home: 44.7, draw: 27.8, away: 27.5 },
  { name: "Machine Learning",   weight: 20, home: 51.2, draw: 23.4, away: 25.4 },
  { name: "API-Football",       weight: 15, home: 52.0, draw: 24.0, away: 24.0 },
  { name: "ELO Contextual",     weight: 10, home: 36.8, draw: 28.4, away: 34.8 },
];

const RADAR_DATA = [
  { subject: "xG",        home: 82, away: 54 },
  { subject: "Pressão",   home: 78, away: 61 },
  { subject: "Escanteios",home: 75, away: 68 },
  { subject: "Posse",     home: 70, away: 55 },
  { subject: "Finalizações",home:80,away: 60 },
  { subject: "Defensivo", home: 65, away: 72 },
];

export default function MatchAnalysis({ params }: { params: { id: string } }) {
  const [tab, setTab] = useState<"overview"|"models"|"bets"|"scenarios"|"stats">("overview");

  const TABS = [
    { id: "overview",  label: "Visão Geral" },
    { id: "models",    label: "Modelos" },
    { id: "bets",      label: "Value Bets" },
    { id: "scenarios", label: "Cenários" },
    { id: "stats",     label: "Estatísticas" },
  ] as const;

  return (
    <div className="space-y-5">
      {/* Match Header */}
      <Card className="p-6" glow="blue">
        <div className="flex flex-col md:flex-row items-center gap-6">
          <div className="flex-1 text-center md:text-left">
            <div className="flex items-center gap-2 mb-1">
              <Badge color="blue">Copa do Mundo 2026</Badge>
              <Badge color="yellow">Final</Badge>
            </div>
            <div className="flex items-center gap-4 mt-3">
              <div className="flex-1 text-right md:text-left">
                <div className="text-2xl font-black text-white">🏠 Brasil</div>
                <div className="text-xs text-[#9CA3AF] mt-1">ELO: 2041 · Forma: ●●●●●</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-black text-[#2196F3]">×</div>
                <div className="text-[10px] text-[#4B5563] mt-1">21:00 BRT</div>
              </div>
              <div className="flex-1 text-left md:text-right">
                <div className="text-2xl font-black text-white">França ✈️</div>
                <div className="text-xs text-[#9CA3AF] mt-1">ELO: 2011 · Forma: ●●●○●</div>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-3 text-center text-xs text-[#9CA3AF] flex-shrink-0">
            <div><div className="text-white font-semibold">MetLife</div>Stadium</div>
            <div><div className="text-white font-semibold">28°C</div>Temperatura</div>
            <div><div className="text-white font-semibold">81/100</div>Confiança</div>
          </div>
        </div>
      </Card>

      {/* Tabs */}
      <div className="flex gap-1 bg-[#111827] p-1 rounded-lg border border-[#1F2937] w-fit">
        {TABS.map(t => (
          <button key={t.id} onClick={() => setTab(t.id as typeof tab)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-all
              ${tab === t.id ? "bg-[#2196F3] text-white shadow-sm" : "text-[#9CA3AF] hover:text-white"}`}>
            {t.label}
          </button>
        ))}
      </div>

      {/* Tab: Visão Geral */}
      {tab === "overview" && (
        <div className="space-y-5 fade-up">
          {/* Prob blocks */}
          <div className="flex gap-4">
            <ProbBlock label="🏠 Brasil" prob={46.8} fairOdd={2.14} marketOdd={2.05} ev={-4.2} color="#2196F3" />
            <ProbBlock label="🤝 Empate" prob={26.2} fairOdd={3.82} marketOdd={3.60} ev={-5.8} color="#8B5CF6" />
            <ProbBlock label="✈️ França"  prob={27.0} fairOdd={3.70} marketOdd={3.50} ev={-5.4} color="#FF5252" />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            {/* Odds movement */}
            <Card className="p-5">
              <SectionTitle>📉 Movimento de Odds (24h)</SectionTitle>
              <ResponsiveContainer width="100%" height={180}>
                <AreaChart data={mockOddsHistory}>
                  <defs>
                    <linearGradient id="gh" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#2196F3" stopOpacity={0.2} />
                      <stop offset="95%" stopColor="#2196F3" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="ga" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%"  stopColor="#FF5252" stopOpacity={0.2} />
                      <stop offset="95%" stopColor="#FF5252" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="t" tick={{ fill: "#4B5563", fontSize: 10 }} axisLine={false} tickLine={false} />
                  <YAxis domain={[1.5, 4.5]} tick={{ fill: "#4B5563", fontSize: 10 }} axisLine={false} tickLine={false} width={30} />
                  <Tooltip contentStyle={{ background: "#1F2937", border: "1px solid #374151", borderRadius: 8, fontSize: 11 }} />
                  <Area type="monotone" dataKey="home" stroke="#2196F3" fill="url(#gh)" strokeWidth={2} name="Casa" />
                  <Area type="monotone" dataKey="draw" stroke="#8B5CF6" fill="none" strokeWidth={1.5} strokeDasharray="4 2" name="Empate" />
                  <Area type="monotone" dataKey="away" stroke="#FF5252" fill="url(#ga)" strokeWidth={2} name="Fora" />
                </AreaChart>
              </ResponsiveContainer>
            </Card>

            {/* Radar tático */}
            <Card className="p-5">
              <SectionTitle>🎯 Radar Tático</SectionTitle>
              <ResponsiveContainer width="100%" height={180}>
                <RadarChart data={RADAR_DATA}>
                  <PolarGrid stroke="#1F2937" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: "#9CA3AF", fontSize: 10 }} />
                  <Radar name="Brasil" dataKey="home" stroke="#2196F3" fill="#2196F3" fillOpacity={0.15} strokeWidth={2} />
                  <Radar name="França" dataKey="away" stroke="#FF5252" fill="#FF5252" fillOpacity={0.1} strokeWidth={2} />
                  <Tooltip contentStyle={{ background: "#1F2937", border: "1px solid #374151", borderRadius: 8, fontSize: 11 }} />
                </RadarChart>
              </ResponsiveContainer>
            </Card>
          </div>

          {/* Confidence */}
          <Card className="p-5">
            <SectionTitle>🔬 Confiança Global da Análise</SectionTitle>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <ConfGauge value={81} label="Score Global" />
                <div className="text-xs text-[#9CA3AF] mt-2">Todos os 7 componentes verificados</div>
              </div>
              <div className="space-y-2.5">
                {[
                  { label: "Dados históricos", v: 18 },
                  { label: "ELO Contextual",   v: 10 },
                  { label: "xG calibrado",     v: 12 },
                ].map(c => (
                  <div key={c.label}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-[#9CA3AF]">{c.label}</span>
                      <span className="text-white">{c.v}/20</span>
                    </div>
                    <Bar value={c.v} max={20} color="#2196F3" height={4} />
                  </div>
                ))}
              </div>
              <div className="space-y-2.5">
                {[
                  { label: "Lambda calibrado", v: 9 },
                  { label: "Escalações",       v: 15 },
                  { label: "H2H recente",      v: 5 },
                ].map(c => (
                  <div key={c.label}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-[#9CA3AF]">{c.label}</span>
                      <span className="text-white">{c.v}/20</span>
                    </div>
                    <Bar value={c.v} max={20} color="#8B5CF6" height={4} />
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Tab: Modelos */}
      {tab === "models" && (
        <div className="space-y-5 fade-up">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            <Card className="p-5">
              <SectionTitle>🧮 Ensemble por Modelo</SectionTitle>
              <div className="space-y-3">
                {MODELS.map(m => (
                  <div key={m.name} className="bg-[#1F2937] rounded-lg p-3">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-semibold text-white">{m.name}</span>
                      <Badge color="blue">Peso {m.weight}%</Badge>
                    </div>
                    <div className="flex gap-3 text-xs">
                      <div className="flex-1 text-center">
                        <div className="text-[#2196F3] font-bold text-base">{m.home.toFixed(1)}%</div>
                        <div className="text-[#4B5563]">Casa</div>
                      </div>
                      <div className="flex-1 text-center">
                        <div className="text-[#8B5CF6] font-bold text-base">{m.draw.toFixed(1)}%</div>
                        <div className="text-[#4B5563]">Empate</div>
                      </div>
                      <div className="flex-1 text-center">
                        <div className="text-[#FF5252] font-bold text-base">{m.away.toFixed(1)}%</div>
                        <div className="text-[#4B5563]">Fora</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            <Card className="p-5">
              <SectionTitle>📊 Probabilidades Comparadas</SectionTitle>
              <ResponsiveContainer width="100%" height={280}>
                <ReBarChart data={MODELS} layout="vertical" margin={{ left: 10 }}>
                  <CartesianGrid horizontal={false} stroke="#1F2937" />
                  <XAxis type="number" domain={[0, 60]} tick={{ fill: "#4B5563", fontSize: 10 }} axisLine={false} tickLine={false} />
                  <YAxis type="category" dataKey="name" tick={{ fill: "#9CA3AF", fontSize: 10 }} axisLine={false} tickLine={false} width={110} />
                  <Tooltip contentStyle={{ background: "#1F2937", border: "1px solid #374151", borderRadius: 8, fontSize: 11 }} />
                  <ReBar dataKey="home" fill="#2196F3" name="Casa" radius={[0,3,3,0]} maxBarSize={12} />
                  <ReBar dataKey="draw" fill="#8B5CF6" name="Empate" radius={[0,3,3,0]} maxBarSize={12} />
                  <ReBar dataKey="away" fill="#FF5252" name="Fora" radius={[0,3,3,0]} maxBarSize={12} />
                </ReBarChart>
              </ResponsiveContainer>
            </Card>
          </div>
        </div>
      )}

      {/* Tab: Value Bets */}
      {tab === "bets" && (
        <div className="space-y-4 fade-up">
          <Card className="overflow-hidden">
            <div className="px-5 py-3 border-b border-[#1F2937]">
              <div className="grid grid-cols-6 text-[10px] font-semibold uppercase tracking-wider text-[#4B5563]">
                <div className="col-span-2">Mercado</div>
                <div className="text-right">Prob</div>
                <div className="text-right">Odd Mkt</div>
                <div className="text-right">EV</div>
                <div className="text-right">Stake</div>
              </div>
            </div>
            {[
              { market: "Vitória Brasil + Over 1.5", prob: 55.3, odd: 1.85, ev: 2.2, stake: "R$28", ev_pos: true },
              { market: "Over 2.5 Gols",            prob: 63.1, odd: 1.62, ev: 2.5, stake: "R$21", ev_pos: true },
              { market: "BTTS — Ambas Marcam",       prob: 47.8, odd: 2.10, ev: 0.5, stake: "R$6",  ev_pos: true },
              { market: "Brasil Vence",              prob: 46.8, odd: 2.05, ev: -4.2,stake: "SKIP",ev_pos: false },
              { market: "Empate",                   prob: 26.2, odd: 3.60, ev: -5.8,stake: "SKIP",ev_pos: false },
            ].map((b, i) => (
              <div key={i} className={`px-5 py-4 border-b border-[#1F2937] grid grid-cols-6 items-center hover:bg-[#1F2937] transition-colors ${b.ev_pos ? "" : "opacity-50"}`}>
                <div className="col-span-2">
                  <div className="text-sm font-semibold text-white">{b.market}</div>
                </div>
                <div className="text-right text-sm font-mono">{b.prob.toFixed(1)}%</div>
                <div className="text-right text-[#FFC107] font-bold font-mono">{b.odd.toFixed(2)}</div>
                <div className={`text-right font-bold ${b.ev_pos ? "text-[#00C853]" : "text-[#FF5252]"}`}>
                  {b.ev > 0 ? "+" : ""}{b.ev.toFixed(1)}%
                </div>
                <div className={`text-right text-sm font-semibold ${b.ev_pos ? "text-[#2196F3]" : "text-[#4B5563]"}`}>{b.stake}</div>
              </div>
            ))}
          </Card>
        </div>
      )}

      {/* Tab: Cenários */}
      {tab === "scenarios" && (
        <div className="space-y-4 fade-up">
          <Card className="overflow-hidden">
            <div className="px-5 py-3 border-b border-[#1F2937]">
              <div className="grid grid-cols-4 text-[10px] font-semibold uppercase tracking-wider text-[#4B5563]">
                <div className="col-span-1">Cenário</div>
                <div className="text-right">Casa</div>
                <div className="text-right">Empate</div>
                <div className="text-right">Fora</div>
              </div>
            </div>
            {mockScenarios.map((s, i) => (
              <div key={i} className={`px-5 py-4 border-b border-[#1F2937] grid grid-cols-4 items-center hover:bg-[#1F2937] transition-colors ${i === 0 ? "bg-[#1a2233]" : ""}`}>
                <div className="text-sm text-white font-medium">{s.name}{i === 0 && <Badge color="blue">Base</Badge>}</div>
                <div className="text-right text-[#2196F3] font-bold">{s.home.toFixed(1)}%</div>
                <div className="text-right text-[#8B5CF6] font-bold">{s.draw.toFixed(1)}%</div>
                <div className="text-right text-[#FF5252] font-bold">{s.away.toFixed(1)}%</div>
              </div>
            ))}
          </Card>
        </div>
      )}

      {/* Tab: Stats */}
      {tab === "stats" && (
        <div className="space-y-5 fade-up">
          <Card className="p-5">
            <SectionTitle>📊 Métricas Comparativas</SectionTitle>
            <div className="flex items-center justify-between text-xs mb-4 text-[#9CA3AF]">
              <span className="text-[#2196F3] font-semibold">🏠 Brasil</span>
              <span className="text-[#4B5563]">ESTATÍSTICA</span>
              <span className="text-[#FF5252] font-semibold">França ✈️</span>
            </div>
            {[
              { label: "Gols/jogo",         hv: 3.00, av: 2.00 },
              { label: "xG/jogo",           hv: 1.98, av: 1.41 },
              { label: "Chutes/jogo",       hv: 16.8, av: 14.2 },
              { label: "No alvo/jogo",      hv: 6.2,  av: 5.4  },
              { label: "Escanteios/jogo",   hv: 6.2,  av: 5.8  },
              { label: "Posse (%)",         hv: 56.4, av: 51.6 },
              { label: "Pressure Index",    hv: 78,   av: 65   },
            ].map(s => <StatRow key={s.label} {...s} />)}
          </Card>
        </div>
      )}
    </div>
  );
}
