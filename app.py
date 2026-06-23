# -*- coding: utf-8 -*-
"""
Streamlit Web App — Análise de Futebol V3 PRO
Copa do Mundo 2026
"""

import streamlit as st
import sys
import io
import contextlib
import datetime
import threading
import time
import os
import requests

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚽ Análise Copa 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .stApp { background-color: #0e1117; }
  .block-container { padding-top: 1rem; }
  pre { background: #161b22 !important; color: #e6edf3 !important;
        border-radius: 8px; padding: 1rem; font-size: 0.78rem;
        line-height: 1.45; overflow-x: auto; white-space: pre; font-family: 'Courier New', monospace; }
  .metric-card { background: #161b22; border-radius: 8px; padding: 1rem;
                 border: 1px solid #30363d; margin-bottom: 0.5rem; }
  .team-badge { font-size: 1.4rem; font-weight: 700; }
  .score-big  { font-size: 2.5rem; font-weight: 900; color: #58a6ff; text-align: center; }
  div[data-testid="stMetric"] { background: #161b22; border-radius: 8px;
                                padding: 0.75rem; border: 1px solid #30363d; }
  .stButton > button { border-radius: 6px; font-weight: 600; }
  .stSelectbox > div > div { background: #161b22; }
</style>
""", unsafe_allow_html=True)

# ── Load analysis module ──────────────────────────────────────────────
@st.cache_resource(show_spinner="Carregando módulos de análise...")
def _load_module():
    import importlib.util, os
    path = os.path.join(os.path.dirname(__file__), "programa_analise_v3.py")
    spec = importlib.util.spec_from_file_location("analise_v3", path)
    mod  = importlib.util.module_from_spec(spec)
    # Suppress stdout during import
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod

try:
    analise = _load_module()
    MODULE_OK = True
except Exception as e:
    MODULE_OK = False
    MODULE_ERR = str(e)

# ── API helpers ───────────────────────────────────────────────────────
API_KEY  = os.environ.get("API_KEY", "906f4989978807460c85bcc0c9e87367")
BASE_URL = "https://v3.football.api-sports.io"
HEADERS  = {"x-apisports-key": API_KEY}
WC_LEAGUE = 1
WC_SEASON = 2026


@st.cache_data(ttl=120, show_spinner=False)
def fetch_matches(date_str: str):
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS,
                         params={"league": WC_LEAGUE, "season": WC_SEASON,
                                 "date": date_str, "timezone": "America/Sao_Paulo"},
                         timeout=15)
        r.raise_for_status()
        return r.json().get("response", [])
    except Exception as e:
        return []


def run_analysis_captured(fn, *args, **kwargs):
    """Run a function and capture all its print output."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            fn(*args, **kwargs)
    except SystemExit:
        pass
    except Exception as e:
        buf.write(f"\n❌ Erro durante análise: {e}\n")
        import traceback
        buf.write(traceback.format_exc())
    return buf.getvalue()


# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/b/b8/2026_FIFA_World_Cup_emblem.svg/220px-2026_FIFA_World_Cup_emblem.svg.png",
             width=120)
    st.title("⚽ Copa 2026")
    st.caption("Sistema de Análise Profissional V3 PRO")
    st.divider()

    mode = st.radio("Modo", ["📅 Calendário & Análise", "📡 Trading Ao Vivo"], index=0)
    st.divider()

    sel_date = st.date_input("📅 Data", value=datetime.date.today(),
                              min_value=datetime.date(2026, 6, 1),
                              max_value=datetime.date(2026, 7, 20))
    st.divider()
    st.caption("API-Football V3 · Poisson · ELO · ML · xG")

# ── Main content ──────────────────────────────────────────────────────
if not MODULE_OK:
    st.error(f"❌ Erro ao carregar módulo de análise: {MODULE_ERR}")
    st.stop()

date_str = sel_date.strftime("%Y-%m-%d")

# ──────────────────────────────────────────────────────────────────────
# MODE: Calendário & Análise Pré-Jogo
# ──────────────────────────────────────────────────────────────────────
if mode == "📅 Calendário & Análise":
    st.header(f"📅 Jogos da Copa do Mundo — {date_str}")

    with st.spinner("Buscando partidas..."):
        matches = fetch_matches(date_str)

    if not matches:
        st.warning(f"Nenhuma partida encontrada para **{date_str}**. Tente outra data.")
        st.info("💡 A Copa do Mundo 2026 começa em 11 de junho de 2026.")
        st.stop()

    # ── Match cards ────────────────────────────────────────────────────
    st.subheader(f"⚽ {len(matches)} partida(s) encontrada(s)")

    match_options = {}
    cols = st.columns(min(len(matches), 3))
    for i, m in enumerate(matches):
        fid   = m["fixture"]["id"]
        h_t   = m["teams"]["home"]
        a_t   = m["teams"]["away"]
        dt_raw = m["fixture"]["date"]
        try:
            t_str = dt_raw.split("T")[1][:5]
        except Exception:
            t_str = "--:--"
        status = m["fixture"]["status"]["short"]

        label = f"{h_t['name']} x {a_t['name']} ({t_str})"
        match_options[label] = {
            "fixture_id": fid, "home_id": h_t["id"], "home_name": h_t["name"],
            "away_id": a_t["id"], "away_name": a_t["name"],
            "time": t_str, "raw_data": m, "status": status,
        }

        with cols[i % 3]:
            score_h = m.get("goals", {}).get("home")
            score_a = m.get("goals", {}).get("away")
            score_txt = f"{score_h} – {score_a}" if score_h is not None else "– vs –"
            st.markdown(f"""
            <div class="metric-card">
                <div style="color:#8b949e; font-size:0.75rem;">{t_str} Brasília · #{fid}</div>
                <div class="team-badge">🏠 {h_t['name']}</div>
                <div class="score-big">{score_txt}</div>
                <div class="team-badge">✈️ {a_t['name']}</div>
                <div style="margin-top:0.5rem; color:#58a6ff; font-size:0.8rem;">Status: {status}</div>
            </div>""", unsafe_allow_html=True)

    st.divider()

    # ── Match selector ────────────────────────────────────────────────
    selected_label = st.selectbox("Selecione a partida para análise:", list(match_options.keys()))
    selected = match_options[selected_label]

    c1, c2 = st.columns(2)
    run_pregame = c1.button("🚀 ANÁLISE PRÉ-JOGO V3 PRO", use_container_width=True, type="primary")
    run_value   = c2.button("🎯 MELHORES VALUE BETS",     use_container_width=True)

    if run_pregame or run_value:
        if not MODULE_OK:
            st.error("Módulo não carregado.")
            st.stop()

        # Set global state
        analise.selected_match = selected

        if run_pregame:
            st.info(f"⏳ Analisando **{selected['home_name']} x {selected['away_name']}** — isso leva ~30s...")
            with st.spinner("Coletando dados de múltiplas APIs..."):
                output = run_analysis_captured(analise.execute_advanced_pre_live_analysis_v3)

            st.success("✅ Análise concluída!")
            st.subheader("📊 Relatório Completo")
            st.code(output, language=None)

        elif run_value:
            st.info("⏳ Buscando value bets...")
            def _value_fn():
                # Run analysis and focus on EV report
                analise.execute_advanced_pre_live_analysis_v3()
            with st.spinner("Calculando EV e Kelly..."):
                output = run_analysis_captured(_value_fn)

            # Try to extract just the EV section
            lines = output.split("\n")
            ev_start = next((i for i, l in enumerate(lines) if "VALUE BETTING" in l or "EV+" in l), None)
            ev_end   = next((i for i, l in enumerate(lines[ev_start or 0:], ev_start or 0)
                             if i > (ev_start or 0) and "╚" in l), len(lines))

            if ev_start:
                st.code("\n".join(lines[ev_start:ev_end+1]), language=None)
            else:
                st.code(output, language=None)

# ──────────────────────────────────────────────────────────────────────
# MODE: Trading Ao Vivo
# ──────────────────────────────────────────────────────────────────────
else:
    st.header("📡 Dashboard de Trading Ao Vivo")

    with st.spinner("Buscando partidas ao vivo..."):
        live_r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS,
                               params={"league": WC_LEAGUE, "season": WC_SEASON,
                                       "live": "all"}, timeout=15)
        live_matches = live_r.json().get("response", []) if live_r.ok else []

    if not live_matches:
        st.warning("⚪ Nenhuma partida ao vivo no momento.")
        st.info("O dashboard ao vivo atualiza automaticamente quando há jogos em andamento.")

        # Offer scheduled matches as fallback
        st.subheader("Partidas agendadas para hoje:")
        with st.spinner("Buscando partidas do dia..."):
            todays = fetch_matches(date_str)
        if todays:
            for m in todays:
                h = m["teams"]["home"]["name"]
                a = m["teams"]["away"]["name"]
                t = m["fixture"]["date"].split("T")[1][:5] if "T" in m["fixture"]["date"] else "--"
                st.write(f"⚽ {h} x {a} — {t} Brasília")
        st.stop()

    live_options = {}
    for m in live_matches:
        h_t = m["teams"]["home"]; a_t = m["teams"]["away"]
        gh  = m.get("goals", {}).get("home", 0) or 0
        ga  = m.get("goals", {}).get("away", 0) or 0
        mn  = m["fixture"]["status"].get("elapsed", "?")
        label = f"{h_t['name']} {gh}–{ga} {a_t['name']} ({mn}')"
        live_options[label] = {
            "fixture_id": m["fixture"]["id"],
            "home_id": h_t["id"], "home_name": h_t["name"],
            "away_id": a_t["id"], "away_name": a_t["name"],
            "raw_data": m,
        }

    sel_live = st.selectbox("Partida ao vivo:", list(live_options.keys()))
    live_sel = live_options[sel_live]

    col1, col2 = st.columns([2, 1])
    with col1:
        auto_refresh = st.toggle("🔄 Auto-atualizar (30s)", value=False)
    with col2:
        manual_btn = st.button("▶️ Iniciar Dashboard", type="primary", use_container_width=True)

    dashboard_placeholder = st.empty()

    def _run_live():
        analise.selected_match = live_sel
        output = run_analysis_captured(
            analise.live_trading_dashboard,
            live_sel["fixture_id"],
            live_sel["home_name"],
            live_sel["away_name"],
            live_sel["home_id"],
        )
        return output

    if manual_btn or auto_refresh:
        with dashboard_placeholder.container():
            with st.spinner(f"📡 Coletando dados ao vivo..."):
                out = _run_live()
            st.success(f"✅ Atualizado às {datetime.datetime.now().strftime('%H:%M:%S')}")
            st.code(out, language=None)

        if auto_refresh:
            time.sleep(30)
            st.rerun()
