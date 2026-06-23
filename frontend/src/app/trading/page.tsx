"use client";
import { useState, useEffect } from "react";
import { Card, SectionTitle, Bar, StatRow, Badge } from "@/components/ui";
import { mockLiveMatch, mockPressureHistory } from "@/lib/mock";
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer,
  LineChart, Line, ReferenceLine,
} from "recharts";

function LiveBadge() {
  return (
    <span className="inline-flex items-center gap-1.5 bg-[#1a2d1a] border border-[#00C85333] text-[#00C853] text-[10px] font-bold px-2.5 py-1 rounded-full">
      <span className="w-1.5 h-1.5 rounded-full bg-[#00C853] pulse-dot inline-block" />
      AO VIVO
    </span>
  );
}

function SignalCard({ signal, team, detail, strength }: { signal: "ENTRAR"|"AGUARDAR"|"EVITAR"; team: string; detail: string; strength: string }) {
  const cfg = {
    ENTRAR:  { bg: "bg-[#1a2d1a]", border: "border-[#00C85333]", color: "text-[#00C853]",  icon: "🟢" },
    AGUARDAR:{ bg: "bg-[#2d2510]", border: "border-[#FFC10733]", color: "text-[#FFC107]",  icon: "🟡" },
    EVITAR:  { bg: "bg-[#2d1a1a]", border: "border-[#FF525233]", color: "text-[#FF5252]",  icon: "🔴" },
  }[signal];
  return (
    <div className={`${cfg.bg} border ${cfg.border} rounded-lg p-3`}>
      <div className="flex items-center gap-2 mb-1">
        <span>{cfg.icon}</span>
        <span className={`text-sm font-bold ${cfg.color}`}>{signal}</span>
        <span className="text-[10px] text-[#9CA3AF]">{strength}</span>
      </div>
      <div className="text-xs text-[#9CA3AF]">{team}</div>
      <div className="text-[10px] text-[#4B5563] mt-0.5">{detail}</div>
    </div>
  );
}

function MiniGauge({ value, label, color }: { value: number; label: string; color: string }) {
  const radius = 28, circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="70" height="70" className="-rotate-90">
        <circle cx="35" cy="35" r={radius} fill="none" stroke="#1F2937" strokeWidth="5" />
        <circle cx="35" cy="35" r={radius} fill="none" stroke={color} strokeWidth="5"
          strokeDasharray={circumference} strokeDashoffset={offset} strokeLinecap="round"
          style={{ transition: "stroke-dashoffset 0.5s ease" }} />
      </svg>
      <div style={{ marginTop: -52 }} className="text-center z-10 relative">
        <div className="text-lg font-black" style={{ color }}>{value}</div>
      </div>
      <div className="text-[10px] text-[#9CA3AF] mt-6">{label}</div>
    </div>
  );
}

