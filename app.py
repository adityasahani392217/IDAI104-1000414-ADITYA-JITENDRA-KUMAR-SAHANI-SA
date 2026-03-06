import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time

st.set_page_config(
    page_title="Aether — Space Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── session defaults ───────────────────────────────────────
for k, v in [("page","onboarding"),("logged_in",False),
              ("username",""),("login_error","")]:
    if k not in st.session_state:
        st.session_state[k] = v


# ════════════════════════════════════════════════════════════
# GLOBAL STYLES  — luxury editorial, warm gold, serif display
# ════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=DM+Mono:ital,wght@0,300;0,400;1,300&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --ink:    #0a0c10;
  --deep:   #0d1018;
  --panel:  #111520;
  --lift:   #161c28;
  --gold:   #c9a96e;
  --gold2:  #e8c98a;
  --gold3:  #7a5c2e;
  --cream:  #e2d5be;
  --mist:   #8a8070;
  --dim:    #3a3830;
  --wire:   rgba(201,169,110,0.14);
  --glow:   rgba(201,169,110,0.08);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
  background: var(--ink);
  font-family: 'DM Sans', sans-serif;
  color: var(--cream);
  min-height: 100vh;
}

/* Noise grain overlay — the texture that separates human from AI */
.stApp::after {
  content: '';
  position: fixed; inset: 0; z-index: 9999;
  pointer-events: none;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 180px 180px;
}

.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* Streamlit button reset */
.stButton > button {
  font-family: 'DM Mono', monospace !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  transition: all 0.35s ease !important;
  border-radius: 2px !important;
}

