"use client";
import { KpiCard, Card, SectionTitle, Badge, AlertCard, ProbBlock, ConfGauge } from "@/components/ui";
import { mockKPIs, mockMatches, mockValueBets, mockAlerts } from "@/lib/mock";
import Link from "next/link";

export default function Dashboard() {
  const topBets = mockValueBets.filter(b => b.ev > 0).slice(0, 3);

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-black text-white">Dashboard</h1>
          <p className="text-sm text-[#9CA3AF] mt-0.5">Copa do Mundo 2026 · {new Date().toLocaleDateString("pt-BR", { weekday:"long", day:"2-digit", month:"long" })}</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-[#00C853] pulse-dot inline-block" />
          <span className="text-xs text-[#9CA3AF]">Engine ativo</span>
        </div>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard {...mockKPIs.hitRate}  unit="%" delta={mockKPIs.hitRate.delta}  color="#00C853" />
        <KpiCard {...mockKPIs.roi}      unit="%" delta={mockKPIs.roi.delta}      color="#2196F3" />
        <KpiCard {...mockKPIs.evMedio}  unit="%" delta={mockKPIs.evMedio.delta}  color="#FFC107" />
        <KpiCard {...mockKPIs.confidence} unit="%" delta={mockKPIs.confidence.delta} color="#8B5CF6" />
      </div>

      {/* Main grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

        {/* Left — Jogos hoje */}
        <div className="xl:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <SectionTitle>⚽ Jogos Hoje</SectionTitle>
            <Link href="/matches" className="text-xs text-[#2196F3] hover:underline">Ver todos →</Link>
          </div>

          <Card className="overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-[#1F2937]">
                  {["Hora","Jogo","Liga","1 · X · 2","EV","Conf",""].map(h => (
                    <th key={h} className="px-4 py-3 text-left text-[10px] font-semibold uppercase tracking-wider text-[#4B5563]">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {mockMatches.map((m, i) => (
                  <tr key={m.id} className="border-b border-[#1F2937] hover:bg-[#1F2937] transition-colors cursor-pointer group"
                      style={{ animationDelay: `${i * 60}ms` }}>
                    <td className="px-4 py-3.5 text-[#9CA3AF] font-mono text-xs">{m.time}</td>
                    <td className="px-4 py-3.5">
                      <div className="font-semibold text-white">{m.home} <span className="text-[#4B5563]">×</span> {m.away}</div>
                      <div className="text-[10px] text-[#4B5563]">{m.country}</div>
                    </td>
                    <td className="px-4 py-3.5">
                      <Badge color="blue">{m.league}</Badge>
                    </td>
                    <td className="px-4 py-3.5 font-mono text-xs">
                      <span className="text-[#2196F3]">{m.odd_h.toFixed(2)}</span>
                      <span className="text-[#4B5563] mx-1.5">·</span>
                      <span className="text-[#8B5CF6]">{m.odd_d.toFixed(2)}</span>
                      <span className="text-[#4B5563] mx-1.5">·</span>
                      <span className="text-[#FF5252]">{m.odd_a.toFixed(2)}</span>
                    </td>
                    <td className="px-4 py-3.5">
                      <span className={`text-xs font-bold ${m.ev > 0 ? "text-[#00C853]" : "text-[#FF5252]"}`}>
                        {m.ev > 0 ? "+" : ""}{m.ev.toFixed(1)}%
                      </span>
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="w-16">
                        <ConfGauge value={m.confidence} />
                      </div>
                    </td>
                    <td className="px-4 py-3.5">
                      <Link href={`/matches/${m.id}`}>
                        <button className="text-xs bg-[#1F2937] hover:bg-[#2196F3] px-3 py-1.5 rounded-lg transition-colors text-[#9CA3AF] hover:text-white opacity-0 group-hover:opacity-100">
                          Analisar
                        </button>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        </div>

        {/* Right column */}
        <div className="space-y-4">

          {/* Top Value Bets */}
          <SectionTitle>🎯 Top Value Bets</SectionTitle>
          <div className="space-y-2">
            {topBets.map((b, i) => (
              <Card key={i} className="p-4 hover:border-[#2196F333] transition-colors cursor-pointer" glow="green">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1">
                    <div className="text-sm font-semibold text-white">{b.market}</div>
                    <div className="text-[10px] text-[#4B5563] mt-0.5">{b.match}</div>
                  </div>
                  <div className="text-right flex-shrink-0">
                    <div className="text-sm font-black text-[#00C853]">+{b.ev.toFixed(1)}%</div>
                    <div className="text-[10px] text-[#4B5563]">EV</div>
                  </div>
                </div>
                <div className="flex items-center justify-between mt-3">
                  <div className="text-xs text-[#9CA3AF]">Odd <span className="text-[#FFC107] font-bold">{b.odd.toFixed(2)}</span></div>
                  <div className="text-xs text-[#9CA3AF]">Stake <span className="text-[#2196F3] font-bold">R${b.stake}</span></div>
                  <Badge color="green">{b.confidence}% conf.</Badge>
                </div>
              </Card>
            ))}
            <Link href="/valuebets" className="block text-xs text-[#2196F3] hover:underline text-center pt-1">Ver todos os value bets →</Link>
          </div>

          {/* Alerts */}
          <SectionTitle>🔔 Alertas de Mercado</SectionTitle>
          <div className="space-y-2">
            {mockAlerts.map(a => (
              <AlertCard key={a.id} {...a} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
