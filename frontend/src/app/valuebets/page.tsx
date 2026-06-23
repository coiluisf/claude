"use client";
import { Card, Badge } from "@/components/ui";
import { mockValueBets } from "@/lib/mock";

export default function ValueBets() {
  const sorted = [...mockValueBets].sort((a, b) => b.ev - a.ev);
  return (
    <div className="space-y-5">
      <h1 className="text-xl font-black">🎯 Value Bets</h1>
      <Card className="overflow-hidden">
        <div className="px-5 py-3 border-b border-[#1F2937]">
          <div className="grid grid-cols-6 text-[10px] font-semibold uppercase tracking-wider text-[#4B5563]">
            <div className="col-span-2">Mercado</div>
            <div className="text-right">Prob Modelo</div>
            <div className="text-right">Odd</div>
            <div className="text-right">EV</div>
            <div className="text-right">Stake</div>
          </div>
        </div>
        {sorted.map((b, i) => (
          <div key={i} className="px-5 py-4 border-b border-[#1F2937] grid grid-cols-6 items-center hover:bg-[#1F2937] transition-colors">
            <div className="col-span-2">
              <div className="font-semibold text-white text-sm">{b.market}</div>
              <div className="text-[10px] text-[#4B5563] mt-0.5">{b.match}</div>
            </div>
            <div className="text-right font-mono text-sm">{b.prob.toFixed(1)}%</div>
            <div className="text-right text-[#FFC107] font-bold font-mono">{b.odd.toFixed(2)}</div>
            <div className="text-right font-bold text-[#00C853]">+{b.ev.toFixed(1)}%</div>
            <div className="text-right text-[#2196F3] font-semibold">R${b.stake}</div>
          </div>
        ))}
      </Card>
    </div>
  );
}
