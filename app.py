# -*- coding: utf-8 -*-
"""
Sports Intelligence PRO — Streamlit Web App
Copa do Mundo 2026
"""

import streamlit as st
import sys, io, contextlib, datetime, os, re, time, builtins, requests, importlib.util
import plotly.graph_objects as go
import plotly.express as px

# ── Page config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sports Intelligence PRO",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS premium ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Remove Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Main background */
.stApp { background: #0B0F14; }
.block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1400px !important; }

/* Grid background */
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.013) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.013) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none; z-index: 0;
}

/* Cards */
.card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    position: relative;
    overflow: hidden;
}
.card-blue   { border-left: 3px solid #2196F3; }
.card-green  { border-left: 3px solid #00C853; }
.card-red    { border-left: 3px solid #FF5252; }
.card-yellow { border-left: 3px solid #FFC107; }
.card-purple { border-left: 3px solid #8B5CF6; }
.card-glow-green { box-shadow: 0 0 24px rgba(0,200,83,0.10); }
.card-glow-blue  { box-shadow: 0 0 24px rgba(33,150,243,0.10); }

/* Hero match card */
.hero {
    background: linear-gradient(135deg, #111827 0%, #1a2235 100%);
    border: 1px solid #1F2937;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.hero-score {
    font-size: 3.5rem;
    font-weight: 900;
    color: #2196F3;
    line-height: 1;
    margin: 0.5rem 0;
}
.hero-team { font-size: 1.5rem; font-weight: 800; color: #FFFFFF; }
.hero-meta { font-size: 0.8rem; color: #6B7280; margin-top: 0.75rem; }

/* KPI cards */
.kpi-card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
}
.kpi-value { font-size: 2.4rem; font-weight: 900; line-height: 1; margin: 0.4rem 0; }
.kpi-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #6B7280; }
.kpi-delta-pos { font-size: 0.75rem; color: #00C853; font-weight: 600; margin-top: 0.3rem; }
.kpi-delta-neg { font-size: 0.75rem; color: #FF5252; font-weight: 600; margin-top: 0.3rem; }

/* Section title */
.sec-title {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6B7280;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sec-title::after { content: ''; flex: 1; height: 1px; background: #1F2937; }

/* Probability blocks */
.prob-row { display: flex; gap: 0.75rem; margin-bottom: 1rem; }
.prob-block {
    flex: 1;
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    border: 1px solid transparent;
}
.prob-home   { background: #0d1a2e; border-color: #2196F344; }
.prob-draw   { background: #150d2e; border-color: #8B5CF644; }
.prob-away   { background: #2e0d0d; border-color: #FF525244; }
.prob-pct    { font-size: 2.5rem; font-weight: 900; line-height: 1; margin: 0.3rem 0; }
.prob-label  { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.06em; color: #6B7280; }
.prob-fair   { font-size: 0.8rem; color: #4B5563; margin-top: 0.4rem; }
.prob-ev-pos { font-size: 0.8rem; color: #00C853; font-weight: 700; margin-top: 0.3rem; }
.prob-ev-neg { font-size: 0.8rem; color: #FF5252; font-weight: 700; margin-top: 0.3rem; }

/* Bet rows */
.bet-table { width: 100%; }
.bet-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.85rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.4rem;
    border: 1px solid #1F2937;
    transition: border-color 0.2s;
}
.bet-row:hover { border-color: #374151; }
.bet-row-pos { background: #0d1f0d; }
.bet-row-neg { background: #111827; opacity: 0.55; }
.bet-name  { flex: 1; font-size: 0.9rem; font-weight: 600; color: #FFFFFF; }
.bet-prob  { font-size: 0.82rem; color: #9CA3AF; width: 42px; text-align: right; }
.bet-odd   { font-size: 0.95rem; font-weight: 700; color: #FFC107; width: 40px; text-align: right; }
.bet-ev-p  { font-size: 0.88rem; font-weight: 700; color: #00C853; width: 54px; text-align: right; }
.bet-ev-n  { font-size: 0.88rem; font-weight: 700; color: #FF5252; width: 54px; text-align: right; }
.bet-stake { font-size: 0.82rem; color: #2196F3; font-weight: 600; width: 50px; text-align: right; }

/* Alert cards */
.alert-card {
    border-radius: 8px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.5rem;
    border-left: 3px solid transparent;
    background: #111827;
    border: 1px solid #1F2937;
}
.alert-green  { border-left-color: #00C853 !important; }
.alert-red    { border-left-color: #FF5252 !important; }
.alert-yellow { border-left-color: #FFC107 !important; }
.alert-blue   { border-left-color: #2196F3 !important; }

/* Signal cards */
.signal-enter  { background: #0d1f0d; border: 1px solid #00C85333; border-radius: 8px; padding: 0.75rem; margin-bottom: 0.4rem; }
.signal-wait   { background: #1f1a0d; border: 1px solid #FFC10733; border-radius: 8px; padding: 0.75rem; margin-bottom: 0.4rem; }
.signal-avoid  { background: #1f0d0d; border: 1px solid #FF525233; border-radius: 8px; padding: 0.75rem; margin-bottom: 0.4rem; }

/* Gauge circle */
.gauge-wrap { text-align: center; }
.gauge-val  { font-size: 1.6rem; font-weight: 900; }
.gauge-lbl  { font-size: 0.68rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.06em; }

/* Live status */
.live-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #0d1f0d; border: 1px solid #00C85344;
    color: #00C853; font-size: 0.72rem; font-weight: 700;
    padding: 3px 10px; border-radius: 20px;
}
.live-dot { width: 6px; height: 6px; border-radius: 50%; background: #00C853; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* Badges */
.badge {
    display: inline-block; font-size: 0.68rem; font-weight: 600;
    padding: 2px 8px; border-radius: 20px; border: 1px solid;
}
.badge-blue   { background: #0d1a2e; color: #2196F3; border-color: #2196F333; }
.badge-green  { background: #0d1f0d; color: #00C853; border-color: #00C85333; }
.badge-red    { background: #1f0d0d; color: #FF5252; border-color: #FF525233; }
.badge-yellow { background: #1f1a0d; color: #FFC107; border-color: #FFC10733; }

/* Confidence bar */
.conf-track { background: #1F2937; border-radius: 4px; height: 6px; overflow: hidden; margin: 4px 0; }
.conf-fill  { height: 6px; border-radius: 4px; transition: width 0.4s; }

/* Table */
.data-table { width: 100%; border-collapse: collapse; font-size: 0.83rem; }
.data-table th { color: #4B5563; font-size: 0.68rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; padding: 8px 12px; border-bottom: 1px solid #1F2937; text-align: left; }
.data-table td { padding: 10px 12px; border-bottom: 1px solid #111827; color: #D1D5DB; }
.data-table tr:hover td { background: #1F2937; }
.data-table .num { text-align: right; font-weight: 600; color: #FFFFFF; }
.data-table .ev-pos { color: #00C853; font-weight: 700; }
.data-table .ev-neg { color: #FF5252; }
.data-table .odd    { color: #FFC107; font-weight: 700; font-family: monospace; }
.data-table .stake  { color: #2196F3; font-weight: 600; }

/* Bar chart row */
.bar-row { display: flex; align-items: center; gap: 8px; margin: 6px 0; }
.bar-label { font-size: 0.75rem; color: #9CA3AF; flex-shrink: 0; }
.bar-val   { font-size: 0.8rem; font-weight: 700; color: #FFFFFF; width: 32px; text-align: right; flex-shrink: 0; }
.bar-track { flex: 1; background: #1F2937; border-radius: 3px; height: 6px; overflow: hidden; }
.bar-inner { height: 6px; border-radius: 3px; }

/* Override Streamlit defaults */
div[data-testid="stMetric"] { background: #111827 !important; border: 1px solid #1F2937 !important; border-radius: 10px !important; padding: 1rem !important; }
div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 800 !important; }
.stButton > button { border-radius: 8px !important; font-weight: 600 !important; transition: all 0.2s !important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg,#1565C0,#2196F3) !important; border: none !important; }
.stSelectbox > div > div { background: #111827 !important; border-color: #1F2937 !important; }
.stTabs [data-baseweb="tab-list"] { background: #111827 !important; border-radius: 10px !important; padding: 4px !important; gap: 4px !important; border: 1px solid #1F2937 !important; }
.stTabs [data-baseweb="tab"] { border-radius: 7px !important; font-weight: 500 !important; font-size: 0.85rem !important; }
.stTabs [aria-selected="true"] { background: #2196F3 !important; color: #FFFFFF !important; }
div[data-testid="stProgress"] > div > div { background: #2196F3 !important; }
div[data-testid="column"] { padding: 0 0.4rem !important; }
.stSpinner > div { border-color: #2196F3 !important; }
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
    ori  = builtins.input
    builtins.input = lambda *a, **k: ""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            spec.loader.exec_module(mod)
    finally:
        builtins.input = ori
    mod._clear = lambda: None
    mod.CLEAR_SCREEN = False
    return mod

def get_module():
    try: return _load_module(), None
    except Exception:
        import traceback; return None, traceback.format_exc()

# ── API helpers ────────────────────────────────────────────────────────
@st.cache_data(ttl=90, show_spinner=False)
def fetch_matches(date_str):
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS,
            params={"league":WC_LEAGUE,"season":WC_SEASON,
                    "date":date_str,"timezone":"America/Sao_Paulo"}, timeout=15)
        r.raise_for_status(); return r.json().get("response",[])
    except: return []

@st.cache_data(ttl=20, show_spinner=False)
def fetch_live():
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS,
            params={"league":WC_LEAGUE,"season":WC_SEASON,"live":"all"}, timeout=15)
        r.raise_for_status(); return r.json().get("response",[])
    except: return []

def run_captured(fn, *args, **kwargs):
    buf = io.StringIO()
    ori = builtins.input; builtins.input = lambda *a,**k: ""; err=None
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            fn(*args, **kwargs)
    except SystemExit: pass
    except Exception:
        import traceback; err=traceback.format_exc()
    finally: builtins.input = ori
    return buf.getvalue(), err

def run_live_snap(mod, fid, h_name, a_name, home_id, history=None):
    if history is None: history=[]
    buf=io.StringIO(); ori=builtins.input; builtins.input=lambda *a,**k:""
    snap_out=[None]; trader_out=[None]
    try:
        with contextlib.redirect_stdout(buf):
            snap=mod._snapshot(fid,home_id)
            if snap is None:
                return "⚠️ Aguardando dados da API...", None, history, None
            snap_out[0]=snap
            gs=mod._signal_goal(snap,history,h_name,a_name)
            cs=mod._signal_corner(snap,history,h_name,a_name)
            ks=mod._signal_card(snap,history,h_name,a_name,snap["minute"])
            co=mod._game_consciousness(snap,history,h_name,a_name)
            try: lf=mod.calculate_live_fair_odds(snap,history,snap.get("minute",1),snap.get("score_h",0),snap.get("score_a",0),h_name,a_name)
            except: lf=None
            try: fp_h=mod.detect_false_pressure(snap,"h_",snap.get("minute",1)); fp_a=mod.detect_false_pressure(snap,"a_",snap.get("minute",1))
            except: fp_h=fp_a=None
            try: rg=mod.detect_game_regime(snap,history,h_name,a_name)
            except: rg=None
            try: evts=mod._fetch_live_events(fid)
            except: evts=None
            try:
                mom=mod._live_momentum_engine(snap,history)
                ph=mod._pressure_windows(snap,history,"h_"); pa=mod._pressure_windows(snap,history,"a_")
                gii=mod._goal_imminent_index(snap,history,mom["h_score"],mom["a_score"],ph,pa)
                aoh=mod._anti_false_over(snap,"h_"); aoa=mod._anti_false_over(snap,"a_")
                cash=mod._smart_cashout(snap,history,gii["h_gii"],gii["a_gii"],mom)
                coh=mod._corner_imminent_prob(snap,history,"h_"); coa=mod._corner_imminent_prob(snap,history,"a_")
                tact=mod._tactical_change_detector(snap,history)
                fat=mod._fatigue_live(snap,snap["minute"])
                xgm=mod._xg_momentum_live(snap,history)
                red=mod._red_card_impact(snap,history)
                gs2=mod._game_state_engine(snap,h_name,a_name)
                wp=mod._win_prob_live(snap,history,h_name,a_name)
                ta=mod._trader_assistant(snap,h_name,a_name,mom,gii,ph,pa,xgm,gs2,snap["minute"])
                alrt=mod._professional_alerts(gii,mom,ph,pa,aoh,aoa,red,tact,cash,snap)
                trader_out[0]=ta
            except: mom=ph=pa=gii=aoh=aoa=cash=coh=coa=tact=fat=None; xgm=red=gs2=wp=ta=alrt=None
            mod._render_dashboard(snap,history,h_name,a_name,home_id,gs,cs,ks,1,30,co,
                live_fair=lf,regime=rg,false_pressure_h=fp_h,false_pressure_a=fp_a,live_events=evts,
                v5_momentum=mom,v5_press_h=ph,v5_press_a=pa,v5_gii=gii,v5_anti_h=aoh,v5_anti_a=aoa,
                v5_cashout=cash,v5_corn_h=coh,v5_corn_a=coa,v5_tactical=tact,v5_fatigue=fat,v5_xgm=xgm,
                v5_red=red,v5_game_state=gs2,v5_win_prob=wp,v5_trader=ta,v5_alerts=alrt)
            history.append(snap)
            if len(history)>8: history.pop(0)
            return buf.getvalue(), snap_out[0], history, trader_out[0]
    except Exception:
        import traceback; return traceback.format_exc(), None, history, None
    finally: builtins.input=ori

# ── Report parser ──────────────────────────────────────────────────────
def _cl(line): return re.sub(r'[║╔╠╚╝╗╣─═]','',line).strip()

def parse_report(text):
    d={}; lines=[_cl(l) for l in text.split("\n") if _cl(l)]
    m=re.search(r"ENSEMBLE FINAL.*?Casa:\s*([\d.]+)%.*?Empate:\s*([\d.]+)%.*?Fora:\s*([\d.]+)%",text)
    if m: d["ph"],d["pd"],d["pa"]=float(m.group(1)),float(m.group(2)),float(m.group(3))
    models=[]
    for line in lines:
        for nm in ["Monte Carlo","Poisson","Machine Learning","API-Football","ELO"]:
            if nm in line:
                pcts=re.findall(r"([\d.]+)%",line)
                if len(pcts)>=3: models.append({"name":nm,"home":float(pcts[-3]),"draw":float(pcts[-2]),"away":float(pcts[-1])})
                break
    d["models"]=models
    bets=[]
    in_ev=False
    for line in lines:
        if "VALUE BETTING" in line.upper(): in_ev=True; continue
        if in_ev:
            if "BANKROLL" in line.upper() or "RECOMENDAÇÃO" in line.upper(): break
            m2=re.match(r"(\d)\s+(.+?)\s+([\d.]+)%\s+([\d.]+)\s+([\d.]+)\s+([+\-][\d.]+)%\s+([\d.]+%|SKIP)",line)
            if m2: bets.append({"rank":m2.group(1),"name":m2.group(2).strip(),"prob":float(m2.group(3)),"odd":float(m2.group(4)),"ev":float(m2.group(6)),"kelly":m2.group(7)})
    d["bets"]=bets
    cm=re.search(r"Score:\s*(\d+)/100",text)
    d["conf"]=int(cm.group(1)) if cm else None
    recs=[]
    for line in lines:
        for sig in ["ENTRADA FORTE","ENTRADA","AGUARDAR","EVITAR"]:
            if sig in line.upper():
                em=re.search(r"([+\-][\d.]+)%",line); sm=re.search(r"R\$([\d,]+)",line)
                nm2=re.sub(r"(🟢|🟡|🟠|🔴)","",line); nm2=re.sub(r"(ENTRADA FORTE|ENTRADA|AGUARDAR|EVITAR|EV:.*|Kelly:.*|STAKE:.*)", "",nm2,flags=re.I).strip()
                recs.append({"signal":sig,"name":nm2[:45],"ev":em.group(1)+"%"if em else "","stake":"R$"+sm.group(1) if sm else "SKIP"})
                break
    d["recs"]=recs
    d["metrics"]=[]
    in_m=False
    for line in lines:
        if "MÉTRICAS OFENSIVAS" in line.upper(): in_m=True; continue
        if in_m:
            if any(k in line.upper() for k in ["PRESSURE","ESCANTEIO","ÁRBITRO","ENSEMBLE","PREDIÇÃO"]): break
            nums=re.findall(r"([\d.]+)%?",line)
            nm3=re.sub(r"[\d.%]+.*","",line).strip()
            if len(nums)>=2 and nm3 and len(nm3)>3:
                d["metrics"].append({"label":nm3,"h":float(nums[-2]),"a":float(nums[-1])})
    d["metrics"]=d["metrics"][:7]
    narr_lines=[]
    in_n=False
    for line in lines:
        if "NARRATIVA" in line.upper(): in_n=True; continue
        if in_n:
            if any(k in line.upper() for k in ["RECOMENDAÇÃO","RANKING","VALUE","BANKROLL"]): break
            if line: narr_lines.append(line)
    d["narrative"]=" ".join(narr_lines)
    return d

# ── HTML helpers ──────────────────────────────────────────────────────
def conf_color(v):
    if v>=75: return "#00C853"
    if v>=55: return "#FFC107"
    return "#FF5252"

def _badge(text,color="blue"):
    return f'<span class="badge badge-{color}">{text}</span>'

def _bar_row(label,v,max_v,color):
    pct=min(100,int(v/max(max_v,0.01)*100))
    return f'<div class="bar-row"><span class="bar-label" style="width:130px">{label}</span><div class="bar-track"><div class="bar-inner" style="width:{pct}%;background:{color}"></div></div><span class="bar-val">{v:.1f}</span></div>'

def _conf_bar(v,color):
    return f'<div class="conf-track"><div class="conf-fill" style="width:{v}%;background:{color}"></div></div>'

def _status_chip(s):
    live={"1H","2H","HT","ET","BT"}; done={"FT","AET","PEN"}
    if s in live: return f'<span class="badge badge-green">🔴 AO VIVO</span>'
    if s in done: return f'<span class="badge badge-red">✅ ENCERRADO</span>'
    return f'<span class="badge badge-blue">🕐 AGENDADO</span>'

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem;text-align:center">
        <div style="font-size:2rem;margin-bottom:6px">⚽</div>
        <div style="font-size:0.95rem;font-weight:800;letter-spacing:0.04em;color:#FFFFFF">Sports Intelligence</div>
        <div style="font-size:0.68rem;color:#4B5563;letter-spacing:0.12em;text-transform:uppercase;margin-top:2px">PRO · Copa 2026</div>
    </div>
    <hr style="border-color:#1F2937;margin:0.75rem 0"/>
    """, unsafe_allow_html=True)

    page = st.radio("", [
        "🏠  Dashboard",
        "⚽  Jogos",
        "🚀  Análise Pré-Jogo",
        "📡  Trading Ao Vivo",
        "🎯  Value Bets",
        "ℹ️   Sobre",
    ], label_visibility="collapsed")

    st.markdown('<hr style="border-color:#1F2937;margin:0.75rem 0"/>', unsafe_allow_html=True)

    sel_date = st.date_input("📅 Data",
        value=datetime.date.today(),
        min_value=datetime.date(2026,6,1),
        max_value=datetime.date(2026,7,20),
        label_visibility="visible")

    st.markdown("""
    <hr style="border-color:#1F2937;margin:0.75rem 0"/>
    <div style="font-size:0.68rem;color:#374151;line-height:2;padding-bottom:0.5rem">
        <div style="color:#6B7280;font-weight:600;margin-bottom:4px">Modelos ativos</div>
        Monte Carlo · Poisson<br/>
        ELO · xG · ML · API V3<br/>
        Kelly · GII · Momentum
    </div>
    """, unsafe_allow_html=True)

date_str = sel_date.strftime("%Y-%m-%d")
mod, mod_err = get_module()

# ══════════════════════════════════════════════════════════════════════
# PAGE: Dashboard
# ══════════════════════════════════════════════════════════════════════
if page == "🏠  Dashboard":
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem">
        <div>
            <h1 style="font-size:1.5rem;font-weight:900;margin:0">Dashboard</h1>
            <p style="font-size:0.82rem;color:#6B7280;margin:4px 0 0">{date_str} · Copa do Mundo 2026</p>
        </div>
        <div class="live-badge"><div class="live-dot"></div>Engine ativo</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Buscando partidas..."):
        matches = fetch_matches(date_str)

    live_c = sum(1 for m in matches if m["fixture"]["status"]["short"] in {"1H","2H","HT","ET"})
    ev_c   = len(matches)

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(f'<div class="kpi-card"><div class="kpi-label">Jogos Hoje</div><div class="kpi-value" style="color:#2196F3">{len(matches)}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi-card"><div class="kpi-label">Ao Vivo 🔴</div><div class="kpi-value" style="color:#00C853">{live_c}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi-card"><div class="kpi-label">API Status</div><div class="kpi-value" style="color:#FFC107">{"OK" if matches else "—"}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="kpi-card"><div class="kpi-label">Modelos</div><div class="kpi-value" style="color:#8B5CF6">5</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="margin:1.5rem 0 0.5rem"><div class="sec-title">⚽ Partidas do Dia</div></div>', unsafe_allow_html=True)

    if not matches:
        st.markdown('<div class="card card-blue"><p style="color:#6B7280;margin:0">Nenhuma partida encontrada para esta data.</p></div>', unsafe_allow_html=True)
    else:
        rows=""
        for m in matches:
            h_t=m["teams"]["home"]; a_t=m["teams"]["away"]
            st_=m["fixture"]["status"]["short"]
            dt_=m["fixture"]["date"]; t_=dt_.split("T")[1][:5] if "T" in dt_ else "--"
            gh=m.get("goals",{}).get("home"); ga=m.get("goals",{}).get("away")
            score=f"{gh}–{ga}" if gh is not None else "–"
            rows+=f"""<tr>
                <td style="color:#6B7280;font-family:monospace;font-size:0.8rem">{t_}</td>
                <td style="font-weight:600;color:#FFFFFF">{h_t['name']} <span style="color:#374151">×</span> {a_t['name']}</td>
                <td>{_badge("Copa 2026","blue")}</td>
                <td style="font-family:monospace;font-size:0.85rem;color:#2196F3">{score}</td>
                <td>{_status_chip(st_)}</td>
            </tr>"""
        st.markdown(f"""
        <div class="card">
        <table class="data-table"><thead><tr>
            <th>Hora</th><th>Partida</th><th>Liga</th><th>Placar</th><th>Status</th>
        </tr></thead><tbody>{rows}</tbody></table>
        </div>""", unsafe_allow_html=True)

    if st.button("🔄 Atualizar", key="dash_ref"):
        st.cache_data.clear(); st.rerun()


# ══════════════════════════════════════════════════════════════════════
# PAGE: Jogos
# ══════════════════════════════════════════════════════════════════════
elif page == "⚽  Jogos":
    st.markdown('<h1 style="font-size:1.5rem;font-weight:900;margin-bottom:1.5rem">⚽ Jogos</h1>', unsafe_allow_html=True)

    with st.spinner("Buscando partidas..."):
        matches = fetch_matches(date_str)

    if not matches:
        st.info("Nenhuma partida encontrada.")
    else:
        cols = st.columns(min(len(matches), 3))
        for i, m in enumerate(matches):
            h_t=m["teams"]["home"]; a_t=m["teams"]["away"]
            st_=m["fixture"]["status"]["short"]
            dt_=m["fixture"]["date"]; t_=dt_.split("T")[1][:5] if "T" in dt_ else "--"
            gh=m.get("goals",{}).get("home"); ga=m.get("goals",{}).get("away")
            score=f"{gh} — {ga}" if gh is not None else "⚫ ⚫"
            fid=m["fixture"]["id"]
            with cols[i % 3]:
                st.markdown(f"""
                <div class="card" style="text-align:center;cursor:pointer">
                    <div style="font-size:0.7rem;color:#4B5563;margin-bottom:8px">⏰ {t_} BRT &nbsp;·&nbsp; #{fid}</div>
                    <div style="font-size:1.05rem;font-weight:700">🏠 {h_t['name']}</div>
                    <div style="font-size:2rem;font-weight:900;color:#2196F3;margin:6px 0">{score}</div>
                    <div style="font-size:1.05rem;font-weight:700">✈️ {a_t['name']}</div>
                    <div style="margin-top:10px">{_status_chip(st_)}</div>
                </div>""", unsafe_allow_html=True)

    if st.button("🔄 Atualizar", key="jogos_ref"):
        st.cache_data.clear(); st.rerun()


# ══════════════════════════════════════════════════════════════════════
# PAGE: Análise Pré-Jogo
# ══════════════════════════════════════════════════════════════════════
elif page == "🚀  Análise Pré-Jogo":
    st.markdown('<h1 style="font-size:1.5rem;font-weight:900;margin-bottom:0.25rem">🚀 Análise Pré-Jogo V3 PRO</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6B7280;font-size:0.82rem;margin-bottom:1.5rem">Ensemble · ELO · xG · Monte Carlo · Kelly Criterion · Value Bets</p>', unsafe_allow_html=True)

    if mod_err:
        st.error(f"Erro no módulo:\n```\n{mod_err[:400]}\n```"); st.stop()

    with st.spinner("Buscando partidas..."):
        matches = fetch_matches(date_str)

    if not matches:
        st.warning(f"Nenhuma partida em {date_str}."); st.stop()

    opts={}
    for m in matches:
        h_t=m["teams"]["home"]; a_t=m["teams"]["away"]
        t_=m["fixture"]["date"].split("T")[1][:5] if "T" in m["fixture"]["date"] else "--"
        opts[f"{h_t['name']}  ×  {a_t['name']}  ({t_})"]={
            "fixture_id":m["fixture"]["id"],"home_id":h_t["id"],"home_name":h_t["name"],
            "away_id":a_t["id"],"away_name":a_t["name"],"time":t_,"raw_data":m}

    sel_lbl = st.selectbox("Selecione a partida:", list(opts.keys()), key="pg_sel")
    sel = opts[sel_lbl]

    if st.button("🚀 Rodar Análise Completa", type="primary", use_container_width=True, key="run_pg"):
        mod.selected_match = sel
        prog = st.progress(0)
        steps=[(10,"📡 Conectando à API..."),(25,"📊 Histórico dos times..."),(45,"🧮 Lambdas e xG..."),(65,"🎲 Monte Carlo + Poisson + ML..."),(82,"⚡ EV e Kelly..."),(95,"📝 Gerando relatório...")]
        ph=st.empty()
        for pct,msg in steps:
            prog.progress(pct,text=msg); ph.caption(msg); time.sleep(0.22)
        output, err = run_captured(mod.execute_advanced_pre_live_analysis_v3)
        prog.progress(100,text="✅ Concluído!"); ph.empty(); time.sleep(0.3); prog.empty()

        if err:
            with st.expander("⚠️ Erros (não críticos)",expanded=False): st.code(err[:1000])

        if not output:
            st.warning("Sem dados disponíveis para esta partida."); st.stop()

        d = parse_report(output)
        h_name=sel["home_name"]; a_name=sel["away_name"]

        # ── Hero ────────────────────────────────────────────────────
        st.markdown(f"""
        <div class="hero">
            <div style="font-size:0.7rem;color:#4B5563;margin-bottom:12px">
                {_badge("Copa do Mundo 2026","blue")} &nbsp; {_badge("V3 PRO","purple")}
            </div>
            <div style="display:flex;align-items:center;justify-content:center;gap:3rem">
                <div>
                    <div class="hero-team">🏠 {h_name}</div>
                    <div style="font-size:0.75rem;color:#4B5563;margin-top:4px">Mandante</div>
                </div>
                <div style="font-size:1.5rem;font-weight:900;color:#374151">×</div>
                <div>
                    <div class="hero-team">{a_name} ✈️</div>
                    <div style="font-size:0.75rem;color:#4B5563;margin-top:4px">Visitante</div>
                </div>
            </div>
            <div class="hero-meta">⏰ {sel.get('time','--')} BRT &nbsp;·&nbsp; Fixture #{sel['fixture_id']} &nbsp;·&nbsp; Análise gerada às {datetime.datetime.now().strftime('%H:%M')}</div>
        </div>
        """, unsafe_allow_html=True)

        tabs = st.tabs(["🎯 Veredicto","📊 Probabilidades","💰 Value Bets","📈 Estatísticas","📄 Relatório Completo"])

        # ── TAB: Veredicto ─────────────────────────────────────────
        with tabs[0]:
            # Confidence
            if d.get("conf"):
                conf=d["conf"]; cc=conf_color(conf)
                st.markdown(f"""
                <div class="card card-blue">
                    <div class="sec-title">🔬 Confiança Global</div>
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
                        <span style="font-size:0.9rem;font-weight:600">Score da Análise</span>
                        <span style="font-size:2rem;font-weight:900;color:{cc}">{conf}<span style="font-size:1rem;color:#374151">/100</span></span>
                    </div>
                    {_conf_bar(conf,cc)}
                </div>
                """, unsafe_allow_html=True)

            # Narrative
            if d.get("narrative"):
                st.markdown(f"""
                <div class="card card-purple">
                    <div class="sec-title">📝 Narrativa Analítica</div>
                    <p style="color:#D1D5DB;font-size:0.9rem;line-height:1.75;margin:0">{d['narrative']}</p>
                </div>""", unsafe_allow_html=True)

            # Recommendations
            if d.get("recs"):
                st.markdown('<div class="sec-title" style="margin-top:1rem">🏆 Recomendações Finais</div>', unsafe_allow_html=True)
                for r in d["recs"]:
                    sig=r["signal"]
                    if sig=="ENTRADA FORTE": cls,icon,ev_col="card card-green card-glow-green","🟢","#00C853"
                    elif sig=="ENTRADA":     cls,icon,ev_col="card card-yellow","🟡","#FFC107"
                    elif sig=="AGUARDAR":    cls,icon,ev_col="card","🟠","#FFC107"
                    else:                    cls,icon,ev_col="card","🔴","#FF5252"
                    ev_v=r.get("ev","")
                    st.markdown(f"""
                    <div class="{cls}" style="display:flex;align-items:center;gap:1rem">
                        <span style="font-size:1.5rem">{icon}</span>
                        <div style="flex:1">
                            <div style="font-size:0.65rem;text-transform:uppercase;letter-spacing:0.08em;color:#4B5563">{sig}</div>
                            <div style="font-size:0.95rem;font-weight:700;color:#FFFFFF;margin-top:2px">{r['name']}</div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-size:0.95rem;font-weight:800;color:{ev_col}">EV {ev_v}</div>
                            <div style="font-size:0.82rem;color:#2196F3;font-weight:600">{r['stake']}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)

        # ── TAB: Probabilidades ────────────────────────────────────
        with tabs[1]:
            if d.get("ph"):
                ph_,pd_,pa_=d["ph"],d["pd"],d["pa"]
                fh=round(100/ph_,2) if ph_ else "-"
                fd=round(100/pd_,2) if pd_ else "-"
                fa=round(100/pa_,2) if pa_ else "-"
                st.markdown(f"""
                <div class="sec-title">⚡ Ensemble Final (5 modelos calibrados)</div>
                <div class="prob-row">
                    <div class="prob-block prob-home">
                        <div class="prob-label">🏠 {h_name[:18]}</div>
                        <div class="prob-pct" style="color:#2196F3">{ph_:.1f}%</div>
                        <div class="prob-fair">Odd justa: {fh}</div>
                    </div>
                    <div class="prob-block prob-draw">
                        <div class="prob-label">🤝 Empate</div>
                        <div class="prob-pct" style="color:#8B5CF6">{pd_:.1f}%</div>
                        <div class="prob-fair">Odd justa: {fd}</div>
                    </div>
                    <div class="prob-block prob-away">
                        <div class="prob-label">✈️ {a_name[:18]}</div>
                        <div class="prob-pct" style="color:#FF5252">{pa_:.1f}%</div>
                        <div class="prob-fair">Odd justa: {fa}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if d.get("models"):
                st.markdown('<div class="sec-title">🧮 Detalhamento por Modelo</div>', unsafe_allow_html=True)
                w_map={"Monte Carlo":30,"Poisson":25,"Machine Learning":20,"API-Football":15,"ELO":10}
                fig = go.Figure()
                model_names=[m["name"] for m in d["models"]]
                fig.add_bar(name="Casa",   x=model_names, y=[m["home"] for m in d["models"]], marker_color="#2196F3", marker_line_width=0)
                fig.add_bar(name="Empate", x=model_names, y=[m["draw"] for m in d["models"]], marker_color="#8B5CF6", marker_line_width=0)
                fig.add_bar(name="Fora",   x=model_names, y=[m["away"] for m in d["models"]], marker_color="#FF5252", marker_line_width=0)
                fig.update_layout(
                    barmode="group", template="plotly_dark",
                    paper_bgcolor="#111827", plot_bgcolor="#111827",
                    margin=dict(l=0,r=0,t=20,b=0), height=240,
                    legend=dict(orientation="h",yanchor="bottom",y=1.02,bgcolor="rgba(0,0,0,0)"),
                    font=dict(family="Inter",size=11,color="#9CA3AF"),
                    yaxis=dict(gridcolor="#1F2937",ticksuffix="%"),
                    xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

        # ── TAB: Value Bets ────────────────────────────────────────
        with tabs[2]:
            if d.get("bets"):
                rank_icons={1:"🥇",2:"🥈",3:"🥉"}
                rows=""
                for b in d["bets"]:
                    r=int(b["rank"]); ico=rank_icons.get(r,f"#{r}")
                    ev_cls="ev-pos" if b["ev"]>0 else "ev-neg"
                    ev_s=f"+{b['ev']:.1f}%" if b["ev"]>0 else f"{b['ev']:.1f}%"
                    kelly_s=b["kelly"] if b["kelly"]!="SKIP" else '<span style="color:#374151">SKIP</span>'
                    row_bg="background:#0d1f0d" if b["ev"]>0 else "opacity:0.5"
                    rows+=f"""<tr style="{row_bg}">
                        <td style="font-size:1.1rem">{ico}</td>
                        <td style="font-weight:600;color:#FFFFFF">{b['name']}</td>
                        <td class="num">{b['prob']:.0f}%</td>
                        <td class="num odd">{b['odd']:.2f}</td>
                        <td class="num {ev_cls}">{ev_s}</td>
                        <td class="num stake">{kelly_s}</td>
                    </tr>"""
                st.markdown(f"""
                <div class="card">
                <table class="data-table"><thead><tr>
                    <th>#</th><th>Mercado</th><th class="num">Prob</th>
                    <th class="num">Odd</th><th class="num">EV</th><th class="num">Stake</th>
                </tr></thead><tbody>{rows}</tbody></table>
                </div>""", unsafe_allow_html=True)
            else:
                st.info("Nenhuma aposta com EV positivo encontrada.")

        # ── TAB: Estatísticas ──────────────────────────────────────
        with tabs[3]:
            if d.get("metrics"):
                c1,c2=st.columns(2)
                with c1:
                    st.markdown(f'<div style="font-size:0.85rem;font-weight:700;color:#2196F3;margin-bottom:12px">🏠 {h_name}</div>', unsafe_allow_html=True)
                    html=""
                    for m_ in d["metrics"]:
                        html+=_bar_row(m_["label"][:24],m_["h"],max(m_["h"],m_["a"],0.01),"#2196F3")
                    st.markdown(html, unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div style="font-size:0.85rem;font-weight:700;color:#FF5252;margin-bottom:12px">✈️ {a_name}</div>', unsafe_allow_html=True)
                    html=""
                    for m_ in d["metrics"]:
                        html+=_bar_row(m_["label"][:24],m_["a"],max(m_["h"],m_["a"],0.01),"#FF5252")
                    st.markdown(html, unsafe_allow_html=True)

                # Plotly radar
                cats=[m_["label"] for m_ in d["metrics"]]
                fig=go.Figure()
                fig.add_scatterpolar(r=[m_["h"] for m_ in d["metrics"]]+[d["metrics"][0]["h"]], theta=cats+[cats[0]],
                    fill="toself",name=h_name,line_color="#2196F3",fillcolor="rgba(33,150,243,0.12)")
                fig.add_scatterpolar(r=[m_["a"] for m_ in d["metrics"]]+[d["metrics"][0]["a"]], theta=cats+[cats[0]],
                    fill="toself",name=a_name,line_color="#FF5252",fillcolor="rgba(255,82,82,0.10)")
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True,gridcolor="#1F2937",linecolor="#1F2937",tickfont_size=9,tickfont_color="#6B7280"),
                               angularaxis=dict(gridcolor="#1F2937",linecolor="#1F2937",tickfont_color="#9CA3AF")),
                    paper_bgcolor="#111827",plot_bgcolor="#111827",
                    template="plotly_dark",height=300,margin=dict(l=20,r=20,t=20,b=20),
                    font=dict(family="Inter",size=11),
                    legend=dict(bgcolor="rgba(0,0,0,0)"),
                )
                st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

        # ── TAB: Relatório Completo ────────────────────────────────
        with tabs[4]:
            st.markdown(f"""
            <div style="background:#0B0F14;border:1px solid #1F2937;border-radius:10px;padding:1.2rem;
                        font-family:'JetBrains Mono','Courier New',monospace;font-size:0.72rem;
                        line-height:1.55;color:#6B7280;white-space:pre;overflow-x:auto;
                        max-height:600px;overflow-y:auto">
{output[:20000]}
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE: Trading Ao Vivo
# ══════════════════════════════════════════════════════════════════════
elif page == "📡  Trading Ao Vivo":
    st.markdown('<h1 style="font-size:1.5rem;font-weight:900;margin-bottom:0.25rem">📡 Trading Ao Vivo</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6B7280;font-size:0.82rem;margin-bottom:1.5rem">GII · Momentum · Win Probability · Trader Assistant · Auto-refresh</p>', unsafe_allow_html=True)

    if mod_err:
        st.error(f"Erro no módulo:\n```\n{mod_err[:400]}\n```"); st.stop()

    with st.spinner("Verificando partidas..."):
        live_ms=fetch_live()

    day_ms=fetch_matches(date_str)

    if live_ms:
        st.markdown(f'<div class="card card-green" style="margin-bottom:1rem"><div class="live-badge" style="display:inline-flex"><div class="live-dot"></div>{len(live_ms)} partida(s) ao vivo</div></div>', unsafe_allow_html=True)
        use=live_ms
    else:
        st.markdown('<div class="card card-yellow" style="margin-bottom:1rem">⚪ Nenhuma partida ao vivo — mostrando partidas do dia</div>', unsafe_allow_html=True)
        use=day_ms

    if not use:
        st.info("Nenhuma partida disponível."); st.stop()

    live_opts={}
    for m in use:
        h_t=m["teams"]["home"]; a_t=m["teams"]["away"]
        gh=m.get("goals",{}).get("home",0) or 0; ga=m.get("goals",{}).get("away",0) or 0
        mn=m["fixture"]["status"].get("elapsed") or "--"
        label=f"{h_t['name']}  {gh}–{ga}  {a_t['name']}  ({mn}')"
        live_opts[label]={"fixture_id":m["fixture"]["id"],"home_id":h_t["id"],
            "home_name":h_t["name"],"away_id":a_t["id"],"away_name":a_t["name"],
            "score_h":gh,"score_a":ga,"minute":mn}

    sel_live=st.selectbox("Partida:",list(live_opts.keys()),key="live_sel")
    lsel=live_opts[sel_live]

    c1,c2=st.columns([3,1])
    with c1: run_btn=st.button("▶️ Atualizar Dashboard",type="primary",use_container_width=True,key="live_run")
    with c2: auto=st.toggle("🔄 Auto (30s)",value=False,key="live_auto")

    if "live_hist" not in st.session_state: st.session_state.live_hist=[]
    if "live_fid"  not in st.session_state: st.session_state.live_fid=None
    if st.session_state.live_fid!=lsel["fixture_id"]:
        st.session_state.live_hist=[]; st.session_state.live_fid=lsel["fixture_id"]

    def _do_live():
        output,snap,new_hist,trader=run_live_snap(mod,lsel["fixture_id"],lsel["home_name"],lsel["away_name"],lsel["home_id"],st.session_state.live_hist)
        st.session_state.live_hist=new_hist

        # Score header
        st.markdown(f"""
        <div class="hero" style="margin-bottom:1rem">
            <div class="live-badge" style="display:inline-flex;margin-bottom:12px"><div class="live-dot"></div>AO VIVO — {lsel['minute']}'</div>
            <div style="display:flex;align-items:center;justify-content:center;gap:3rem;margin-top:8px">
                <div class="hero-team">🏠 {lsel['home_name']}</div>
                <div class="hero-score">{lsel['score_h']} — {lsel['score_a']}</div>
                <div class="hero-team">{lsel['away_name']} ✈️</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Trader AI card
        if trader:
            conf=trader.get("confidence",0)
            cc=conf_color(conf)
            rec=trader.get("recommendation","")
            narr=trader.get("narrative","")
            st.markdown(f"""
            <div class="card card-blue card-glow-blue" style="margin-bottom:1rem">
                <div class="sec-title">🤖 Trader Assistant</div>
                <p style="color:#D1D5DB;font-size:0.9rem;line-height:1.7;margin-bottom:12px">{narr}</p>
                <div style="display:flex;align-items:center;gap:1rem">
                    <div style="font-size:1rem;font-weight:800;color:#FFFFFF">{rec}</div>
                    <div style="font-size:0.88rem;font-weight:700;color:{cc}">Confiança: {conf}%</div>
                </div>
                {_conf_bar(conf,cc)}
            </div>""", unsafe_allow_html=True)

        tabs=st.tabs(["📊 Dashboard","📈 Gráficos","🚦 Sinais"])

        with tabs[0]:
            if snap:
                h_upi=snap.get("h_shots",0)*2+snap.get("h_sot",0)*4+snap.get("h_corners",0)*3
                a_upi=snap.get("a_shots",0)*2+snap.get("a_sot",0)*4+snap.get("a_corners",0)*3
                c1_,c2_=st.columns(2)
                with c1_:
                    st.markdown(f'<div style="font-size:0.85rem;font-weight:700;color:#2196F3;margin-bottom:10px">🏠 {lsel["home_name"]}</div>',unsafe_allow_html=True)
                    stats=[("UPI Pressão",h_upi,120),("Chutes",snap.get("h_shots",0),25),("No Alvo",snap.get("h_sot",0),15),("Escanteios",snap.get("h_corners",0),12),("At. Perigosos",snap.get("h_dangerous",0),12)]
                    for lbl,v,mx in stats: st.markdown(_bar_row(lbl,v,mx,"#2196F3"),unsafe_allow_html=True)
                with c2_:
                    st.markdown(f'<div style="font-size:0.85rem;font-weight:700;color:#FF5252;margin-bottom:10px">✈️ {lsel["away_name"]}</div>',unsafe_allow_html=True)
                    stats=[("UPI Pressão",a_upi,120),("Chutes",snap.get("a_shots",0),25),("No Alvo",snap.get("a_sot",0),15),("Escanteios",snap.get("a_corners",0),12),("At. Perigosos",snap.get("a_dangerous",0),12)]
                    for lbl,v,mx in stats: st.markdown(_bar_row(lbl,v,mx,"#FF5252"),unsafe_allow_html=True)

        with tabs[1]:
            if len(st.session_state.live_hist)>=2:
                hist=st.session_state.live_hist
                minutes=[s.get("minute",0) for s in hist]
                h_upi_h=[s.get("h_shots",0)*2+s.get("h_sot",0)*4+s.get("h_corners",0)*3 for s in hist]
                a_upi_h=[s.get("a_shots",0)*2+s.get("a_sot",0)*4+s.get("a_corners",0)*3 for s in hist]
                fig=go.Figure()
                fig.add_scatter(x=minutes,y=h_upi_h,name=lsel["home_name"],line=dict(color="#2196F3",width=2.5),fill="tozeroy",fillcolor="rgba(33,150,243,0.08)")
                fig.add_scatter(x=minutes,y=a_upi_h,name=lsel["away_name"],line=dict(color="#FF5252",width=2.5),fill="tozeroy",fillcolor="rgba(255,82,82,0.08)")
                fig.update_layout(template="plotly_dark",paper_bgcolor="#111827",plot_bgcolor="#111827",
                    height=220,margin=dict(l=0,r=0,t=20,b=0),
                    yaxis=dict(gridcolor="#1F2937"),xaxis=dict(title="Minuto",gridcolor="#1F2937"),
                    legend=dict(bgcolor="rgba(0,0,0,0)"),font=dict(family="Inter",size=11))
                st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
            else:
                st.info("Acumule 2+ ciclos para ver os gráficos.")

        with tabs[2]:
            st.markdown(f"""
            <div style="background:#0B0F14;border:1px solid #1F2937;border-radius:10px;padding:1rem;
                        font-family:'JetBrains Mono',monospace;font-size:0.72rem;
                        line-height:1.55;color:#6B7280;white-space:pre;overflow-x:auto;
                        max-height:400px;overflow-y:auto">
{output[:6000]}
            </div>""", unsafe_allow_html=True)

        st.caption(f"🔄 {datetime.datetime.now().strftime('%H:%M:%S')} · {len(st.session_state.live_hist)} ciclo(s) acumulados")

    if run_btn:
        with st.spinner("📡 Coletando dados ao vivo..."): _do_live()
    if auto:
        with st.spinner("📡 Atualizando..."): _do_live()
        time.sleep(30); st.rerun()


# ══════════════════════════════════════════════════════════════════════
# PAGE: Value Bets
# ══════════════════════════════════════════════════════════════════════
elif page == "🎯  Value Bets":
    st.markdown('<h1 style="font-size:1.5rem;font-weight:900;margin-bottom:0.25rem">🎯 Value Bets</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6B7280;font-size:0.82rem;margin-bottom:1.5rem">Para ver value bets, rode a Análise Pré-Jogo de uma partida.</p>', unsafe_allow_html=True)

    if mod_err:
        st.error("Módulo não carregado."); st.stop()

    with st.spinner("Buscando partidas..."):
        matches=fetch_matches(date_str)
    if not matches:
        st.warning("Nenhuma partida disponível."); st.stop()

    opts={}
    for m in matches:
        h_t=m["teams"]["home"]; a_t=m["teams"]["away"]
        t_=m["fixture"]["date"].split("T")[1][:5] if "T" in m["fixture"]["date"] else "--"
        opts[f"{h_t['name']} × {a_t['name']} ({t_})"]={
            "fixture_id":m["fixture"]["id"],"home_id":h_t["id"],"home_name":h_t["name"],
            "away_id":a_t["id"],"away_name":a_t["name"],"time":t_,"raw_data":m}

    sel_lbl=st.selectbox("Partida:",list(opts.keys()),key="vb_sel")
    sel=opts[sel_lbl]

    if st.button("🎯 Calcular Value Bets",type="primary",use_container_width=True,key="vb_run"):
        mod.selected_match=sel
        with st.spinner("Calculando EV e Kelly..."):
            output,err=run_captured(mod.execute_advanced_pre_live_analysis_v3)
        d=parse_report(output)

        if d.get("bets"):
            rank_icons={1:"🥇",2:"🥈",3:"🥉"}
            rows=""
            for b in d["bets"]:
                r=int(b["rank"]); ico=rank_icons.get(r,f"#{r}")
                ev_cls="ev-pos" if b["ev"]>0 else "ev-neg"
                ev_s=f"+{b['ev']:.1f}%" if b["ev"]>0 else f"{b['ev']:.1f}%"
                kelly_s=b["kelly"] if b["kelly"]!="SKIP" else '<span style="color:#374151">SKIP</span>'
                row_bg="background:#0d1f0d" if b["ev"]>0 else "opacity:0.5"
                rows+=f"""<tr style="{row_bg}">
                    <td style="font-size:1.1rem">{ico}</td>
                    <td style="font-weight:600;color:#FFFFFF">{b['name']}</td>
                    <td class="num">{b['prob']:.0f}%</td>
                    <td class="num odd">{b['odd']:.2f}</td>
                    <td class="num {ev_cls}">{ev_s}</td>
                    <td class="num stake">{kelly_s}</td>
                </tr>"""
            st.markdown(f"""
            <div class="card">
            <table class="data-table"><thead><tr>
                <th>#</th><th>Mercado</th><th class="num">Prob</th>
                <th class="num">Odd</th><th class="num">EV</th><th class="num">Stake</th>
            </tr></thead><tbody>{rows}</tbody></table>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Nenhuma aposta com EV positivo encontrada.")


# ══════════════════════════════════════════════════════════════════════
# PAGE: Sobre
# ══════════════════════════════════════════════════════════════════════
elif page == "ℹ️   Sobre":
    st.markdown('<h1 style="font-size:1.5rem;font-weight:900;margin-bottom:1.5rem">ℹ️ Sobre</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card card-blue">
        <div class="sec-title">⚽ Sports Intelligence PRO — Copa do Mundo 2026</div>
        <p style="color:#9CA3AF;font-size:0.88rem;margin-bottom:1.5rem">Terminal profissional de análise quantitativa esportiva.</p>
        <div class="sec-title">🧮 Modelos</div>
        <table class="data-table" style="margin-bottom:1.5rem">
            <tr><th>Modelo</th><th>Peso</th><th>Método</th></tr>
            <tr><td>Monte Carlo</td><td>30%</td><td>50.000 simulações estocásticas</td></tr>
            <tr><td>Poisson</td><td>25%</td><td>Distribuição de probabilidade de gols</td></tr>
            <tr><td>Machine Learning</td><td>20%</td><td>Regressão logística + Platt Scaling</td></tr>
            <tr><td>API-Football</td><td>15%</td><td>Predição nativa V3</td></tr>
            <tr><td>ELO Contextual</td><td>10%</td><td>Rating dinâmico com HFA e forma</td></tr>
        </table>
        <div class="sec-title">📡 Módulos Live</div>
        <table class="data-table">
            <tr><td>GII — Goal Imminent Index</td><td style="color:#6B7280">Score 0–100 de iminência de gol</td></tr>
            <tr><td>UPI — Unified Pressure Index</td><td style="color:#6B7280">Pressão ponderada com sparklines</td></tr>
            <tr><td>Momentum Engine</td><td style="color:#6B7280">Janelas 1/3/5/10 ciclos</td></tr>
            <tr><td>xG Momentum Live</td><td style="color:#6B7280">Aceleração de xG em tempo real</td></tr>
            <tr><td>Anti-False Over</td><td style="color:#6B7280">Detector de pressão estéril</td></tr>
            <tr><td>Smart Cashout</td><td style="color:#6B7280">Recomendação inteligente de saída</td></tr>
            <tr><td>Win Probability Live</td><td style="color:#6B7280">Poisson residual por minuto restante</td></tr>
            <tr><td>Trader Assistant AI</td><td style="color:#6B7280">Narrativa + recomendação + confiança</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
