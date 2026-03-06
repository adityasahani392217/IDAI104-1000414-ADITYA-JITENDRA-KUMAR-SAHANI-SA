# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  Æther — Space Mission Intelligence                                      ║
# ║  Enhanced edition: Google Drive data, full animations,                  ║
# ║  onboarding sequence, terms agreement, animated login                   ║
# ╚══════════════════════════════════════════════════════════════════════════╝

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
import os
import io

st.set_page_config(
    page_title="Æther — Space Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── session defaults ────────────────────────────────────────────────────────
DEFAULTS = {
    "page": "onboarding",
    "logged_in": False,
    "username": "",
    "login_error": "",
    "terms_accepted": False,
    "onboard_step": 0,
    "data": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=DM+Mono:ital,wght@0,300;0,400;1,300&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --ink:   #08090d;
  --deep:  #0b0e16;
  --panel: #101420;
  --lift:  #161c2a;
  --gold:  #c9a96e;
  --gold2: #e8c98a;
  --gold3: #7a5c2e;
  --cream: #e0d3bb;
  --mist:  #7a7060;
  --dim:   #302e28;
  --wire:  rgba(201,169,110,0.13);
  --glow:  rgba(201,169,110,0.07);
  --red:   #9b5a5a;
  --green: #5a9b6e;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
  background: var(--ink);
  font-family: 'DM Sans', sans-serif;
  color: var(--cream);
  min-height: 100vh;
}

/* Grain overlay */
.stApp::after {
  content: '';
  position: fixed; inset: 0; z-index: 9999;
  pointer-events: none;
  opacity: 0.022;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 160px 160px;
}

/* Star-field canvas (injected) */
#star-canvas {
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
}

.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* Hide default Streamlit decorations */
header[data-testid="stHeader"] { display: none !important; }
.stDeployButton { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }

/* Streamlit button base */
.stButton > button {
  font-family: 'DM Mono', monospace !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  transition: all 0.3s ease !important;
  border-radius: 2px !important;
}

/* Inputs */
.stTextInput input, .stTextInput textarea {
  background: rgba(11,14,22,0.95) !important;
  border: 1px solid var(--dim) !important;
  border-radius: 2px !important;
  color: var(--cream) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.84rem !important;
  padding: 12px 16px !important;
  transition: border-color 0.3s, box-shadow 0.3s !important;
}
.stTextInput input:focus {
  border-color: rgba(201,169,110,0.45) !important;
  box-shadow: 0 0 0 1px rgba(201,169,110,0.15) !important;
  outline: none !important;
}
.stTextInput input::placeholder { color: rgba(58,56,48,0.8) !important; }

