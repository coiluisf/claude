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
import requests
import importlib.util
import builtins
import time

# ── Page config (must be first Streamlit call) ────────────────────────
st.set_page_config(
    page_title="⚽ Copa 2026 Analyst",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Sistema de Análise Profissional — Copa do Mundo 2026"},
)

# ── Global CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Base */
.stApp { background-color: #0d1117; color: #e6edf3; }
.block-container { padding: 1.5rem 2rem 2rem; max-width: 1400px; }

/* Terminal output */
.terminal-output {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.2rem;
    font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
    font-size: 0.76rem;
    line-height: 1.55;
    white-space: pre;
    overflow-x: auto;
    color: #c9d1d9;
}

/* Cards */
.match-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1.2rem;
    margin-bottom: 0.5rem;
    transition: border-color 0.2s;
}
.match-card:hover { border-color: #58a6ff; }
.match-card .time-badge {
    font-size: 0.72rem;
    color: #8b949e;
    margin-bottom: 0.4rem;
}
.match-card .team-name { font-size: 1rem; font-weight: 600; color: #e6edf3; }
.match-card .score { font-size: 1.8rem; font-weight: 800; color: #58a6ff; text-align: center; }
.match-card .status-pill {
    display: inline-block;
    font-size: 0.68rem;
    padding: 2px 8px;
    border-radius: 20px;
    margin-top: 0.4rem;
}
.status-live    { background: #1f2d1f; color: #3fb950; border: 1px solid #3fb950; }
.status-sched   { background: #1a2440; color: #58a6ff; border: 1px solid #58a6ff; }
.status-done    { background: #2a1f1f; color: #f85149; border: 1px solid #f85149; }

/* Metric override */
div[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 0.8rem 1rem;
}
div[data-testid="stMetricValue"] { font-size: 1.6rem; font-weight: 700; }

/* Buttons */
.stButton > button {
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1f6feb, #388bfd);
    border: none;
}
.stButton > button[kind="primary"]:hover { opacity: 0.88; transform: translateY(-1px); }

/* Sidebar */
section[data-testid="stSidebar"] { background: #161b22; border-right: 1px solid #30363d; }
section[data-testid="stSidebar"] .stRadio label { font-size: 0.9rem; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #161b22; border-radius: 8px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 6px; font-weight: 500; }
.stTabs [aria-selected="true"] { background: #1f6feb !important; color: white !important; }

/* Alert boxes */
.alert-critical { background:#2a1a1a; border-left:3px solid #f85149; border-radius:6px; padding:0.8rem; margin:0.4rem 0; }
.alert-warning  { background:#2a2010; border-left:3px solid #d29922; border-radius:6px; padding:0.8rem; margin:0.4rem 0; }
.alert-success  { background:#1a2a1a; border-left:3px solid #3fb950; border-radius:6px; padding:0.8rem; margin:0.4rem 0; }
.alert-info     { background:#1a1f2a; border-left:3px solid #58a6ff; border-radius:6px; padding:0.8rem; margin:0.4rem 0; }

/* Progress bars */
.bar-container { display:flex; align-items:center; gap:8px; margin:2px 0; }
.bar-track { background:#21262d; border-radius:4px; height:8px; flex:1; overflow:hidden; }
.bar-fill  { height:8px; border-radius:4px; transition: width 0.4s; }
.bar-blue  { background: linear-gradient(90deg, #1f6feb, #58a6ff); }
.bar-green { background: linear-gradient(90deg, #238636, #3fb950); }
.bar-red   { background: linear-gradient(90deg, #b91c1c, #f85149); }
.bar-orange{ background: linear-gradient(90deg, #b45309, #d97706); }

/* Divider */
hr { border-color: #30363d; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────
API_KEY   = os.environ.get("API_KEY", "906f4989978807460c85bcc0c9e87367")
BASE_URL  = "https://v3.football.api-sports.io"
HEADERS   = {"x-apisports-key": API_KEY}
WC_LEAGUE = 1
WC_SEASON = 2026


# ── Load analysis module safely ───────────────────────────────────────
@st.cache_resource(show_spinner="⚙️ Carregando módulos de análise...")
def _load_module():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "programa_analise_v3.py")
    spec = importlib.util.spec_from_file_location("analise_v3", path)
    mod  = importlib.util.module_from_spec(spec)

    # Patch input() to never block during import
    original_input = builtins.input
    builtins.input = lambda *a, **k: ""
    try:
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            spec.loader.exec_module(mod)
    finally:
        builtins.input = original_input

    # Patch module-level functions that interfere with web context
    mod._clear = lambda: None                    # no terminal clear
    mod.CLEAR_SCREEN = False
    return mod


def get_module():
    try:
        return _load_module(), None
    except Exception as e:
        import traceback
        return None, traceback.format_exc()


# ── API helpers ───────────────────────────────────────────────────────
@st.cache_data(ttl=90, show_spinner=False)
def fetch_matches(date_str: str):
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
    """Run fn(*args, **kwargs) capturing all print output. Returns (output, error)."""
    buf = io.StringIO()
    err = None
    original_input = builtins.input
    builtins.input = lambda *a, **k: ""   # mock all input() calls
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
    """Run a single polling cycle of the live dashboard."""
    if history is None:
        history = []

    buf = io.StringIO()
    original_input = builtins.input
    builtins.input = lambda *a, **k: ""

    try:
        with contextlib.redirect_stdout(buf):
            snap = mod._snapshot(fixture_id, home_id)
            if snap is None:
                buf.write("⚠️  Aguardando dados da API... Partida pode não ter iniciado.\n")
                return buf.getvalue(), None, history, None

            goal_sigs   = mod._signal_goal(snap, history, h_name, a_name)
            corner_sigs = mod._signal_corner(snap, history, h_name, a_name)
            card_sigs   = mod._signal_card(snap, history, h_name, a_name, snap["minute"])
            consciousness = mod._game_consciousness(snap, history, h_name, a_name)

            try:
                _lf = mod.calculate_live_fair_odds(snap, history,
                          snap.get("minute",1), snap.get("score_h",0),
                          snap.get("score_a",0), h_name, a_name)
            except Exception:
                _lf = None
            try:
                _fp_h = mod.detect_false_pressure(snap, "h_", snap.get("minute",1))
                _fp_a = mod.detect_false_pressure(snap, "a_", snap.get("minute",1))
            except Exception:
                _fp_h = _fp_a = None
            try:
                _regime = mod.detect_game_regime(snap, history, h_name, a_name)
            except Exception:
                _regime = None
            try:
                _evts = mod._fetch_live_events(fixture_id)
            except Exception:
                _evts = None

            try:
                _mom  = mod._live_momentum_engine(snap, history)
                _ph   = mod._pressure_windows(snap, history, "h_")
                _pa   = mod._pressure_windows(snap, history, "a_")
                _gii  = mod._goal_imminent_index(snap, history,
                            _mom["h_score"], _mom["a_score"], _ph, _pa)
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
            except Exception:
                _mom=_ph=_pa=_gii=_aoh=_aoa=_cash=_coh=_coa=_tact=_fat=None
                _xgm=_red=_gs=_wp=_ta=_alrt=None

            mod._render_dashboard(
                snap, history, h_name, a_name, home_id,
                goal_sigs, corner_sigs, card_sigs, 1, 30, consciousness,
                live_fair=_lf, regime=_regime,
                false_pressure_h=_fp_h, false_pressure_a=_fp_a,
                live_events=_evts,
                v5_momentum=_mom, v5_press_h=_ph, v5_press_a=_pa,
                v5_gii=_gii, v5_anti_h=_aoh, v5_anti_a=_aoa,
                v5_cashout=_cash, v5_corn_h=_coh, v5_corn_a=_coa,
                v5_tactical=_tact, v5_fatigue=_fat, v5_xgm=_xgm,
                v5_red=_red, v5_game_state=_gs, v5_win_prob=_wp,
                v5_trader=_ta, v5_alerts=_alrt,
            )

            history.append(snap)
            if len(history) > 8:
                history.pop(0)

            return buf.getvalue(), snap, history, _ta

    except Exception as e:
        import traceback
        return traceback.format_exc(), None, history, None
    finally:
        builtins.input = original_input


# ── Helper renderers ──────────────────────────────────────────────────
def _status_pill(status):
    live_statuses = {"1H","2H","HT","ET","BT","P","SUSP","INT","LIVE"}
    done_statuses = {"FT","AET","PEN","AWD","WO"}
    if status in live_statuses:
        return f'<span class="status-pill status-live">🔴 AO VIVO</span>'
    elif status in done_statuses:
        return f'<span class="status-pill status-done">✅ ENCERRADO</span>'
    else:
        return f'<span class="status-pill status-sched">🕐 AGENDADO</span>'


def _html_bar(value, max_val, color="blue", label=""):
    pct = min(100, int(value / max(max_val, 1) * 100))
    return f"""
    <div class="bar-container">
        <span style="width:140px;font-size:0.78rem;color:#8b949e;">{label}</span>
        <div class="bar-track"><div class="bar-fill bar-{color}" style="width:{pct}%"></div></div>
        <span style="width:36px;font-size:0.82rem;font-weight:600;text-align:right;">{value}</span>
    </div>"""


# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0">
        <div style="font-size:3rem">⚽</div>
        <div style="font-size:1.1rem;font-weight:700;color:#e6edf3">Copa 2026</div>
        <div style="font-size:0.75rem;color:#8b949e">Análise Profissional V3 PRO</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio("Navegação", [
        "📅  Calendário",
        "🚀  Análise Pré-Jogo",
        "📡  Trading Ao Vivo",
        "ℹ️  Sobre",
    ], label_visibility="collapsed")

    st.divider()
    sel_date = st.date_input("Data", value=datetime.date.today(),
                              min_value=datetime.date(2026, 6, 1),
                              max_value=datetime.date(2026, 7, 20),
                              label_visibility="visible")

    st.divider()
    st.markdown("""
    <div style="font-size:0.7rem;color:#484f58;line-height:1.8">
        <b style="color:#8b949e">Modelos</b><br>
        Monte Carlo · Poisson · ELO<br>
        Machine Learning · xG · API<br><br>
        <b style="color:#8b949e">Módulos</b><br>
        Kelly Criterion · Value Betting<br>
        GII · Momentum · Pressão<br>
        Cashout · Trader Assistant
    </div>
    """, unsafe_allow_html=True)


date_str = sel_date.strftime("%Y-%m-%d")
mod, mod_err = get_module()

# ══════════════════════════════════════════════════════════════════════
# PAGE: Calendário
# ══════════════════════════════════════════════════════════════════════
if page == "📅  Calendário":
    st.markdown(f"## 📅 Calendário — {date_str}")
    st.caption("Copa do Mundo 2026 · Fuso: Brasília (UTC-3)")

    with st.spinner("Buscando partidas..."):
        matches = fetch_matches(date_str)

    if not matches:
        st.markdown("""
        <div class="alert-info">
            <b>⚽ Nenhuma partida encontrada</b><br>
            Tente outra data. A Copa do Mundo 2026 começa em 11 de junho de 2026.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Summary metrics
        live_count = sum(1 for m in matches
                         if m["fixture"]["status"]["short"] in {"1H","2H","HT","ET"})
        done_count = sum(1 for m in matches
                         if m["fixture"]["status"]["short"] in {"FT","AET","PEN"})
        sched_count = len(matches) - live_count - done_count

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total", len(matches))
        c2.metric("Ao Vivo 🔴", live_count)
        c3.metric("Encerrados ✅", done_count)
        c4.metric("Agendados 🕐", sched_count)

        st.markdown("---")

        cols = st.columns(min(len(matches), 3))
        for i, m in enumerate(matches):
            fid    = m["fixture"]["id"]
            h_t    = m["teams"]["home"]
            a_t    = m["teams"]["away"]
            status = m["fixture"]["status"]["short"]
            dt_raw = m["fixture"]["date"]
            t_str  = dt_raw.split("T")[1][:5] if "T" in dt_raw else "--:--"
            gh     = m.get("goals", {}).get("home")
            ga     = m.get("goals", {}).get("away")
            score  = f"{gh} — {ga}" if gh is not None else "— vs —"

            with cols[i % 3]:
                st.markdown(f"""
                <div class="match-card">
                    <div class="time-badge">⏰ {t_str} BRT &nbsp;·&nbsp; #{fid}</div>
                    <div class="team-name">🏠 {h_t['name']}</div>
                    <div class="score">{score}</div>
                    <div class="team-name">✈️ {a_t['name']}</div>
                    <div>{_status_pill(status)}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.caption(f"🔄 Cache: 90s · Última busca: {datetime.datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔄 Atualizar"):
            st.cache_data.clear()
            st.rerun()


# ══════════════════════════════════════════════════════════════════════
# PAGE: Análise Pré-Jogo
# ══════════════════════════════════════════════════════════════════════
elif page == "🚀  Análise Pré-Jogo":
    st.markdown("## 🚀 Análise Pré-Jogo V3 PRO")
    st.caption("Relatório completo: Ensemble · ELO · xG · Kelly · Cenários · Narrativa")

    if mod_err:
        st.error(f"Erro no módulo de análise:\n```\n{mod_err}\n```")
        st.stop()

    with st.spinner("Buscando partidas..."):
        matches = fetch_matches(date_str)

    if not matches:
        st.warning(f"Nenhuma partida em {date_str}.")
        st.stop()

    # Build options
    match_opts = {}
    for m in matches:
        h_t = m["teams"]["home"]; a_t = m["teams"]["away"]
        dt_raw = m["fixture"]["date"]
        t_str  = dt_raw.split("T")[1][:5] if "T" in dt_raw else "--"
        label  = f"{h_t['name']}  x  {a_t['name']}  ({t_str})"
        match_opts[label] = {
            "fixture_id": m["fixture"]["id"],
            "home_id": h_t["id"], "home_name": h_t["name"],
            "away_id": a_t["id"], "away_name": a_t["name"],
            "time": t_str, "raw_data": m,
        }

    sel_label = st.selectbox("Selecione a partida:", list(match_opts.keys()), key="pregame_sel")
    sel = match_opts[sel_label]

    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        run_btn = st.button("🚀 Rodar Análise Completa", type="primary", use_container_width=True,
                            key="run_pregame")
    with c2:
        val_btn = st.button("🎯 Só Value Bets & Kelly", use_container_width=True, key="run_value")
    with c3:
        st.write("")  # spacer

    if run_btn or val_btn:
        mod.selected_match = sel

        progress = st.progress(0, text="Iniciando coleta de dados...")
        status_txt = st.empty()

        steps = [
            (10, "📡 Conectando à API-Football..."),
            (25, "📊 Coletando histórico dos times..."),
            (45, "🧮 Calculando lambdas e xG..."),
            (65, "🎲 Rodando Monte Carlo + Poisson + ML..."),
            (80, "⚡ Calculando EV, Kelly e Ensemble..."),
            (95, "📝 Gerando relatório final..."),
        ]

        for pct, msg in steps:
            progress.progress(pct, text=msg)
            time.sleep(0.3)

        output, err = run_captured(mod.execute_advanced_pre_live_analysis_v3)
        progress.progress(100, text="✅ Concluído!")
        time.sleep(0.3)
        progress.empty()
        status_txt.empty()

        if err:
            st.markdown(f'<div class="alert-critical">❌ <b>Erro durante análise:</b><br><pre style="font-size:0.72rem;margin-top:0.5rem">{err}</pre></div>',
                        unsafe_allow_html=True)

        if output:
            tabs = st.tabs(["📊 Relatório Completo", "🎯 Value Bets", "📈 Calibração"])

            with tabs[0]:
                st.markdown(f'<div class="terminal-output">{output}</div>', unsafe_allow_html=True)

            with tabs[1]:
                lines = output.split("\n")
                # Extract VALUE BETTING section
                start = next((i for i, l in enumerate(lines) if "VALUE BETTING" in l), None)
                end_  = next((i for i, l in enumerate(lines[start or 0:], start or 0)
                              if i > (start or 0) and "╚" in l), len(lines))
                if start:
                    vb_text = "\n".join(lines[start:end_+1])
                    st.markdown(f'<div class="terminal-output">{vb_text}</div>', unsafe_allow_html=True)
                else:
                    st.info("Seção de Value Bets não encontrada no output.")

            with tabs[2]:
                lines = output.split("\n")
                start = next((i for i, l in enumerate(lines) if "CALIBRAÇÃO" in l), None)
                if start:
                    cal_text = "\n".join(lines[start:])
                    st.markdown(f'<div class="terminal-output">{cal_text}</div>', unsafe_allow_html=True)
                else:
                    st.info("Seção de calibração não encontrada.")
        else:
            st.warning("A análise não gerou output. Verifique se a partida tem dados disponíveis.")


# ══════════════════════════════════════════════════════════════════════
# PAGE: Trading Ao Vivo
# ══════════════════════════════════════════════════════════════════════
elif page == "📡  Trading Ao Vivo":
    st.markdown("## 📡 Dashboard de Trading Ao Vivo")
    st.caption("Atualização automática · GII · Momentum · Win Probability · Trader Assistant")

    if mod_err:
        st.error(f"Erro no módulo de análise:\n```\n{mod_err}\n```")
        st.stop()

    # Live match selector
    with st.spinner("Buscando partidas ao vivo..."):
        live_matches = fetch_live_matches()

    # Also check scheduled matches for today as fallback
    all_day_matches = fetch_matches(date_str)

    if not live_matches:
        st.markdown("""
        <div class="alert-warning">
            <b>⚪ Nenhuma partida ao vivo no momento</b><br>
            Você pode monitorar partidas agendadas para hoje abaixo.
        </div>
        """, unsafe_allow_html=True)
        use_matches = all_day_matches
        is_live_mode = False
    else:
        st.markdown(f'<div class="alert-success">🔴 <b>{len(live_matches)} partida(s) ao vivo detectada(s)</b></div>',
                    unsafe_allow_html=True)
        use_matches = live_matches
        is_live_mode = True

    if not use_matches:
        st.info("Nenhuma partida disponível para monitoramento.")
        st.stop()

    live_opts = {}
    for m in use_matches:
        h_t = m["teams"]["home"]; a_t = m["teams"]["away"]
        gh  = m.get("goals", {}).get("home", 0) or 0
        ga  = m.get("goals", {}).get("away", 0) or 0
        mn  = m["fixture"]["status"].get("elapsed") or "--"
        status = m["fixture"]["status"]["short"]
        label = f"{h_t['name']}  {gh}–{ga}  {a_t['name']}  ({mn}'  ·  {status})"
        live_opts[label] = {
            "fixture_id": m["fixture"]["id"],
            "home_id": h_t["id"], "home_name": h_t["name"],
            "away_id": a_t["id"], "away_name": a_t["name"],
            "score_h": gh, "score_a": ga, "minute": mn,
        }

    sel_live_label = st.selectbox("Partida:", list(live_opts.keys()), key="live_sel")
    live_sel = live_opts[sel_live_label]

    # Controls
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        start_btn = st.button("▶️ Atualizar Dashboard", type="primary",
                               use_container_width=True, key="live_start")
    with col2:
        auto_ref = st.toggle("🔄 Auto-refresh (30s)", value=False, key="auto_ref")
    with col3:
        if st.button("🗑️ Limpar Cache", key="clear_live"):
            st.cache_data.clear()
            st.rerun()

    # History stored in session state
    if "live_history" not in st.session_state:
        st.session_state.live_history = []
    if "last_live_fid" not in st.session_state:
        st.session_state.last_live_fid = None

    # Reset history when match changes
    if st.session_state.last_live_fid != live_sel["fixture_id"]:
        st.session_state.live_history = []
        st.session_state.last_live_fid = live_sel["fixture_id"]

    dashboard_area = st.empty()

    def _render_live():
        output, snap, new_history, trader = run_live_single_cycle(
            mod,
            live_sel["fixture_id"],
            live_sel["home_name"],
            live_sel["away_name"],
            live_sel["home_id"],
            st.session_state.live_history,
        )
        st.session_state.live_history = new_history

        with dashboard_area.container():
            # Top info bar
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("⏱️ Minuto", f"{live_sel['minute']}'")
            c2.metric("🏠 Casa", live_sel["home_name"][:18])
            c3.metric("✈️ Visita", live_sel["away_name"][:18])
            c4.metric("⚽ Placar", f"{live_sel['score_h']} – {live_sel['score_a']}")

            if trader:
                conf = trader.get("confidence", 0)
                rec  = trader.get("recommendation", "")
                narr = trader.get("narrative", "")
                col  = "#3fb950" if conf >= 70 else ("#d97706" if conf >= 50 else "#f85149")
                st.markdown(f"""
                <div class="alert-info" style="margin:0.8rem 0">
                    <b>🤖 Trader Assistant</b> &nbsp;·&nbsp; Confiança:
                    <span style="color:{col};font-weight:700">{conf}%</span> &nbsp;·&nbsp;
                    <span style="font-weight:600">{rec}</span><br>
                    <span style="color:#8b949e;font-size:0.85rem">{narr}</span>
                </div>
                """, unsafe_allow_html=True)

            # Main terminal output
            tabs = st.tabs(["📊 Dashboard Completo", "📋 Sinais", "⚡ Métricas Rápidas"])
            with tabs[0]:
                st.markdown(f'<div class="terminal-output">{output}</div>', unsafe_allow_html=True)

            with tabs[1]:
                lines = output.split("\n")
                sig_start = next((i for i, l in enumerate(lines) if "SINAIS ATIVOS" in l), None)
                alr_start = next((i for i, l in enumerate(lines) if "ALERTAS" in l), None)
                if sig_start:
                    sig_end = next((i for i, l in enumerate(lines[sig_start:], sig_start)
                                    if i > sig_start and ("╠" in l or "╚" in l)), sig_start+20)
                    sig_text = "\n".join(lines[sig_start:sig_end])
                    st.markdown(f'<div class="terminal-output">{sig_text}</div>', unsafe_allow_html=True)
                if alr_start:
                    alr_end = next((i for i, l in enumerate(lines[alr_start:], alr_start)
                                    if i > alr_start and ("╠" in l or "╚" in l)), alr_start+20)
                    alr_text = "\n".join(lines[alr_start:alr_end])
                    st.markdown(f'<div class="terminal-output">{alr_text}</div>', unsafe_allow_html=True)
                if not sig_start and not alr_start:
                    st.info("Nenhum sinal ativo no momento.")

            with tabs[2]:
                # Quick metrics extracted from snap if available
                if snap:
                    ma, mb = st.columns(2)
                    with ma:
                        st.markdown("**🏠 Casa**")
                        st.markdown(_html_bar(snap.get("h_shots",0), 25, "blue",  "Chutes"), unsafe_allow_html=True)
                        st.markdown(_html_bar(snap.get("h_sot",0),   15, "green", "No alvo"), unsafe_allow_html=True)
                        st.markdown(_html_bar(snap.get("h_corners",0),12, "blue",  "Escanteios"), unsafe_allow_html=True)
                        st.markdown(_html_bar(snap.get("h_dangerous",0),10,"orange","Ataques perig."), unsafe_allow_html=True)
                        h_upi = (snap.get("h_shots",0)*2 + snap.get("h_sot",0)*4 +
                                 snap.get("h_corners",0)*3 + snap.get("h_dangerous",0)*3)
                        st.markdown(_html_bar(h_upi, 120, "blue", "UPI Pressão"), unsafe_allow_html=True)
                    with mb:
                        st.markdown("**✈️ Visita**")
                        st.markdown(_html_bar(snap.get("a_shots",0), 25, "red",  "Chutes"), unsafe_allow_html=True)
                        st.markdown(_html_bar(snap.get("a_sot",0),   15, "red",  "No alvo"), unsafe_allow_html=True)
                        st.markdown(_html_bar(snap.get("a_corners",0),12, "red", "Escanteios"), unsafe_allow_html=True)
                        st.markdown(_html_bar(snap.get("a_dangerous",0),10,"orange","Ataques perig."), unsafe_allow_html=True)
                        a_upi = (snap.get("a_shots",0)*2 + snap.get("a_sot",0)*4 +
                                 snap.get("a_corners",0)*3 + snap.get("a_dangerous",0)*3)
                        st.markdown(_html_bar(a_upi, 120, "red", "UPI Pressão"), unsafe_allow_html=True)
                else:
                    st.info("Dados do snapshot não disponíveis.")

            st.caption(f"🔄 Último update: {ts}  ·  Histórico: {len(st.session_state.live_history)} ciclo(s)")

    if start_btn:
        with st.spinner("📡 Coletando dados ao vivo..."):
            _render_live()

    if auto_ref:
        with st.spinner("📡 Coletando dados ao vivo..."):
            _render_live()
        time.sleep(30)
        st.rerun()


# ══════════════════════════════════════════════════════════════════════
# PAGE: Sobre
# ══════════════════════════════════════════════════════════════════════
elif page == "ℹ️  Sobre":
    st.markdown("## ℹ️ Sobre o Sistema")
    st.markdown("""
    <div class="metric-card" style="background:#161b22;border:1px solid #30363d;border-radius:10px;padding:1.5rem">
        <h3 style="color:#58a6ff;margin-top:0">⚽ Copa do Mundo 2026 — Análise Profissional V3 PRO</h3>
        <p style="color:#8b949e">Sistema de análise e trading para apostas esportivas profissionais.</p>
        <hr style="border-color:#30363d">
        <h4 style="color:#e6edf3">🧮 Modelos Probabilísticos</h4>
        <ul style="color:#c9d1d9">
            <li><b>Monte Carlo</b> (30%) — simulação estocástica de 50.000 cenários</li>
            <li><b>Poisson</b> (25%) — modelagem de distribuição de gols</li>
            <li><b>Machine Learning</b> (20%) — regressão logística calibrada (Platt Scaling)</li>
            <li><b>API-Football</b> (15%) — predição nativa da plataforma</li>
            <li><b>ELO Contextual</b> (10%) — rating dinâmico com HFA e forma recente</li>
        </ul>
        <h4 style="color:#e6edf3">💰 Módulos Financeiros</h4>
        <ul style="color:#c9d1d9">
            <li><b>Value Betting Engine</b> — EV calculado por mercado, rankeado por oportunidade</li>
            <li><b>Kelly Criterion</b> — stake ótimo (Full / 50% / 25% Kelly)</li>
            <li><b>CLV (Closing Line Value)</b> — validação de edge ao longo do tempo</li>
        </ul>
        <h4 style="color:#e6edf3">📡 Módulos Live (16 profissionais)</h4>
        <ul style="color:#c9d1d9">
            <li><b>GII</b> — Goal Imminent Index (0-100)</li>
            <li><b>UPI</b> — Unified Pressure Index com sparklines</li>
            <li><b>Momentum Engine</b> — trend em múltiplas janelas (1/3/5/10 ciclos)</li>
            <li><b>xG Momentum</b> — aceleração de xG em tempo real</li>
            <li><b>Anti-False Over</b> — detector de pressão estéril</li>
            <li><b>Smart Cashout</b> — recomendação de saída com contexto</li>
            <li><b>Win Probability Live</b> — Poisson residual por minuto</li>
            <li><b>Game State Engine</b> — estado tático de cada time</li>
            <li><b>Trader Assistant IA</b> — narrativa + recomendação com confiança</li>
        </ul>
        <hr style="border-color:#30363d">
        <div style="font-size:0.78rem;color:#484f58">
            Dados: API-Football V3 · Versão: 3 PRO · Build: 2026
        </div>
    </div>
    """, unsafe_allow_html=True)
