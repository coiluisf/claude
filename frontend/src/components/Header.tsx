"use client";
import { useState } from "react";

export function Header() {
  const [search, setSearch] = useState("");
  return (
    <header className="h-14 flex items-center px-6 gap-4 border-b border-[#1F2937] bg-[#0B0F14] flex-shrink-0">
      {/* Search */}
      <div className="flex-1 max-w-md">
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-[#4B5563] text-sm">🔍</span>
          <input
            type="text"
            placeholder="Buscar times, competições, jogos..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-[#111827] border border-[#1F2937] rounded-lg pl-9 pr-4 py-2 text-sm text-white placeholder-[#4B5563] focus:outline-none focus:border-[#2196F3] transition-colors"
          />
        </div>
      </div>

      <div className="flex items-center gap-3 ml-auto">
        {/* Live indicator */}
        <div className="flex items-center gap-1.5 text-xs text-[#9CA3AF]">
          <span className="w-2 h-2 rounded-full bg-[#00C853] pulse-dot inline-block" />
          4 ao vivo
        </div>

        {/* Alerts */}
        <button className="relative p-2 rounded-lg hover:bg-[#111827] transition-colors">
          <span className="text-[#9CA3AF]">🔔</span>
          <span className="absolute top-1 right-1 w-2 h-2 bg-[#FF5252] rounded-full" />
        </button>

        {/* Date */}
        <div className="text-xs text-[#4B5563] hidden md:block">
          {new Date().toLocaleDateString("pt-BR", { weekday: "short", day: "2-digit", month: "short" })}
        </div>

        {/* User */}
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#2196F3] to-[#8B5CF6] flex items-center justify-center text-xs font-bold cursor-pointer">
          U
        </div>
      </div>
    </header>
  );
}