/* Checkbox */
.stCheckbox > label {
  font-family: 'DM Mono', monospace !important;
  font-size: 0.7rem !important;
  letter-spacing: 0.06em !important;
  color: var(--mist) !important;
}
.stCheckbox > label:hover { color: var(--cream) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb { background: var(--gold3); border-radius: 2px; }

/* Multiselect */
[data-baseweb="tag"] {
  background: rgba(201,169,110,0.10) !important;
  border: 1px solid var(--gold3) !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] [role="slider"] {
  background: var(--gold) !important;
  border-color: var(--gold) !important;
}

/* ── Keyframe library ── */
@keyframes fade-up   { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
@keyframes fade-in   { from { opacity:0; } to { opacity:1; } }
@keyframes spin      { to { transform:rotate(360deg); } }
@keyframes pulse-ring { 0%,100%{ opacity:0.15; transform:scale(1); } 50%{ opacity:0.35; transform:scale(1.04); } }
@keyframes shimmer   { 0%{background-position:-400px 0} 100%{background-position:400px 0} }
@keyframes draw-line { from{width:0} to{width:100%} }
@keyframes float-up  { 0%{transform:translateY(0)} 50%{transform:translateY(-8px)} 100%{transform:translateY(0)} }
@keyframes flicker   { 0%,100%{opacity:1} 92%{opacity:1} 93%{opacity:0.4} 94%{opacity:1} 97%{opacity:0.6} 98%{opacity:1} }
@keyframes data-stream {
  0%  { transform: translateY(0);   opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100%{ transform: translateY(-60px); opacity: 0; }
}
@keyframes comet {
  0%   { transform: translateX(-200px) translateY(0); opacity: 0; }
  10%  { opacity: 1; }
  90%  { opacity: 0.6; }
  100% { transform: translateX(110vw) translateY(-80px); opacity: 0; }
}
@keyframes planet-orbit { from{ transform:rotate(0deg) translateX(var(--r)) rotate(0deg); } to{ transform:rotate(360deg) translateX(var(--r)) rotate(-360deg); } }
@keyframes nebula-drift { 0%,100%{transform:scale(1) translate(0,0)} 50%{transform:scale(1.06) translate(12px,-8px)} }
@keyframes terminal-blink { 0%,100%{opacity:1} 50%{opacity:0} }
@keyframes progress-fill { from{width:0%} to{width:100%} }
@keyframes scan-line { 0%{top:-4%} 100%{top:104%} }
@keyframes glow-pulse { 0%,100%{ box-shadow:0 0 20px rgba(201,169,110,0.15); } 50%{ box-shadow:0 0 40px rgba(201,169,110,0.35); } }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STAR CANVAS JS + COMETS
# ══════════════════════════════════════════════════════════════════════════════
STARFIELD_JS = """
<canvas id="star-canvas"></canvas>
<script>
(function(){
  const c = document.getElementById('star-canvas');
  if(!c) return;
  const ctx = c.getContext('2d');
  let W, H, stars = [];

  function resize(){
    W = c.width  = window.innerWidth;
    H = c.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  // Generate stars with twinkling params
  function makeStars(n){
    stars = [];
    for(let i=0;i<n;i++){
      stars.push({
        x: Math.random()*W,
        y: Math.random()*H,
        r: Math.random()*1.1+0.15,
        a: Math.random(),
        da: (Math.random()-0.5)*0.004,
        hue: Math.random()<0.08 ? 35 : (Math.random()<0.05 ? 200 : 0),
        sat: Math.random()<0.13 ? 60 : 0,
      });
    }
  }
  makeStars(340);

  // Shooting stars
  let comets = [];
  function spawnComet(){
    comets.push({
      x: Math.random()*W*0.5,
      y: Math.random()*H*0.4,
      vx: 3+Math.random()*5,
      vy: 0.8+Math.random()*2,
      len: 80+Math.random()*120,
      life: 1,
    });
  }
  setInterval(spawnComet, 4500);

  function draw(){
    ctx.clearRect(0,0,W,H);

    // Stars
    stars.forEach(s=>{
      s.a += s.da;
      if(s.a > 1 || s.a < 0.05) s.da *= -1;
      s.a = Math.max(0.05, Math.min(1, s.a));
      const color = s.sat>0
        ? `hsla(${s.hue},${s.sat}%,80%,${s.a})`
        : `rgba(220,210,190,${s.a*0.75})`;
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI*2);
      ctx.fillStyle = color;
      ctx.fill();
    });

    // Comets
    comets = comets.filter(cm=>{
      cm.x += cm.vx; cm.y += cm.vy; cm.life -= 0.012;
      if(cm.life <= 0) return false;
      const grd = ctx.createLinearGradient(cm.x-cm.len,cm.y-cm.len*0.3,cm.x,cm.y);
      grd.addColorStop(0,'rgba(201,169,110,0)');
      grd.addColorStop(1,`rgba(230,200,140,${cm.life*0.7})`);
      ctx.beginPath();
      ctx.moveTo(cm.x-cm.len, cm.y-cm.len*0.3);
      ctx.lineTo(cm.x, cm.y);
      ctx.strokeStyle = grd;
      ctx.lineWidth = 1.2;
      ctx.stroke();
      // Head glow
      ctx.beginPath();
      ctx.arc(cm.x, cm.y, 1.5, 0, Math.PI*2);
      ctx.fillStyle = `rgba(240,220,160,${cm.life})`;
      ctx.fill();
      return true;
    });

    requestAnimationFrame(draw);
  }
  draw();
})();
</script>
"""


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING  — Google Drive → local cache
# ══════════════════════════════════════════════════════════════════════════════
GDRIVE_ID  = "1V3E0wDWHC2Xh2o_Pb8hHLtNurPAfGMlK"
CACHE_PATH = "space_missions_cached.csv"

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Load dataset.
    Priority: 1) pre-cached CSV  2) Google Drive via gdown  3) local fallback
    """
    # 1. Already cached locally
    if os.path.exists(CACHE_PATH):
        df = pd.read_csv(CACHE_PATH)
        return _clean(df)

    # 2. Try Google Drive download
    try:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown", "-q"])
        import gdown
        url = f"https://drive.google.com/uc?id={GDRIVE_ID}"
        gdown.download(url, CACHE_PATH, quiet=True)
        df = pd.read_csv(CACHE_PATH)
        return _clean(df)
    except Exception:
        pass

    # 3. Fallback — generate synthetic data so app still runs
    return _synthetic()


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Launch Date"]  = pd.to_datetime(df.get("Launch Date",""), errors="coerce")
    df["Launch Year"]  = df["Launch Date"].dt.year
    df["Launch Month"] = df["Launch Date"].dt.month
    nums = [
        "Distance from Earth (light-years)", "Mission Duration (years)",
        "Mission Cost (billion USD)", "Scientific Yield (points)", "Crew Size",
        "Mission Success (%)", "Fuel Consumption (tons)", "Payload Weight (tons)"
    ]
    for c in nums:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df.drop_duplicates(inplace=True)
    df.dropna(subset=[c for c in nums if c in df.columns], inplace=True)
    df.reset_index(drop=True, inplace=True)
    if "Mission Success (%)" in df.columns:
        df["Outcome"] = df["Mission Success (%)"].apply(
            lambda x: "Successful" if x >= 90 else ("Partial" if x >= 70 else "Failed"))
    if "Payload Weight (tons)" in df.columns and "Fuel Consumption (tons)" in df.columns:
        df["Fuel Efficiency"] = df["Payload Weight (tons)"] / \
                                 df["Fuel Consumption (tons)"].replace(0, np.nan)
    if "Mission Cost (billion USD)" in df.columns and "Mission Duration (years)" in df.columns:
        df["Cost per Year"] = df["Mission Cost (billion USD)"] / \
                               df["Mission Duration (years)"].replace(0, np.nan)
    return df


def _synthetic() -> pd.DataFrame:
    """Minimal synthetic dataset used only if Drive download fails."""
    rng = np.random.default_rng(42)
    n = 500
    types = ["Research", "Commercial", "Defense", "Exploration"]
    vehs  = ["Falcon Heavy", "SLS", "Starship", "Ariane 6"]
    weather = ["Clear", "Cloudy", "Stormy", "Windy"]
    rows = []
    for i in range(n):
        mt = types[i % 4]; veh = vehs[i % 4]
        cost = float(rng.uniform(0.5, 40))
        dur  = float(rng.uniform(0.1, 12))
        dist = float(rng.uniform(0.001, 80))
        fuel = float(rng.uniform(50, 800))
        pw   = float(rng.uniform(1, 120))
        crew = int(rng.integers(0, 12))
        succ = float(rng.uniform(55, 100))
        yield_ = float(rng.uniform(10, 500))
        yr = int(rng.integers(2000, 2025))
        rows.append({
            "Mission Name": f"Mission-{i+1:04d}",
            "Mission Type": mt,
            "Launch Vehicle": veh,
            "Launch Date": f"{yr}-{rng.integers(1,13):02d}-{rng.integers(1,28):02d}",
            "Distance from Earth (light-years)": dist,
            "Mission Duration (years)": dur,
            "Mission Cost (billion USD)": cost,
            "Scientific Yield (points)": yield_,
            "Crew Size": crew,
            "Mission Success (%)": succ,
            "Fuel Consumption (tons)": fuel,
            "Payload Weight (tons)": pw,
            "Weather Condition": weather[i % 4],
        })
    return _clean(pd.DataFrame(rows))


# ══════════════════════════════════════════════════════════════════════════════
# CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════
PAL = ["#c9a96e","#7a9e8a","#9b7a6a","#6a8a9b","#a08a6a","#7a6a9b","#8a9b7a","#9b8a7a"]
INK, PANEL, GOLD, CREAM, MIST = "#08090d","#101420","#c9a96e","#e0d3bb","#7a7060"
OUT_CLR = {"Successful":"#5a9b6e","Partial":"#c9a96e","Failed":"#9b5a5a"}

def chart_theme(fig, h=None):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=PANEL,
        font=dict(family="DM Sans", color=MIST, size=11),
        title_font=dict(family="Cormorant Garamond, serif", color=CREAM, size=15),
        margin=dict(l=20,r=20,t=50,b=20),
        legend=dict(bgcolor="rgba(11,14,22,0.7)",bordercolor="rgba(201,169,110,0.14)",
                    borderwidth=1,font=dict(family="DM Mono",size=10,color=MIST)),
    )
    if h: fig.update_layout(height=h)
    for ax in ("xaxis","yaxis"):
        fig.update_layout(**{ax: dict(
            gridcolor="rgba(201,169,110,0.055)", linecolor="rgba(201,169,110,0.10)",
            tickfont=dict(color=MIST,family="DM Mono"),
            title_font=dict(color=MIST), zeroline=False)})
    return fig

def trendline(fig, xv, yv, color=GOLD):
    m2 = ~(np.isnan(xv)|np.isnan(yv))
    x,y = xv[m2], yv[m2]
    if len(x)<2: return fig
    m,b = np.polyfit(x,y,1)
    xl = np.linspace(x.min(),x.max(),200)
    fig.add_trace(go.Scatter(x=xl,y=m*xl+b,mode="lines",
        line=dict(color=color,width=1.3,dash="dot"),opacity=0.5,showlegend=False))
    return fig

def note_card(text, accent=GOLD):
    st.markdown(f"""
    <div style="border-left:2px solid {accent};padding:14px 20px;margin:16px 0 8px;
                background:rgba(201,169,110,0.025);border-radius:0 4px 4px 0;">
      <p style="font-family:'DM Sans',sans-serif;font-size:0.88rem;
                color:{MIST};line-height:1.8;margin:0;">{text}</p>
    </div>""", unsafe_allow_html=True)

def section_title(text, sub=""):
    st.markdown(f"""
    <div style="margin:28px 0 16px;">
      <p style="font-family:'Cormorant Garamond',serif;font-size:1.55rem;
                font-weight:400;color:{CREAM};letter-spacing:0.02em;
                line-height:1.2;margin-bottom:4px;">{text}</p>
      {"" if not sub else f'<p style="font-family:DM Mono,monospace;font-size:0.66rem;color:{MIST};letter-spacing:0.1em;margin:0;text-transform:uppercase;">{sub}</p>'}
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — ONBOARDING  (3-step animated sequence)
# ══════════════════════════════════════════════════════════════════════════════
def page_onboarding():
    step = st.session_state.onboard_step   # 0 = splash, 1 = intro, 2 = data reveal

    st.markdown(STARFIELD_JS, unsafe_allow_html=True)

    if step == 0:
        # ── Step 0: Animated splash / title card ─────────────────────────────
        st.markdown("""
        <style>
        /* Nebula blobs */
        .nebula {
          position:fixed; border-radius:50%; pointer-events:none; z-index:2;
          filter:blur(80px); animation:nebula-drift 18s ease-in-out infinite;
        }
        .nb1 { width:420px;height:420px;background:radial-gradient(circle,rgba(120,80,30,0.09),transparent 70%);
               top:-80px;right:-100px;animation-delay:0s; }
        .nb2 { width:320px;height:320px;background:radial-gradient(circle,rgba(40,60,100,0.07),transparent 70%);
               bottom:10%;left:-60px;animation-delay:-7s; }
        .nb3 { width:260px;height:260px;background:radial-gradient(circle,rgba(80,120,90,0.06),transparent 70%);
               bottom:30%;right:15%;animation-delay:-13s; }

        /* Orrery */
        .orrery { position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
                   z-index:2;pointer-events:none;width:0;height:0; }
        .o-ring { position:absolute;border-radius:50%;border:1px solid rgba(201,169,110,0.1);
                   transform:translate(-50%,-50%); }
        .o-ring:nth-child(1){width:280px;height:280px;animation:spin 36s linear infinite;}
        .o-ring:nth-child(2){width:460px;height:460px;animation:spin 58s linear infinite reverse;border-color:rgba(201,169,110,0.07);}
        .o-ring:nth-child(3){width:660px;height:660px;animation:spin 90s linear infinite;border-color:rgba(201,169,110,0.045);}
        .o-ring:nth-child(4){width:900px;height:900px;animation:spin 144s linear infinite reverse;border-color:rgba(201,169,110,0.025);}
        .o-planet {
          position:absolute;top:0;left:50%;
          transform-origin: 0 50%;
          width:10px;height:10px;border-radius:50%;
          margin-left:-5px;margin-top:-5px;
        }
        /* Sun */
        .o-sun {
          position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
          width:56px;height:56px;border-radius:50%;z-index:3;pointer-events:none;
          background:radial-gradient(circle at 38% 38%,#fdf0d0 0%,#e8c060 35%,#9a5c18 70%,transparent 90%);
          box-shadow:0 0 50px 15px rgba(201,160,50,0.18),0 0 100px 40px rgba(180,100,20,0.09);
          animation:float-up 6s ease-in-out infinite;
        }

        /* Main copy */
        .ob-wrap {
          position:relative;z-index:10;
          min-height:100vh;display:flex;flex-direction:column;
          align-items:center;justify-content:center;
          text-align:center;padding:80px 24px 60px;
          gap:0;
        }
        .ob-eyebrow {
          font-family:'DM Mono',monospace;font-size:0.6rem;
          letter-spacing:0.22em;color:var(--gold3);text-transform:uppercase;
          margin-bottom:28px;animation:fade-up 1s ease both;
        }
        .ob-title {
          font-family:'Cormorant Garamond',serif;
          font-size:clamp(4.5rem,12vw,9rem);font-weight:300;font-style:italic;
          color:var(--cream);line-height:0.88;letter-spacing:-0.01em;
          margin:0 0 10px;animation:fade-up 1.1s ease 0.15s both;
        }
        .ob-title em{color:var(--gold);font-style:normal;}
        .ob-rule{width:52px;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);
                  margin:22px auto;animation:fade-up 1s ease 0.3s both;}
        .ob-sub{font-family:'DM Mono',monospace;font-size:0.68rem;letter-spacing:0.16em;
                 color:var(--mist);margin-bottom:24px;animation:fade-up 1s ease 0.4s both;}
        .ob-body{font-family:'DM Sans',sans-serif;font-weight:300;font-size:0.98rem;
                  color:rgba(122,112,96,0.85);max-width:440px;line-height:1.95;
                  margin:0 auto 48px;animation:fade-up 1s ease 0.55s both;}
        .ob-stats{display:flex;gap:56px;justify-content:center;margin-bottom:52px;
                   animation:fade-up 1s ease 0.7s both;}
        .ob-stat-v{font-family:'Cormorant Garamond',serif;font-weight:300;
                    font-size:2.5rem;color:var(--gold);display:block;letter-spacing:-0.02em;}
        .ob-stat-l{font-family:'DM Mono',monospace;font-size:0.58rem;letter-spacing:0.16em;
                    color:var(--gold3);text-transform:uppercase;margin-top:2px;display:block;}
        .ob-cta{animation:fade-up 1s ease 0.9s both;position:relative;z-index:20;}

        /* CTA button wrapper override */
        .cta-btn .stButton>button {
          background:transparent !important;
          color:var(--gold) !important;
          border:1px solid rgba(201,169,110,0.40) !important;
          font-size:0.63rem !important;font-weight:400 !important;
          padding:15px 48px !important;letter-spacing:0.2em !important;
          border-radius:1px !important;
          animation:glow-pulse 3s ease-in-out infinite;
        }
        .cta-btn .stButton>button:hover {
          background:rgba(201,169,110,0.07) !important;
          border-color:rgba(201,169,110,0.7) !important;color:#e8c98a !important;
        }
        </style>

        <div class="nebula nb1"></div>
        <div class="nebula nb2"></div>
        <div class="nebula nb3"></div>
        <div class="orrery">
          <div class="o-ring"></div>
          <div class="o-ring"></div>
          <div class="o-ring"></div>
          <div class="o-ring"></div>
        </div>
        <div class="o-sun"></div>

        <div class="ob-wrap">
          <p class="ob-eyebrow">Mathematics for AI · Summative Assessment · 2025</p>
          <h1 class="ob-title"><em>Æ</em>ther</h1>
          <div class="ob-rule"></div>
          <p class="ob-sub">Space Mission Intelligence Platform</p>
          <p class="ob-body">
            Five hundred missions. Four launch vehicles. Decades of orbital history.
            Explore the physics, economics, and outcomes of humanity's reach into the cosmos.
          </p>
          <div class="ob-stats">
            <div><span class="ob-stat-v">500</span><span class="ob-stat-l">Missions</span></div>
            <div><span class="ob-stat-v">4</span><span class="ob-stat-l">Vehicles</span></div>
            <div><span class="ob-stat-v">15</span><span class="ob-stat-l">Variables</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        _, mc, _ = st.columns([2.2, 1.2, 2.2])
        with mc:
            st.markdown('<div class="cta-btn" style="margin-top:-200px;position:relative;z-index:20;">', unsafe_allow_html=True)
            if st.button("Enter the Observatory", key="ob0"):
                st.session_state.onboard_step = 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif step == 1:
        # ── Step 1: Mission data teaser with stream animation ─────────────────
        st.markdown("""
        <style>
        .teaser-wrap {
          min-height:100vh;display:flex;flex-direction:column;
          align-items:center;justify-content:center;
          padding:60px 24px;position:relative;z-index:10;
          text-align:center;
        }
        .teaser-heading {
          font-family:'Cormorant Garamond',serif;font-size:clamp(2rem,5vw,3.4rem);
          font-weight:300;color:var(--cream);line-height:1.25;
          max-width:680px;margin:0 auto 16px;
          animation:fade-up 0.9s ease both;
        }
        .teaser-sub {
          font-family:'DM Mono',monospace;font-size:0.68rem;letter-spacing:0.14em;
          color:var(--gold3);text-transform:uppercase;
          margin-bottom:48px;animation:fade-up 0.9s ease 0.15s both;
        }
        /* Animated data stream cards */
        .stream-grid {
          display:grid;grid-template-columns:repeat(3,1fr);
          gap:1px;max-width:780px;width:100%;
          border:1px solid rgba(201,169,110,0.1);border-radius:3px;overflow:hidden;
          background:rgba(201,169,110,0.06);margin-bottom:48px;
          animation:fade-up 0.9s ease 0.3s both;
        }
        .stream-cell {
          background:var(--panel);padding:22px 18px;text-align:left;
          position:relative;overflow:hidden;
        }
        /* Shimmer effect on each cell */
        .stream-cell::before {
          content:'';position:absolute;inset:0;
          background:linear-gradient(90deg,transparent,rgba(201,169,110,0.04),transparent);
          background-size:400px 100%;animation:shimmer 3s linear infinite;
          animation-delay:var(--d,0s);
        }
        .sc-label{font-family:'DM Mono',monospace;font-size:0.58rem;
                   letter-spacing:0.14em;color:var(--gold3);text-transform:uppercase;
                   margin-bottom:8px;}
        .sc-val{font-family:'Cormorant Garamond',serif;font-size:1.8rem;
                 font-weight:300;color:var(--cream);}
        .sc-unit{font-family:'DM Mono',monospace;font-size:0.58rem;
                  color:var(--mist);margin-top:3px;}

        /* Scan line overlay */
        .stream-grid::after {
          content:'';position:absolute;left:0;right:0;height:2px;
          background:linear-gradient(90deg,transparent,rgba(201,169,110,0.15),transparent);
          animation:scan-line 4s linear infinite;pointer-events:none;
        }
        .stream-grid { position:relative; }

        .features-row {
          display:flex;gap:32px;max-width:780px;width:100%;
          animation:fade-up 0.9s ease 0.5s both;margin-bottom:48px;
          flex-wrap:wrap;justify-content:center;
        }
        .feat-chip {
          font-family:'DM Mono',monospace;font-size:0.62rem;
          letter-spacing:0.12em;color:var(--mist);
          border:1px solid rgba(201,169,110,0.12);
          padding:8px 16px;border-radius:2px;
          background:rgba(201,169,110,0.025);
        }
        .feat-chip span{color:var(--gold3);margin-right:6px;}

        .nav-row{display:flex;gap:12px;justify-content:center;
                  animation:fade-up 0.9s ease 0.65s both;}
        .btn-back .stButton>button{
          background:transparent !important;color:var(--mist) !important;
          border:1px solid rgba(138,112,96,0.2) !important;
          font-size:0.6rem !important;padding:12px 28px !important;
          letter-spacing:0.16em !important;border-radius:1px !important;
        }
        .btn-back .stButton>button:hover{border-color:rgba(138,112,96,0.45)!important;color:var(--cream)!important;}
        .btn-next .stButton>button{
          background:rgba(201,169,110,0.08) !important;color:var(--gold) !important;
          border:1px solid rgba(201,169,110,0.38) !important;
          font-size:0.6rem !important;padding:12px 28px !important;
          letter-spacing:0.16em !important;border-radius:1px !important;
        }
        .btn-next .stButton>button:hover{background:rgba(201,169,110,0.14)!important;border-color:rgba(201,169,110,0.65)!important;}
        </style>

        <div class="teaser-wrap">
          <h2 class="teaser-heading">The universe mapped in data.<br>One observatory for all of it.</h2>
          <p class="teaser-sub">What awaits inside</p>

          <div class="stream-grid">
            <div class="stream-cell" style="--d:0s">
              <p class="sc-label">Orbital Cartography</p>
              <p class="sc-val">500</p>
              <p class="sc-unit">missions plotted in solar reference</p>
            </div>
            <div class="stream-cell" style="--d:0.4s">
              <p class="sc-label">Physics Engine</p>
              <p class="sc-val">∫ a dt</p>
              <p class="sc-unit">euler-integrated launch simulation</p>
            </div>
            <div class="stream-cell" style="--d:0.8s">
              <p class="sc-label">Fuel Analysis</p>
              <p class="sc-val">F = ma</p>
              <p class="sc-unit">payload ÷ propellant regression</p>
            </div>
            <div class="stream-cell" style="--d:1.2s">
              <p class="sc-label">Cost Intelligence</p>
              <p class="sc-val">$B USD</p>
              <p class="sc-unit">outcome vs expenditure mapping</p>
            </div>
            <div class="stream-cell" style="--d:1.6s">
              <p class="sc-label">Correlation Matrix</p>
              <p class="sc-val">8 × 8</p>
              <p class="sc-unit">pearson heatmap · all variables</p>
            </div>
            <div class="stream-cell" style="--d:2.0s">
              <p class="sc-label">Mission Explorer</p>
              <p class="sc-val">↓ CSV</p>
              <p class="sc-unit">filtered export · dynamic table</p>
            </div>
          </div>

          <div class="features-row">
            <div class="feat-chip"><span>✦</span>Real-time filters</div>
            <div class="feat-chip"><span>✦</span>Interactive sliders</div>
            <div class="feat-chip"><span>✦</span>Phase space charts</div>
            <div class="feat-chip"><span>✦</span>Sunburst breakdown</div>
            <div class="feat-chip"><span>✦</span>Dark editorial theme</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        _, lc, rc, _ = st.columns([2, 1, 1, 2])
        with lc:
            st.markdown('<div class="btn-back" style="margin-top:-120px;position:relative;z-index:20;">', unsafe_allow_html=True)
            if st.button("← Back", key="ob1_back"):
                st.session_state.onboard_step = 0
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with rc:
            st.markdown('<div class="btn-next" style="margin-top:-120px;position:relative;z-index:20;">', unsafe_allow_html=True)
            if st.button("Continue →", key="ob1_next"):
                st.session_state.onboard_step = 2
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif step == 2:
        # ── Step 2: Terms of Entry ─────────────────────────────────────────────
        st.markdown("""
        <style>
        .terms-wrap {
          min-height:100vh;display:flex;align-items:center;justify-content:center;
          padding:60px 24px;position:relative;z-index:10;
        }
        .terms-card {
          background:var(--panel);border:1px solid rgba(201,169,110,0.10);
          border-radius:3px;max-width:600px;width:100%;
          padding:52px 56px 44px;position:relative;overflow:hidden;
          animation:fade-up 0.8s ease both;
        }
        .terms-card::before{content:'';position:absolute;top:0;left:0;width:56px;height:1px;background:var(--gold);}
        .terms-card::after {content:'';position:absolute;top:0;left:0;width:1px;height:56px;background:var(--gold);}

        /* Bottom right corner accent */
        .terms-corner-br {
          position:absolute;bottom:0;right:0;
          width:32px;height:1px;background:rgba(201,169,110,0.3);
        }
        .terms-corner-br::after{
          content:'';position:absolute;right:0;bottom:0;
          width:1px;height:32px;background:rgba(201,169,110,0.3);
        }

        .terms-eyebrow{font-family:'DM Mono',monospace;font-size:0.6rem;
                        letter-spacing:0.2em;color:var(--gold3);text-transform:uppercase;margin-bottom:16px;}
        .terms-title{font-family:'Cormorant Garamond',serif;font-size:2.1rem;
                      font-weight:300;color:var(--cream);margin-bottom:24px;letter-spacing:0.02em;}
        .terms-rule{height:1px;background:rgba(201,169,110,0.10);margin-bottom:24px;}
        .terms-body{font-family:'DM Sans',sans-serif;font-weight:300;font-size:0.86rem;
                     color:var(--mist);line-height:1.9;margin-bottom:28px;}
        .terms-list{margin:0 0 28px;padding:0;list-style:none;}
        .terms-list li{
          font-family:'DM Mono',monospace;font-size:0.68rem;
          color:var(--mist);letter-spacing:0.04em;
          padding:9px 0 9px 20px;border-bottom:1px solid rgba(201,169,110,0.05);
          position:relative;line-height:1.6;
        }
        .terms-list li::before{
          content:'—';position:absolute;left:0;color:var(--gold3);
        }
        .terms-check{margin:24px 0 28px;}
        .terms-btns{display:flex;gap:12px;}
        .terms-accept .stButton>button{
          background:rgba(201,169,110,0.10)!important;color:var(--gold)!important;
          border:1px solid rgba(201,169,110,0.40)!important;
          font-size:0.62rem!important;padding:13px 28px!important;
          letter-spacing:0.18em!important;border-radius:1px!important;flex:1;
        }
        .terms-accept .stButton>button:hover{background:rgba(201,169,110,0.18)!important;border-color:rgba(201,169,110,0.65)!important;}
        .terms-decline .stButton>button{
          background:transparent!important;color:var(--mist)!important;
          border:1px solid rgba(138,112,96,0.18)!important;
          font-size:0.62rem!important;padding:13px 28px!important;
          letter-spacing:0.18em!important;border-radius:1px!important;
        }
        .terms-decline .stButton>button:hover{border-color:rgba(138,112,96,0.4)!important;color:var(--cream)!important;}
        </style>

        <div class="terms-wrap">
          <div class="terms-card">
            <div class="terms-corner-br"></div>
            <p class="terms-eyebrow">Step 3 of 3 · Access Agreement</p>
            <h2 class="terms-title">Terms of Entry</h2>
            <div class="terms-rule"></div>
            <p class="terms-body">
              Before entering the Æther Observatory, please review and accept the
              conditions of access. This platform contains mission-classified data
              compiled from public space agency archives for academic research purposes.
            </p>
            <ul class="terms-list">
              <li>Data is provided for educational and research use only.</li>
              <li>Mission records may not be redistributed without attribution.</li>
              <li>Simulation results are approximations, not certified flight data.</li>
              <li>All analysis conclusions remain the responsibility of the analyst.</li>
              <li>Session data is not stored beyond your active browser window.</li>
            </ul>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # checkbox + buttons rendered outside the HTML card
        _, mc, _ = st.columns([1.4, 2.2, 1.4])
        with mc:
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            accepted = st.checkbox(
                "I have read and agree to the Terms of Entry",
                key="terms_chk"
            )
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            lc2, rc2 = st.columns(2, gap="small")
            with lc2:
                st.markdown('<div class="terms-decline">', unsafe_allow_html=True)
                if st.button("← Back", key="terms_back"):
                    st.session_state.onboard_step = 1
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with rc2:
                st.markdown('<div class="terms-accept">', unsafe_allow_html=True)
                if st.button("Accept & Enter", key="terms_accept"):
                    if accepted:
                        st.session_state.terms_accepted = True
                        st.session_state.page = "loading"
                        st.rerun()
                    else:
                        st.error("Please accept the Terms of Entry to continue.")
                st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — LOADING  (animated terminal + progress bar)
# ══════════════════════════════════════════════════════════════════════════════
def page_loading():
    # Trigger data load during loading screen
    with st.spinner(""):
        _ = load_data()

    steps = [
        ( 5, "Establishing uplink"),
        (14, "Authenticating mission archives"),
        (26, "Fetching Black Friday dataset"),
        (38, "Parsing 500 flight logs"),
        (52, "Calibrating physics engine"),
        (65, "Rendering orbital reference"),
        (78, "Compiling visualisation modules"),
        (89, "Running integrity checks"),
        (100,"Observatory ready"),
    ]
    ph = st.empty()
    for pct, msg in steps:
        with ph.container():
            st.markdown(f"""
            <style>
            .ld-outer{{display:flex;flex-direction:column;align-items:center;
                        justify-content:center;min-height:100vh;gap:0;
                        position:relative;z-index:10;}}

            /* Terminal window */
            .ld-terminal{{
              width:460px;background:rgba(8,9,13,0.95);
              border:1px solid rgba(201,169,110,0.14);border-radius:4px;
              overflow:hidden;margin-bottom:40px;
              box-shadow:0 24px 64px rgba(0,0,0,0.6);
            }}
            .ld-term-bar{{
              display:flex;align-items:center;gap:8px;
              padding:10px 16px;background:rgba(16,20,32,0.95);
              border-bottom:1px solid rgba(201,169,110,0.08);
            }}
            .term-dot{{width:10px;height:10px;border-radius:50%;}}
            .term-dot-r{{background:rgba(155,90,90,0.7);}}
            .term-dot-y{{background:rgba(201,169,110,0.5);}}
            .term-dot-g{{background:rgba(90,155,110,0.6);}}
            .term-title{{font-family:'DM Mono',monospace;font-size:0.6rem;
                          letter-spacing:0.1em;color:rgba(122,112,96,0.6);margin-left:auto;margin-right:auto;}}
            .ld-term-body{{padding:22px 24px 24px;min-height:140px;}}
            .term-line{{font-family:'DM Mono',monospace;font-size:0.7rem;
                         color:rgba(122,112,96,0.55);letter-spacing:0.04em;
                         line-height:1.9;display:block;}}
            .term-active{{color:var(--gold3)!important;}}
            .term-done{{color:rgba(90,155,110,0.7)!important;}}
            .term-cursor{{display:inline-block;width:7px;height:12px;
                           background:var(--gold);vertical-align:middle;margin-left:4px;
                           animation:terminal-blink 1s step-end infinite;}}

            /* Progress */
            .ld-progress-wrap{{width:460px;margin-bottom:20px;}}
            .ld-prog-header{{display:flex;justify-content:space-between;
                              font-family:'DM Mono',monospace;font-size:0.6rem;
                              letter-spacing:0.1em;color:var(--gold3);margin-bottom:8px;}}
            .ld-prog-track{{height:1px;background:rgba(201,169,110,0.1);border-radius:1px;overflow:hidden;}}
            .ld-prog-fill{{height:1px;background:linear-gradient(90deg,var(--gold3),var(--gold));
                            border-radius:1px;width:{pct}%;transition:width 0.4s ease;}}

            /* Logo */
            .ld-logo{{font-family:'Cormorant Garamond',serif;font-style:italic;
                       font-size:2rem;font-weight:300;color:var(--cream);
                       letter-spacing:0.05em;margin-bottom:36px;
                       animation:flicker 8s ease-in-out infinite;}}
            .ld-logo em{{color:var(--gold);font-style:normal;}}
            </style>

            <div class="ld-outer">
              <p class="ld-logo"><em>Æ</em>ther</p>

              <div class="ld-terminal">
                <div class="ld-term-bar">
                  <div class="term-dot term-dot-r"></div>
                  <div class="term-dot term-dot-y"></div>
                  <div class="term-dot term-dot-g"></div>
                  <span class="term-title">aether — mission_control</span>
                </div>
                <div class="ld-term-body">
                  {''.join([
                      f'<span class="term-line term-done">✓  {m}</span>'
                      for _, m in steps[:max(0, steps.index((pct, msg)))]
                  ])}
                  <span class="term-line term-active">
                    ›  {msg}<span class="term-cursor"></span>
                  </span>
                </div>
              </div>

              <div class="ld-progress-wrap">
                <div class="ld-prog-header">
                  <span>Loading mission data</span>
                  <span>{pct}%</span>
                </div>
                <div class="ld-prog-track"><div class="ld-prog-fill"></div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.33)

    st.session_state.page = "login"
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — LOGIN  (animated card with field-by-field reveal)
# ══════════════════════════════════════════════════════════════════════════════
def page_login():
    st.markdown(STARFIELD_JS, unsafe_allow_html=True)
    st.markdown("""
    <style>
    section[data-testid="stSidebar"]{display:none!important;}

    /* Radial vignette */
    .lg-vig{position:fixed;inset:0;z-index:1;pointer-events:none;
             background:radial-gradient(ellipse 55% 55% at 50% 50%,transparent 35%,rgba(0,0,0,0.55) 100%);}

    /* Subtle grid lines — depth cue */
    .lg-grid{position:fixed;inset:0;z-index:1;pointer-events:none;
              background-image:
                linear-gradient(rgba(201,169,110,0.025) 1px,transparent 1px),
                linear-gradient(90deg,rgba(201,169,110,0.025) 1px,transparent 1px);
              background-size:60px 60px;}

    /* Login card */
    .lg-card{
      background:rgba(16,20,32,0.97);backdrop-filter:blur(20px);
      border:1px solid rgba(201,169,110,0.11);border-radius:3px;
      padding:52px 52px 44px;max-width:420px;width:100%;
      position:relative;overflow:hidden;
      animation:fade-up 0.85s ease both;
      box-shadow:0 32px 80px rgba(0,0,0,0.7),0 0 0 1px rgba(201,169,110,0.04);
    }
    /* Corner accents */
    .lg-card::before{content:'';position:absolute;top:0;left:0;width:52px;height:1px;background:var(--gold);}
    .lg-card::after {content:'';position:absolute;top:0;left:0;width:1px;height:52px;background:var(--gold);}
    .lg-corner-br{position:absolute;bottom:0;right:0;}
    .lg-corner-br::before{content:'';position:absolute;bottom:0;right:0;width:32px;height:1px;background:rgba(201,169,110,0.3);}
    .lg-corner-br::after {content:'';position:absolute;bottom:0;right:0;width:1px;height:32px;background:rgba(201,169,110,0.3);}

    /* Scanning line animation over the card */
    .lg-scan{position:absolute;left:0;right:0;height:40px;
              background:linear-gradient(180deg,transparent,rgba(201,169,110,0.025),transparent);
              animation:scan-line 4s linear infinite;pointer-events:none;z-index:2;}

    .lg-mark{font-family:'Cormorant Garamond',serif;font-size:2.3rem;
              font-weight:300;font-style:italic;color:var(--cream);
              letter-spacing:0.04em;margin-bottom:4px;
              animation:fade-up 0.9s ease 0.1s both;}
    .lg-mark em{color:var(--gold);font-style:normal;}
    .lg-tag{font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.18em;
             color:var(--gold3);text-transform:uppercase;margin-bottom:36px;
             animation:fade-up 0.9s ease 0.2s both;}
    .lg-rule{height:1px;background:rgba(201,169,110,0.10);margin-bottom:28px;
              animation:draw-line 0.8s ease 0.3s both;}
    .lg-field-lbl{font-family:'DM Mono',monospace;font-size:0.58rem;
                   letter-spacing:0.18em;color:var(--gold3);text-transform:uppercase;
                   margin-bottom:6px;margin-top:18px;display:block;
                   animation:fade-up 0.8s ease var(--d,0.4s) both;}
    .lg-hint{font-family:'DM Mono',monospace;font-size:0.62rem;
              letter-spacing:0.05em;color:rgba(122,92,46,0.55);
              margin-top:18px;text-align:center;
              animation:fade-up 0.8s ease 0.7s both;}
    .lg-hint span{color:var(--gold3);}
    .lg-err{font-family:'DM Mono',monospace;font-size:0.64rem;
             letter-spacing:0.04em;color:#9b5a5a;margin-top:10px;
             padding:9px 12px;border:1px solid rgba(155,90,90,0.22);
             border-radius:2px;background:rgba(155,90,90,0.05);}

    /* Button variants */
    .btn-primary .stButton>button{
      width:100%!important;background:rgba(201,169,110,0.10)!important;
      color:var(--gold)!important;border:1px solid rgba(201,169,110,0.38)!important;
      font-size:0.61rem!important;padding:13px!important;border-radius:1px!important;
      letter-spacing:0.18em!important;
    }
    .btn-primary .stButton>button:hover{background:rgba(201,169,110,0.18)!important;border-color:rgba(201,169,110,0.65)!important;}
    .btn-ghost .stButton>button{
      width:100%!important;background:transparent!important;
      color:var(--mist)!important;border:1px solid rgba(138,112,96,0.20)!important;
      font-size:0.61rem!important;padding:13px!important;border-radius:1px!important;
      letter-spacing:0.18em!important;
    }
    .btn-ghost .stButton>button:hover{border-color:rgba(138,112,96,0.42)!important;color:var(--cream)!important;}
    </style>
    <div class="lg-vig"></div>
    <div class="lg-grid"></div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1.15, 1.4, 1.15])
    with col:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;
                    justify-content:center;min-height:100vh;">
        <div class="lg-card">
          <div class="lg-scan"></div>
          <div class="lg-corner-br"></div>
          <p class="lg-mark"><em>Æ</em>ther</p>
          <p class="lg-tag">Mission Control Access</p>
          <div class="lg-rule"></div>
        """, unsafe_allow_html=True)

        st.markdown('<span class="lg-field-lbl" style="--d:0.35s">Username</span>', unsafe_allow_html=True)
        uname = st.text_input("", placeholder="your.name@aether.space",
                               key="lg_u", label_visibility="collapsed")

        st.markdown('<span class="lg-field-lbl" style="--d:0.45s">Access Code</span>', unsafe_allow_html=True)
        pword = st.text_input("", placeholder="••••••••",
                               type="password", key="lg_p",
                               label_visibility="collapsed")

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        b1, b2 = st.columns(2, gap="small")
        with b1:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            do_login = st.button("Sign in", key="do_login")
            st.markdown('</div>', unsafe_allow_html=True)
        with b2:
            st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
            do_demo  = st.button("Demo", key="do_demo")
            st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.login_error:
            st.markdown(f'<p class="lg-err">⚠  {st.session_state.login_error}</p>',
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
                st.session_state.update(logged_in=True, username="admin",
                                        login_error="", page="dashboard")
                st.rerun()
            else:
                st.session_state.login_error = "Incorrect credentials. Try the demo button."
                st.rerun()
        if do_demo:
            st.session_state.update(logged_in=True, username="observer",
                                    login_error="", page="dashboard")
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    df = load_data()

    # Re-enable sidebar
    st.markdown("""
    <style>
    section[data-testid="stSidebar"]{
      display:flex!important;
      background:var(--deep)!important;
      border-right:1px solid rgba(201,169,110,0.07)!important;
    }
    .sb-head{font-family:'Cormorant Garamond',serif;font-weight:400;font-style:italic;
              font-size:1.2rem;color:var(--cream);margin-bottom:4px;}
    .sb-sub{font-family:'DM Mono',monospace;font-size:0.56rem;letter-spacing:0.14em;
             color:var(--gold3);text-transform:uppercase;margin-bottom:20px;
             border-bottom:1px solid rgba(201,169,110,0.07);padding-bottom:14px;}
    .sb-lbl{font-family:'DM Mono',monospace;font-size:0.56rem;letter-spacing:0.14em;
             color:var(--gold3);text-transform:uppercase;margin:14px 0 5px;display:block;}
    .btn-so .stButton>button{
      width:100%!important;background:transparent!important;
      color:rgba(122,112,96,0.45)!important;
      border:1px solid rgba(122,112,96,0.14)!important;
      font-size:0.56rem!important;padding:9px!important;
      border-radius:1px!important;letter-spacing:0.14em!important;margin-top:10px!important;
    }
    .btn-so .stButton>button:hover{color:var(--mist)!important;border-color:rgba(122,112,96,0.35)!important;}
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<p class="sb-head"><em>Æ</em>ther</p>', unsafe_allow_html=True)
        st.markdown('<p class="sb-sub">Mission Filters</p>', unsafe_allow_html=True)

        st.markdown('<span class="sb-lbl">Mission type</span>', unsafe_allow_html=True)
        mtypes = st.multiselect("", sorted(df["Mission Type"].unique()),
                                 default=sorted(df["Mission Type"].unique()),
                                 label_visibility="collapsed")

        st.markdown('<span class="sb-lbl">Launch vehicle</span>', unsafe_allow_html=True)
        vehs = st.multiselect("", sorted(df["Launch Vehicle"].unique()),
                               default=sorted(df["Launch Vehicle"].unique()),
                               label_visibility="collapsed")

        st.markdown('<span class="sb-lbl">Outcome</span>', unsafe_allow_html=True)
        outcs = st.multiselect("", ["Successful","Partial","Failed"],
                                default=["Successful","Partial","Failed"],
                                label_visibility="collapsed")

        st.markdown('<span class="sb-lbl">Cost range · B USD</span>', unsafe_allow_html=True)
        cmin = float(df["Mission Cost (billion USD)"].min())
        cmax = float(df["Mission Cost (billion USD)"].max())
        crng = st.slider("", cmin, cmax, (cmin,cmax), label_visibility="collapsed")

        st.markdown('<span class="sb-lbl">Launch years</span>', unsafe_allow_html=True)
        ymin = int(df["Launch Year"].min())
        ymax = int(df["Launch Year"].max())
        yrng = st.slider("", ymin, ymax, (ymin,ymax), label_visibility="collapsed")

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="btn-so">', unsafe_allow_html=True)
        if st.button("Sign out", key="signout"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Filter ────────────────────────────────────────────────────────────────
    fdf = df[
        df["Mission Type"].isin(mtypes) &
        df["Launch Vehicle"].isin(vehs) &
        df["Outcome"].isin(outcs) &
        df["Mission Cost (billion USD)"].between(crng[0], crng[1]) &
        df["Launch Year"].between(yrng[0], yrng[1])
    ].copy()

    # ── Top bar ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <style>
    .topbar{{display:flex;align-items:center;justify-content:space-between;
              padding:13px 36px;background:rgba(8,9,13,0.94);
              border-bottom:1px solid rgba(201,169,110,0.07);
              backdrop-filter:blur(18px);position:sticky;top:0;z-index:999;}}
    .tb-brand{{font-family:'Cormorant Garamond',serif;font-weight:300;font-style:italic;
                font-size:1.2rem;color:var(--cream);letter-spacing:0.04em;}}
    .tb-brand em{{color:var(--gold);font-style:normal;}}
    .tb-meta{{font-family:'DM Mono',monospace;font-size:0.58rem;
               letter-spacing:0.09em;color:var(--gold3);}}
    </style>
    <div class="topbar">
      <span class="tb-brand"><em>Æ</em>ther · Space Intelligence</span>
      <span class="tb-meta">{len(fdf)} missions · {st.session_state.username}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding:30px 36px;">', unsafe_allow_html=True)

    if len(fdf) == 0:
        st.warning("No missions match the current filters.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── KPI strip ─────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .kpi-row{display:grid;grid-template-columns:repeat(6,1fr);gap:1px;margin-bottom:32px;
              border:1px solid rgba(201,169,110,0.09);border-radius:3px;
              overflow:hidden;background:rgba(201,169,110,0.06);}
    .kpi-cell{background:var(--panel);padding:22px 16px;text-align:left;
               position:relative;overflow:hidden;}
    .kpi-cell::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;
                      background:linear-gradient(90deg,transparent,rgba(201,169,110,0.08),transparent);}
    .kpi-v{font-family:'Cormorant Garamond',serif;font-weight:300;font-size:1.9rem;
             color:var(--cream);display:block;margin-bottom:5px;letter-spacing:-0.01em;}
    .kpi-l{font-family:'DM Mono',monospace;font-size:0.56rem;
             letter-spacing:0.14em;color:var(--gold3);text-transform:uppercase;}
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
    for v,l in kpis:
        kpi_html += f'<div class="kpi-cell"><span class="kpi-v">{v}</span><span class="kpi-l">{l}</span></div>'
    kpi_html += '</div>'
    st.markdown(kpi_html, unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"]{background:transparent;padding:0;gap:0;
                                        border-bottom:1px solid rgba(201,169,110,0.10);}
    .stTabs [data-baseweb="tab"]{font-family:'DM Mono',monospace!important;
      font-size:0.6rem!important;letter-spacing:0.14em!important;
      color:var(--gold3)!important;text-transform:uppercase!important;
      padding:11px 22px!important;border-radius:0!important;
      background:transparent!important;border-bottom:2px solid transparent!important;}
    .stTabs [aria-selected="true"]{color:var(--cream)!important;
                                    border-bottom:2px solid var(--gold)!important;}
    .stTabs [data-baseweb="tab-panel"]{padding-top:26px!important;}
    </style>
    """, unsafe_allow_html=True)

    tab1,tab2,tab3,tab4,tab5 = st.tabs(
        ["Overview","Fuel & Payload","Cost","Simulation","Data & Insights"])

    # ── TAB 1 — Overview ──────────────────────────────────────────────────────
    with tab1:
        section_title("Solar mission map","Distance-scaled orbital reference")
        fdf2 = fdf.sort_values("Distance from Earth (light-years)").reset_index(drop=True)
        fdf2["Angle"] = np.linspace(0,2*np.pi*4,len(fdf2))
        fdf2["SX"] = fdf2["Distance from Earth (light-years)"]*np.cos(fdf2["Angle"])
        fdf2["SY"] = fdf2["Distance from Earth (light-years)"]*np.sin(fdf2["Angle"])
        type_clr = {t:PAL[i%len(PAL)] for i,t in enumerate(sorted(fdf2["Mission Type"].unique()))}

        fig_sol = go.Figure()
        fig_sol.add_trace(go.Scatter(x=[0],y=[0],mode="markers+text",
            marker=dict(size=24,color="#e8c060",line=dict(color="#9a6020",width=2)),
            text=["Earth"],textposition="top center",
            textfont=dict(size=9,color="rgba(201,160,80,0.7)",family="DM Mono"),name="Earth"))
        for r in [10,25,42,58]:
            th = np.linspace(0,2*np.pi,300)
            fig_sol.add_trace(go.Scatter(x=r*np.cos(th),y=r*np.sin(th),mode="lines",
                line=dict(color="rgba(201,169,110,0.055)",width=0.8,dash="dot"),
                showlegend=False,hoverinfo="skip"))
        for mt,grp in fdf2.groupby("Mission Type"):
            fig_sol.add_trace(go.Scatter(
                x=grp["SX"],y=grp["SY"],mode="markers",name=mt,
                marker=dict(size=4+grp["Mission Success (%)"]/30,
                            color=type_clr[mt],opacity=0.65,
                            line=dict(color="rgba(0,0,0,0.3)",width=0.4)),
                customdata=np.stack([grp["Mission Name"],grp["Mission Success (%)"].round(1),
                    grp["Mission Cost (billion USD)"].round(1),grp["Launch Vehicle"]],axis=-1),
                hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}% · $%{customdata[2]}B · %{customdata[3]}<extra></extra>"))
        fig_sol.update_layout(height=480,showlegend=True,
            xaxis=dict(showticklabels=False,showgrid=False,zeroline=False),
            yaxis=dict(showticklabels=False,showgrid=False,zeroline=False,scaleanchor="x"))
        chart_theme(fig_sol)
        st.plotly_chart(fig_sol,use_container_width=True)

        c1,c2 = st.columns([1.1,1],gap="large")
        with c1:
            section_title("Success distribution","By mission type")
            fig_bx = go.Figure()
            for i,(mt,grp) in enumerate(fdf.groupby("Mission Type")):
                col = PAL[i%len(PAL)]
                r,g,b = int(col[1:3],16),int(col[3:5],16),int(col[5:7],16)
                fig_bx.add_trace(go.Box(y=grp["Mission Success (%)"],name=mt,
                    marker_color=col,line_color=col,
                    fillcolor=f"rgba({r},{g},{b},0.10)",boxpoints="outliers"))
            chart_theme(fig_bx,300)
            fig_bx.update_layout(showlegend=False,yaxis_title="Success (%)")
            st.plotly_chart(fig_bx,use_container_width=True)

        with c2:
            section_title("Missions per vehicle","Fleet activity")
            vc = fdf["Launch Vehicle"].value_counts().reset_index()
            vc.columns=["V","C"]
            fig_vb = go.Figure(go.Bar(x=vc["V"],y=vc["C"],
                marker=dict(color=PAL[:len(vc)],line=dict(color="rgba(0,0,0,0.3)",width=0.5)),
                text=vc["C"],textposition="outside",
                textfont=dict(color=MIST,family="DM Mono",size=9)))
            chart_theme(fig_vb,300)
            fig_vb.update_layout(showlegend=False,yaxis_title="Count")
            st.plotly_chart(fig_vb,use_container_width=True)

        section_title("Variable correlations","Pearson correlation matrix")
        ndf = fdf[["Distance from Earth (light-years)","Mission Duration (years)",
                   "Mission Cost (billion USD)","Scientific Yield (points)",
                   "Crew Size","Mission Success (%)","Fuel Consumption (tons)",
                   "Payload Weight (tons)"]]
        corr = ndf.corr()
        fh,ax = plt.subplots(figsize=(11,4.2))
        fh.patch.set_facecolor("none"); ax.set_facecolor(PANEL)
        cmap = sns.diverging_palette(28,200,s=55,l=48,as_cmap=True)
        sns.heatmap(corr,annot=True,fmt=".2f",cmap=cmap,linewidths=0.3,ax=ax,
                    annot_kws={"size":7.5,"family":"DM Mono"},cbar_kws={"shrink":0.7})
        ax.set_title("Pearson Correlation Matrix",color=CREAM,fontsize=12,fontfamily="serif",pad=12)
        ax.tick_params(colors=MIST)
        plt.xticks(color=MIST,fontsize=7.5,rotation=28,ha="right",fontfamily="monospace")
        plt.yticks(color=MIST,fontsize=7.5,fontfamily="monospace")
        plt.tight_layout(); st.pyplot(fh); plt.close(fh)
        note_card("Mission duration and fuel consumption share the strongest positive correlation. "
                  "Distance from Earth is the master variable driving both — mirroring Δv requirements.")

    # ── TAB 2 — Fuel & Payload ────────────────────────────────────────────────
    with tab2:
        c1,c2 = st.columns([1,1],gap="large")
        with c1:
            section_title("Payload vs fuel","Scatter with OLS trend")
            fig_pf = go.Figure()
            for i,(mt,grp) in enumerate(fdf.groupby("Mission Type")):
                fig_pf.add_trace(go.Scatter(x=grp["Payload Weight (tons)"],
                    y=grp["Fuel Consumption (tons)"],mode="markers",name=mt,
                    marker=dict(size=6.5,color=PAL[i%len(PAL)],opacity=0.65,
                                line=dict(color="rgba(0,0,0,0.25)",width=0.4)),
                    customdata=grp["Mission Name"].values,
                    hovertemplate="<b>%{customdata}</b><br>%{x:.1f} t · %{y:.1f} t<extra></extra>"))
            trendline(fig_pf,fdf["Payload Weight (tons)"].values,fdf["Fuel Consumption (tons)"].values)
            chart_theme(fig_pf,330)
            fig_pf.update_layout(xaxis_title="Payload (tons)",yaxis_title="Fuel (tons)")
            st.plotly_chart(fig_pf,use_container_width=True)
        with c2:
            section_title("Distance vs duration","OLS regression")
            fig_dd = go.Figure()
            for i,(veh,grp) in enumerate(fdf.groupby("Launch Vehicle")):
                fig_dd.add_trace(go.Scatter(
                    x=grp["Distance from Earth (light-years)"],y=grp["Mission Duration (years)"],
                    mode="markers",name=veh,
                    marker=dict(size=6,color=PAL[i%len(PAL)],opacity=0.65),
                    customdata=grp["Mission Name"].values,
                    hovertemplate="<b>%{customdata}</b><br>%{x:.2f} ly · %{y:.1f} yrs<extra></extra>"))
            trendline(fig_dd,fdf["Distance from Earth (light-years)"].values,
                      fdf["Mission Duration (years)"].values,color="#9b7a6a")
            chart_theme(fig_dd,330)
            fig_dd.update_layout(xaxis_title="Distance (light-years)",yaxis_title="Duration (years)")
            st.plotly_chart(fig_dd,use_container_width=True)

        section_title("Fuel efficiency by type","Payload ÷ Fuel consumed")
        eff = fdf.groupby("Mission Type")["Fuel Efficiency"].mean().reset_index().sort_values("Fuel Efficiency",ascending=False)
        fig_ef = go.Figure(go.Bar(x=eff["Mission Type"],y=eff["Fuel Efficiency"],
            marker=dict(color=PAL[:len(eff)],line=dict(color="rgba(0,0,0,0.3)",width=0.5)),
            text=eff["Fuel Efficiency"].round(5),textposition="outside",
            textfont=dict(color=MIST,family="DM Mono",size=9.5)))
        chart_theme(fig_ef,260)
        fig_ef.update_layout(showlegend=False,yaxis_title="Efficiency ratio")
        st.plotly_chart(fig_ef,use_container_width=True)

        section_title("Fuel distribution by vehicle","Violin + box overlay")
        fig_vi = go.Figure()
        for i,(veh,grp) in enumerate(fdf.groupby("Launch Vehicle")):
            col = PAL[i%len(PAL)]; r,g,b = int(col[1:3],16),int(col[3:5],16),int(col[5:7],16)
            fig_vi.add_trace(go.Violin(x=grp["Launch Vehicle"],y=grp["Fuel Consumption (tons)"],
                name=veh,line_color=col,fillcolor=f"rgba({r},{g},{b},0.11)",
                box_visible=True,meanline_visible=True,points="outliers"))
        chart_theme(fig_vi,280)
        fig_vi.update_layout(showlegend=False,yaxis_title="Fuel (tons)")
        st.plotly_chart(fig_vi,use_container_width=True)
        note_card("OLS confirms F=ma in practice — heavier payloads demand proportionally more propellant. "
                  "Greater mass requires greater sustained thrust and larger fuel reserves.","#7a9e8a")

    # ── TAB 3 — Cost ──────────────────────────────────────────────────────────
    with tab3:
        c1,c2 = st.columns([1,1],gap="large")
        with c1:
            section_title("Cost vs success rate","Bubble size = crew")
            fig_cs = go.Figure()
            for outc,grp in fdf.groupby("Outcome"):
                col = OUT_CLR.get(outc,MIST)
                fig_cs.add_trace(go.Scatter(
                    x=grp["Mission Cost (billion USD)"],y=grp["Mission Success (%)"],
                    mode="markers",name=outc,
                    marker=dict(size=5+grp["Crew Size"]/14,color=col,opacity=0.65,
                                line=dict(color="rgba(0,0,0,0.25)",width=0.4)),
                    customdata=np.stack([grp["Mission Name"],grp["Launch Vehicle"]],axis=-1),
                    hovertemplate="<b>%{customdata[0]}</b><br>$%{x:.1f}B · %{y:.1f}%<extra></extra>"))
            chart_theme(fig_cs,330)
            fig_cs.update_layout(xaxis_title="Cost (B USD)",yaxis_title="Success (%)")
            st.plotly_chart(fig_cs,use_container_width=True)
        with c2:
            section_title("Avg cost by outcome","")
            cg = fdf.groupby("Outcome")["Mission Cost (billion USD)"].mean().reset_index()
            fig_cb = go.Figure(go.Bar(x=cg["Outcome"],y=cg["Mission Cost (billion USD)"],
                marker=dict(color=[OUT_CLR.get(c,MIST) for c in cg["Outcome"]],
                            line=dict(color="rgba(0,0,0,0.3)",width=0.5)),
                text=["$"+str(round(v,1))+"B" for v in cg["Mission Cost (billion USD)"]],
                textposition="outside",textfont=dict(color=MIST,family="DM Mono",size=9.5)))
            chart_theme(fig_cb,330)
            fig_cb.update_layout(showlegend=False,yaxis_title="Avg cost (B USD)")
            st.plotly_chart(fig_cb,use_container_width=True)

        section_title("Scientific yield over time","Average by mission type · year")
        yt = fdf.groupby(["Launch Year","Mission Type"])["Scientific Yield (points)"].mean().reset_index()
        fyt,ayt = plt.subplots(figsize=(13,3.8))
        fyt.patch.set_facecolor("none"); ayt.set_facecolor(PANEL)
        for i,mt in enumerate(yt["Mission Type"].unique()):
            sub=yt[yt["Mission Type"]==mt]; c=PAL[i%len(PAL)]
            ayt.plot(sub["Launch Year"],sub["Scientific Yield (points)"],
                     marker="o",label=mt,linewidth=1.8,color=c,markersize=4.5,markeredgewidth=0)
            ayt.fill_between(sub["Launch Year"],sub["Scientific Yield (points)"],alpha=0.06,color=c)
        ayt.set_title("Average Scientific Yield by Year & Mission Type",color=CREAM,fontsize=12,fontfamily="serif")
        ayt.set_xlabel("Year",color=MIST,fontfamily="monospace")
        ayt.set_ylabel("Yield (pts)",color=MIST,fontfamily="monospace")
        ayt.tick_params(colors=MIST)
        ayt.legend(facecolor=PANEL,labelcolor=MIST,framealpha=0.7,fontsize=9)
        for sp in ayt.spines.values(): sp.set_color("rgba(201,169,110,0.09)")
        ayt.grid(color="rgba(201,169,110,0.05)",linestyle="--",linewidth=0.5)
        plt.tight_layout(); st.pyplot(fyt); plt.close(fyt)

        section_title("Mission type × outcome","Sunburst breakdown")
        sb = fdf.groupby(["Mission Type","Outcome"]).size().reset_index(name="Count")
        fig_sb = px.sunburst(sb,path=["Mission Type","Outcome"],values="Count",
                             color="Mission Type",color_discrete_sequence=PAL)
        chart_theme(fig_sb,370)
        st.plotly_chart(fig_sb,use_container_width=True)
        note_card("Higher cost does not reliably predict success. Research missions deliver the highest "
                  "scientific yield per billion — the most efficient academic investment.","#9b7a6a")

    # ── TAB 4 — Simulation ────────────────────────────────────────────────────
    with tab4:
        section_title("Launch simulation","Euler integration · differential equations")
        st.markdown("""
        <div style="font-family:'DM Mono',monospace;font-size:0.7rem;color:var(--mist);
                    line-height:2.1;border-left:2px solid rgba(201,169,110,0.16);
                    padding:12px 20px;margin-bottom:28px;background:rgba(201,169,110,0.018);">
          a(t) = [ T &minus; m(t)·g &minus; ½·Cd·ρ(h)·A·v² ] / m(t)
          &emsp;|&emsp; v(t+Δt) = v + a·Δt &emsp;|&emsp; h(t+Δt) = h + v·Δt<br>
          ρ(h) = 1.225 · e<sup>−h/8500</sup> &emsp;[ISA exponential atmosphere]
        </div>""", unsafe_allow_html=True)

        cs1,cs2,cs3 = st.columns(3,gap="large")
        with cs1:
            thr = st.slider("Thrust kN",500,5000,2500,100)
            pl  = st.slider("Payload tons",1,150,30,1)
        with cs2:
            fu  = st.slider("Fuel tons",100,1200,400,50)
            cd  = st.slider("Drag coeff Cd",0.05,1.0,0.3,0.05)
        with cs3:
            ns  = st.slider("Time steps",50,600,250,50)
            dt  = st.slider("Δt seconds",1,10,2,1)

        G=9.81; A=12.0
        m=(pl+fu)*1000.0; T_N=thr*1000.0
        burn=(fu*1000.0)/max(ns,1)
        alt_a=[0.0]; vel_a=[0.0]; acc_a=[0.0]; mass_a=[m/1000]
        fr=fu*1000.0

        for _ in range(ns):
            if fr>0:
                bs=burn*dt; fr=max(0.0,fr-bs); m=max(pl*1000.0,m-bs)
                eff_T=T_N
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

        section_title("Launch path","Altitude & velocity dual-axis")
        fig_rv=go.Figure()
        fig_rv.add_trace(go.Scatter(x=sd["t"],y=sd["alt"],name="Altitude km",
            line=dict(color=PAL[0],width=2.2),fill="tozeroy",
            fillcolor=f"rgba({int(PAL[0][1:3],16)},{int(PAL[0][3:5],16)},{int(PAL[0][5:7],16)},0.06)"))
        fig_rv.add_trace(go.Scatter(x=sd["t"],y=sd["vel"],name="Velocity m/s",
            line=dict(color=PAL[1],width=2.0),yaxis="y2"))
        bx=sd["vel"].idxmax()
        fig_rv.add_trace(go.Scatter(x=[sd.loc[bx,"t"]],y=[sd.loc[bx,"alt"]],
            mode="markers+text",name="Burnout",
            marker=dict(size=10,color=PAL[2],symbol="diamond"),
            text=["burnout"],textposition="top right",
            textfont=dict(size=9,color=PAL[2],family="DM Mono"),yaxis="y1"))
        fig_rv.update_layout(height=370,xaxis_title="Time (s)",
            yaxis=dict(title="Altitude (km)",color=PAL[0],gridcolor="rgba(201,169,110,0.05)"),
            yaxis2=dict(title="Velocity (m/s)",overlaying="y",side="right",color=PAL[1]),
            margin=dict(l=20,r=60,t=50,b=20))
        chart_theme(fig_rv); st.plotly_chart(fig_rv,use_container_width=True)

        ca1,ca2=st.columns(2,gap="large")
        with ca1:
            section_title("Acceleration","")
            fig_ac=go.Figure()
            fig_ac.add_trace(go.Scatter(x=sd["t"],y=sd["acc"],name="Accel",
                line=dict(color=PAL[3],width=2),fill="tozeroy",
                fillcolor=f"rgba({int(PAL[3][1:3],16)},{int(PAL[3][3:5],16)},{int(PAL[3][5:7],16)},0.06)"))
            fig_ac.add_hline(y=0,line_dash="dot",line_color="rgba(155,90,90,0.5)",
                annotation_text="equilibrium",
                annotation_font=dict(color="rgba(155,90,90,0.7)",size=9,family="DM Mono"))
            chart_theme(fig_ac,260); fig_ac.update_layout(yaxis_title="m/s²",showlegend=False)
            st.plotly_chart(fig_ac,use_container_width=True)
        with ca2:
            section_title("Mass decrease","Fuel burn profile")
            fig_ms=go.Figure()
            fig_ms.add_trace(go.Scatter(x=sd["t"],y=sd["mass"],name="Mass",
                line=dict(color=PAL[4],width=2),fill="tozeroy",
                fillcolor=f"rgba({int(PAL[4][1:3],16)},{int(PAL[4][3:5],16)},{int(PAL[4][5:7],16)},0.06)"))
            chart_theme(fig_ms,260); fig_ms.update_layout(yaxis_title="tonnes",showlegend=False)
            st.plotly_chart(fig_ms,use_container_width=True)

        section_title("Phase space trajectory","Velocity vs altitude · coloured by time")
        fig_ph=go.Figure(go.Scatter(x=sd["alt"],y=sd["vel"],mode="lines+markers",
            marker=dict(size=3,color=sd["t"],colorscale=[[0,"rgba(122,92,46,0.6)"],[0.5,PAL[0]],[1,PAL[1]]],
                showscale=True,colorbar=dict(title="s",thickness=8,
                    tickfont=dict(color=MIST,size=8,family="DM Mono"))),
            line=dict(color="rgba(201,169,110,0.2)",width=1)))
        chart_theme(fig_ph,290)
        fig_ph.update_layout(xaxis_title="Altitude (km)",yaxis_title="Velocity (m/s)")
        st.plotly_chart(fig_ph,use_container_width=True)

        mx_a=sd["alt"].max(); mx_v=sd["vel"].max()
        mx_ac=sd["acc"].max(); bt=sd.loc[sd["vel"].idxmax(),"t"]
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;
                    border:1px solid rgba(201,169,110,0.09);border-radius:2px;
                    overflow:hidden;background:rgba(201,169,110,0.06);margin-top:14px;">
          {"".join([
            f'<div style="background:var(--panel);padding:18px 16px;">'
            f'<span style="font-family:Cormorant Garamond,serif;font-size:1.75rem;font-weight:300;color:var(--cream);display:block;">{vl}</span>'
            f'<span style="font-family:DM Mono,monospace;font-size:0.56rem;letter-spacing:0.14em;color:var(--gold3);text-transform:uppercase;">{lb}</span></div>'
            for vl,lb in [(f"{mx_a:.1f} km","Max altitude"),(f"{mx_v:.0f} m/s","Max velocity"),
                          (f"{mx_ac:.2f} m/s²","Peak accel"),(f"{bt:.0f} s","Burnout time")]
          ])}
        </div>""", unsafe_allow_html=True)

    # ── TAB 5 — Data & Insights ───────────────────────────────────────────────
    with tab5:
        c1,c2=st.columns([1.2,1],gap="large")
        with c1:
            section_title("Dataset summary","Post-cleaning statistics")
            st.dataframe(fdf.describe().T.round(2),use_container_width=True,height=300)
        with c2:
            section_title("Mission type split","")
            pd_=fdf["Mission Type"].value_counts().reset_index()
            pd_.columns=["T","C"]
            fig_pie=go.Figure(go.Pie(labels=pd_["T"],values=pd_["C"],hole=0.55,
                marker=dict(colors=PAL[:len(pd_)],line=dict(color=INK,width=2)),
                textfont=dict(family="DM Mono",size=9,color=CREAM)))
            chart_theme(fig_pie,300); st.plotly_chart(fig_pie,use_container_width=True)

        section_title("Research insights","")
        insights=[
            (GOLD,"Payload and propellant","Heavier payloads demand more fuel — F=ma confirmed statistically across all mission types via OLS regression."),
            ("#9b7a6a","The cost paradox","Higher expenditure doesn't predict success. Execution quality and vehicle selection matter more than budget."),
            ("#7a9e8a","Distance as master variable","Distance drives both duration and fuel requirements — mirroring the Tsiolkovsky equation's Δv dependency."),
            (PAL[3],"Vehicle selection","Starship dominates heavy-payload missions; Falcon Heavy shows the strongest mid-range fuel efficiency."),
            (PAL[4],"Research mission ROI","Research missions yield the highest scientific points per billion — the most efficient academic investment."),
            (MIST,"ISA atmosphere model","ρ(h)=1.225·e⁻ʰ/⁸⁵⁰⁰ captures exponential density drop. Drag near-vanishes above 50 km, enabling dramatic acceleration gains."),
        ]
        for ac,title,body_text in insights:
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:2px 1fr;gap:0;
                        margin-bottom:1px;overflow:hidden;border-radius:2px;">
              <div style="background:{ac};"></div>
              <div style="background:var(--panel);padding:16px 20px;">
                <p style="font-family:'Cormorant Garamond',serif;font-size:1.05rem;
                           font-weight:400;color:var(--cream);margin:0 0 5px;">{title}</p>
                <p style="font-family:'DM Sans',sans-serif;font-weight:300;font-size:0.87rem;
                           color:var(--mist);margin:0;line-height:1.8;">{body_text}</p>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
        section_title("Mission data explorer","")
        default_cols=["Mission Name","Mission Type","Launch Vehicle",
                      "Mission Cost (billion USD)","Fuel Consumption (tons)",
                      "Payload Weight (tons)","Mission Success (%)","Outcome","Launch Year"]
        cols_sel = st.multiselect("Columns",fdf.columns.tolist(),
                                   default=[c for c in default_cols if c in fdf.columns])
        if cols_sel:
            st.dataframe(fdf[cols_sel].reset_index(drop=True),use_container_width=True,height=340)

        csv_b = fdf.to_csv(index=False).encode("utf-8")
        st.markdown("""
        <style>
        .dl-btn .stDownloadButton>button{
          background:transparent!important;color:var(--gold)!important;
          border:1px solid rgba(201,169,110,0.32)!important;
          font-size:0.6rem!important;padding:11px 22px!important;
          border-radius:1px!important;letter-spacing:0.16em!important;}
        .dl-btn .stDownloadButton>button:hover{
          background:rgba(201,169,110,0.07)!important;
          border-color:rgba(201,169,110,0.6)!important;}
        </style><div class="dl-btn">""", unsafe_allow_html=True)
        st.download_button("Download filtered dataset", csv_b,
                           "aether_missions.csv","text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:22px 36px;border-top:1px solid rgba(201,169,110,0.06);
                font-family:'DM Mono',monospace;font-size:0.56rem;
                color:rgba(122,92,46,0.45);letter-spacing:0.12em;">
      Æther · Space Mission Intelligence · Mathematics for AI-I · 2025
      &ensp;·&ensp; Data sourced via Google Drive · Streamlit · Plotly · Seaborn
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
p = st.session_state.get("page","onboarding")
if   p == "onboarding": page_onboarding()
elif p == "loading":    page_loading()
elif p == "login":      page_login()
elif p == "dashboard":
    if st.session_state.get("logged_in"):
        page_dashboard()
    else:
        st.session_state.page = "login"
        st.rerun()
