// Mock data — replace with real API calls to FastAPI backend

export const mockKPIs = {
  hitRate:     { value: 68.4, delta: +2.1, label: "Taxa de Acerto" },
  roi:         { value: 14.7, delta: +1.8, label: "ROI" },
  evMedio:     { value: 5.2,  delta: -0.3, label: "EV Médio" },
  confidence:  { value: 81.0, delta: +0.9, label: "Confiança Modelo" },
};

export const mockMatches = [
  { id: 1001, time: "13:00", home: "Brasil", away: "França",     league: "Copa do Mundo", country: "FIFA",
    prob_h: 46.8, prob_d: 26.2, prob_a: 27.0, odd_h: 2.05, odd_d: 3.60, odd_a: 3.50,
    ev: 2.5, confidence: 81, status: "NS",  has_value: true  },
  { id: 1002, time: "16:00", home: "Argentina", away: "Alemanha", league: "Copa do Mundo", country: "FIFA",
    prob_h: 42.1, prob_d: 28.0, prob_a: 29.9, odd_h: 2.30, odd_d: 3.40, odd_a: 3.10,
    ev: 3.1, confidence: 77, status: "NS",  has_value: true  },
  { id: 1003, time: "19:00", home: "Espanha",  away: "Inglaterra", league: "Copa do Mundo", country: "FIFA",
    prob_h: 38.5, prob_d: 30.1, prob_a: 31.4, odd_h: 2.55, odd_d: 3.20, odd_a: 2.95,
    ev: -1.2, confidence: 62, status: "NS",  has_value: false },
  { id: 1004, time: "22:00", home: "Portugal", away: "Holanda",  league: "Copa do Mundo", country: "FIFA",
    prob_h: 51.2, prob_d: 24.8, prob_a: 24.0, odd_h: 1.95, odd_d: 3.75, odd_a: 3.90,
    ev: 4.8, confidence: 88, status: "NS",  has_value: true  },
];

export const mockValueBets = [
  { market: "Portugal Vence", prob: 51.2, odd: 1.95, ev: 4.8, stake: 28, confidence: 88, match: "Portugal × Holanda" },
  { market: "Over 2.5 Gols",  prob: 63.1, odd: 1.62, ev: 3.1, stake: 21, confidence: 82, match: "Argentina × Alemanha" },
  { market: "Brasil + Over 1.5", prob: 55.3, odd: 1.85, ev: 2.5, stake: 18, confidence: 79, match: "Brasil × França" },
  { market: "BTTS",           prob: 58.4, odd: 1.72, ev: 1.8, stake: 12, confidence: 71, match: "Espanha × Inglaterra" },
  { market: "Escanteios Over 9.5", prob: 62.0, odd: 1.74, ev: 2.1, stake: 15, confidence: 74, match: "Brasil × França" },
];

export const mockLiveMatch = {
  id: 9999, home: "Brasil", away: "França",
  score_h: 3, score_a: 2, minute: 74,
  status: "2H",
  h_shots: 18, a_shots: 9,
  h_sot: 8,   a_sot: 4,
  h_corners: 11, a_corners: 6,
  h_possession: 58, a_possession: 42,
  h_dangerous: 9, a_dangerous: 4,
  h_fouls: 12, a_fouls: 15,
  h_yellow: 2, a_yellow: 3,
  h_upi: 84, a_upi: 36,
  xg_h: 2.41, xg_a: 1.62,
  win_prob_h: 82.4, win_prob_d: 9.1, win_prob_a: 8.5,
  gii_h: 82, gii_a: 24,
  momentum_h: 84.2, momentum_a: 31.4,
  trader_rec: "SEGURAR POSIÇÃO",
  trader_conf: 88,
  trader_narr: "Brasil domina com UPI=84 e GII=82. Gol iminente com alta probabilidade.",
  h_state: "CONTROLANDO",
  a_state: "DESESPERADO",
};

export const mockAlerts = [
  { id: 1, type: "steam",  icon: "🚨", title: "Steam Move", desc: "Portugal × Holanda — Odd caiu 2.15→1.95 em 8 min", time: "2m atrás",  color: "red" as const    },
  { id: 2, type: "ev",     icon: "🔥", title: "EV > 15%",   desc: "Novo mercado com EV calculado em +15.3%",          time: "5m atrás",  color: "green" as const  },
  { id: 3, type: "drop",   icon: "📉", title: "Queda de Odd", desc: "Brasil Vence: 2.40 → 2.05",                      time: "12m atrás", color: "yellow" as const },
  { id: 4, type: "volume", icon: "⚡", title: "Volume Anormal", desc: "Over 2.5 Brasil × França — vol +340%",         time: "18m atrás", color: "blue" as const   },
];

export const mockOddsHistory = Array.from({ length: 24 }, (_, i) => ({
  t: `${i}h`, home: 2.40 - i * 0.015, draw: 3.55 + i * 0.005, away: 3.60 - i * 0.01,
}));

export const mockPressureHistory = Array.from({ length: 20 }, (_, i) => ({
  min: (i + 55), pressure_h: 40 + Math.random() * 45, pressure_a: 20 + Math.random() * 30,
  xg_h: i * 0.12, xg_a: i * 0.08,
}));

export const mockScenarios = [
  { name: "Base",                 home: 46.8, draw: 26.2, away: 27.0 },
  { name: "Sem Vinicius Jr.",     home: 38.4, draw: 28.8, away: 32.8 },
  { name: "Sem Mbappé",          home: 52.1, draw: 25.6, away: 22.3 },
  { name: "Chuva forte",         home: 44.2, draw: 30.1, away: 25.7 },
  { name: "Prorrogação",         home: 35.0, draw: 40.0, away: 25.0 },
];