export default function TradingLive() {
  const m = mockLiveMatch;
  const [minute, setMinute] = useState(m.minute);
  const [pressData, setPressData] = useState(mockPressureHistory);

  // Simulate live updates
  useEffect(() => {
    const timer = setInterval(() => {
      setMinute(prev => Math.min(90, prev + 1));
      setPressData(prev => {
        const last = prev[prev.length - 1];
        return [...prev.slice(-19), {
          min: (last.min || 74) + 1,
          pressure_h: Math.min(100, last.pressure_h + (Math.random() - 0.4) * 8),
          pressure_a: Math.min(100, last.pressure_a + (Math.random() - 0.5) * 8),
          xg_h: last.xg_h + Math.random() * 0.06,
          xg_a: last.xg_a + Math.random() * 0.03,
        }];
      });
    }, 8000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="space-y-4">
      {/* Score Header */}
      <Card className="p-4" glow="blue">
        <div className="flex items-center gap-4">
          <LiveBadge />
          <div className="flex-1 flex items-center gap-6">
            <div className="text-lg font-black text-white">🏠 {m.home}</div>
            <div className="text-center">
              <div className="text-3xl font-black text-[#2196F3]">{m.score_h} — {m.score_a}</div>
              <div className="text-xs text-[#9CA3AF]">{minute}' · 2T</div>
            </div>
            <div className="text-lg font-black text-white">{m.away} ✈️</div>
          </div>
          <div className="flex gap-4 text-center text-xs">
            <div><div className="text-[#2196F3] font-bold text-base">{m.xg_h.toFixed(2)}</div><div className="text-[#4B5563]">xG Casa</div></div>
            <div><div className="text-[#FF5252] font-bold text-base">{m.xg_a.toFixed(2)}</div><div className="text-[#4B5563]">xG Fora</div></div>
            <div><div className="text-[#FFC107] font-bold text-base">{m.h_upi}</div><div className="text-[#4B5563]">UPI Casa</div></div>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">

        {/* Center — Charts */}
        <div className="xl:col-span-2 space-y-4">

          {/* Pressure chart */}
          <Card className="p-5">
            <SectionTitle>⚡ Pressão & xG em Tempo Real</SectionTitle>
            <ResponsiveContainer width="100%" height={200}>
              <AreaChart data={pressData}>
                <defs>
                  <linearGradient id="ph" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#2196F3" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#2196F3" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="pa" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#FF5252" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#FF5252" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="min" tick={{ fill: "#4B5563", fontSize: 10 }} axisLine={false} tickLine={false} label={{ value: "min", fill: "#4B5563", fontSize: 10, position: "insideRight" }} />
                <YAxis domain={[0, 110]} tick={{ fill: "#4B5563", fontSize: 10 }} axisLine={false} tickLine={false} width={30} />
                <Tooltip contentStyle={{ background: "#1F2937", border: "1px solid #374151", borderRadius: 8, fontSize: 11 }} />
                <ReferenceLine y={70} stroke="#FFC107" strokeDasharray="3 3" strokeOpacity={0.4} />
                <Area type="monotone" dataKey="pressure_h" stroke="#2196F3" fill="url(#ph)" strokeWidth={2} name="Pressão Casa" />
                <Area type="monotone" dataKey="pressure_a" stroke="#FF5252" fill="url(#pa)" strokeWidth={2} name="Pressão Fora" />
              </AreaChart>
            </ResponsiveContainer>
          </Card>

          {/* xG Accumulated */}
          <Card className="p-5">
            <SectionTitle>📈 xG Acumulado</SectionTitle>
            <ResponsiveContainer width="100%" height={150}>
              <LineChart data={pressData}>
                <XAxis dataKey="min" tick={{ fill: "#4B5563", fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: "#4B5563", fontSize: 10 }} axisLine={false} tickLine={false} width={30} />
                <Tooltip contentStyle={{ background: "#1F2937", border: "1px solid #374151", borderRadius: 8, fontSize: 11 }} />
                <Line type="monotone" dataKey="xg_h" stroke="#2196F3" strokeWidth={2.5} dot={false} name={`xG ${m.home}`} />
                <Line type="monotone" dataKey="xg_a" stroke="#FF5252" strokeWidth={2.5} dot={false} name={`xG ${m.away}`} />
              </LineChart>
            </ResponsiveContainer>
          </Card>

          {/* Stats table */}
          <Card className="p-5">
            <SectionTitle>📊 Estatísticas</SectionTitle>
            <StatRow label="UPI Pressão"   hv={m.h_upi}       av={m.a_upi}       max={120} />
            <StatRow label="Chutes"        hv={m.h_shots}     av={m.a_shots}     max={25}  />
            <StatRow label="No Alvo"       hv={m.h_sot}       av={m.a_sot}       max={15}  />
            <StatRow label="Escanteios"    hv={m.h_corners}   av={m.a_corners}   max={15}  />
            <StatRow label="Ataques Perig" hv={m.h_dangerous} av={m.a_dangerous} max={12}  />
            <StatRow label="Faltas"        hv={m.h_fouls}     av={m.a_fouls}     max={20}  />
            <div className="flex justify-between text-xs text-[#4B5563] mt-3">
              <span className="text-[#2196F3] font-semibold">← {m.home}</span>
              <span className="text-[#FF5252] font-semibold">{m.away} →</span>
            </div>
          </Card>
        </div>

        {/* Right — Gauges + Signals */}
        <div className="space-y-4">

          {/* Gauges */}
          <Card className="p-5">
            <SectionTitle>🎯 Índices</SectionTitle>
            <div className="grid grid-cols-2 gap-4">
              <MiniGauge value={m.gii_h}      label="GII Casa"    color="#00C853" />
              <MiniGauge value={m.gii_a}      label="GII Fora"    color="#FF5252" />
              <MiniGauge value={m.momentum_h} label="Mom. Casa"   color="#2196F3" />
              <MiniGauge value={m.momentum_a} label="Mom. Fora"   color="#FFC107" />
            </div>
          </Card>

          {/* Win Probability */}
          <Card className="p-5">
            <SectionTitle>🎲 Win Probability Live</SectionTitle>
            <div className="space-y-3">
              {[
                { label: m.home,  val: m.win_prob_h, color: "#2196F3" },
                { label: "Empate", val: m.win_prob_d, color: "#8B5CF6" },
                { label: m.away,  val: m.win_prob_a, color: "#FF5252" },
              ].map(r => (
                <div key={r.label}>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-[#9CA3AF]">{r.label}</span>
                    <span className="font-bold" style={{ color: r.color }}>{r.val.toFixed(1)}%</span>
                  </div>
                  <Bar value={r.val} max={100} color={r.color} height={5} />
                </div>
              ))}
            </div>
          </Card>

          {/* Game State */}
          <Card className="p-5">
            <SectionTitle>🎮 Game State</SectionTitle>
            <div className="space-y-2">
              <div className="bg-[#1a2d1a] border border-[#00C85333] rounded-lg p-3">
                <div className="text-xs text-[#9CA3AF] mb-0.5">{m.home}</div>
                <div className="text-sm font-bold text-[#00C853]">⚡ {m.h_state}</div>
              </div>
              <div className="bg-[#2d1a1a] border border-[#FF525233] rounded-lg p-3">
                <div className="text-xs text-[#9CA3AF] mb-0.5">{m.away}</div>
                <div className="text-sm font-bold text-[#FF5252]">😰 {m.a_state}</div>
              </div>
            </div>
          </Card>

          {/* Trader AI */}
          <Card className="p-5" glow="green">
            <SectionTitle>🤖 Trader Assistant</SectionTitle>
            <p className="text-xs text-[#9CA3AF] leading-relaxed mb-3">{m.trader_narr}</p>
            <div className="bg-[#1a2d1a] border border-[#00C85333] rounded-lg px-4 py-3">
              <div className="text-sm font-bold text-[#00C853]">{m.trader_rec}</div>
              <div className="text-xs text-[#4B5563] mt-0.5">Confiança: {m.trader_conf}%</div>
            </div>
          </Card>

          {/* Signals */}
          <Card className="p-5">
            <SectionTitle>🚦 Sinais</SectionTitle>
            <div className="space-y-2">
              <SignalCard signal="ENTRAR"   team={`${m.home} — Próx. Gol`}    detail="GII=82 + UPI=84 + xGm ↑" strength="★★★★★" />
              <SignalCard signal="ENTRAR"   team="Over 2.5 Gols"              detail="Prob 74% · EV +3.1%"       strength="★★★★" />
              <SignalCard signal="AGUARDAR" team={`${m.away} — Próx. Gol`}   detail="GII baixo (24)"            strength="★★" />
              <SignalCard signal="EVITAR"   team="Escanteio Fora"             detail="Pressão estéril detectada" strength="★" />
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
