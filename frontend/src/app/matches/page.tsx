"use client";
import Link from "next/link";
import { Card, Badge, ConfGauge } from "@/components/ui";
import { mockMatches } from "@/lib/mock";

export default function Matches() {
  return (
    <div className="space-y-5">
      <h1 className="text-xl font-black">⚽ Jogos</h1>
      <Card className="overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[#1F2937]">
              {["Hora","Jogo","Liga","1 · X · 2","EV","Confiança",""].map(h => (
                <th key={h} className="px-4 py-3 text-left text-[10px] font-semibold uppercase tracking-wider text-[#4B5563]">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {mockMatches.map((m) => (
              <tr key={m.id} className="border-b border-[#1F2937] hover:bg-[#1F2937] transition-colors group">
                <td className="px-4 py-4 text-[#9CA3AF] font-mono text-xs">{m.time}</td>
                <td className="px-4 py-4">
                  <div className="font-semibold text-white">{m.home} × {m.away}</div>
                </td>
                <td className="px-4 py-4"><Badge color="blue">{m.league}</Badge></td>
                <td className="px-4 py-4 font-mono text-xs">
                  <span className="text-[#2196F3]">{m.odd_h.toFixed(2)}</span>
                  <span className="text-[#4B5563] mx-1.5">·</span>
                  <span className="text-[#8B5CF6]">{m.odd_d.toFixed(2)}</span>
                  <span className="text-[#4B5563] mx-1.5">·</span>
                  <span className="text-[#FF5252]">{m.odd_a.toFixed(2)}</span>
                </td>
                <td className="px-4 py-4">
                  <span className={`text-xs font-bold ${m.ev > 0 ? "text-[#00C853]" : "text-[#FF5252]"}`}>
                    {m.ev > 0 ? "+" : ""}{m.ev.toFixed(1)}%
                  </span>
                </td>
                <td className="px-4 py-4 w-24"><ConfGauge value={m.confidence} /></td>
                <td className="px-4 py-4">
                  <Link href={`/matches/${m.id}`}>
                    <button className="text-xs bg-[#1F2937] hover:bg-[#2196F3] px-3 py-1.5 rounded-lg transition-colors text-[#9CA3AF] hover:text-white opacity-0 group-hover:opacity-100">
                      Analisar →
                    </button>
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