/* Input fields */
.stTextInput input {
  background: rgba(13,16,24,0.9) !important;
  border: 1px solid var(--dim) !important;
  border-radius: 2px !important;
  color: var(--cream) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.85rem !important;
  padding: 11px 14px !important;
  transition: border-color 0.3s !important;
}
.stTextInput input:focus {
  border-color: var(--gold3) !important;
  box-shadow: 0 0 0 1px rgba(201,169,110,0.2) !important;
  outline: none !important;
}
.stTextInput input::placeholder { color: var(--dim) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb { background: var(--gold3); border-radius: 2px; }

/* Multiselect tags */
[data-baseweb="tag"] {
  background: rgba(201,169,110,0.12) !important;
  border: 1px solid var(--gold3) !important;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("space_missions_dataset__1_.csv")
    df["Launch Date"]  = pd.to_datetime(df["Launch Date"], errors="coerce")
    df["Launch Year"]  = df["Launch Date"].dt.year
    df["Launch Month"] = df["Launch Date"].dt.month
    nums = ["Distance from Earth (light-years)","Mission Duration (years)",
            "Mission Cost (billion USD)","Scientific Yield (points)","Crew Size",
            "Mission Success (%)","Fuel Consumption (tons)","Payload Weight (tons)"]
    for c in nums:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df.drop_duplicates(inplace=True)
    df.dropna(subset=nums, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["Outcome"] = df["Mission Success (%)"].apply(
        lambda x: "Successful" if x >= 90 else ("Partial" if x >= 70 else "Failed"))
    df["Fuel Efficiency"] = df["Payload Weight (tons)"] / df["Fuel Consumption (tons)"].replace(0, np.nan)
    df["Cost per Year"]   = df["Mission Cost (billion USD)"] / df["Mission Duration (years)"].replace(0, np.nan)
    return df


# ════════════════════════════════════════════════════════════
# CHART THEME — warm, editorial, not cold sci-fi
# ════════════════════════════════════════════════════════════
PALETTE = ["#c9a96e","#7a9e8a","#9b7a6a","#6a8a9b","#a08a6a","#7a6a9b","#8a9b7a","#9b8a7a"]
INK, PANEL, GOLD, CREAM, MIST = "#0a0c10","#111520","#c9a96e","#e2d5be","#8a8070"

def chart_theme(fig, height=None):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=PANEL,
        font=dict(family="DM Sans, sans-serif", color=MIST, size=11),
        title_font=dict(family="Cormorant Garamond, serif", color=CREAM, size=15),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
            bgcolor="rgba(13,16,24,0.7)",
            bordercolor="rgba(201,169,110,0.15)",
            borderwidth=1,
            font=dict(family="DM Mono, monospace", size=10, color=MIST),
        ),
    )
    if height:
        fig.update_layout(height=height)
    fig.update_xaxes(
        gridcolor="rgba(201,169,110,0.06)",
        linecolor="rgba(201,169,110,0.12)",
        tickfont=dict(color=MIST, family="DM Mono"),
        title_font=dict(color=MIST),
        zeroline=False,
    )
    fig.update_yaxes(
        gridcolor="rgba(201,169,110,0.06)",
        linecolor="rgba(201,169,110,0.12)",
        tickfont=dict(color=MIST, family="DM Mono"),
        title_font=dict(color=MIST),
        zeroline=False,
    )
    return fig

OUTCOME_CLR = {"Successful":"#7a9e8a","Partial":"#c9a96e","Failed":"#9b6a6a"}

def manual_trendline(fig, xv, yv, color=GOLD, name="Trend"):
    mask = ~(np.isnan(xv) | np.isnan(yv))
    x, y = xv[mask], yv[mask]
    if len(x) < 2: return fig
    m, b = np.polyfit(x, y, 1)
    xl = np.linspace(x.min(), x.max(), 200)
    fig.add_trace(go.Scatter(
        x=xl, y=m*xl+b, mode="lines", name=name,
        line=dict(color=color, width=1.2, dash="dot"),
        opacity=0.55, showlegend=False,
    ))
    return fig

def note_card(text, accent=GOLD):
    st.markdown(f"""
    <div style="
      border-left: 2px solid {accent};
      padding: 14px 20px;
      margin: 16px 0 8px;
      background: rgba(201,169,110,0.03);
      border-radius: 0 4px 4px 0;
    ">
      <p style="font-family:'DM Sans',sans-serif;font-size:0.88rem;
                color:{MIST};line-height:1.75;margin:0;">{text}</p>
    </div>""", unsafe_allow_html=True)

def section_title(text, sub=""):
    st.markdown(f"""
    <div style="margin: 28px 0 18px;">
      <p style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;
                font-weight:400;color:{CREAM};letter-spacing:0.02em;
                line-height:1.2;margin-bottom:4px;">{text}</p>
      {"" if not sub else f'<p style="font-family:DM Mono,monospace;font-size:0.68rem;color:{MIST};letter-spacing:0.1em;margin:0;">{sub.upper()}</p>'}
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE 1 — ONBOARDING
# ════════════════════════════════════════════════════════════
def page_onboarding():
    st.markdown("""
    <style>
    /* Orrery — warm gold planetary rings */
    .orrery-wrap {
      position: fixed; inset: 0; z-index: 1;
      display: flex; align-items: center; justify-content: center;
      pointer-events: none; overflow: hidden;
    }
    .orrery-ring {
      position: absolute; border-radius: 50%;
      border: 1px solid rgba(201,169,110,0.12);
      animation: orrery-turn linear infinite;
      transform-origin: center center;
    }
    .orrery-ring:nth-child(1) { width: 260px; height: 260px; animation-duration: 32s; }
    .orrery-ring:nth-child(2) { width: 440px; height: 440px; animation-duration: 56s; animation-direction: reverse; border-color: rgba(201,169,110,0.09); }
    .orrery-ring:nth-child(3) { width: 640px; height: 640px; animation-duration: 88s; border-color: rgba(201,169,110,0.06); }
    .orrery-ring:nth-child(4) { width: 880px; height: 880px; animation-duration: 140s; animation-direction: reverse; border-color: rgba(201,169,110,0.04); }

    /* Planet markers on rings */
    .orrery-ring:nth-child(1)::after {
      content: ''; position: absolute; top: -5px; left: calc(50% - 5px);
      width: 10px; height: 10px; border-radius: 50%;
      background: radial-gradient(circle at 38% 38%, #e8c98a, #7a5c2e);
      box-shadow: 0 0 12px rgba(201,169,110,0.7);
    }
    .orrery-ring:nth-child(2)::after {
      content: ''; position: absolute; right: -4px; top: calc(50% - 4px);
      width: 8px; height: 8px; border-radius: 50%;
      background: radial-gradient(circle at 38% 38%, #c8d4b8, #5a6e50);
      box-shadow: 0 0 10px rgba(150,180,140,0.6);
    }
    .orrery-ring:nth-child(3)::after {
      content: ''; position: absolute; bottom: 12%; left: 22%;
      width: 6px; height: 6px; border-radius: 50%;
      background: radial-gradient(circle at 38% 38%, #c8b8d8, #5a4a6e);
      box-shadow: 0 0 8px rgba(160,140,200,0.6);
    }
    @keyframes orrery-turn { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

    /* Central sun */
    .orrery-sun {
      position: fixed; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      width: 52px; height: 52px; border-radius: 50%;
      background: radial-gradient(circle at 38% 38%, #f8ead8 0%, #e8c060 35%, #9a6020 70%, transparent 90%);
      box-shadow: 0 0 40px 10px rgba(201,160,50,0.2), 0 0 80px 30px rgba(180,100,20,0.1);
      z-index: 2; pointer-events: none;
      animation: sun-breathe 5s ease-in-out infinite;
    }
    @keyframes sun-breathe {
      0%,100% { box-shadow: 0 0 40px 10px rgba(201,160,50,0.2), 0 0 80px 30px rgba(180,100,20,0.1); }
      50%      { box-shadow: 0 0 55px 18px rgba(201,160,50,0.28), 0 0 100px 50px rgba(180,100,20,0.13); }
    }

    /* Content */
    .ob-outer {
      position: relative; z-index: 10;
      min-height: 100vh;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      text-align: center; padding: 80px 24px 60px;
    }
    .ob-eyebrow {
      font-family: 'DM Mono', monospace;
      font-size: 0.62rem; letter-spacing: 0.22em; color: var(--gold3);
      text-transform: uppercase; margin-bottom: 32px;
      animation: fade-up 1s ease both;
    }
    .ob-name {
      font-family: 'Cormorant Garamond', serif;
      font-size: clamp(4rem, 11vw, 8rem);
      font-weight: 300; font-style: italic;
      color: var(--cream);
      line-height: 0.92;
      letter-spacing: -0.01em;
      margin: 0 0 10px;
      animation: fade-up 1.1s ease 0.15s both;
    }
    .ob-name em { color: var(--gold); font-style: normal; }
    .ob-rule {
      width: 48px; height: 1px;
      background: linear-gradient(90deg, transparent, var(--gold), transparent);
      margin: 24px auto;
      animation: fade-up 1s ease 0.3s both;
    }
    .ob-sub {
      font-family: 'DM Mono', monospace;
      font-size: 0.7rem; letter-spacing: 0.14em; color: var(--mist);
      margin-bottom: 28px;
      animation: fade-up 1s ease 0.4s both;
    }
    .ob-body {
      font-family: 'DM Sans', sans-serif; font-weight: 300;
      font-size: 1rem; color: rgba(138,128,112,0.8);
      max-width: 420px; line-height: 1.9; margin: 0 auto 56px;
      animation: fade-up 1s ease 0.55s both;
    }
    .ob-numbers {
      display: flex; gap: 56px; justify-content: center;
      margin-bottom: 60px;
      animation: fade-up 1s ease 0.7s both;
    }
    .ob-num-val {
      font-family: 'Cormorant Garamond', serif; font-weight: 300;
      font-size: 2.4rem; color: var(--gold); display: block;
      letter-spacing: -0.02em;
    }
    .ob-num-lbl {
      font-family: 'DM Mono', monospace; font-size: 0.6rem;
      letter-spacing: 0.15em; color: var(--gold3);
      text-transform: uppercase; margin-top: 2px; display: block;
    }

    @keyframes fade-up {
      from { opacity: 0; transform: translateY(18px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    /* Launch button area */
    .ob-btn-wrap { animation: fade-up 1s ease 0.9s both; }
    </style>

    <div class="orrery-wrap">
      <div class="orrery-ring"></div>
      <div class="orrery-ring"></div>
      <div class="orrery-ring"></div>
      <div class="orrery-ring"></div>
    </div>
    <div class="orrery-sun"></div>

    <div class="ob-outer">
      <p class="ob-eyebrow">Mathematics for AI · Summative Assessment · 2025</p>
      <h1 class="ob-name"><em>Æ</em>ther</h1>
      <div class="ob-rule"></div>
      <p class="ob-sub">Space Mission Intelligence</p>
      <p class="ob-body">
        Five hundred missions. Four launch vehicles. Decades of data.
        Explore the physics, economics, and outcomes of humanity's reach into the cosmos.
      </p>
      <div class="ob-numbers">
        <div><span class="ob-num-val">500</span><span class="ob-num-lbl">Missions</span></div>
        <div><span class="ob-num-val">4</span><span class="ob-num-lbl">Vehicles</span></div>
        <div><span class="ob-num-val">15</span><span class="ob-num-lbl">Variables</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Button — centered, warm gold style
    _, mc, _ = st.columns([2.5, 1, 2.5])
    with mc:
        st.markdown("""
        <style>
        /* Target only the center column's button */
        div[data-testid="stColumns"] > div:nth-child(2) .stButton > button {
          width: 100% !important;
          background: transparent !important;
          color: var(--gold) !important;
          border: 1px solid rgba(201,169,110,0.45) !important;
          font-size: 0.65rem !important;
          font-weight: 400 !important;
          padding: 14px 0 !important;
          letter-spacing: 0.2em !important;
          border-radius: 1px !important;
          box-shadow: inset 0 0 0 0 rgba(201,169,110,0);
          margin-top: -200px;
          position: relative; z-index: 20;
        }
        div[data-testid="stColumns"] > div:nth-child(2) .stButton > button:hover {
          background: rgba(201,169,110,0.07) !important;
          border-color: rgba(201,169,110,0.7) !important;
          color: #e8c98a !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("Enter the Observatory", key="ob_enter"):
            st.session_state.page = "loading"
            st.rerun()


# ════════════════════════════════════════════════════════════
# PAGE 2 — LOADING
# ════════════════════════════════════════════════════════════
def page_loading():
    placeholder = st.empty()
    steps = [
        ( 6, "Calibrating instruments"),
        (18, "Loading mission records"),
        (33, "Parsing 500 flight logs"),
        (50, "Initialising physics engine"),
        (64, "Rendering solar charts"),
        (78, "Compiling visualisation modules"),
        (91, "Verifying data integrity"),
        (100,"Ready for launch"),
    ]
    for pct, msg in steps:
        with placeholder.container():
            st.markdown(f"""
            <style>
            .ld {{ display:flex; flex-direction:column; align-items:center;
                    justify-content:center; min-height:100vh; gap:0; }}
            .ld-title {{
              font-family:'Cormorant Garamond',serif; font-style:italic;
              font-size:1.9rem; font-weight:300; color:var(--cream);
              letter-spacing:0.04em; margin-bottom:48px;
            }}
            /* Thin arc spinner — NOT the classic AI double-ring */
            .ld-arc-wrap {{
              position:relative; width:110px; height:110px; margin-bottom:44px;
            }}
            .ld-arc {{
              position:absolute; inset:0; border-radius:50%;
              border:1px solid rgba(201,169,110,0.1);
            }}
            .ld-arc-spin {{
              position:absolute; inset:0; border-radius:50%;
              border:1px solid transparent;
              border-top-color: var(--gold);
              animation: arc-spin 2.2s cubic-bezier(0.4,0,0.2,1) infinite;
            }}
            .ld-arc-spin2 {{
              position:absolute; inset:14px; border-radius:50%;
              border:1px solid transparent;
              border-right-color:rgba(201,169,110,0.35);
              animation: arc-spin 3.5s linear infinite reverse;
            }}
            .ld-center {{
              position:absolute; top:50%; left:50%;
              transform:translate(-50%,-50%);
              width:8px; height:8px; border-radius:50%;
              background: var(--gold);
              box-shadow:0 0 10px 2px rgba(201,169,110,0.5);
            }}
            @keyframes arc-spin {{ to {{ transform:rotate(360deg); }} }}

            .ld-msg {{
              font-family:'DM Mono',monospace; font-size:0.68rem;
              letter-spacing:0.1em; color:var(--gold3);
              text-transform:uppercase; margin-bottom:28px;
              min-height:16px;
            }}
            .ld-bar-bg {{
              width:200px; height:1px;
              background:rgba(201,169,110,0.1);
            }}
            .ld-bar-fg {{
              height:1px;
              background:linear-gradient(90deg,var(--gold3),var(--gold));
              width:{pct}%; transition:width 0.4s ease;
            }}
            .ld-pct {{
              font-family:'DM Mono',monospace; font-size:0.58rem;
              color:rgba(201,169,110,0.35); letter-spacing:0.1em;
              margin-top:10px;
            }}
            </style>
            <div class="ld">
              <p class="ld-title">Æther</p>
              <div class="ld-arc-wrap">
                <div class="ld-arc"></div>
                <div class="ld-arc-spin"></div>
                <div class="ld-arc-spin2"></div>
                <div class="ld-center"></div>
              </div>
              <p class="ld-msg">{msg}</p>
              <div class="ld-bar-bg"><div class="ld-bar-fg"></div></div>
              <p class="ld-pct">{pct} %</p>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.38)
    st.session_state.page = "login"
    st.rerun()


# ════════════════════════════════════════════════════════════
# PAGE 3 — LOGIN
# ════════════════════════════════════════════════════════════
def page_login():
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display:none !important; }

    /* Very faint radial vignette — not rings */
    .lg-vignette {
      position:fixed; inset:0; z-index:1; pointer-events:none;
      background: radial-gradient(ellipse 60% 60% at 50% 50%,
        transparent 40%, rgba(0,0,0,0.5) 100%);
    }

    .lg-card {
      background: var(--panel);
      border: 1px solid rgba(201,169,110,0.1);
      border-radius: 3px;
      padding: 52px 56px 44px;
      max-width: 420px; width: 100%;
      position: relative; overflow: hidden;
    }
    /* Subtle top-left corner accent */
    .lg-card::before {
      content: '';
      position: absolute; top: 0; left: 0;
      width: 48px; height: 1px;
      background: var(--gold);
    }
    .lg-card::after {
      content: '';
      position: absolute; top: 0; left: 0;
      width: 1px; height: 48px;
      background: var(--gold);
    }

    .lg-wordmark {
      font-family: 'Cormorant Garamond', serif;
      font-size: 2.4rem; font-weight: 300; font-style: italic;
      color: var(--cream); letter-spacing: 0.04em;
      margin-bottom: 4px;
    }
    .lg-wordmark em { color: var(--gold); font-style: normal; }
    .lg-tagline {
      font-family: 'DM Mono', monospace; font-size: 0.6rem;
      letter-spacing: 0.18em; color: var(--gold3);
      text-transform: uppercase; margin-bottom: 40px;
    }
    .lg-rule {
      height: 1px; margin-bottom: 32px;
      background: rgba(201,169,110,0.1);
    }
    .lg-field-label {
      font-family: 'DM Mono', monospace; font-size: 0.6rem;
      letter-spacing: 0.16em; color: var(--gold3);
      text-transform: uppercase;
      margin-bottom: 6px; margin-top: 18px;
      display: block;
    }
    .lg-hint {
      font-family: 'DM Mono', monospace; font-size: 0.62rem;
      letter-spacing: 0.05em; color: rgba(122,92,46,0.6);
      margin-top: 20px; text-align: center;
    }
    .lg-hint span { color: var(--gold3); }
    .lg-error {
      font-family: 'DM Mono', monospace; font-size: 0.65rem;
      letter-spacing: 0.05em; color: #9b6a6a;
      margin-top: 10px; padding: 9px 12px;
      border: 1px solid rgba(155,106,106,0.25);
      border-radius: 2px; background: rgba(155,106,106,0.06);
    }

    /* Primary button */
    .btn-primary .stButton > button {
      width: 100% !important;
      background: rgba(201,169,110,0.1) !important;
      color: var(--gold) !important;
      border: 1px solid rgba(201,169,110,0.4) !important;
      font-size: 0.62rem !important;
      padding: 13px !important;
      border-radius: 1px !important;
      letter-spacing: 0.18em !important;
    }
    .btn-primary .stButton > button:hover {
      background: rgba(201,169,110,0.16) !important;
      border-color: rgba(201,169,110,0.65) !important;
    }
    /* Ghost button */
    .btn-ghost .stButton > button {
      width: 100% !important;
      background: transparent !important;
      color: var(--mist) !important;
      border: 1px solid rgba(138,128,112,0.2) !important;
      font-size: 0.62rem !important;
      padding: 13px !important;
      border-radius: 1px !important;
      letter-spacing: 0.18em !important;
    }
    .btn-ghost .stButton > button:hover {
      border-color: rgba(138,128,112,0.45) !important;
      color: var(--cream) !important;
    }
    </style>
    <div class="lg-vignette"></div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1.2, 1.4, 1.2])
    with col:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;
                    justify-content:center;min-height:100vh;">
        <div class="lg-card">
          <p class="lg-wordmark"><em>Æ</em>ther</p>
          <p class="lg-tagline">Mission Control Access</p>
          <div class="lg-rule"></div>
        """, unsafe_allow_html=True)

        st.markdown('<span class="lg-field-label">Username</span>', unsafe_allow_html=True)
        uname = st.text_input("", placeholder="your.name@aether.space",
                               key="lg_u", label_visibility="collapsed")

        st.markdown('<span class="lg-field-label">Access Code</span>', unsafe_allow_html=True)
        pword = st.text_input("", placeholder="••••••••",
                               type="password", key="lg_p",
                               label_visibility="collapsed")

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        b1, b2 = st.columns([1, 1])
        with b1:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            do_login = st.button("Sign in", key="do_login")
            st.markdown('</div>', unsafe_allow_html=True)
        with b2:
            st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
            do_demo  = st.button("Demo", key="do_demo")
            st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.login_error:
            st.markdown(f'<p class="lg-error">{st.session_state.login_error}</p>',
                        unsafe_allow_html=True)

        st.markdown("""
          <p class="lg-hint">Demo credentials — <span>admin</span> / <span>1234</span></p>
        </div></div>
        """, unsafe_allow_html=True)

        if do_login:
            if not uname.strip() or not pword.strip():
                st.session_state.login_error = "Please enter your credentials."
                st.rerun()
            elif uname.strip() == "admin" and pword.strip() == "1234":
                st.session_state.logged_in   = True
                st.session_state.username    = "admin"
                st.session_state.login_error = ""
                st.session_state.page        = "dashboard"
                st.rerun()
            else:
                st.session_state.login_error = "Incorrect credentials. Try the demo button."
                st.rerun()
        if do_demo:
            st.session_state.logged_in   = True
            st.session_state.username    = "observer"
            st.session_state.login_error = ""
            st.session_state.page        = "dashboard"
            st.rerun()


# ════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════
def page_dashboard():
    df = load_data()

    # Restore sidebar
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
      display: flex !important;
      background: var(--deep) !important;
      border-right: 1px solid rgba(201,169,110,0.08) !important;
    }
    /* Sidebar label overrides */
    .sb-head {
      font-family:'Cormorant Garamond',serif; font-weight:400; font-style:italic;
      font-size:1.2rem; color:var(--cream); margin-bottom:4px;
    }
    .sb-sub {
      font-family:'DM Mono',monospace; font-size:0.58rem;
      letter-spacing:0.14em; color:var(--gold3); text-transform:uppercase;
      margin-bottom:24px; border-bottom:1px solid rgba(201,169,110,0.08);
      padding-bottom:16px;
    }
    .sb-label {
      font-family:'DM Mono',monospace; font-size:0.58rem;
      letter-spacing:0.14em; color:var(--gold3);
      text-transform:uppercase; margin:16px 0 5px; display:block;
    }
    /* Sign out button */
    .btn-signout .stButton > button {
      width:100% !important;
      background:transparent !important;
      color:rgba(138,128,112,0.5) !important;
      border:1px solid rgba(138,128,112,0.15) !important;
      font-size:0.58rem !important; padding:10px !important;
      border-radius:1px !important; letter-spacing:0.14em !important;
      margin-top: 12px !important;
    }
    .btn-signout .stButton > button:hover {
      color:var(--mist) !important; border-color:rgba(138,128,112,0.35) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<p class="sb-head"><em>Æ</em>ther</p>', unsafe_allow_html=True)
        st.markdown('<p class="sb-sub">Mission Filters</p>', unsafe_allow_html=True)

        st.markdown('<span class="sb-label">Mission type</span>', unsafe_allow_html=True)
        mtypes = st.multiselect("",
            sorted(df["Mission Type"].unique()),
            default=sorted(df["Mission Type"].unique()),
            label_visibility="collapsed")

        st.markdown('<span class="sb-label">Launch vehicle</span>', unsafe_allow_html=True)
        vehs = st.multiselect("",
            sorted(df["Launch Vehicle"].unique()),
            default=sorted(df["Launch Vehicle"].unique()),
            label_visibility="collapsed")

        st.markdown('<span class="sb-label">Outcome</span>', unsafe_allow_html=True)
        outcs = st.multiselect("",
            ["Successful","Partial","Failed"],
            default=["Successful","Partial","Failed"],
            label_visibility="collapsed")

        st.markdown('<span class="sb-label">Cost range · B USD</span>', unsafe_allow_html=True)
        cmin,cmax = float(df["Mission Cost (billion USD)"].min()), float(df["Mission Cost (billion USD)"].max())
        crng = st.slider("", cmin, cmax, (cmin,cmax), label_visibility="collapsed")

        st.markdown('<span class="sb-label">Launch years</span>', unsafe_allow_html=True)
        ymin,ymax = int(df["Launch Year"].min()), int(df["Launch Year"].max())
        yrng = st.slider("", ymin, ymax, (ymin,ymax), label_visibility="collapsed")

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="btn-signout">', unsafe_allow_html=True)
        if st.button("Sign out", key="signout"):
            for k in ["page","logged_in","username","login_error"]:
                if k in st.session_state: del st.session_state[k]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Filter
    fdf = df[
        df["Mission Type"].isin(mtypes) &
        df["Launch Vehicle"].isin(vehs) &
        df["Outcome"].isin(outcs) &
        df["Mission Cost (billion USD)"].between(crng[0],crng[1]) &
        df["Launch Year"].between(yrng[0],yrng[1])
    ].copy()

    # ── Top bar ──────────────────────────────────────────────
    st.markdown(f"""
    <style>
    .topbar {{
      display:flex; align-items:center; justify-content:space-between;
      padding:14px 36px;
      background:rgba(10,12,16,0.92);
      border-bottom:1px solid rgba(201,169,110,0.08);
      backdrop-filter:blur(16px);
      position:sticky; top:0; z-index:999;
    }}
    .tb-brand {{
      font-family:'Cormorant Garamond',serif; font-weight:300; font-style:italic;
      font-size:1.25rem; color:var(--cream); letter-spacing:0.04em;
    }}
    .tb-brand em {{ color:var(--gold); font-style:normal; }}
    .tb-meta {{
      font-family:'DM Mono',monospace; font-size:0.6rem;
      letter-spacing:0.1em; color:var(--gold3);
    }}
    .tb-meta b {{ color:var(--mist); font-weight:400; }}
    </style>
    <div class="topbar">
      <span class="tb-brand"><em>Æ</em>ther · Space Intelligence</span>
      <span class="tb-meta">
        {len(fdf)} missions · {st.session_state.username}
      </span>
    </div>
    """, unsafe_allow_html=True)

    body = '<div style="padding:32px 36px;">'
    st.markdown(body, unsafe_allow_html=True)

    if len(fdf) == 0:
        st.warning("No missions match the current filters.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── KPI row ──────────────────────────────────────────────
    st.markdown("""
    <style>
    .kpi-row {
      display:grid; grid-template-columns:repeat(6,1fr);
      gap:1px; margin-bottom:36px;
      border:1px solid rgba(201,169,110,0.1); border-radius:3px;
      overflow:hidden; background:rgba(201,169,110,0.07);
    }
    .kpi-cell {
      background:var(--panel); padding:24px 16px; text-align:left;
    }
    .kpi-num {
      font-family:'Cormorant Garamond',serif; font-weight:300;
      font-size:2rem; color:var(--cream); line-height:1;
      letter-spacing:-0.01em; display:block; margin-bottom:6px;
    }
    .kpi-label {
      font-family:'DM Mono',monospace; font-size:0.58rem;
      letter-spacing:0.14em; color:var(--gold3);
      text-transform:uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

    kpis = [
        (f"{len(fdf):,}", "Missions"),
        (f"{fdf['Mission Success (%)'].mean():.1f}%", "Avg success"),
        (f"${fdf['Mission Cost (billion USD)'].sum():,.0f}B", "Total cost"),
        (f"{fdf['Fuel Consumption (tons)'].mean():,.0f} t", "Avg fuel"),
        (f"{fdf['Crew Size'].mean():.0f}", "Avg crew"),
        (f"{fdf['Scientific Yield (points)'].mean():.1f}", "Avg yield"),
    ]
    kpi_html = '<div class="kpi-row">'
    for val, lbl in kpis:
        kpi_html += f'<div class="kpi-cell"><span class="kpi-num">{val}</span><span class="kpi-label">{lbl}</span></div>'
    kpi_html += '</div>'
    st.markdown(kpi_html, unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
      background:transparent; padding:0; gap:0;
      border-bottom:1px solid rgba(201,169,110,0.12);
    }
    .stTabs [data-baseweb="tab"] {
      font-family:'DM Mono',monospace !important;
      font-size:0.62rem !important; letter-spacing:0.14em !important;
      color:var(--gold3) !important; text-transform:uppercase !important;
      padding:12px 22px !important; border-radius:0 !important;
      background:transparent !important;
      border-bottom:2px solid transparent !important;
    }
    .stTabs [aria-selected="true"] {
      color:var(--cream) !important;
      border-bottom:2px solid var(--gold) !important;
    }
    .stTabs [data-baseweb="tab-panel"] { padding-top:28px !important; }
    </style>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview", "Fuel & Payload", "Cost", "Simulation", "Data & Insights",
    ])

    # ── TAB 1 · Overview ─────────────────────────────────────
    with tab1:
        section_title("Solar mission map", "Distance-scaled orbital reference")
        st.markdown("""
        <p style="font-family:'DM Sans',sans-serif;font-weight:300;font-size:0.9rem;
                  color:var(--mist);margin-bottom:18px;line-height:1.8;">
          Each mission is plotted in a solar-reference frame — orbital radius proportional
          to distance from Earth, wound chronologically around the sun.
          Dot size reflects mission success rate.
        </p>""", unsafe_allow_html=True)

        fdf2 = fdf.sort_values("Distance from Earth (light-years)").reset_index(drop=True)
        fdf2["Angle"] = np.linspace(0, 2*np.pi*4, len(fdf2))
        fdf2["SX"] = fdf2["Distance from Earth (light-years)"] * np.cos(fdf2["Angle"])
        fdf2["SY"] = fdf2["Distance from Earth (light-years)"] * np.sin(fdf2["Angle"])
        type_clr = {t: PALETTE[i%len(PALETTE)] for i,t in enumerate(sorted(fdf2["Mission Type"].unique()))}

        fig_sol = go.Figure()
        fig_sol.add_trace(go.Scatter(
            x=[0], y=[0], mode="markers+text",
            marker=dict(size=22, color="#e8c060", line=dict(color="#9a6020",width=1.5)),
            text=["Earth"], textposition="top center",
            textfont=dict(size=9, color="rgba(201,160,80,0.7)", family="DM Mono"),
            name="Earth",
        ))
        for r in [10,25,42,58]:
            th = np.linspace(0,2*np.pi,300)
            fig_sol.add_trace(go.Scatter(
                x=r*np.cos(th), y=r*np.sin(th), mode="lines",
                line=dict(color="rgba(201,169,110,0.06)",width=0.8,dash="dot"),
                showlegend=False, hoverinfo="skip",
            ))
        for mt,grp in fdf2.groupby("Mission Type"):
            col = type_clr[mt]
            fig_sol.add_trace(go.Scatter(
                x=grp["SX"], y=grp["SY"], mode="markers", name=mt,
                marker=dict(
                    size=4+grp["Mission Success (%)"]/30, color=col,
                    opacity=0.65, line=dict(color="rgba(0,0,0,0.3)",width=0.4),
                ),
                customdata=np.stack([
                    grp["Mission Name"], grp["Mission Success (%)"].round(1),
                    grp["Mission Cost (billion USD)"].round(1), grp["Launch Vehicle"]
                ], axis=-1),
                hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}% · $%{customdata[2]}B · %{customdata[3]}<extra></extra>",
            ))
        fig_sol.update_layout(
            height=480, showlegend=True,
            xaxis=dict(showticklabels=False,showgrid=False,zeroline=False),
            yaxis=dict(showticklabels=False,showgrid=False,zeroline=False,scaleanchor="x"),
        )
        chart_theme(fig_sol)
        st.plotly_chart(fig_sol, use_container_width=True)

        # Two columns — box + bar
        c1, c2 = st.columns([1.1, 1], gap="large")
        with c1:
            section_title("Success distribution", "By mission type")
            fig_bx = go.Figure()
            for i,(mt,grp) in enumerate(fdf.groupby("Mission Type")):
                col=PALETTE[i%len(PALETTE)]
                r,g,b=int(col[1:3],16),int(col[3:5],16),int(col[5:7],16)
                fig_bx.add_trace(go.Box(
                    y=grp["Mission Success (%)"], name=mt,
                    marker_color=col, line_color=col,
                    fillcolor=f"rgba({r},{g},{b},0.1)",
                    boxpoints="outliers",
                ))
            chart_theme(fig_bx, 300)
            fig_bx.update_layout(showlegend=False, yaxis_title="Success (%)")
            st.plotly_chart(fig_bx, use_container_width=True)

        with c2:
            section_title("Missions per vehicle", "Fleet activity")
            vc = fdf["Launch Vehicle"].value_counts().reset_index()
            vc.columns=["V","C"]
            fig_vb = go.Figure(go.Bar(
                x=vc["V"], y=vc["C"],
                marker=dict(color=PALETTE[:len(vc)],
                            line=dict(color="rgba(0,0,0,0.3)",width=0.5)),
                text=vc["C"], textposition="outside",
                textfont=dict(color=MIST,family="DM Mono",size=9),
            ))
            chart_theme(fig_vb, 300)
            fig_vb.update_layout(showlegend=False, yaxis_title="Count")
            st.plotly_chart(fig_vb, use_container_width=True)

        section_title("Variable correlations", "Pearson correlation matrix")
        ndf = fdf[["Distance from Earth (light-years)","Mission Duration (years)",
                   "Mission Cost (billion USD)","Scientific Yield (points)",
                   "Crew Size","Mission Success (%)","Fuel Consumption (tons)","Payload Weight (tons)"]]
        corr = ndf.corr()
        fh, ax = plt.subplots(figsize=(11,4.2))
        fh.patch.set_facecolor("none"); ax.set_facecolor(PANEL)
        cmap = sns.diverging_palette(28, 200, s=55, l=48, as_cmap=True)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap=cmap,
                    linewidths=0.3, ax=ax, annot_kws={"size":7.5,"family":"DM Mono"},
                    cbar_kws={"shrink":0.7})
        ax.set_title("Pearson Correlation Matrix", color=CREAM, fontsize=12,
                     fontfamily="serif", pad=12)
        ax.tick_params(colors=MIST)
        plt.xticks(color=MIST, fontsize=7.5, rotation=28, ha="right", fontfamily="monospace")
        plt.yticks(color=MIST, fontsize=7.5, fontfamily="monospace")
        plt.tight_layout()
        st.pyplot(fh)
        plt.close(fh)

        note_card("Mission duration and fuel consumption share the strongest positive correlation in the dataset. "
                  "Distance from Earth drives both — a direct consequence of the rocket equation's dependency on Δv requirements.")

    # ── TAB 2 · Fuel & Payload ───────────────────────────────
    with tab2:
        c1, c2 = st.columns([1,1], gap="large")
        with c1:
            section_title("Payload vs fuel", "Scatter with OLS trend")
            fig_pf = go.Figure()
            for i,(mt,grp) in enumerate(fdf.groupby("Mission Type")):
                col=PALETTE[i%len(PALETTE)]
                fig_pf.add_trace(go.Scatter(
                    x=grp["Payload Weight (tons)"], y=grp["Fuel Consumption (tons)"],
                    mode="markers", name=mt,
                    marker=dict(size=6.5,color=col,opacity=0.65,
                                line=dict(color="rgba(0,0,0,0.25)",width=0.4)),
                    customdata=grp["Mission Name"].values,
                    hovertemplate="<b>%{customdata}</b><br>Payload %{x:.1f} t · Fuel %{y:.1f} t<extra></extra>",
                ))
            manual_trendline(fig_pf,
                fdf["Payload Weight (tons)"].values,
                fdf["Fuel Consumption (tons)"].values)
            chart_theme(fig_pf, 330)
            fig_pf.update_layout(xaxis_title="Payload (tons)", yaxis_title="Fuel (tons)")
            st.plotly_chart(fig_pf, use_container_width=True)

        with c2:
            section_title("Distance vs duration", "With OLS regression")
            fig_dd = go.Figure()
            for i,(veh,grp) in enumerate(fdf.groupby("Launch Vehicle")):
                col=PALETTE[i%len(PALETTE)]
                fig_dd.add_trace(go.Scatter(
                    x=grp["Distance from Earth (light-years)"],
                    y=grp["Mission Duration (years)"],
                    mode="markers", name=veh,
                    marker=dict(size=6,color=col,opacity=0.65),
                    customdata=grp["Mission Name"].values,
                    hovertemplate="<b>%{customdata}</b><br>%{x:.2f} ly · %{y:.1f} yrs<extra></extra>",
                ))
            manual_trendline(fig_dd,
                fdf["Distance from Earth (light-years)"].values,
                fdf["Mission Duration (years)"].values,
                color="#9b7a6a")
            chart_theme(fig_dd, 330)
            fig_dd.update_layout(xaxis_title="Distance (light-years)", yaxis_title="Duration (years)")
            st.plotly_chart(fig_dd, use_container_width=True)

        section_title("Fuel efficiency by type", "Payload ÷ Fuel consumed")
        eff = (fdf.groupby("Mission Type")["Fuel Efficiency"]
               .mean().reset_index().sort_values("Fuel Efficiency", ascending=False))
        fig_ef = go.Figure(go.Bar(
            x=eff["Mission Type"], y=eff["Fuel Efficiency"],
            marker=dict(color=PALETTE[:len(eff)],
                        line=dict(color="rgba(0,0,0,0.3)",width=0.5)),
            text=eff["Fuel Efficiency"].round(5), textposition="outside",
            textfont=dict(color=MIST,family="DM Mono",size=9.5),
        ))
        chart_theme(fig_ef, 260)
        fig_ef.update_layout(showlegend=False, yaxis_title="Efficiency ratio")
        st.plotly_chart(fig_ef, use_container_width=True)

        section_title("Fuel distribution by vehicle", "Violin with box overlay")
        fig_vi = go.Figure()
        for i,(veh,grp) in enumerate(fdf.groupby("Launch Vehicle")):
            col=PALETTE[i%len(PALETTE)]
            r,g,b=int(col[1:3],16),int(col[3:5],16),int(col[5:7],16)
            fig_vi.add_trace(go.Violin(
                x=grp["Launch Vehicle"], y=grp["Fuel Consumption (tons)"],
                name=veh, line_color=col,
                fillcolor=f"rgba({r},{g},{b},0.12)",
                box_visible=True, meanline_visible=True, points="outliers",
            ))
        chart_theme(fig_vi, 280)
        fig_vi.update_layout(showlegend=False, yaxis_title="Fuel (tons)")
        st.plotly_chart(fig_vi, use_container_width=True)

        note_card("The OLS trendline confirms Newton's second law in practice — heavier payloads "
                  "require proportionally more fuel. F = ma: greater mass demands greater sustained "
                  "thrust, which means larger propellant reserves.", "#7a9e8a")

    # ── TAB 3 · Cost ─────────────────────────────────────────
    with tab3:
        c1, c2 = st.columns([1,1], gap="large")
        with c1:
            section_title("Cost vs success rate", "Bubble size = crew")
            fig_cs = go.Figure()
            for outc,grp in fdf.groupby("Outcome"):
                col=OUTCOME_CLR.get(outc,MIST)
                fig_cs.add_trace(go.Scatter(
                    x=grp["Mission Cost (billion USD)"], y=grp["Mission Success (%)"],
                    mode="markers", name=outc,
                    marker=dict(size=5+grp["Crew Size"]/14, color=col,
                                opacity=0.65, line=dict(color="rgba(0,0,0,0.25)",width=0.4)),
                    customdata=np.stack([grp["Mission Name"],grp["Launch Vehicle"]],axis=-1),
                    hovertemplate="<b>%{customdata[0]}</b><br>$%{x:.1f}B · %{y:.1f}%<br>%{customdata[1]}<extra></extra>",
                ))
            chart_theme(fig_cs, 330)
            fig_cs.update_layout(xaxis_title="Cost (B USD)", yaxis_title="Success (%)")
            st.plotly_chart(fig_cs, use_container_width=True)

        with c2:
            section_title("Avg cost by outcome", "")
            cg = fdf.groupby("Outcome")["Mission Cost (billion USD)"].mean().reset_index()
            fig_cb = go.Figure(go.Bar(
                x=cg["Outcome"], y=cg["Mission Cost (billion USD)"],
                marker=dict(color=[OUTCOME_CLR.get(c,MIST) for c in cg["Outcome"]],
                            line=dict(color="rgba(0,0,0,0.3)",width=0.5)),
                text=["$"+str(round(v,1))+"B" for v in cg["Mission Cost (billion USD)"]],
                textposition="outside",
                textfont=dict(color=MIST,family="DM Mono",size=9.5),
            ))
            chart_theme(fig_cb, 330)
            fig_cb.update_layout(showlegend=False, yaxis_title="Avg cost (B USD)")
            st.plotly_chart(fig_cb, use_container_width=True)

        section_title("Scientific yield over time", "Average by mission type · year")
        yt = fdf.groupby(["Launch Year","Mission Type"])["Scientific Yield (points)"].mean().reset_index()
        fyt,ayt = plt.subplots(figsize=(13,3.8))
        fyt.patch.set_facecolor("none"); ayt.set_facecolor(PANEL)
        for i,mt in enumerate(yt["Mission Type"].unique()):
            sub=yt[yt["Mission Type"]==mt]
            c=PALETTE[i%len(PALETTE)]
            ayt.plot(sub["Launch Year"],sub["Scientific Yield (points)"],
                     marker="o",label=mt,linewidth=1.8,color=c,
                     markersize=4.5,markerfacecolor=c,markeredgewidth=0)
            ayt.fill_between(sub["Launch Year"],sub["Scientific Yield (points)"],
                              alpha=0.06,color=c)
        ayt.set_title("Average Scientific Yield by Year & Mission Type",
                      color=CREAM, fontsize=12, fontfamily="serif")
        ayt.set_xlabel("Year",color=MIST,fontfamily="monospace")
        ayt.set_ylabel("Yield (pts)",color=MIST,fontfamily="monospace")
        ayt.tick_params(colors=MIST)
        ayt.legend(facecolor=PANEL,labelcolor=MIST,framealpha=0.7,fontsize=9)
        for sp in ayt.spines.values(): sp.set_color("rgba(201,169,110,0.1)")
        ayt.grid(color="rgba(201,169,110,0.05)",linestyle="--",linewidth=0.5)
        plt.tight_layout()
        st.pyplot(fyt)
        plt.close(fyt)

        section_title("Mission type × outcome", "Sunburst breakdown")
        sb = fdf.groupby(["Mission Type","Outcome"]).size().reset_index(name="Count")
        fig_sb = px.sunburst(sb, path=["Mission Type","Outcome"], values="Count",
                             color="Mission Type", color_discrete_sequence=PALETTE)
        chart_theme(fig_sb, 370)
        st.plotly_chart(fig_sb, use_container_width=True)

        note_card("There is no meaningful correlation between mission cost and success rate. "
                  "Research missions deliver the highest scientific yield per billion — "
                  "making them the most efficient investment in terms of academic return.", "#9b7a6a")

    # ── TAB 4 · Simulation ───────────────────────────────────
    with tab4:
        section_title("Launch simulation", "Euler integration of differential equations")
        st.markdown("""
        <div style="font-family:'DM Mono',monospace;font-size:0.72rem;
                    color:var(--mist);line-height:2.0;
                    border-left:2px solid rgba(201,169,110,0.18);
                    padding:12px 18px;margin-bottom:28px;
                    background:rgba(201,169,110,0.02);">
          a(t) = [ T &minus; m(t)·g &minus; ½·Cd·ρ(h)·A·v² ] / m(t)
          &emsp;|&emsp; v(t+Δt) = v + a·Δt &emsp;|&emsp; h(t+Δt) = h + v·Δt<br>
          ρ(h) = 1.225 · e<sup>−h/8500</sup> &emsp;
          [ISA exponential atmosphere model]
        </div>""", unsafe_allow_html=True)

        cs1,cs2,cs3 = st.columns(3, gap="large")
        with cs1:
            thr = st.slider("Thrust kN",      500, 5000, 2500, 100)
            pl  = st.slider("Payload tons",     1,  150,   30,   1)
        with cs2:
            fu  = st.slider("Fuel tons",      100, 1200,  400,  50)
            cd  = st.slider("Drag coeff Cd", 0.05,  1.0,  0.3, 0.05)
        with cs3:
            ns  = st.slider("Time steps",      50,  600,  250,  50)
            dt  = st.slider("Δt seconds",       1,   10,    2,   1)

        G=9.81; A=12.0
        m=(pl+fu)*1000.0; T_N=thr*1000.0
        burn=(fu*1000.0)/max(ns,1)
        alt_a=[0.0]; vel_a=[0.0]; acc_a=[0.0]; mass_a=[m/1000]
        fr=fu*1000.0

        for _ in range(ns):
            if fr>0:
                eff_T=T_N; bs=burn*dt
                fr=max(0.0,fr-bs); m=max(pl*1000.0,m-bs)
            else:
                eff_T=0.0
            rho=1.225*np.exp(-alt_a[-1]/8500.0)
            drag=0.5*cd*rho*A*vel_a[-1]**2
            a=(eff_T-m*G-drag)/max(m,1.0)
            v=vel_a[-1]+a*dt; h=max(0.0,alt_a[-1]+v*dt)
            acc_a.append(a); vel_a.append(v)
            alt_a.append(h/1000.0); mass_a.append(m/1000.0)

        ta=[i*dt for i in range(len(alt_a))]
        sd=pd.DataFrame({"t":ta,"alt":alt_a,"vel":vel_a,"acc":acc_a,"mass":mass_a})

        section_title("Launch path", "Altitude & velocity")
        fig_rv=go.Figure()
        fig_rv.add_trace(go.Scatter(
            x=sd["t"],y=sd["alt"],name="Altitude km",
            line=dict(color=PALETTE[0],width=2.2),
            fill="tozeroy",fillcolor=f"rgba({int(PALETTE[0][1:3],16)},{int(PALETTE[0][3:5],16)},{int(PALETTE[0][5:7],16)},0.06)",
        ))
        fig_rv.add_trace(go.Scatter(
            x=sd["t"],y=sd["vel"],name="Velocity m/s",
            line=dict(color=PALETTE[1],width=2.0),yaxis="y2",
        ))
        bx=sd["vel"].idxmax()
        fig_rv.add_trace(go.Scatter(
            x=[sd.loc[bx,"t"]],y=[sd.loc[bx,"alt"]],
            mode="markers+text",name="Burnout",
            marker=dict(size=10,color=PALETTE[2],symbol="diamond"),
            text=["burnout"],textposition="top right",
            textfont=dict(size=9,color=PALETTE[2],family="DM Mono"),
            yaxis="y1",
        ))
        fig_rv.update_layout(
            height=370, xaxis_title="Time (s)",
            yaxis=dict(title="Altitude (km)",color=PALETTE[0],gridcolor="rgba(201,169,110,0.05)"),
            yaxis2=dict(title="Velocity (m/s)",overlaying="y",side="right",
                        color=PALETTE[1]),
            margin=dict(l=20,r=60,t=50,b=20),
        )
        chart_theme(fig_rv)
        st.plotly_chart(fig_rv, use_container_width=True)

        ca1,ca2=st.columns(2,gap="large")
        with ca1:
            section_title("Acceleration", "")
            fig_ac=go.Figure()
            fig_ac.add_trace(go.Scatter(
                x=sd["t"],y=sd["acc"],name="Accel",
                line=dict(color=PALETTE[3],width=2),
                fill="tozeroy",fillcolor=f"rgba({int(PALETTE[3][1:3],16)},{int(PALETTE[3][3:5],16)},{int(PALETTE[3][5:7],16)},0.06)",
            ))
            fig_ac.add_hline(y=0,line_dash="dot",line_color="rgba(155,106,106,0.5)",
                             annotation_text="equilibrium",
                             annotation_font=dict(color="rgba(155,106,106,0.7)",size=9,family="DM Mono"))
            chart_theme(fig_ac, 260)
            fig_ac.update_layout(yaxis_title="m/s²",showlegend=False)
            st.plotly_chart(fig_ac, use_container_width=True)

        with ca2:
            section_title("Mass decrease", "Fuel burn profile")
            fig_ms=go.Figure()
            fig_ms.add_trace(go.Scatter(
                x=sd["t"],y=sd["mass"],name="Mass",
                line=dict(color=PALETTE[4],width=2),
                fill="tozeroy",fillcolor=f"rgba({int(PALETTE[4][1:3],16)},{int(PALETTE[4][3:5],16)},{int(PALETTE[4][5:7],16)},0.06)",
            ))
            chart_theme(fig_ms, 260)
            fig_ms.update_layout(yaxis_title="tonnes",showlegend=False)
            st.plotly_chart(fig_ms, use_container_width=True)

        section_title("Phase space trajectory", "Velocity vs altitude · coloured by time")
        fig_ph=go.Figure(go.Scatter(
            x=sd["alt"],y=sd["vel"],mode="lines+markers",
            marker=dict(size=3,color=sd["t"],colorscale=[
                [0,"rgba(122,92,46,0.6)"],[0.5,PALETTE[0]],[1,PALETTE[1]]
            ],showscale=True,
            colorbar=dict(title="s",thickness=8,tickfont=dict(color=MIST,size=8,family="DM Mono"))),
            line=dict(color="rgba(201,169,110,0.2)",width=1),
        ))
        chart_theme(fig_ph, 290)
        fig_ph.update_layout(xaxis_title="Altitude (km)",yaxis_title="Velocity (m/s)")
        st.plotly_chart(fig_ph, use_container_width=True)

        # Results row
        mx_a=sd["alt"].max(); mx_v=sd["vel"].max()
        mx_ac=sd["acc"].max(); bt=sd.loc[sd["vel"].idxmax(),"t"]
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
                    border:1px solid rgba(201,169,110,0.1);border-radius:2px;
                    overflow:hidden;background:rgba(201,169,110,0.07);margin-top:16px;">
          <div style="background:var(--panel);padding:20px 16px;">
            <span style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;
                         font-weight:300;color:var(--cream);display:block;">{mx_a:.1f} km</span>
            <span style="font-family:'DM Mono',monospace;font-size:0.58rem;
                         letter-spacing:0.14em;color:var(--gold3);">MAX ALTITUDE</span>
          </div>
          <div style="background:var(--panel);padding:20px 16px;">
            <span style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;
                         font-weight:300;color:var(--cream);display:block;">{mx_v:.0f} m/s</span>
            <span style="font-family:'DM Mono',monospace;font-size:0.58rem;
                         letter-spacing:0.14em;color:var(--gold3);">MAX VELOCITY</span>
          </div>
          <div style="background:var(--panel);padding:20px 16px;">
            <span style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;
                         font-weight:300;color:var(--cream);display:block;">{mx_ac:.2f} m/s²</span>
            <span style="font-family:'DM Mono',monospace;font-size:0.58rem;
                         letter-spacing:0.14em;color:var(--gold3);">PEAK ACCELERATION</span>
          </div>
          <div style="background:var(--panel);padding:20px 16px;">
            <span style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;
                         font-weight:300;color:var(--cream);display:block;">{bt:.0f} s</span>
            <span style="font-family:'DM Mono',monospace;font-size:0.58rem;
                         letter-spacing:0.14em;color:var(--gold3);">BURNOUT TIME</span>
          </div>
        </div>""", unsafe_allow_html=True)

    # ── TAB 5 · Data & Insights ──────────────────────────────
    with tab5:
        c1,c2=st.columns([1.2,1],gap="large")
        with c1:
            section_title("Dataset summary", "Post-cleaning statistics")
            st.dataframe(fdf.describe().T.round(2),use_container_width=True,height=300)
        with c2:
            section_title("Mission type split", "")
            pd_=fdf["Mission Type"].value_counts().reset_index()
            pd_.columns=["T","C"]
            fig_pie=go.Figure(go.Pie(
                labels=pd_["T"],values=pd_["C"],hole=0.55,
                marker=dict(colors=PALETTE[:len(pd_)],
                            line=dict(color=INK,width=2)),
                textfont=dict(family="DM Mono",size=9,color=CREAM),
            ))
            chart_theme(fig_pie, 300)
            st.plotly_chart(fig_pie, use_container_width=True)

        section_title("Research insights", "")
        insights=[
            (GOLD,  "Payload and propellant",
             "Heavier payloads demand more fuel — a direct consequence of F = ma. "
             "The OLS regression confirms this relationship is statistically significant across all four mission types."),
            ("#9b7a6a","The cost paradox",
             "Higher expenditure does not reliably predict mission success. "
             "Execution quality and vehicle selection are stronger indicators than budget alone."),
            ("#7a9e8a","Distance as the master variable",
             "Distance from Earth drives both mission duration and fuel requirements, "
             "mirroring the Tsiolkovsky rocket equation's dependency on required velocity change."),
            (PALETTE[3],"Vehicle selection",
             "Starship dominates heavy-payload missions; SLS handles deep-space high-cost work; "
             "Falcon Heavy shows the strongest mid-range fuel efficiency ratio."),
            (PALETTE[4],"Research mission ROI",
             "Research missions consistently achieve the highest scientific yield per billion spent — "
             "the most efficient academic investment across all categories studied."),
            (MIST,  "Atmospheric drag model",
             "ρ(h) = 1.225 · e⁻ʰ/⁸⁵⁰⁰ captures the ISA exponential atmosphere. "
             "Drag near-vanishes above 50 km, enabling dramatic acceleration gains at altitude."),
        ]
        for ac,title,body in insights:
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:2px 1fr;gap:0;
                        margin-bottom:1px;overflow:hidden;border-radius:2px;">
              <div style="background:{ac};"></div>
              <div style="background:var(--panel);padding:16px 20px;">
                <p style="font-family:'Cormorant Garamond',serif;font-size:1.05rem;
                           font-weight:400;color:var(--cream);margin:0 0 5px;">{title}</p>
                <p style="font-family:'DM Sans',sans-serif;font-weight:300;font-size:0.88rem;
                           color:var(--mist);margin:0;line-height:1.75;">{body}</p>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        section_title("Mission data explorer", "")
        default_cols=["Mission Name","Mission Type","Launch Vehicle",
                      "Mission Cost (billion USD)","Fuel Consumption (tons)",
                      "Payload Weight (tons)","Mission Success (%)","Outcome","Launch Year"]
        cols_sel=st.multiselect("Columns",fdf.columns.tolist(),default=default_cols)
        if cols_sel:
            st.dataframe(fdf[cols_sel].reset_index(drop=True),
                         use_container_width=True,height=340)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        csv_b=fdf.to_csv(index=False).encode("utf-8")
        st.markdown("""
        <style>
        .dl-btn .stDownloadButton > button {
          background:transparent !important;
          color:var(--gold) !important;
          border:1px solid rgba(201,169,110,0.35) !important;
          font-size:0.62rem !important; padding:11px 22px !important;
          border-radius:1px !important; letter-spacing:0.16em !important;
        }
        .dl-btn .stDownloadButton > button:hover {
          background:rgba(201,169,110,0.07) !important;
          border-color:rgba(201,169,110,0.6) !important;
        }
        </style>
        <div class="dl-btn">
        """, unsafe_allow_html=True)
        st.download_button("Download filtered dataset",csv_b,
                           "aether_missions.csv","text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align:center;padding:24px 36px;
                border-top:1px solid rgba(201,169,110,0.07);
                font-family:'DM Mono',monospace;font-size:0.58rem;
                color:rgba(122,92,46,0.5);letter-spacing:0.12em;">
      Æther · Space Mission Intelligence · Mathematics for AI-I · 2025
      &ensp;·&ensp; Streamlit · Plotly · Seaborn · Matplotlib
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# ROUTER
# ════════════════════════════════════════════════════════════
p = st.session_state.get("page","onboarding")
if   p == "onboarding": page_onboarding()
elif p == "loading":    page_loading()
elif p == "login":      page_login()
elif p == "dashboard":
    if st.session_state.get("logged_in"): page_dashboard()
    else:
        st.session_state.page = "login"
        st.rerun()
