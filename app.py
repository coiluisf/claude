# -*- coding: utf-8 -*-
"""
Análise Copa do Mundo 2026 — Web App Profissional
Powered by Streamlit + API-Football V3
"""

import streamlit as st
import sys
import io
import contextlib
import datetime
import os
import re
import requests
import importlib.util
import builtins
import time

# ── Page config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚽ Copa 2026 Analyst",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Sistema de Análise Profissional — Copa do Mundo 2026"},
)

# ── Global CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp { background: #0d1117; font-family: 'Inter', sans-serif; }
.block-container { padding: 1.5rem 2rem 3rem; max-width: 1400px; }

/* ── Cards ── */
.card {
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
}
.card-accent { border-left: 3px solid #58a6ff; }
.card-green  { border-left: 3px solid #3fb950; }
.card-red    { border-left: 3px solid #f85149; }
.card-yellow { border-left: 3px solid #d29922; }
.card-purple { border-left: 3px solid #bc8cff; }

/* ── Section title ── */
.section-title {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #58a6ff;
  margin-bottom: 0.9rem;
  display: flex;
  align-items: center;
  gap: 6px;
}
.section-title::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #21262d;
}

/* ── Hero match card ── */
.hero-card {
  background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
  border: 1px solid #30363d;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
}
.hero-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(ellipse at 50% 50%, rgba(88,166,255,0.04) 0%, transparent 60%);
  pointer-events: none;
}
.hero-teams { display: flex; align-items: center; justify-content: center; gap: 2rem; }
.hero-team  { text-align: center; flex: 1; }
.hero-team-name  { font-size: 1.4rem; font-weight: 800; color: #e6edf3; }
.hero-vs    { font-size: 1.1rem; font-weight: 700; color: #484f58; padding: 0 1rem; }
.hero-meta  { font-size: 0.82rem; color: #8b949e; margin-top: 1rem; }
.hero-badge {
  display: inline-block;
  font-size: 0.72rem;
  padding: 3px 10px;
  border-radius: 20px;
  margin: 3px;
}
.badge-blue   { background: #1a2740; color: #58a6ff; border: 1px solid #1f6feb44; }
.badge-green  { background: #1a2d1a; color: #3fb950; border: 1px solid #23863644; }
.badge-orange { background: #2d1f0a; color: #d97706; border: 1px solid #92400e44; }

/* ── Prob gauge ── */
.prob-row    { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
.prob-block  { flex: 1; border-radius: 10px; padding: 1rem; text-align: center; }
.prob-home   { background: linear-gradient(135deg, #1a2740, #1f2d40); border: 1px solid #1f6feb55; }
.prob-draw   { background: linear-gradient(135deg, #1f1a2d, #241f32); border: 1px solid #8957e555; }
.prob-away   { background: linear-gradient(135deg, #2a1a1a, #321f1f); border: 1px solid #f8514955; }
.prob-pct    { font-size: 2.2rem; font-weight: 800; line-height: 1; margin: 0.2rem 0; }
.prob-label  { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; color: #8b949e; }
.prob-fair   { font-size: 0.8rem; color: #484f58; margin-top: 0.3rem; }

/* ── Bar chart ── */
.stat-bar-row { display: flex; align-items: center; margin: 5px 0; gap: 8px; }
.stat-bar-row .label { font-size: 0.78rem; color: #8b949e; width: 130px; flex-shrink: 0; }
.stat-bar-row .val   { font-size: 0.82rem; font-weight: 600; color: #e6edf3; width: 36px; text-align: right; flex-shrink: 0; }
.bar-wrap { flex: 1; background: #21262d; border-radius: 4px; height: 7px; overflow: hidden; }
.bar-inner { height: 7px; border-radius: 4px; }
.bar-blue   { background: linear-gradient(90deg, #1f6feb, #58a6ff); }
.bar-green  { background: linear-gradient(90deg, #238636, #3fb950); }
.bar-red    { background: linear-gradient(90deg, #b91c1c, #f85149); }
.bar-purple { background: linear-gradient(90deg, #6e40c9, #bc8cff); }
.bar-orange { background: linear-gradient(90deg, #b45309, #d97706); }

/* ── Value bet card ── */
.bet-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.85rem 1rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  border: 1px solid #21262d;
}
.bet-row:hover { border-color: #30363d; background: #1c2128; }
.bet-rank { font-size: 1.1rem; width: 28px; flex-shrink: 0; }
.bet-name { flex: 1; font-size: 0.92rem; font-weight: 600; color: #e6edf3; }
.bet-prob { font-size: 0.82rem; color: #8b949e; width: 44px; text-align: right; }
.bet-odd  { font-size: 0.95rem; font-weight: 700; color: #d29922; width: 42px; text-align: right; }
.bet-ev   { font-size: 0.88rem; font-weight: 700; width: 56px; text-align: right; }
.bet-ev-pos { color: #3fb950; }
.bet-ev-neg { color: #f85149; }
.bet-kelly { font-size: 0.82rem; color: #58a6ff; width: 52px; text-align: right; }
.bet-skip  { color: #484f58; font-size: 0.82rem; }
.bet-header { font-size: 0.68rem; color: #484f58; text-transform: uppercase; letter-spacing: 0.05em; }

/* ── Kelly stake box ── */
.kelly-box {
  background: #1a2d1a;
  border: 1px solid #23863644;
  border-radius: 8px;
  padding: 0.85rem 1rem;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.kelly-ev   { font-size: 0.82rem; color: #3fb950; width: 60px; font-weight: 700; }
.kelly-name { flex: 1; font-size: 0.88rem; color: #e6edf3; }
.kelly-full  { font-size: 1rem; font-weight: 700; color: #e6edf3; width: 60px; text-align: right; }
.kelly-half  { font-size: 0.82rem; color: #8b949e; width: 52px; text-align: right; }

/* ── Confidence gauge ── */
.conf-wrap { background: #21262d; border-radius: 8px; height: 12px; overflow: hidden; margin: 6px 0 3px; }
.conf-fill { height: 12px; border-radius: 8px; }

/* ── Form dots ── */
.form-dot {
  display: inline-block;
  width: 28px; height: 28px;
  line-height: 28px;
  border-radius: 50%;
  text-align: center;
  font-size: 0.72rem;
  font-weight: 700;
  margin: 2px;
}
.form-w { background: #1a3a20; color: #3fb950; border: 1px solid #3fb95055; }
.form-d { background: #2a2a12; color: #d29922; border: 1px solid #d2992255; }
.form-l { background: #3a1a1a; color: #f85149; border: 1px solid #f8514955; }

/* ── H2H bar ── */
.h2h-bar-wrap { display: flex; height: 10px; border-radius: 5px; overflow: hidden; margin: 8px 0; }
.h2h-bar-h { background: #1f6feb; }
.h2h-bar-d { background: #484f58; }
.h2h-bar-a { background: #f85149; }

/* ── Table ── */
.data-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.data-table th { color: #484f58; font-weight: 600; padding: 6px 10px; border-bottom: 1px solid #21262d; text-align: left; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; }
.data-table td { color: #c9d1d9; padding: 7px 10px; border-bottom: 1px solid #161b22; }
.data-table tr:hover td { background: #1c2128; }
.data-table .num { text-align: right; font-weight: 600; color: #e6edf3; }
.data-table .pos { text-align: right; color: #3fb950; font-weight: 700; }
.data-table .neg { text-align: right; color: #f85149; font-weight: 700; }
.data-table .muted { color: #484f58; }

/* ── Alert boxes ── */
.alert { border-radius: 8px; padding: 0.9rem 1.1rem; margin: 0.5rem 0; font-size: 0.88rem; }
.alert-ok  { background: #1a2d1a; border: 1px solid #23863644; color: #3fb950; }
.alert-warn{ background: #2d1f0a; border: 1px solid #92400e44; color: #d97706; }
.alert-err { background: #2a1a1a; border: 1px solid #b91c1c44; color: #f85149; }
.alert-info{ background: #1a1f2a; border: 1px solid #1f6feb44; color: #58a6ff; }

/* ── ELO rating ── */
.elo-box { display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1rem; background: #1c2128; border-radius: 8px; margin-bottom: 6px; }
.elo-name { font-size: 0.9rem; font-weight: 600; color: #e6edf3; }
.elo-val  { font-size: 1.5rem; font-weight: 800; color: #58a6ff; }
.elo-trend{ font-size: 0.82rem; color: #3fb950; }
.elo-trend-neg { color: #f85149; }

/* ── Recommendation card ── */
.rec-card { display: flex; align-items: center; gap: 1rem; padding: 1rem 1.2rem; border-radius: 10px; margin-bottom: 0.6rem; }
.rec-strong { background: #1a3a20; border: 1px solid #3fb95055; }
.rec-medium { background: #2a2a12; border: 1px solid #d2992255; }
.rec-skip   { background: #1c2128; border: 1px solid #21262d; }
.rec-avoid  { background: #2a1a1a; border: 1px solid #f8514955; }
.rec-icon   { font-size: 1.4rem; flex-shrink: 0; }
.rec-name   { flex: 1; font-size: 0.95rem; font-weight: 600; color: #e6edf3; }
.rec-ev     { font-size: 0.88rem; font-weight: 700; }
.rec-stake  { font-size: 0.88rem; color: #58a6ff; font-weight: 600; }

/* ── Player table ── */
.player-row { display: flex; align-items: center; gap: 10px; padding: 6px 0; border-bottom: 1px solid #1c2128; }
.player-num  { font-size: 0.75rem; color: #484f58; width: 20px; }
.player-name { font-size: 0.88rem; font-weight: 500; color: #e6edf3; flex: 1; }
.player-stat { font-size: 0.8rem; color: #8b949e; width: 30px; text-align: right; }
.player-stat-hl { color: #d29922; font-weight: 700; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid #21262d; }
div[data-testid="stMetric"] { background: #161b22; border: 1px solid #21262d; border-radius: 8px; padding: 0.75rem 1rem; }
.stButton > button { border-radius: 8px; font-weight: 600; font-size: 0.9rem; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, #1f6feb, #388bfd); border: none; }
hr { border-color: #21262d; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: #161b22; border-radius: 8px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 6px; font-weight: 500; font-size: 0.85rem; }
.stTabs [aria-selected="true"] { background: #1f6feb !important; }

/* ── Spinner ── */
div[data-testid="stSpinner"] { color: #58a6ff; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────
API_KEY   = os.environ.get("API_KEY", "906f4989978807460c85bcc0c9e87367")
BASE_URL  = "https://v3.football.api-sports.io"
HEADERS   = {"x-apisports-key": API_KEY}
WC_LEAGUE = 1
WC_SEASON = 2026


# ── Load analysis module ───────────────────────────────────────────────
@st.cache_resource(show_spinner="⚙️ Carregando engine de análise...")
def _load_module():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "programa_analise_v3.py")
    spec = importlib.util.spec_from_file_location("analise_v3", path)
    mod  = importlib.util.module_from_spec(spec)
    original_input = builtins.input
    builtins.input = lambda *a, **k: ""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(mod)
    finally:
        builtins.input = original_input
    mod._clear = lambda: None
    mod.CLEAR_SCREEN = False
    return mod


def get_module():
    try:
        return _load_module(), None
    except Exception as e:
        import traceback
        return None, traceback.format_exc()


# ── API helpers ────────────────────────────────────────────────────────
@st.cache_data(ttl=90, show_spinner=False)
def fetch_matches(date_str):
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS,
                         params={"league": WC_LEAGUE, "season": WC_SEASON,
                                 "date": date_str, "timezone": "America/Sao_Paulo"},
                         timeout=15)
        r.raise_for_status()
        return r.json().get("response", [])
    except Exception:
        return []


@st.cache_data(ttl=20, show_spinner=False)
def fetch_live_matches():
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS,
                         params={"league": WC_LEAGUE, "season": WC_SEASON, "live": "all"},
                         timeout=15)
        r.raise_for_status()
        return r.json().get("response", [])
    except Exception:
        return []


def run_captured(fn, *args, **kwargs):
    buf = io.StringIO()
    original_input = builtins.input
    builtins.input = lambda *a, **k: ""
    err = None
    try:
        with contextlib.redirect_stdout(buf):
            with contextlib.redirect_stderr(buf):
                fn(*args, **kwargs)
    except SystemExit:
        pass
    except Exception as e:
        import traceback
        err = traceback.format_exc()
    finally:
        builtins.input = original_input
    return buf.getvalue(), err


def run_live_single_cycle(mod, fixture_id, h_name, a_name, home_id, history=None):
    if history is None:
        history = []
    buf = io.StringIO()
    original_input = builtins.input
    builtins.input = lambda *a, **k: ""
    snap_out = [None]
    trader_out = [None]
    try:
        with contextlib.redirect_stdout(buf):
            snap = mod._snapshot(fixture_id, home_id)
            if snap is None:
                buf.write("⚠️  Aguardando dados da API...\n")
                return buf.getvalue(), None, history, None
            snap_out[0] = snap
            goal_sigs   = mod._signal_goal(snap, history, h_name, a_name)
            corner_sigs = mod._signal_corner(snap, history, h_name, a_name)
            card_sigs   = mod._signal_card(snap, history, h_name, a_name, snap["minute"])
            consciousness = mod._game_consciousness(snap, history, h_name, a_name)
            try:
                _lf = mod.calculate_live_fair_odds(snap, history, snap.get("minute",1),
                          snap.get("score_h",0), snap.get("score_a",0), h_name, a_name)
            except Exception: _lf = None
            try:
                _fp_h = mod.detect_false_pressure(snap, "h_", snap.get("minute",1))
                _fp_a = mod.detect_false_pressure(snap, "a_", snap.get("minute",1))
            except Exception: _fp_h = _fp_a = None
            try:
                _regime = mod.detect_game_regime(snap, history, h_name, a_name)
            except Exception: _regime = None
            try: _evts = mod._fetch_live_events(fixture_id)
            except Exception: _evts = None
            try:
                _mom  = mod._live_momentum_engine(snap, history)
                _ph   = mod._pressure_windows(snap, history, "h_")
                _pa   = mod._pressure_windows(snap, history, "a_")
                _gii  = mod._goal_imminent_index(snap, history, _mom["h_score"], _mom["a_score"], _ph, _pa)
                _aoh  = mod._anti_false_over(snap, "h_")
                _aoa  = mod._anti_false_over(snap, "a_")
                _cash = mod._smart_cashout(snap, history, _gii["h_gii"], _gii["a_gii"], _mom)
                _coh  = mod._corner_imminent_prob(snap, history, "h_")
                _coa  = mod._corner_imminent_prob(snap, history, "a_")
                _tact = mod._tactical_change_detector(snap, history)
                _fat  = mod._fatigue_live(snap, snap["minute"])
                _xgm  = mod._xg_momentum_live(snap, history)
                _red  = mod._red_card_impact(snap, history)
                _gs   = mod._game_state_engine(snap, h_name, a_name)
                _wp   = mod._win_prob_live(snap, history, h_name, a_name)
                _ta   = mod._trader_assistant(snap, h_name, a_name, _mom, _gii,
                            _ph, _pa, _xgm, _gs, snap["minute"])
                _alrt = mod._professional_alerts(_gii, _mom, _ph, _pa,
                            _aoh, _aoa, _red, _tact, _cash, snap)
                trader_out[0] = _ta
            except Exception:
                _mom=_ph=_pa=_gii=_aoh=_aoa=_cash=_coh=_coa=_tact=_fat=None
                _xgm=_red=_gs=_wp=_ta=_alrt=None
            mod._render_dashboard(
                snap, history, h_name, a_name, home_id,
                goal_sigs, corner_sigs, card_sigs, 1, 30, consciousness,
                live_fair=_lf, regime=_regime,
                false_pressure_h=_fp_h, false_pressure_a=_fp_a, live_events=_evts,
                v5_momentum=_mom, v5_press_h=_ph, v5_press_a=_pa,
                v5_gii=_gii, v5_anti_h=_aoh, v5_anti_a=_aoa,
                v5_cashout=_cash, v5_corn_h=_coh, v5_corn_a=_coa,
                v5_tactical=_tact, v5_fatigue=_fat, v5_xgm=_xgm,
                v5_red=_red, v5_game_state=_gs, v5_win_prob=_wp,
                v5_trader=_ta, v5_alerts=_alrt,
            )
            history.append(snap)
            if len(history) > 8: history.pop(0)
            return buf.getvalue(), snap_out[0], history, trader_out[0]
    except Exception as e:
        import traceback
        return traceback.format_exc(), None, history, None
    finally:
        builtins.input = original_input


# ══════════════════════════════════════════════════════════════════════
# REPORT PARSER — turns captured text into structured data
# ══════════════════════════════════════════════════════════════════════

def _clean(line):
    """Strip box-drawing chars and leading/trailing whitespace."""
    return re.sub(r'[║╔╠╚╝╗╣─═]', '', line).strip()


def _extract_section(text, keyword):
    """Return lines of the first section whose title contains keyword."""
    lines = text.split("\n")
    in_section = False
    result = []
    for line in lines:
        clean = _clean(line)
        if not clean:
            continue
        if keyword.upper() in clean.upper() and ("═" * 5 in line or not in_section):
            in_section = True
            continue
        if in_section:
            if "╠" in line and "═" * 5 in line:
                break
            if "╚" in line:
                break
            result.append(clean)
    return result


def _parse_float(s):
    try:
        return float(re.sub(r"[^0-9.\-+]", "", s))
    except Exception:
        return 0.0


def parse_report(text):
    """Parse the captured terminal report into a structured dict."""
    data = {}
    lines = [_clean(l) for l in text.split("\n") if _clean(l)]

    # ── Ensemble probabilities ────────────────────────────────────────
    ens_match = re.search(r"ENSEMBLE FINAL.*?Casa:\s*([\d.]+)%.*?Empate:\s*([\d.]+)%.*?Fora:\s*([\d.]+)%", text)
    if ens_match:
        data["ens_home"] = float(ens_match.group(1))
        data["ens_draw"] = float(ens_match.group(2))
        data["ens_away"] = float(ens_match.group(3))

    # ── Model table ───────────────────────────────────────────────────
    models = []
    for line in lines:
        for m in ["Monte Carlo", "Poisson", "Machine Learning", "API-Football", "ELO"]:
            if m in line:
                pcts = re.findall(r"([\d.]+)%", line)
                peso = re.search(r"(\d+)%", line)
                if len(pcts) >= 3:
                    models.append({"name": m, "home": float(pcts[-3]),
                                   "draw": float(pcts[-2]), "away": float(pcts[-1])})
                break
    data["models"] = models

    # ── Value Betting ─────────────────────────────────────────────────
    bets = []
    in_ev = False
    for line in lines:
        if "VALUE BETTING" in line.upper():
            in_ev = True
            continue
        if in_ev:
            if "BANKROLL" in line.upper() or "KELLY" in line.upper() or "RECOMENDAÇÃO" in line.upper():
                break
            # Try to parse bet row: #  NAME  PROB%  ODD  FAIR  EV%  KELLY
            m = re.match(r"(\d)\s+(.+?)\s+([\d.]+)%\s+([\d.]+)\s+([\d.]+)\s+([+\-][\d.]+)%\s+([\d.]+%|SKIP)", line)
            if m:
                bets.append({
                    "rank": m.group(1), "name": m.group(2).strip(),
                    "prob": float(m.group(3)), "odd": float(m.group(4)),
                    "fair": float(m.group(5)), "ev": float(m.group(6)),
                    "kelly": m.group(7),
                })
    data["bets"] = bets

    # ── Kelly stakes ──────────────────────────────────────────────────
    kelly_rows = []
    in_kelly = False
    for line in lines:
        if "BANKROLL" in line.upper() and "KELLY" in line.upper():
            in_kelly = True
            continue
        if in_kelly:
            if "RECOMENDAÇÃO" in line.upper() or "CALIBRAÇÃO" in line.upper():
                break
            # Format: NAME  EV%  KELLY%  R$FULL  R$HALF  R$QUART
            m = re.search(r"([+][\d.]+)%.*?R\$([\d,]+)", line)
            if m and len(line) > 20:
                name = re.sub(r"[+\-][\d.]+%.*", "", line).strip()
                stakes = re.findall(r"R\$([\d,]+)", line)
                kelly_rows.append({
                    "name": name[:40],
                    "ev": m.group(1),
                    "full": stakes[0] if stakes else "?",
                    "half": stakes[1] if len(stakes) > 1 else "?",
                })
    data["kelly"] = kelly_rows

    # ── Global Confidence ─────────────────────────────────────────────
    conf_m = re.search(r"(?:Score|SCORE):\s*(\d+)/100", text)
    data["confidence"] = int(conf_m.group(1)) if conf_m else None
    conf_label_m = re.search(r"Score:\s*\d+/100\s+[█░]+\s+([A-ZÁÉÍÓÚÇ ]+)", text)
    data["confidence_label"] = conf_label_m.group(1).strip() if conf_label_m else ""

    # ── ELO ───────────────────────────────────────────────────────────
    elo_home = re.search(r"ELO Contextual.*?Casa.*?(\d+\.\d+)%.*?Emp.*?(\d+\.\d+)%.*?Fora.*?(\d+\.\d+)%", text)
    data["elo_probs"] = {
        "home": float(elo_home.group(1)) if elo_home else None,
        "draw": float(elo_home.group(2)) if elo_home else None,
        "away": float(elo_home.group(3)) if elo_home else None,
    }

    elo_lines = _extract_section(text, "ELO RATING")
    data["elo_lines"] = elo_lines

    # ── Forma recente ─────────────────────────────────────────────────
    data["forma_lines"] = _extract_section(text, "FORMA RECENTE")

    # ── Recomendação final ────────────────────────────────────────────
    recs = []
    for line in lines:
        for signal in ["ENTRADA FORTE", "ENTRADA", "AGUARDAR", "EVITAR"]:
            if signal in line.upper():
                m = re.search(r"([+\-][\d.]+)%", line)
                stake_m = re.search(r"R\$([\d,]+)", line)
                bet_name = re.sub(r"(🟢|🟡|🟠|🔴)", "", line)
                bet_name = re.sub(r"(ENTRADA FORTE|ENTRADA|AGUARDAR|EVITAR|EV:.*|Kelly:.*)", "", bet_name, flags=re.I).strip()
                recs.append({
                    "signal": signal,
                    "name": bet_name[:45],
                    "ev": m.group(1) + "%" if m else "",
                    "stake": "R$" + stake_m.group(1) if stake_m else "SKIP",
                })
                break
    data["recs"] = recs

    # ── Métricas ofensivas ────────────────────────────────────────────
    metrics = []
    in_metrics = False
    for line in lines:
        if "MÉTRICAS OFENSIVAS" in line.upper():
            in_metrics = True
            continue
        if in_metrics:
            if any(k in line.upper() for k in ["PRESSURE", "ESCANTEIO", "ÁRBITRO", "ENSEMBLE", "PREDIÇÃO"]):
                break
            nums = re.findall(r"([\d.]+)%?", line)
            if len(nums) >= 2 and not line.startswith("MÉTRICA"):
                label = re.sub(r"[\d.%]+.*", "", line).strip()
                if label and len(label) > 3:
                    metrics.append({"label": label, "h": float(nums[-2]), "a": float(nums[-1])})
    data["metrics"] = metrics[:7]

    # ── Árbitro ────────────────────────────────────────────────────────
    ref_lines = _extract_section(text, "ÁRBITRO")
    data["ref_lines"] = ref_lines

    # ── Clima ──────────────────────────────────────────────────────────
    weather_lines = _extract_section(text, "CLIMÁTICAS")
    data["weather_lines"] = weather_lines

    # ── Cenários ───────────────────────────────────────────────────────
    scenario_lines = _extract_section(text, "CENÁRIOS")
    data["scenario_lines"] = scenario_lines

    # ── Narrativa ─────────────────────────────────────────────────────
    narr_lines = _extract_section(text, "NARRATIVA")
    data["narrative"] = " ".join(narr_lines)

    # ── Consistency / Confidence details ──────────────────────────────
    data["calib_lines"] = _extract_section(text, "CONSISTENCY")

    return data


# ══════════════════════════════════════════════════════════════════════
# BEAUTIFUL REPORT RENDERER
# ══════════════════════════════════════════════════════════════════════

def render_report(output, sel):
    """Render the full analysis as a beautiful HTML report."""
    d = parse_report(output)
    h_name = sel["home_name"]
    a_name = sel["away_name"]

    # ── HERO CARD ─────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-teams">
            <div class="hero-team">
                <div class="hero-team-name">🏠 {h_name}</div>
            </div>
            <div class="hero-vs">×</div>
            <div class="hero-team">
                <div class="hero-team-name">{a_name} ✈️</div>
            </div>
        </div>
        <div class="hero-meta">
            <span class="hero-badge badge-blue">⚽ Copa do Mundo 2026</span>
            <span class="hero-badge badge-blue">🕐 {sel.get('time','--')} BRT</span>
            <span class="hero-badge badge-green">🔬 Análise V3 PRO</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TABS ──────────────────────────────────────────────────────────
    tabs = st.tabs(["🎯 Veredicto", "📊 Probabilidades", "💰 Value Bets",
                    "📈 Estatísticas", "📋 Detalhes", "📄 Relatório Bruto"])

    # ── TAB 1: Veredicto ──────────────────────────────────────────────
    with tabs[0]:
        # Confidence
        if d.get("confidence") is not None:
            conf = d["confidence"]
            conf_color = "#3fb950" if conf >= 70 else ("#d97706" if conf >= 50 else "#f85149")
            st.markdown(f"""
            <div class="section-title">🔬 Confiança Global da Análise</div>
            <div class="card card-accent">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
                    <span style="font-size:1rem;font-weight:600;color:#e6edf3">Score de Confiança</span>
                    <span style="font-size:2rem;font-weight:800;color:{conf_color}">{conf}<span style="font-size:1rem;color:#484f58">/100</span></span>
                </div>
                <div class="conf-wrap"><div class="conf-fill" style="width:{conf}%;background:{conf_color}"></div></div>
                <div style="font-size:0.78rem;color:#8b949e;margin-top:6px">{d.get('confidence_label','')}</div>
            </div>
            """, unsafe_allow_html=True)

        # Narrative
        if d.get("narrative"):
            st.markdown(f"""
            <div class="section-title">📝 Narrativa Analítica</div>
            <div class="card card-accent">
                <p style="color:#c9d1d9;font-size:0.92rem;line-height:1.7;margin:0">{d['narrative']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Recommendations
        if d.get("recs"):
            st.markdown('<div class="section-title">🏆 Recomendações Finais</div>', unsafe_allow_html=True)
            for r in d["recs"]:
                sig = r["signal"]
                if sig == "ENTRADA FORTE":
                    cls, icon = "rec-strong", "🟢"
                elif sig == "ENTRADA":
                    cls, icon = "rec-medium", "🟡"
                elif sig == "AGUARDAR":
                    cls, icon = "rec-medium", "🟠"
                else:
                    cls, icon = "rec-avoid", "🔴"
                ev_col = "#3fb950" if r["ev"].startswith("+") else "#f85149"
                st.markdown(f"""
                <div class="rec-card {cls}">
                    <div class="rec-icon">{icon}</div>
                    <div>
                        <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.05em;color:#484f58">{sig}</div>
                        <div class="rec-name">{r['name']}</div>
                    </div>
                    <div style="text-align:right">
                        <div class="rec-ev" style="color:{ev_col}">EV {r['ev']}</div>
                        <div class="rec-stake">{r['stake']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Fallback from ensemble
            if d.get("ens_home"):
                st.info("As recomendações serão exibidas após parsing completo do relatório.")

        # Kelly stakes
        if d.get("kelly"):
            st.markdown('<div class="section-title">💰 Stakes Recomendados (Kelly)</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="card">
            <table class="data-table" style="width:100%">
            <tr><th>Mercado</th><th>EV</th><th class="num">Kelly Full</th><th class="num">Kelly ½</th></tr>
            """, unsafe_allow_html=True)
            rows = ""
            for k in d["kelly"]:
                rows += f"""<tr>
                    <td>{k['name']}</td>
                    <td><span style="color:#3fb950;font-weight:700">+{k['ev']}%</span></td>
                    <td class="num">{k['full']}</td>
                    <td class="num" style="color:#8b949e">{k['half']}</td>
                </tr>"""
            st.markdown(rows + "</table></div>", unsafe_allow_html=True)

        # Weather
        if d.get("weather_lines"):
            st.markdown('<div class="section-title">🌤️ Condições Climáticas</div>', unsafe_allow_html=True)
            weather_text = "<br>".join(d["weather_lines"][:4])
            st.markdown(f'<div class="card card-yellow"><div style="font-size:0.88rem;color:#c9d1d9;line-height:1.8">{weather_text}</div></div>', unsafe_allow_html=True)

    # ── TAB 2: Probabilidades ─────────────────────────────────────────
    with tabs[1]:
        if d.get("ens_home"):
            ph, pd_, pa = d["ens_home"], d["ens_draw"], d["ens_away"]
            fh = round(100/ph, 2) if ph else "-"
            fd = round(100/pd_, 2) if pd_ else "-"
            fa = round(100/pa, 2) if pa else "-"

            st.markdown('<div class="section-title">⚡ Ensemble Final (5 modelos)</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="prob-row">
                <div class="prob-block prob-home">
                    <div class="prob-label">🏠 {h_name[:18]}</div>
                    <div class="prob-pct" style="color:#58a6ff">{ph:.1f}%</div>
                    <div class="prob-fair">odd justa: {fh}</div>
                </div>
                <div class="prob-block prob-draw">
                    <div class="prob-label">🤝 Empate</div>
                    <div class="prob-pct" style="color:#bc8cff">{pd_:.1f}%</div>
                    <div class="prob-fair">odd justa: {fd}</div>
                </div>
                <div class="prob-block prob-away">
                    <div class="prob-label">✈️ {a_name[:18]}</div>
                    <div class="prob-pct" style="color:#f85149">{pa:.1f}%</div>
                    <div class="prob-fair">odd justa: {fa}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Per-model breakdown
        if d.get("models"):
            st.markdown('<div class="section-title">🧮 Detalhamento por Modelo</div>', unsafe_allow_html=True)
            weights = {"Monte Carlo": 30, "Poisson": 25, "Machine Learning": 20,
                       "API-Football": 15, "ELO": 10}
            st.markdown('<div class="card">', unsafe_allow_html=True)
            html = '<table class="data-table" style="width:100%"><tr><th>Modelo</th><th>Peso</th><th class="num">Casa</th><th class="num">Empate</th><th class="num">Fora</th></tr>'
            for m in d["models"]:
                w = weights.get(m["name"], 0)
                html += f"""<tr>
                    <td>{m['name']}</td>
                    <td><span style="color:#8b949e;font-size:0.78rem">{w}%</span></td>
                    <td class="num">{m['home']:.1f}%</td>
                    <td class="num">{m['draw']:.1f}%</td>
                    <td class="num">{m['away']:.1f}%</td>
                </tr>"""
            st.markdown(html + "</table></div>", unsafe_allow_html=True)

        # ELO
        if d.get("elo_lines"):
            st.markdown('<div class="section-title">♟️ ELO Rating</div>', unsafe_allow_html=True)
            for line in d["elo_lines"]:
                name_m = re.match(r"(.+?)\s+ELO:\s*(\d+)\s+Tend:\s*([+\-][\d.]+)", line)
                if name_m:
                    trend = name_m.group(3)
                    trend_cls = "elo-trend" if "+" in trend else "elo-trend-neg"
                    st.markdown(f"""
                    <div class="elo-box">
                        <div class="elo-name">{name_m.group(1)}</div>
                        <div style="display:flex;align-items:baseline;gap:8px">
                            <div class="elo-val">{name_m.group(2)}</div>
                            <div class="{trend_cls}">{trend}/jogo</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Scenarios
        if d.get("scenario_lines"):
            st.markdown('<div class="section-title">🔮 Cenários de Sensibilidade</div>', unsafe_allow_html=True)
            html = '<div class="card"><table class="data-table" style="width:100%"><tr><th>Cenário</th><th class="num">Casa</th><th class="num">Empate</th><th class="num">Fora</th></tr>'
            for line in d["scenario_lines"]:
                nums = re.findall(r"([\d.]+)%", line)
                name = re.sub(r"[\d.]+%.*", "", line).strip()
                if len(nums) >= 3 and name:
                    html += f'<tr><td>{name}</td><td class="num">{nums[0]}%</td><td class="num">{nums[1]}%</td><td class="num">{nums[2]}%</td></tr>'
            st.markdown(html + "</table></div>", unsafe_allow_html=True)

    # ── TAB 3: Value Bets ─────────────────────────────────────────────
    with tabs[2]:
        st.markdown('<div class="section-title">🎯 Value Bets Rankeadas por EV</div>', unsafe_allow_html=True)
        if d.get("bets"):
            rank_icons = {1: "🥇", 2: "🥈", 3: "🥉"}
            # Header
            st.markdown("""
            <div class="card" style="padding:0.5rem 1rem">
            <div class="bet-row" style="border:none;background:transparent">
                <div class="bet-rank bet-header">#</div>
                <div class="bet-name bet-header" style="font-size:0.68rem">Mercado</div>
                <div class="bet-prob bet-header">Prob</div>
                <div class="bet-odd bet-header">Odd</div>
                <div class="bet-ev bet-header">EV</div>
                <div class="bet-kelly bet-header">Kelly</div>
            </div>
            """, unsafe_allow_html=True)
            for b in d["bets"]:
                r = int(b["rank"])
                icon = rank_icons.get(r, f"#{r}")
                ev_cls = "bet-ev-pos" if b["ev"] > 0 else "bet-ev-neg"
                ev_str = f"+{b['ev']:.1f}%" if b["ev"] > 0 else f"{b['ev']:.1f}%"
                kelly = b["kelly"] if b["kelly"] != "SKIP" else '<span class="bet-skip">SKIP</span>'
                bg = "#1a2d1a" if b["ev"] > 0 else "#1c2128"
                st.markdown(f"""
                <div class="bet-row" style="background:{bg}">
                    <div class="bet-rank">{icon}</div>
                    <div>
                        <div class="bet-name">{b['name']}</div>
                        <div style="font-size:0.72rem;color:#484f58">Fair odd: {b['fair']:.2f}</div>
                    </div>
                    <div class="bet-prob">{b['prob']:.0f}%</div>
                    <div class="bet-odd">{b['odd']:.2f}</div>
                    <div class="bet-ev {ev_cls}">{ev_str}</div>
                    <div class="bet-kelly">{kelly}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Nenhuma aposta com EV positivo encontrada no mercado atual.")

    # ── TAB 4: Estatísticas ───────────────────────────────────────────
    with tabs[3]:
        if d.get("metrics"):
            st.markdown('<div class="section-title">📈 Métricas Ofensivas Comparativas</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div style="font-size:0.85rem;font-weight:700;color:#58a6ff;margin-bottom:8px">🏠 {h_name}</div>', unsafe_allow_html=True)
                for m in d["metrics"]:
                    max_v = max(m["h"], m["a"], 0.01)
                    pct   = min(100, int(m["h"] / max_v * 100))
                    color = "blue" if m["h"] >= m["a"] else "red"
                    st.markdown(f"""
                    <div class="stat-bar-row">
                        <div class="label">{m['label'][:22]}</div>
                        <div class="bar-wrap"><div class="bar-inner bar-{color}" style="width:{pct}%"></div></div>
                        <div class="val">{m['h']:.1f}</div>
                    </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div style="font-size:0.85rem;font-weight:700;color:#f85149;margin-bottom:8px">✈️ {a_name}</div>', unsafe_allow_html=True)
                for m in d["metrics"]:
                    max_v = max(m["h"], m["a"], 0.01)
                    pct   = min(100, int(m["a"] / max_v * 100))
                    color = "red" if m["a"] >= m["h"] else "blue"
                    st.markdown(f"""
                    <div class="stat-bar-row">
                        <div class="label">{m['label'][:22]}</div>
                        <div class="bar-wrap"><div class="bar-inner bar-{color}" style="width:{pct}%"></div></div>
                        <div class="val">{m['a']:.1f}</div>
                    </div>""", unsafe_allow_html=True)

        # Referee
        if d.get("ref_lines"):
            st.markdown('<div class="section-title">🟨 Árbitro</div>', unsafe_allow_html=True)
            ref_html = "<br>".join(d["ref_lines"][:4])
            st.markdown(f'<div class="card card-yellow"><div style="font-size:0.88rem;color:#c9d1d9;line-height:1.9">{ref_html}</div></div>', unsafe_allow_html=True)

    # ── TAB 5: Detalhes ───────────────────────────────────────────────
    with tabs[4]:
        # Forma
        if d.get("forma_lines"):
            st.markdown('<div class="section-title">📋 Forma Recente</div>', unsafe_allow_html=True)
            html_forma = '<div class="card">'
            team = h_name
            for line in d["forma_lines"]:
                if any(r in line for r in ["🟢", "🟡", "🔴"]):
                    results = re.findall(r"(🟢|🟡|🔴)\s*([\d]-[\d])", line)
                    if results:
                        dots = ""
                        for icon, score in results:
                            cls = {"🟢": "form-w", "🟡": "form-d", "🔴": "form-l"}[icon]
                            dots += f'<span class="form-dot {cls}">{score}</span>'
                        html_forma += f'<div style="margin-bottom:8px"><span style="font-size:0.82rem;color:#8b949e;margin-right:8px">{team}</span>{dots}</div>'
                        team = a_name
            st.markdown(html_forma + "</div>", unsafe_allow_html=True)

        # Full calibration text
        calib_text = "\n".join(_extract_section(output, "CALIBRAÇÃO"))
        if calib_text.strip():
            st.markdown('<div class="section-title">🔬 Calibração & Auditoria</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card">
            <pre style="background:transparent;color:#8b949e;font-size:0.75rem;line-height:1.6;margin:0;white-space:pre-wrap">{calib_text[:3000]}</pre>
            </div>""", unsafe_allow_html=True)

    # ── TAB 6: Relatório Bruto ────────────────────────────────────────
    with tabs[5]:
        st.markdown('<div class="section-title">📄 Output Completo do Terminal</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#161b22;border:1px solid #21262d;border-radius:8px;padding:1.2rem;
                    font-family:'JetBrains Mono','Courier New',monospace;font-size:0.73rem;
                    line-height:1.55;white-space:pre;overflow-x:auto;color:#8b949e;max-height:600px;overflow-y:auto">
{output[:15000]}
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# STATUS PILL HELPER
# ══════════════════════════════════════════════════════════════════════
def _status_pill(status):
    live = {"1H","2H","HT","ET","BT","P","SUSP","INT","LIVE"}
    done = {"FT","AET","PEN","AWD","WO"}
    if status in live:
        return '<span style="background:#1f2d1f;color:#3fb950;border:1px solid #3fb95055;border-radius:20px;padding:2px 8px;font-size:0.68rem">🔴 AO VIVO</span>'
    elif status in done:
        return '<span style="background:#2a1f1f;color:#f85149;border:1px solid #f8514955;border-radius:20px;padding:2px 8px;font-size:0.68rem">✅ ENCERRADO</span>'
    return '<span style="background:#1a2440;color:#58a6ff;border:1px solid #1f6feb55;border-radius:20px;padding:2px 8px;font-size:0.68rem">🕐 AGENDADO</span>'


# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1.2rem 0 0.5rem">
        <div style="font-size:2.5rem">⚽</div>
        <div style="font-size:1rem;font-weight:700;color:#e6edf3;margin-top:4px">Copa 2026</div>
        <div style="font-size:0.72rem;color:#484f58">Analyst Pro · V3</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    page = st.radio("", [
        "📅  Calendário",
        "🚀  Análise Pré-Jogo",
        "📡  Trading Ao Vivo",
        "ℹ️  Sobre",
    ], label_visibility="collapsed")

    st.divider()
    sel_date = st.date_input("", value=datetime.date.today(),
                              min_value=datetime.date(2026, 6, 1),
                              max_value=datetime.date(2026, 7, 20),
                              label_visibility="collapsed")
    st.divider()
    st.markdown("""
    <div style="font-size:0.68rem;color:#484f58;line-height:2">
        Monte Carlo · Poisson · ELO<br>
        ML Calibrado · xG · API V3<br>
        Kelly · GII · Momentum<br>
        Cashout · Trader AI
    </div>
    """, unsafe_allow_html=True)


date_str = sel_date.strftime("%Y-%m-%d")
mod, mod_err = get_module()


# ══════════════════════════════════════════════════════════════════════
# PAGE: Calendário
# ══════════════════════════════════════════════════════════════════════
if page == "📅  Calendário":
    st.markdown(f"## 📅 Calendário — {date_str}")

    with st.spinner("Buscando partidas..."):
        matches = fetch_matches(date_str)

    if not matches:
        st.markdown('<div class="alert alert-info">⚽ Nenhuma partida encontrada. Tente outra data.</div>', unsafe_allow_html=True)
    else:
        live_c  = sum(1 for m in matches if m["fixture"]["status"]["short"] in {"1H","2H","HT","ET"})
        done_c  = sum(1 for m in matches if m["fixture"]["status"]["short"] in {"FT","AET","PEN"})
        sched_c = len(matches) - live_c - done_c

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", len(matches))
        c2.metric("🔴 Ao Vivo", live_c)
        c3.metric("✅ Encerrados", done_c)
        c4.metric("🕐 Agendados", sched_c)
        st.markdown("---")

        cols = st.columns(min(len(matches), 3))
        for i, m in enumerate(matches):
            fid    = m["fixture"]["id"]
            h_t    = m["teams"]["home"]
            a_t    = m["teams"]["away"]
            status = m["fixture"]["status"]["short"]
            t_str  = m["fixture"]["date"].split("T")[1][:5] if "T" in m["fixture"]["date"] else "--:--"
            gh     = m.get("goals", {}).get("home")
            ga     = m.get("goals", {}).get("away")
            score  = f"{gh} — {ga}" if gh is not None else "⚫ ⚫"
            with cols[i % 3]:
                st.markdown(f"""
                <div class="card" style="text-align:center">
                    <div style="font-size:0.72rem;color:#484f58;margin-bottom:8px">⏰ {t_str} BRT &nbsp;·&nbsp; #{fid}</div>
                    <div style="font-size:1rem;font-weight:700;color:#e6edf3">🏠 {h_t['name']}</div>
                    <div style="font-size:1.8rem;font-weight:800;color:#58a6ff;margin:6px 0">{score}</div>
                    <div style="font-size:1rem;font-weight:700;color:#e6edf3">✈️ {a_t['name']}</div>
                    <div style="margin-top:10px">{_status_pill(status)}</div>
                </div>""", unsafe_allow_html=True)

    if st.button("🔄 Atualizar lista"):
        st.cache_data.clear()
        st.rerun()


# ══════════════════════════════════════════════════════════════════════
# PAGE: Análise Pré-Jogo
# ══════════════════════════════════════════════════════════════════════
elif page == "🚀  Análise Pré-Jogo":
    st.markdown("## 🚀 Análise Pré-Jogo V3 PRO")

    if mod_err:
        st.error(f"Erro no módulo:\n```\n{mod_err[:500]}\n```")
        st.stop()

    with st.spinner("Buscando partidas..."):
        matches = fetch_matches(date_str)

    if not matches:
        st.warning(f"Nenhuma partida em {date_str}.")
        st.stop()

    match_opts = {}
    for m in matches:
        h_t = m["teams"]["home"]; a_t = m["teams"]["away"]
        t_str = m["fixture"]["date"].split("T")[1][:5] if "T" in m["fixture"]["date"] else "--"
        label = f"{h_t['name']}  ×  {a_t['name']}  ({t_str})"
        match_opts[label] = {
            "fixture_id": m["fixture"]["id"],
            "home_id": h_t["id"], "home_name": h_t["name"],
            "away_id": a_t["id"], "away_name": a_t["name"],
            "time": t_str, "raw_data": m,
        }

    sel_label = st.selectbox("Partida:", list(match_opts.keys()))
    sel = match_opts[sel_label]

    if st.button("🚀 Rodar Análise Completa", type="primary", use_container_width=True):
        mod.selected_match = sel

        progress = st.progress(0)
        msgs = [
            (12,  "📡 Conectando à API-Football..."),
            (28,  "📊 Histórico dos times..."),
            (44,  "🧮 Calculando lambdas e xG..."),
            (62,  "🎲 Monte Carlo + Poisson + ML..."),
            (80,  "⚡ EV, Kelly e Ensemble..."),
            (94,  "📝 Gerando relatório..."),
        ]
        placeholder = st.empty()
        for pct, msg in msgs:
            progress.progress(pct, text=msg)
            placeholder.caption(msg)
            time.sleep(0.25)

        output, err = run_captured(mod.execute_advanced_pre_live_analysis_v3)
        progress.progress(100, text="✅ Análise concluída!")
        placeholder.empty()
        time.sleep(0.3)
        progress.empty()

        if err:
            with st.expander("⚠️ Erros durante análise"):
                st.code(err)

        if output:
            render_report(output, sel)
        else:
            st.warning("Análise sem output. Verifique se a partida tem dados disponíveis.")


# ══════════════════════════════════════════════════════════════════════
# PAGE: Trading Ao Vivo
# ══════════════════════════════════════════════════════════════════════
elif page == "📡  Trading Ao Vivo":
    st.markdown("## 📡 Trading Ao Vivo")

    if mod_err:
        st.error(f"Erro no módulo:\n```\n{mod_err[:500]}\n```")
        st.stop()

    with st.spinner("Verificando partidas ao vivo..."):
        live_matches = fetch_live_matches()

    all_day = fetch_matches(date_str)

    if live_matches:
        st.markdown(f'<div class="alert alert-ok">🔴 {len(live_matches)} partida(s) ao vivo detectada(s)</div>', unsafe_allow_html=True)
        use_matches = live_matches
    else:
        st.markdown('<div class="alert alert-warn">⚪ Nenhuma partida ao vivo — mostrando partidas do dia</div>', unsafe_allow_html=True)
        use_matches = all_day

    if not use_matches:
        st.info("Nenhuma partida disponível.")
        st.stop()

    live_opts = {}
    for m in use_matches:
        h_t = m["teams"]["home"]; a_t = m["teams"]["away"]
        gh  = m.get("goals", {}).get("home", 0) or 0
        ga  = m.get("goals", {}).get("away", 0) or 0
        mn  = m["fixture"]["status"].get("elapsed") or "--"
        label = f"{h_t['name']}  {gh}–{ga}  {a_t['name']}  ({mn}')"
        live_opts[label] = {
            "fixture_id": m["fixture"]["id"],
            "home_id": h_t["id"], "home_name": h_t["name"],
            "away_id": a_t["id"], "away_name": a_t["name"],
            "score_h": gh, "score_a": ga, "minute": mn,
        }

    sel_live_label = st.selectbox("Partida:", list(live_opts.keys()))
    live_sel = live_opts[sel_live_label]

    c1, c2 = st.columns([3, 1])
    with c1: start_btn = st.button("▶️ Atualizar Dashboard", type="primary", use_container_width=True)
    with c2: auto_ref  = st.toggle("🔄 Auto (30s)", value=False)

    if "live_history" not in st.session_state: st.session_state.live_history = []
    if "last_live_fid" not in st.session_state: st.session_state.last_live_fid = None
    if st.session_state.last_live_fid != live_sel["fixture_id"]:
        st.session_state.live_history = []
        st.session_state.last_live_fid = live_sel["fixture_id"]

    def _do_live():
        output, snap, new_hist, trader = run_live_single_cycle(
            mod, live_sel["fixture_id"], live_sel["home_name"],
            live_sel["away_name"], live_sel["home_id"],
            st.session_state.live_history)
        st.session_state.live_history = new_hist

        # Score header
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("⏱️", f"{live_sel['minute']}'")
        c2.metric("🏠 " + live_sel["home_name"][:16], live_sel["score_h"])
        c3.metric("✈️ " + live_sel["away_name"][:16], live_sel["score_a"])
        c4.metric("Ciclos", len(st.session_state.live_history))

        # Trader AI card
        if trader:
            conf = trader.get("confidence", 0)
            col = "#3fb950" if conf >= 70 else ("#d97706" if conf >= 50 else "#f85149")
            st.markdown(f"""
            <div class="card card-accent" style="margin:0.8rem 0">
                <div class="section-title">🤖 Trader Assistant</div>
                <div style="font-size:0.92rem;color:#c9d1d9;margin-bottom:8px">{trader.get('narrative','')}</div>
                <div style="display:flex;align-items:center;gap:12px">
                    <span style="font-size:0.9rem;font-weight:700;color:#e6edf3">{trader.get('recommendation','')}</span>
                    <span style="font-size:0.88rem;font-weight:700;color:{col}">Confiança: {conf}%</span>
                </div>
            </div>""", unsafe_allow_html=True)

        # Live stats bars
        if snap:
            st.markdown('<div class="section-title" style="margin-top:1rem">📊 Estatísticas ao Vivo</div>', unsafe_allow_html=True)
            cols = st.columns(2)
            h_upi = snap.get("h_shots",0)*2+snap.get("h_sot",0)*4+snap.get("h_corners",0)*3
            a_upi = snap.get("a_shots",0)*2+snap.get("a_sot",0)*4+snap.get("a_corners",0)*3
            stats = [
                ("UPI Pressão", h_upi, a_upi, 120),
                ("Chutes Totais", snap.get("h_shots",0), snap.get("a_shots",0), 25),
                ("No Alvo", snap.get("h_sot",0), snap.get("a_sot",0), 15),
                ("Escanteios", snap.get("h_corners",0), snap.get("a_corners",0), 12),
                ("Ataques Perig.", snap.get("h_dangerous",0), snap.get("a_dangerous",0), 12),
                ("Faltas", snap.get("h_fouls",0), snap.get("a_fouls",0), 20),
            ]
            with cols[0]:
                st.markdown(f'<div style="font-size:0.85rem;font-weight:700;color:#58a6ff;margin-bottom:8px">🏠 {live_sel["home_name"]}</div>', unsafe_allow_html=True)
                for label, hv, av, mx in stats:
                    pct = min(100, int(hv/max(mx,1)*100))
                    col_cls = "blue" if hv >= av else "red"
                    st.markdown(f'<div class="stat-bar-row"><div class="label">{label}</div><div class="bar-wrap"><div class="bar-inner bar-{col_cls}" style="width:{pct}%"></div></div><div class="val">{hv}</div></div>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f'<div style="font-size:0.85rem;font-weight:700;color:#f85149;margin-bottom:8px">✈️ {live_sel["away_name"]}</div>', unsafe_allow_html=True)
                for label, hv, av, mx in stats:
                    pct = min(100, int(av/max(mx,1)*100))
                    col_cls = "red" if av >= hv else "blue"
                    st.markdown(f'<div class="stat-bar-row"><div class="label">{label}</div><div class="bar-wrap"><div class="bar-inner bar-{col_cls}" style="width:{pct}%"></div></div><div class="val">{av}</div>', unsafe_allow_html=True)

        # Full dashboard output
        with st.expander("📋 Dashboard Completo (terminal)", expanded=False):
            st.markdown(f"""
            <div style="background:#161b22;border-radius:8px;padding:1rem;font-family:'Courier New',monospace;
                        font-size:0.73rem;line-height:1.55;white-space:pre;overflow-x:auto;color:#8b949e">
{output[:8000]}
            </div>""", unsafe_allow_html=True)

        st.caption(f"🔄 {datetime.datetime.now().strftime('%H:%M:%S')} · Histórico: {len(st.session_state.live_history)} ciclo(s)")

    if start_btn:
        with st.spinner("📡 Coletando dados ao vivo..."):
            _do_live()

    if auto_ref:
        with st.spinner("📡 Atualizando..."):
            _do_live()
        time.sleep(30)
        st.rerun()


# ══════════════════════════════════════════════════════════════════════
# PAGE: Sobre
# ══════════════════════════════════════════════════════════════════════
elif page == "ℹ️  Sobre":
    st.markdown("## ℹ️ Sobre")
    st.markdown("""
    <div class="card card-accent">
        <div class="section-title">⚽ Copa do Mundo 2026 — Análise Profissional V3 PRO</div>
        <p style="color:#8b949e;font-size:0.9rem">Sistema de análise quantitativa e trading para apostas esportivas.</p>
        <table class="data-table" style="width:100%;margin-top:1rem">
            <tr><th>Modelo</th><th>Peso</th><th>Método</th></tr>
            <tr><td>Monte Carlo</td><td>30%</td><td>50.000 simulações estocásticas</td></tr>
            <tr><td>Poisson</td><td>25%</td><td>Distribuição de probabilidade de gols</td></tr>
            <tr><td>Machine Learning</td><td>20%</td><td>Regressão logística + Platt Scaling</td></tr>
            <tr><td>API-Football</td><td>15%</td><td>Predição nativa da plataforma</td></tr>
            <tr><td>ELO Contextual</td><td>10%</td><td>Rating dinâmico com HFA e forma</td></tr>
        </table>
    </div>
    <div class="card card-green" style="margin-top:0.5rem">
        <div class="section-title">💰 Módulos Financeiros</div>
        <table class="data-table" style="width:100%">
            <tr><td>Value Betting Engine</td><td class="muted">EV calculado por mercado, rankeado por edge</td></tr>
            <tr><td>Kelly Criterion</td><td class="muted">Full / 50% / 25% — stake ótimo por banca</td></tr>
            <tr><td>Closing Line Value (CLV)</td><td class="muted">Validação de edge ao longo do tempo</td></tr>
        </table>
    </div>
    <div class="card card-purple" style="margin-top:0.5rem">
        <div class="section-title">📡 16 Módulos Live</div>
        <table class="data-table" style="width:100%">
            <tr><td>GII — Goal Imminent Index</td><td class="muted">Score 0-100 de iminência de gol</td></tr>
            <tr><td>UPI — Unified Pressure Index</td><td class="muted">Pressão ponderada + sparklines</td></tr>
            <tr><td>Momentum Engine</td><td class="muted">Janelas 1/3/5/10 ciclos</td></tr>
            <tr><td>xG Momentum Live</td><td class="muted">Aceleração de xG em tempo real</td></tr>
            <tr><td>Anti-False Over</td><td class="muted">Detector de pressão estéril</td></tr>
            <tr><td>Smart Cashout</td><td class="muted">Recomendação inteligente de saída</td></tr>
            <tr><td>Win Probability Live</td><td class="muted">Poisson residual por minuto restante</td></tr>
            <tr><td>Trader Assistant AI</td><td class="muted">Narrativa + recomendação + confiança</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
