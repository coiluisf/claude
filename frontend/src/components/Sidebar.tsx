"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/",          icon: "⬡",  label: "Dashboard"      },
  { href: "/matches",   icon: "⚽", label: "Jogos"           },
  { href: "/trading",   icon: "📈", label: "Trading"         },
  { href: "/valuebets", icon: "🎯", label: "Value Bets"      },
  { href: "/stats",     icon: "📊", label: "Estatísticas"    },
  { href: "/ai",        icon: "🧠", label: "Inteligência"    },
  { href: "/backtest",  icon: "🔬", label: "Backtests"       },
  { href: "/live",      icon: "📡", label: "Ao Vivo"         },
  { href: "/settings",  icon: "⚙",  label: "Configurações"  },
];

export function Sidebar() {
  const path = usePathname();
  return (
    <aside className="w-[220px] flex-shrink-0 border-r border-[#1F2937] bg-[#0B0F14] flex flex-col">
      {/* Logo */}
      <div className="px-5 py-5 border-b border-[#1F2937]">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#2196F3] to-[#00C853] flex items-center justify-center text-sm font-black">S</div>
          <div>
            <div className="text-[11px] font-black tracking-widest text-white uppercase leading-none">Sports Intel</div>
            <div className="text-[9px] text-[#9CA3AF] tracking-widest uppercase mt-0.5">PRO · V3</div>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        {NAV.map(({ href, icon, label }) => {
          const active = path === href || (href !== "/" && path.startsWith(href));
          return (
            <Link key={href} href={href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-150 group
                ${active
                  ? "bg-[#1F2937] text-white font-semibold"
                  : "text-[#9CA3AF] hover:bg-[#111827] hover:text-white"}`}>
              <span className="text-base w-5 text-center">{icon}</span>
              <span className="leading-none">{label}</span>
              {active && <span className="ml-auto w-1.5 h-1.5 rounded-full bg-[#2196F3]" />}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-[#1F2937]">
        <div className="text-[10px] text-[#4B5563] leading-relaxed">
          <div className="font-semibold text-[#6B7280] mb-1">Engine ativo</div>
          Monte Carlo · Poisson<br/>ELO · xG · ML · API
        </div>
      </div>
    </aside>
  );
}
