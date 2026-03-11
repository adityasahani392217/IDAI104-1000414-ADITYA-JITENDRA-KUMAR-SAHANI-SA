import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import io

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AEGIS · Rocket Mission Analytics",
    layout="wide",
    page_icon="🛸",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# FULL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;600&family=Share+Tech+Mono&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #00000f !important;
    color: #c8d8f0 !important;
    font-family: 'Rajdhani', sans-serif !important;
    overflow-x: hidden;
}

/* ── SCROLLBAR ── */
[data-testid="stApp"] { height: 100vh !important; }

/* Stars */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 10% 15%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 60%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 40% 30%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 80%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 20%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(2px 2px at 80% 55%, rgba(180,200,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 75%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 15% 90%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 35% 45%, rgba(200,220,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 10%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 85%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(2px 2px at 5%  50%, rgba(160,180,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 48% 70%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 88% 35%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 22% 25%, rgba(200,230,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 33% 77%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 67% 44%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(2px 2px at 92% 12%, rgba(180,210,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 3%  88%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 58% 58%, rgba(210,230,255,0.7) 0%, transparent 100%);
    background-size: 900px 700px;
    z-index: 0;
    pointer-events: none;
    animation: starDrift 100s linear infinite;
}
@keyframes starDrift {
    from { background-position: 0 0; }
    to   { background-position: 900px 700px; }
}
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 15% 85%, rgba(15,5,60,0.85) 0%, transparent 65%),
        radial-gradient(ellipse 55% 55% at 85% 15%, rgba(0,15,55,0.80) 0%, transparent 65%),
        radial-gradient(ellipse 90% 45% at 50% 50%, rgba(0,0,18,0.50) 0%, transparent 100%);
    z-index: 0;
    pointer-events: none;
}
[data-testid="stMainBlockContainer"],
section[data-testid="stSidebar"],
[data-testid="stHeader"] { position: relative; z-index: 1; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(0,4,28,0.97) 0%, rgba(0,8,38,0.97) 60%, rgba(0,2,18,0.97) 100%) !important;
    border-right: 1px solid rgba(0,180,255,0.14) !important;
}
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] div, section[data-testid="stSidebar"] label { color: #90b8e0 !important; font-family: 'Rajdhani', sans-serif !important; }

/* Typography */
h1,h2,h3 { font-family: 'Orbitron', sans-serif !important; letter-spacing: 0.07em !important; color: #e8f4ff !important; }
h1 { font-size: 1.85rem !important; font-weight: 700 !important; }
h2 { font-size: 1.3rem !important; font-weight: 600 !important; }
h3 { font-size: 1.05rem !important; font-weight: 600 !important; }
p, li { font-family: 'Rajdhani', sans-serif !important; font-size: 1.05rem !important; line-height: 1.65 !important; }

/* DOOR ANIMATION */
.door-overlay {
    position: fixed; inset: 0; z-index: 9999;
    display: flex; pointer-events: none;
}
.door-left {
    width: 50%; height: 100%;
    background: linear-gradient(135deg, #000d2e 0%, #001a55 50%, #000d2e 100%);
    border-right: 2px solid rgba(0,200,255,0.7);
    box-shadow: inset -30px 0 60px rgba(0,150,255,0.12), 4px 0 40px rgba(0,200,255,0.4);
    animation: doorOpenLeft 1.4s cubic-bezier(0.77,0,0.175,1) 0.3s forwards;
    display: flex; align-items: center; justify-content: flex-end;
    padding-right: 3rem; position: relative; overflow: hidden;
}
.door-left::before {
    content: '';
    position: absolute; inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,180,255,0.03) 3px, rgba(0,180,255,0.03) 4px);
    pointer-events: none;
}
.door-right {
    width: 50%; height: 100%;
    background: linear-gradient(225deg, #000d2e 0%, #001a55 50%, #000d2e 100%);
    border-left: 2px solid rgba(0,200,255,0.7);
    box-shadow: inset 30px 0 60px rgba(0,150,255,0.12), -4px 0 40px rgba(0,200,255,0.4);
    animation: doorOpenRight 1.4s cubic-bezier(0.77,0,0.175,1) 0.3s forwards;
    display: flex; align-items: center; justify-content: flex-start;
    padding-left: 3rem; position: relative; overflow: hidden;
}
.door-right::before {
    content: '';
    position: absolute; inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,180,255,0.03) 3px, rgba(0,180,255,0.03) 4px);
    pointer-events: none;
}
.door-text {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.1rem;
    font-weight: 900;
    color: #00e5ff;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    text-shadow: 0 0 20px rgba(0,220,255,0.9), 0 0 40px rgba(0,180,255,0.5);
    animation: doorTextFade 0.8s ease-out forwards;
    line-height: 1.6;
}
.door-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.62rem;
    color: rgba(0,200,255,0.55);
    letter-spacing: 0.22em;
    text-transform: uppercase;
    display: block;
    margin-top: 0.5rem;
}
@keyframes doorTextFade { from { opacity: 0; transform: scale(0.92); } to { opacity: 1; transform: scale(1); } }
@keyframes doorOpenLeft  { from { transform: translateX(0); } to { transform: translateX(-105%); } }
@keyframes doorOpenRight { from { transform: translateX(0); } to { transform: translateX(105%);  } }

/* Hero */
.hero-banner {
    position: relative;
    border: 1px solid rgba(0,200,255,0.22);
    border-radius: 18px;
    padding: 3rem 2rem;
    margin-bottom: 2rem;
    overflow: hidden;
    text-align: center;
    background:
        linear-gradient(135deg, rgba(0,8,38,0.93) 0%, rgba(0,18,65,0.87) 45%, rgba(4,0,28,0.93) 100%),
        url('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Falcon_Heavy_Demo_Mission_%2840126461851%29.jpg/1280px-Falcon_Heavy_Demo_Mission_%2840126461851%29.jpg')
        center/cover no-repeat;
}
.hero-banner::before {
    content: '';
    position: absolute; top: 0; left: -100%; bottom: 0; width: 300%;
    background: linear-gradient(90deg, transparent 0%, rgba(0,200,255,0.05) 50%, transparent 100%);
    animation: scanline 5s ease-in-out infinite;
    pointer-events: none;
}
@keyframes scanline { 0% { transform: translateX(-33%); } 100% { transform: translateX(33%); } }
.hero-title {
    font-family: 'Orbitron', sans-serif; font-size: 2.5rem; font-weight: 900;
    letter-spacing: 0.14em; color: #fff;
    text-shadow: 0 0 25px rgba(0,200,255,0.85), 0 0 50px rgba(0,150,255,0.45);
    margin: 0 0 0.4rem;
    animation: glowPulse 3.5s ease-in-out infinite;
}
@keyframes glowPulse {
    0%,100% { text-shadow: 0 0 20px rgba(0,200,255,0.8), 0 0 40px rgba(0,150,255,0.4); }
    50%     { text-shadow: 0 0 35px rgba(0,220,255,1.0), 0 0 70px rgba(0,180,255,0.65); }
}
.hero-sub { font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; color: #5aaae0; letter-spacing: 0.2em; text-transform: uppercase; }
.hero-badge { display:inline-block; margin-top:1.2rem; padding:0.3rem 1.2rem; border:1px solid rgba(0,200,255,0.35); border-radius:20px; font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:#00e5ff; letter-spacing:0.14em; background:rgba(0,200,255,0.06); }

/* Cards */
.glass-card { background:rgba(3,12,45,0.62); border:1px solid rgba(0,150,255,0.18); border-radius:14px; padding:1.4rem 1.6rem; margin-bottom:0.8rem; }
.metric-card { background:linear-gradient(135deg,rgba(0,18,65,0.88) 0%,rgba(0,8,45,0.92) 100%); border:1px solid rgba(0,175,255,0.20); border-radius:12px; padding:1.2rem 0.8rem; text-align:center; position:relative; overflow:hidden; }
.metric-card::after { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,transparent,#00b8ff,transparent); }
.metric-val { font-family:'Orbitron',sans-serif; font-size:1.5rem; font-weight:700; color:#00e5ff; text-shadow:0 0 14px rgba(0,200,255,0.55); display:block; }
.metric-lbl { font-family:'Rajdhani',sans-serif; font-size:0.76rem; color:#6a9ab8; text-transform:uppercase; letter-spacing:0.12em; margin-top:5px; display:block; }
.insight-box { background:rgba(0,35,72,0.55); border-left:3px solid #00b8ff; border-radius:0 10px 10px 0; padding:1rem 1.2rem; color:#9ac8e8; font-size:0.95rem; line-height:1.6; font-family:'Rajdhani',sans-serif; }
.insight-box b { color:#00e5ff; }
.force-card { background:linear-gradient(160deg,rgba(0,12,48,0.88),rgba(0,6,30,0.92)); border:1px solid rgba(0,150,255,0.16); border-radius:14px; padding:1.5rem; text-align:center; }
.force-icon { font-size:2.2rem; display:block; margin-bottom:0.5rem; }
.force-title { font-family:'Orbitron',sans-serif; font-size:0.82rem; color:#00d0f5; letter-spacing:0.1em; margin-bottom:0.5rem; }
.force-body { font-family:'Rajdhani',sans-serif; font-size:0.91rem; color:#7aaccc; line-height:1.55; }
.section-tag { display:inline-flex; align-items:center; gap:0.5rem; font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:#00a8e8; letter-spacing:0.18em; text-transform:uppercase; background:rgba(0,170,255,0.07); border:1px solid rgba(0,170,255,0.20); border-radius:4px; padding:0.22rem 0.7rem; margin-bottom:0.5rem; }
.section-tag::before { content:'//'; opacity:0.45; }
.divider-line { border:none; border-top:1px solid rgba(0,150,255,0.12); margin:1.8rem 0; }

/* Onboarding steps */
.step-card {
    background: rgba(0,15,55,0.70);
    border: 1px solid rgba(0,150,255,0.20);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    display: flex; gap: 1rem; align-items: flex-start;
}
.step-num {
    font-family: 'Orbitron', sans-serif; font-size: 1.4rem; font-weight:900;
    color: #00e5ff; text-shadow: 0 0 12px rgba(0,200,255,0.5);
    min-width: 2rem; line-height: 1;
}
.step-body-title { font-family:'Orbitron',sans-serif; font-size:0.78rem; color:#c8e8ff; letter-spacing:0.08em; margin-bottom:0.25rem; }
.step-body-text  { font-family:'Rajdhani',sans-serif; font-size:0.92rem; color:#7aaac8; line-height:1.5; }

/* Terms checkbox area */
.terms-box {
    background: rgba(0,10,40,0.70);
    border: 1px solid rgba(0,150,255,0.18);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.88rem;
    color: #6a9ab8;
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 0.8rem;
}

/* Buttons */
.stButton > button {
    font-family: 'Orbitron', sans-serif !important; font-size: 0.82rem !important;
    letter-spacing: 0.12em !important; font-weight: 700 !important;
    background: linear-gradient(135deg, #002d75, #0050b0) !important;
    color: #00e5ff !important; border: 1px solid rgba(0,195,255,0.38) !important;
    border-radius: 8px !important; transition: all 0.25s !important;
    box-shadow: 0 0 18px rgba(0,140,255,0.14) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #003d99, #0070cc) !important;
    box-shadow: 0 0 32px rgba(0,200,255,0.38) !important;
    border-color: rgba(0,225,255,0.68) !important;
}

/* Inputs */
.stTextInput > div > div > input, .stNumberInput > div > div > input {
    background: rgba(0,12,45,0.82) !important; border: 1px solid rgba(0,155,255,0.24) !important;
    border-radius: 8px !important; color: #c0d8f0 !important; font-family: 'Rajdhani', sans-serif !important;
    width: 100% !important; padding: 0.6rem 1rem !important;
}
.stSelectbox > div > div {
    background: rgba(0,12,45,0.82) !important; border: 1px solid rgba(0,155,255,0.24) !important;
    border-radius: 8px !important; color: #c0d8f0 !important;
    width: 100% !important;
}

/* Slider */
.stSlider > div > div > div > div { background: linear-gradient(90deg, #005cc8, #00b8ff) !important; }

/* Progress */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #002ea8, #00b8ff, #00e5ff) !important;
    box-shadow: 0 0 12px rgba(0,200,255,0.55) !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-family: 'Orbitron', sans-serif !important; font-size: 0.8rem !important;
    letter-spacing: 0.08em !important; color: #55aadd !important;
    background: rgba(0,12,45,0.72) !important; border-radius: 8px !important;
    border: 1px solid rgba(0,135,255,0.16) !important;
}

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #00000f; }
::-webkit-scrollbar-thumb { background: #002d5a; border-radius: 3px; }

#MainMenu, footer { visibility: hidden; }
.stAppDeployButton { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def metric_card(val, lbl):
    return (
        "<div class='metric-card'>"
        "<span class='metric-val'>" + str(val) + "</span>"
        "<span class='metric-lbl'>" + str(lbl) + "</span>"
        "</div>"
    )

def section_tag(text):
    st.markdown("<div class='section-tag'>" + text + "</div>", unsafe_allow_html=True)

def divider():
    st.markdown("<hr class='divider-line'>", unsafe_allow_html=True)

def insight(html):
    st.markdown("<div class='insight-box'>" + html + "</div>", unsafe_allow_html=True)

PLOT_BASE = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,5,22,0.55)",
    font=dict(family="Rajdhani, sans-serif", color="#9ac8e0"),
    title_font=dict(family="Orbitron, sans-serif", size=13, color="#c0e0ff"),
    margin=dict(l=40, r=20, t=48, b=38),
)

# ─────────────────────────────────────────────
# FALLBACK DATASET
# ─────────────────────────────────────────────
FALLBACK_CSV = """Mission ID,Mission Name,Launch Date,Target Type,Target Name,Mission Type,Distance from Earth (light-years),Mission Duration (years),Mission Cost (billion USD),Scientific Yield (points),Crew Size,Mission Success (%),Fuel Consumption (tons),Payload Weight (tons),Launch Vehicle
MSN-0001,Mission-1,2025-01-01,Star,Titan,Colonization,7.05,5.2,526.68,64.3,21,100,731.88,99.78,SLS
MSN-0002,Mission-2,2025-01-08,Exoplanet,Betelgeuse,Colonization,41.76,23,234.08,84.4,72,89.6,4197.41,45.72,Starship
MSN-0003,Mission-3,2025-01-15,Asteroid,Mars,Exploration,49.22,28.8,218.68,98.6,16,98.6,4908,36.12,Starship
MSN-0004,Mission-4,2025-01-22,Exoplanet,Titan,Colonization,26.33,17.8,232.89,36,59,90,2569.05,40.67,Starship
MSN-0005,Mission-5,2025-01-29,Exoplanet,Proxima b,Mining,8.67,9.2,72.14,96.5,31,73.2,892.76,12.4,Starship
MSN-0006,Mission-6,2025-02-05,Moon,Ceres,Colonization,13.69,8.8,452.42,45.1,42,100,1327.29,88.44,Ariane 6
MSN-0007,Mission-7,2025-02-12,Asteroid,Ceres,Research,1.02,5,220.38,44.7,74,95.5,211.2,42.07,SLS
MSN-0008,Mission-8,2025-02-19,Asteroid,Mars,Colonization,45.72,25.2,200.49,40.6,32,89.3,4600.53,39.34,SLS
MSN-0009,Mission-9,2025-02-26,Moon,Europa,Research,5.14,4.1,180.22,77.3,18,95,520.44,25.6,Falcon Heavy
MSN-0010,Mission-10,2025-03-05,Exoplanet,Kepler-452b,Exploration,1400,320,890.5,99.1,8,100,85000,12.3,Starship
MSN-0011,Mission-11,2025-03-12,Asteroid,Vesta,Mining,2.3,3.5,95.75,55.2,12,82.1,312.9,18.4,Falcon Heavy
MSN-0012,Mission-12,2025-03-19,Moon,Titan,Research,8.2,6.7,340.1,88.9,25,97.4,1050.3,67.2,SLS
MSN-0013,Mission-13,2025-03-26,Star,Proxima b,Colonization,4.24,12.5,620.45,72.6,45,100,5800.2,110.5,Starship
MSN-0014,Mission-14,2025-04-02,Exoplanet,55 Cancri e,Mining,41,95,450.8,66.1,30,78.4,18200.7,55.9,Ariane 6
MSN-0015,Mission-15,2025-04-09,Asteroid,Ceres,Exploration,2.8,4.2,110.3,91.3,14,98.1,425.6,22.1,Falcon Heavy
MSN-0016,Mission-16,2025-04-16,Moon,Ganymede,Colonization,6.3,7.8,388.9,58.4,38,100,1680.4,79.8,SLS
MSN-0017,Mission-17,2025-04-23,Exoplanet,Trappist-1e,Research,39.5,88,560.2,95.7,10,93.6,22400.1,18.7,Starship
MSN-0018,Mission-18,2025-04-30,Moon,Io,Mining,5.9,5.5,210.6,47.8,20,85.2,720.9,33.5,Falcon Heavy
MSN-0019,Mission-19,2025-05-07,Star,Alpha Centauri,Exploration,4.37,15.2,780.3,88.2,35,100,6920.5,125.4,Starship
MSN-0020,Mission-20,2025-05-14,Asteroid,Pallas,Colonization,3.1,6.1,165.4,62.9,28,91.5,580.2,44.6,SLS
"""

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    try:
        # Load local dataset from multiple possible locations depending on folder structure
        dataset_paths = [
            "space_missions_dataset__1_.csv",
            "Dataset/space_missions_dataset__1_.csv",
            "../Dataset/space_missions_dataset__1_.csv"
        ]
        
        df = None
        for path in dataset_paths:
            try:
                df = pd.read_csv(path)
                if not df.empty:
                    break
            except Exception:
                continue
                
        if df is None or df.empty:
            raise ValueError("Empty local dataframe or file not found")
    except Exception:
        # Fallback to the in-memory string if the dataset isn't fully staged yet
        df = pd.read_csv(io.StringIO(FALLBACK_CSV))

    # Rename columns to short names for easier use
    col_map = {}
    for c in df.columns:
        cl = c.lower()
        if "mission id"      in cl: col_map[c] = "Mission ID"
        elif "mission name"  in cl: col_map[c] = "Mission Name"
        elif "launch date"   in cl: col_map[c] = "Launch Date"
        elif "target type"   in cl: col_map[c] = "Target Type"
        elif "target name"   in cl: col_map[c] = "Target Name"
        elif "mission type"  in cl: col_map[c] = "Mission Type"
        elif "distance"      in cl: col_map[c] = "Distance from Earth"
        elif "duration"      in cl: col_map[c] = "Mission Duration"
        elif "cost"          in cl: col_map[c] = "Mission Cost"
        elif "yield"         in cl: col_map[c] = "Scientific Yield"
        elif "crew"          in cl: col_map[c] = "Crew Size"
        elif "success"       in cl: col_map[c] = "Mission Success"
        elif "fuel"          in cl: col_map[c] = "Fuel Consumption"
        elif "payload"       in cl: col_map[c] = "Payload Weight"
        elif "vehicle"       in cl: col_map[c] = "Launch Vehicle"
    df = df.rename(columns=col_map)

    if "Launch Date" in df.columns:
        df["Launch Date"] = pd.to_datetime(df["Launch Date"], errors="coerce")
    for col in ["Mission Cost", "Payload Weight", "Fuel Consumption",
                "Mission Duration", "Distance from Earth", "Crew Size",
                "Mission Success", "Scientific Yield"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Mission Cost", "Payload Weight", "Fuel Consumption"]).drop_duplicates().reset_index(drop=True)
    return df


# ─────────────────────────────────────────────
# AUTH — step 0
# ─────────────────────────────────────────────
def show_login():
    st.markdown("""
    <div style='text-align:center; padding:2.5rem 0 1.2rem;'>
        <div class='hero-title' style='font-size:1.8rem;'>AEGIS MISSION CONTROL</div>
        <div class='hero-sub' style='margin-top:0.3rem; font-size:0.78rem;'>
            AEROSPACE DATA INSIGHTS SYSTEM
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        st.markdown(
            "<div style='background:rgba(0,25,70,0.7); border:1px solid rgba(0,180,255,0.2);"
            " border-radius:16px; padding:2rem 1.8rem 1.5rem;'>"
            "<p style='text-align:center; font-family:Share Tech Mono,monospace;"
            " color:#00b8ff; font-size:0.72rem; letter-spacing:0.22em; margin-bottom:1.5rem;"
            " border-bottom:1px solid rgba(0,150,255,0.15); padding-bottom:1rem;'>"
            "// SECURITY CLEARANCE REQUIRED</p>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='background:rgba(0,180,80,0.08); border:1px solid rgba(0,200,80,0.2);"
            " border-radius:8px; padding:0.6rem 1rem; margin-bottom:1rem;"
            " font-family:Share Tech Mono,monospace; font-size:0.72rem; color:#5de8a0;"
            " letter-spacing:0.1em;'>"
            "◉ DEMO &nbsp;·&nbsp; ID: <b style='color:#a0ffcc;'>admin</b>"
            " &nbsp;&nbsp;|&nbsp;&nbsp; KEY: <b style='color:#a0ffcc;'>password</b></div>",
            unsafe_allow_html=True
        )
        user = st.text_input("OPERATOR ID", placeholder="Enter operator ID...", key="login_user",
                             label_visibility="visible")
        pw   = st.text_input("ACCESS CODE", type="password", placeholder="Enter access code...",
                             key="login_pw", label_visibility="visible")

        if st.session_state.get("login_failed"):
            st.error("⛔ Access denied — invalid credentials.")

        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("⚡  AUTHENTICATE", use_container_width=True, key="btn_login"):
            if user == "admin" and pw == "password":
                st.session_state["auth"]         = True
                st.session_state["login_failed"] = False
                st.session_state["flow_step"]    = "terms"
                st.rerun()
            else:
                st.session_state["login_failed"] = True
                st.rerun()


# ─────────────────────────────────────────────
# TERMS — step 1
# ─────────────────────────────────────────────
def show_terms():
    # Door animation only on first visit to terms page
    if not st.session_state.get("door_played"):
        st.session_state["door_played"] = True
        st.markdown(
            "<div class='door-overlay'>"
            "<div class='door-left'>"
            "<div class='door-text'>ACCESS<br>GRANTED"
            "<span class='door-sub'>◉ IDENTITY CONFIRMED</span>"
            "<span class='door-sub'>◈ CLEARANCE: LEVEL 5</span>"
            "</div></div>"
            "<div class='door-right'>"
            "<div class='door-text'>SYSTEM<br>ONLINE"
            "<span class='door-sub'>◉ AEGIS V2.0 READY</span>"
            "<span class='door-sub'>◈ ALL MODULES ACTIVE</span>"
            "</div></div>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("""
    <div style='text-align:center; padding:2rem 0 1rem;'>
        <div class='hero-title' style='font-size:1.6rem;'>MISSION BRIEFING</div>
        <div class='hero-sub' style='font-size:0.75rem; margin-top:0.3rem;'>
            REVIEW TERMS BEFORE ACCESSING CLASSIFIED DATA
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class='terms-box'>
        <b style='color:#00a8e8; font-family:Orbitron,sans-serif; font-size:0.72rem;
                  letter-spacing:0.1em;'>TERMS & CONDITIONS — AEGIS PLATFORM</b><br><br>
        By accessing this system you agree to the following:<br><br>
        <b style='color:#c8e8ff;'>1. Data Usage</b> — All mission data is for educational and analytical purposes only.
        You may not redistribute or commercialise any dataset accessed through this platform.<br><br>
        <b style='color:#c8e8ff;'>2. Simulation Accuracy</b> — Physics simulations are approximations using Euler integration.
        Results are not certified for real aerospace engineering decisions.<br><br>
        <b style='color:#c8e8ff;'>3. Access Control</b> — Your credentials are personal. Do not share your login details.
        Unauthorised access attempts will be logged and reported.<br><br>
        <b style='color:#c8e8ff;'>4. Intellectual Property</b> — All dashboard design, code, and analytical frameworks
        are the intellectual property of Aerospace Data Insights. Reproduction requires written consent.<br><br>
        <b style='color:#c8e8ff;'>5. Liability</b> — The platform is provided as-is. Aerospace Data Insights accepts
        no liability for decisions made based on simulation outputs.
        </div>
        """, unsafe_allow_html=True)

        agreed = st.checkbox(
            "I have read and agree to the Terms & Conditions",
            key="terms_agreed"
        )

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("✖  DECLINE", use_container_width=True, key="btn_decline"):
                st.session_state["auth"]      = False
                st.session_state["flow_step"] = "login"
                st.rerun()
        with btn_col2:
            if st.button("✔  ACCEPT & CONTINUE", use_container_width=True, key="btn_accept"):
                if agreed:
                    st.session_state["flow_step"] = "onboarding"
                    st.rerun()
                else:
                    st.warning("Please check the box above to agree.")


# ─────────────────────────────────────────────
# ONBOARDING — step 2
# ─────────────────────────────────────────────
def show_onboarding():
    st.markdown("""
    <div style='text-align:center; padding:1.5rem 0 1rem;'>
        <div class='hero-title' style='font-size:1.6rem;'>WELCOME, OPERATOR</div>
        <div class='hero-sub' style='font-size:0.75rem; margin-top:0.3rem;'>
            QUICK ORIENTATION — 4 STEPS TO MISSION READY
        </div>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("01", "RESEARCH & PROBLEM",
         "Start here to understand rocket physics — thrust, drag, gravity — and the key research questions driving this mission."),
        ("02", "DATA PREPROCESSING",
         "Explore the cleaned mission dataset: column types, missing value handling, statistical summary, and key KPIs."),
        ("03", "EDA VISUALIZATIONS",
         "Five interactive charts — scatter, bar, line, box plot, and heatmap — each with real-world aerospace insights."),
        ("04", "PHYSICS SIMULATION",
         "Tune rocket parameters in the sidebar and run a live Euler-integration launch simulation with 4 telemetry plots."),
    ]

    _, col, _ = st.columns([1, 3, 1])
    with col:
        for num, title, desc in steps:
            st.markdown(
                "<div class='step-card' style='margin-bottom:0.75rem;'>"
                "<div class='step-num'>" + num + "</div>"
                "<div><div class='step-body-title'>" + title + "</div>"
                "<div class='step-body-text'>" + desc + "</div></div>"
                "</div>",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        tip_col1, tip_col2 = st.columns(2)
        with tip_col1:
            st.markdown("""
            <div class='glass-card' style='text-align:center; padding:1rem;'>
                <div style='font-size:1.6rem;'>🛸</div>
                <div style='font-family:Share Tech Mono,monospace; font-size:0.68rem;
                            color:#00a8e8; margin-top:0.3rem; letter-spacing:0.1em;'>
                    USE SIDEBAR<br>TO NAVIGATE
                </div>
            </div>
            """, unsafe_allow_html=True)
        with tip_col2:
            st.markdown("""
            <div class='glass-card' style='text-align:center; padding:1rem;'>
                <div style='font-size:1.6rem;'>⚙️</div>
                <div style='font-family:Share Tech Mono,monospace; font-size:0.68rem;
                            color:#00a8e8; margin-top:0.3rem; letter-spacing:0.1em;'>
                    TUNE PARAMS<br>IN SIDEBAR
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀  ENTER MISSION CONTROL", use_container_width=True, key="btn_enter"):
            st.session_state["flow_step"] = "app"
            st.rerun()


# ─────────────────────────────────────────────
# FLOW CONTROL
# ─────────────────────────────────────────────
if "flow_step" not in st.session_state:
    st.session_state["flow_step"] = "login"
if "auth" not in st.session_state:
    st.session_state["auth"] = False

step = st.session_state["flow_step"]

if step == "login":
    show_login()
    st.stop()
elif step == "terms":
    show_terms()
    st.stop()
elif step == "onboarding":
    show_onboarding()
    st.stop()
# else: step == "app" → fall through to main dashboard


# ─────────────────────────────────────────────
# LOADING (once, after onboarding)
# ─────────────────────────────────────────────
if "loaded" not in st.session_state:
    ph = st.empty()
    with ph.container():
        st.markdown(
            "<div style='text-align:center; padding:4rem 0 1rem;'>"
            "<div class='hero-title'>INITIATING LAUNCH SEQUENCE</div>"
            "<div class='hero-sub' style='margin-top:0.6rem;'>CALIBRATING TELEMETRY SYSTEMS</div>"
            "</div>",
            unsafe_allow_html=True
        )
        stages = [
            "▸ Establishing uplink to mission database...",
            "▸ Calibrating sensor arrays...",
            "▸ Initialising physics engine...",
            "▸ Rendering visualisation modules...",
            "▸ All systems nominal — GO for launch.",
        ]
        bar  = st.progress(0)
        sph  = st.empty()
        for i, stage in enumerate(stages):
            for p in range(i * 20, (i + 1) * 20 + 1):
                time.sleep(0.012)
                bar.progress(p)
            sph.markdown(
                "<p style='text-align:center; font-family:Share Tech Mono,monospace;"
                " color:#00a8e8; font-size:0.82rem; letter-spacing:0.1em;'>" + stage + "</p>",
                unsafe_allow_html=True
            )
    ph.empty()
    st.session_state["loaded"] = True

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
with st.spinner("Fetching mission telemetry..."):
    df = load_data()

data_source_note = ""
try:
    # Check if dataset is available
    found = False
    for path in ["space_missions_dataset__1_.csv", "Dataset/space_missions_dataset__1_.csv", "../Dataset/space_missions_dataset__1_.csv"]:
        try:
            test = pd.read_csv(path)
            if not test.empty:
                found = True
                break
        except Exception:
            continue
    if not found:
        raise ValueError()
except Exception:
    data_source_note = "📡 Using built-in demo dataset (Local CSV unavailable)"

# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
st.markdown(
    "<div class='hero-banner'>"
    "<div class='hero-title'>🛸 AEGIS MISSION ANALYTICS</div>"
    "<div class='hero-sub'>Rocket Launch Path &nbsp;·&nbsp; Physics Simulation &nbsp;·&nbsp; Exploratory Data Intelligence</div>"
    "<div class='hero-badge'>AEROSPACE DATA INSIGHTS SYSTEM &nbsp;·&nbsp; V2.0 &nbsp;·&nbsp; OPERATIONAL</div>"
    "</div>",
    unsafe_allow_html=True
)

if data_source_note:
    st.info(data_source_note)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='text-align:center; padding:1rem 0 1.2rem;'>"
        "<div style='font-size:2.4rem; line-height:1;'>🛸</div>"
        "<div style='font-family:Orbitron,sans-serif; font-size:0.72rem; color:#00a8e8;"
        " letter-spacing:0.18em; margin-top:0.5rem; text-transform:uppercase;'>Mission Control</div>"
        "<div style='font-family:Share Tech Mono,monospace; font-size:0.62rem;"
        " color:#2a5a7a; margin-top:0.2rem; letter-spacing:0.12em;'>AEGIS · ONLINE</div>"
        "</div>"
        "<hr style='border-color:rgba(0,150,255,0.13); margin:0 0 1rem;'>",
        unsafe_allow_html=True
    )

    menu = st.radio(
        "Navigation",
        ["🔬  Research & Problem",
         "🧹  Data Preprocessing",
         "📊  EDA Visualizations",
         "☄️   Physics Simulation"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:rgba(0,150,255,0.13); margin:1rem 0;'>", unsafe_allow_html=True)

    n_rec  = str(len(df))
    n_feat = str(df.shape[1])
    st.markdown(
        "<div style='font-family:Share Tech Mono,monospace; font-size:0.68rem;"
        " line-height:2.1; padding:0 0.3rem; color:#2a6a4a;'>"
        "◉ DATASET &nbsp;&nbsp;&nbsp; ONLINE<br>"
        "◈ RECORDS &nbsp;&nbsp; " + n_rec + "<br>"
        "◈ FEATURES &nbsp; " + n_feat + "<br>"
        "◉ STATUS &nbsp;&nbsp;&nbsp;&nbsp; NOMINAL"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<hr style='border-color:rgba(0,150,255,0.13); margin:1rem 0;'>", unsafe_allow_html=True)
    if st.button("⏏  LOGOUT", use_container_width=True, key="btn_logout"):
        for k in ["auth", "flow_step", "loaded", "login_failed", "terms_agreed", "door_played"]:
            st.session_state.pop(k, None)
        st.rerun()


# ══════════════════════════════════════════════
# SECTION 1 — RESEARCH
# ══════════════════════════════════════════════
if "Research" in menu:
    section_tag("MODULE 01 · PROBLEM UNDERSTANDING & RESEARCH")
    st.markdown("## 🔬 Mission Briefing")

    img_col, txt_col = st.columns([1, 1.6])
    with img_col:
        st.image(
            "https://images.unsplash.com/photo-1516849841032-87cbac4d88f7?w=800&q=80",
            caption="Space Shuttle Endeavour — STS-134 (NASA, 2011)",
            use_container_width=True
        )
    with txt_col:
        st.markdown(
            "<div class='glass-card'>"
            "<div class='force-title'>🌌 MISSION CONTEXT</div>"
            "<p style='color:#9ac8e0; margin:0.6rem 0 0; font-family:Rajdhani,sans-serif;'>"
            "<b style='color:#c8e8ff;'>Aerospace Data Insights</b> has tasked the project team "
            "with building an interactive analytics platform that visualises past space mission "
            "records and simulates rocket launch physics via differential equations.<br><br>"
            "The dataset captures real mission parameters — payload, fuel, cost, crew size, and "
            "success outcome — enabling data-driven decisions for future launches."
            "</p></div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div class='glass-card'>"
            "<div class='force-title' style='margin-bottom:0.6rem;'>🎯 KEY RESEARCH QUESTIONS & ANSWERS</div>"
            "<div style='color:#9ac8e0; font-family:Rajdhani,sans-serif; margin-bottom:0.8rem;'>"
            "<b style='color:#00a8e8; font-family:Share Tech Mono,monospace;'>[01]</b> <b style='color:#c8e8ff;'>How does payload mass affect altitude and fuel use?</b><br>"
            "<span style='color:#5ab8e0; font-size:0.9rem;'>An increased payload means a heavier rocket. Per F=ma, higher mass drops acceleration for a given thrust, severely limiting altitude unless exponentially more fuel is consumed.</span></div>"
            "<div style='color:#9ac8e0; font-family:Rajdhani,sans-serif; margin-bottom:0.8rem;'>"
            "<b style='color:#00a8e8; font-family:Share Tech Mono,monospace;'>[02]</b> <b style='color:#c8e8ff;'>Does higher thrust always lead to mission success?</b><br>"
            "<span style='color:#5ab8e0; font-size:0.9rem;'>Not always. While it helps overcome gravity/drag, exorbitant thrust can cause aerodynamic stress (max-Q limits) or burn through fuel too quickly before orbit is reached.</span></div>"
            "<div style='color:#9ac8e0; font-family:Rajdhani,sans-serif; margin-bottom:0.8rem;'>"
            "<b style='color:#00a8e8; font-family:Share Tech Mono,monospace;'>[03]</b> <b style='color:#c8e8ff;'>How does atmospheric drag decay with altitude?</b><br>"
            "<span style='color:#5ab8e0; font-size:0.9rem;'>Drag decays exponentially. As air rapidly thins, resistive forces disappear, making acceleration much more efficient in the upper atmosphere.</span></div>"
            "<div style='color:#9ac8e0; font-family:Rajdhani,sans-serif; margin-bottom:0.8rem;'>"
            "<b style='color:#00a8e8; font-family:Share Tech Mono,monospace;'>[04]</b> <b style='color:#c8e8ff;'>Are higher-cost missions necessarily more successful?</b><br>"
            "<span style='color:#5ab8e0; font-size:0.9rem;'>No. Exploratory EDA shows high budgets often correlate with experimental or deep-space attempts, which inherently carry higher risks of failure.</span></div>"
            "<div style='color:#9ac8e0; font-family:Rajdhani,sans-serif;'>"
            "<b style='color:#00a8e8; font-family:Share Tech Mono,monospace;'>[05]</b> <b style='color:#c8e8ff;'>How long does a rocket take to reach orbital velocity?</b><br>"
            "<span style='color:#5ab8e0; font-size:0.9rem;'>Typically ~8 to 12 minutes to hit Low Earth Orbit (LEO), heavily dependent on staging and ascent trajectory.</span></div>"
            "</div>",
            unsafe_allow_html=True
        )

    divider()
    section_tag("CORE PHYSICS ENGINE")
    st.markdown("### ⚙️ Forces Acting on a Rocket")
    c1, c2, c3 = st.columns(3)
    for col, icon, title, eq, body in zip(
        [c1, c2, c3],
        ["🔥", "🌍", "💨"],
        ["THRUST", "WEIGHT / GRAVITY", "AERODYNAMIC DRAG"],
        ["T = ṁ × vₑ", "W = m × 9.81 m/s²", "D = ½ρv²C_dA"],
        ["Upward engine force. Must exceed W + D for liftoff. Reduces as fuel burns off.",
         "Downward gravitational pull. Decreases dynamically as fuel mass depletes.",
         "Air resistance opposing motion. ρ decays exponentially: ρ = ρ₀·e^(−h/8500)"]
    ):
        with col:
            st.markdown(
                "<div class='force-card'>"
                "<span class='force-icon'>" + icon + "</span>"
                "<div class='force-title'>" + title + "</div>"
                "<div style='font-family:Share Tech Mono,monospace;font-size:0.8rem;color:#00ddff;margin:0.4rem 0 0.7rem;'>" + eq + "</div>"
                "<div class='force-body'>" + body + "</div>"
                "</div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div class='glass-card' style='text-align:center; border-color:rgba(0,190,255,0.25);'>"
        "<div class='force-title'>NET ACCELERATION — EULER INTEGRATION</div>"
        "<div style='font-family:Share Tech Mono,monospace;font-size:1.05rem;color:#00e5ff;letter-spacing:0.08em;margin:0.7rem 0;'>"
        "a = ( T &nbsp;−&nbsp; W &nbsp;−&nbsp; D ) / m_total</div>"
        "<div style='color:#5a8aaa;font-family:Rajdhani,sans-serif;font-size:0.9rem;'>"
        "At each Δt = 0.5 s:&nbsp;&nbsp;"
        "<span style='color:#5ab8e0;'>v += a·Δt</span>&nbsp;&nbsp;|&nbsp;&nbsp;"
        "<span style='color:#5ab8e0;'>h += v·Δt</span>&nbsp;&nbsp;|&nbsp;&nbsp;"
        "<span style='color:#5ab8e0;'>m_fuel −= ṁ·Δt</span></div></div>",
        unsafe_allow_html=True
    )

    divider()
    section_tag("REFERENCE CONCEPTS")
    with st.expander("◈  Escape Velocity"):
        st.markdown("<p style='color:#9ac8e0;'>Earth escape velocity = <b style='color:#00e5ff;'>~11.2 km/s</b>. Our simulation models sub-orbital trajectories requiring far less delta-v.</p>", unsafe_allow_html=True)
    with st.expander("◈  Why drag reduces at altitude"):
        st.markdown("<p style='color:#9ac8e0;'>Atmospheric density decreases exponentially (scale height ≈ 8.5 km). By 80 km altitude drag is effectively negligible — rockets accelerate far more efficiently in near-vacuum.</p>", unsafe_allow_html=True)
    with st.expander("◈  Tsiolkovsky Rocket Equation"):
        st.latex(r"\Delta v = v_e \cdot \ln\!\left(\frac{m_0}{m_f}\right)")
        st.markdown("<p style='color:#9ac8e0;'>The fundamental equation of rocketry. Explains why 80–90% of launch mass is propellant. Δv scales logarithmically with the mass ratio.</p>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SECTION 2 — PREPROCESSING
# ══════════════════════════════════════════════
elif "Preprocessing" in menu:
    section_tag("MODULE 02 · DATA PREPROCESSING & CLEANING")
    st.markdown("## 🧹 Mission Data Preparation")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Raw Data Preview")
        st.dataframe(df.head(8), use_container_width=True, height=290)
    with c2:
        st.markdown("### Column Diagnostics")
        info_df = pd.DataFrame({
            "Column":   df.columns.tolist(),
            "Dtype":    [str(t) for t in df.dtypes],
            "Non-Null": df.notnull().sum().tolist(),
            "Unique":   df.nunique().tolist(),
        })
        st.dataframe(info_df, use_container_width=True, height=290)

    divider()
    st.markdown("### Statistical Summary")
    st.dataframe(df.describe().round(2), use_container_width=True)

    divider()
    section_tag("CLEANING PIPELINE")
    for icon, title, desc in [
        ("🗓️", "DATETIME CONVERSION",
         "Converted Launch Date to datetime64 via pd.to_datetime(errors='coerce')."),
        ("🔢", "NUMERIC CASTING",
         "Cast Mission Cost, Payload Weight, Fuel Consumption, Duration, Distance, Crew Size, Mission Success using pd.to_numeric(errors='coerce')."),
        ("🚫", "MISSING VALUES",
         "Applied dropna() on key numeric columns. Final clean dataset: " + str(len(df)) + " records."),
        ("♻️", "DUPLICATE REMOVAL",
         "Applied drop_duplicates() — each mission counted exactly once."),
        ("🏷️", "COLUMN NORMALISATION",
         "Renamed all columns to consistent short names regardless of original header format (e.g. 'Distance from Earth (light-years)' → 'Distance from Earth')."),
    ]:
        st.markdown(
            "<div class='glass-card' style='display:flex;gap:1rem;align-items:flex-start;'>"
            "<div style='font-size:1.4rem;line-height:1;padding-top:2px;'>" + icon + "</div>"
            "<div><div style='font-family:Orbitron,sans-serif;font-size:0.72rem;color:#00a8e8;"
            "letter-spacing:0.1em;margin-bottom:0.3rem;'>" + title + "</div>"
            "<div style='font-family:Rajdhani,sans-serif;color:#7aaac8;font-size:0.95rem;'>" + desc + "</div>"
            "</div></div>",
            unsafe_allow_html=True
        )

    divider()
    section_tag("MISSION KPIs")
    kpi_cols = st.columns(4)

    avg_cost    = ("$" + f"{df['Mission Cost'].mean():,.1f}B")    if "Mission Cost"   in df.columns else "N/A"
    avg_payload = (f"{df['Payload Weight'].mean():,.1f} t")       if "Payload Weight" in df.columns else "N/A"
    avg_success = (f"{df['Mission Success'].mean():,.1f}%")       if "Mission Success" in df.columns else "N/A"

    for col, val, lbl in zip(kpi_cols,
        [str(len(df)), avg_cost, avg_payload, avg_success],
        ["Total Missions", "Avg Mission Cost", "Avg Payload", "Avg Success Rate"]
    ):
        with col:
            st.markdown(metric_card(val, lbl), unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SECTION 3 — EDA
# ══════════════════════════════════════════════
elif "EDA" in menu:
    section_tag("MODULE 03 · EXPLORATORY DATA ANALYSIS")
    st.markdown("## 📊 Mission Intelligence Dashboard")

    # ── Filters ──
    with st.expander("🔎  DASHBOARD FILTERS", expanded=True):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            if "Mission Success" in df.columns:
                # Bucket success into pass/fail
                df["Outcome"] = df["Mission Success"].apply(
                    lambda x: "Success (≥80%)" if x >= 80 else "Partial/Failure (<80%)"
                )
                sf_opts = ["All"] + sorted(df["Outcome"].unique().tolist())
                sf = st.selectbox("Mission Outcome", sf_opts)
            else:
                sf = "All"
        with fc2:
            if "Mission Type" in df.columns:
                tf_opts = ["All"] + sorted(df["Mission Type"].dropna().unique().tolist())
                tf = st.selectbox("Mission Type", tf_opts)
            else:
                tf = "All"
        with fc3:
            if "Launch Vehicle" in df.columns:
                vf_opts = ["All"] + sorted(df["Launch Vehicle"].dropna().unique().tolist())
                vf = st.selectbox("Launch Vehicle", vf_opts)
            else:
                vf = "All"

    fdf = df.copy()
    if sf != "All" and "Outcome" in fdf.columns:
        fdf = fdf[fdf["Outcome"] == sf]
    if tf != "All" and "Mission Type" in df.columns:
        fdf = fdf[fdf["Mission Type"] == tf]
    if vf != "All" and "Launch Vehicle" in df.columns:
        fdf = fdf[fdf["Launch Vehicle"] == vf]

    if fdf.empty:
        st.warning("No missions match the current filters. Try adjusting them.")
        st.stop()

    st.markdown(
        "<p style='font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#2a6a3a;'>"
        "◉ " + str(len(fdf)) + " MISSIONS IN CURRENT VIEW</p>",
        unsafe_allow_html=True
    )
    divider()

    # ── VIZ 1: Payload vs Fuel ──
    section_tag("VISUALIZATION 01 · SCATTER — PAYLOAD vs FUEL CONSUMPTION")
    st.markdown("### Payload Weight vs Fuel Consumption")
    v1a, v1b = st.columns([2, 1])
    with v1a:
        color_col = "Outcome" if "Outcome" in fdf.columns else None
        fig1 = px.scatter(
            fdf, x="Payload Weight", y="Fuel Consumption",
            color=color_col,
            hover_data=["Mission Name"] if "Mission Name" in fdf.columns else None,
            labels={"Payload Weight": "Payload (tons)", "Fuel Consumption": "Fuel (tons)"},
            color_discrete_sequence=["#51cf66", "#ff6b6b", "#00b8ff"]
        )
        fig1.update_traces(marker=dict(size=10, opacity=0.85))
        # Manual numpy trendline (no statsmodels needed)
        try:
            x_t = fdf["Payload Weight"].dropna().values
            y_t = fdf["Fuel Consumption"].dropna().values
            if len(x_t) >= 2:
                m, b = np.polyfit(x_t, y_t, 1)
                x_line = np.linspace(x_t.min(), x_t.max(), 100)
                fig1.add_scatter(x=x_line, y=m * x_line + b, mode="lines",
                                 name="Trend", line=dict(color="#ffd43b", width=2, dash="dot"),
                                 showlegend=False)
        except Exception:
            pass
        fig1.update_layout(**PLOT_BASE)
        st.plotly_chart(fig1, use_container_width=True)
    with v1b:
        insight(
            "<b>📡 Insight</b><br><br>"
            "Clear <b>positive correlation</b> between payload mass and fuel use.<br><br>"
            "<b>Physics:</b> F = ma — heavier payload increases total mass, requiring more thrust and more fuel.<br><br>"
            "Confirms the <b>Tsiolkovsky Rocket Equation</b>: Δv = vₑ · ln(m₀/mf)"
        )

    divider()

    # ── VIZ 2: Cost vs Mission Success ──
    section_tag("VISUALIZATION 02 · BAR CHART — COST BY MISSION SUCCESS")
    st.markdown("### Average Mission Cost (Successful vs Unsuccessful)")
    v2a, v2b = st.columns([1, 2])
    with v2a:
        insight(
            "<b>💰 Insight</b><br><br>"
            "Comparing average mission costs between successful and unsuccessful missions.<br><br>"
            "This analysis helps determine if higher capital investment directly correlates "
            "with a higher probability of mission success."
        )
    with v2b:
        if "Outcome" in fdf.columns and "Mission Cost" in fdf.columns:
            cost_df = fdf.groupby("Outcome")["Mission Cost"].mean().reset_index().sort_values("Mission Cost", ascending=False)
            fig2 = px.bar(
                cost_df, x="Outcome", y="Mission Cost",
                color="Outcome",
                labels={"Mission Cost": "Avg Cost (billion USD)", "Outcome": "Mission Outcome"},
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig2.update_layout(**PLOT_BASE, showlegend=False)
            fig2.update_traces(marker_line_width=0)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Required columns not available.")

    divider()

    # ── VIZ 3 & 4 ──
    v3c, v4c = st.columns(2)
    with v3c:
        section_tag("VIZ 03 · SCATTER — DISTANCE vs DURATION")
        st.markdown("### Distance from Earth vs Mission Duration")
        if "Distance from Earth" in fdf.columns and "Mission Duration" in fdf.columns:
            color_col3 = "Mission Type" if "Mission Type" in fdf.columns else None
            fig3 = px.scatter(
                fdf, x="Distance from Earth", y="Mission Duration",
                color=color_col3,
                hover_data=["Mission Name"] if "Mission Name" in fdf.columns else None,
                labels={"Distance from Earth": "Distance (ly)", "Mission Duration": "Duration (yrs)"},
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            # Manual numpy trendline
            try:
                x_t = fdf["Distance from Earth"].dropna().values
                y_t = fdf["Mission Duration"].dropna().values
                if len(x_t) >= 2:
                    m, b = np.polyfit(x_t, y_t, 1)
                    x_line = np.linspace(x_t.min(), x_t.max(), 100)
                    fig3.add_scatter(x=x_line, y=m * x_line + b, mode="lines",
                                     name="Trend", line=dict(color="#ffd43b", width=2, dash="dot"),
                                     showlegend=False)
            except Exception:
                pass
            fig3.update_layout(**PLOT_BASE)
            st.plotly_chart(fig3, use_container_width=True)
            insight("Deeper space = longer mission. Confirms distance scales with travel time — critical for crew life support planning.")
        else:
            st.info("Required columns not available.")

    with v4c:
        section_tag("VIZ 04 · BOX PLOT — COST BY VEHICLE")
        st.markdown("### Mission Cost by Launch Vehicle")
        if "Mission Cost" in fdf.columns and "Launch Vehicle" in fdf.columns:
            fig4 = px.box(
                fdf, x="Launch Vehicle", y="Mission Cost",
                color="Launch Vehicle",
                labels={"Mission Cost": "Cost (billion USD)"},
                color_discrete_sequence=["#00b8ff", "#ff6b6b", "#51cf66", "#ffd43b", "#cc5de8"]
            )
            fig4.update_layout(**PLOT_BASE, showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)
            insight("Box plots reveal cost spread per vehicle. Outliers represent unusually expensive missions — useful for fleet budget planning.")
        else:
            st.info("Required columns not available.")

    divider()

    # ── VIZ 5: Heatmap ──
    section_tag("VISUALIZATION 05 · CORRELATION HEATMAP")
    st.markdown("### Feature Correlation Matrix")
    numeric_cols = ["Payload Weight", "Fuel Consumption", "Mission Cost",
                    "Mission Duration", "Distance from Earth", "Crew Size",
                    "Mission Success", "Scientific Yield"]
    avail_num = [c for c in numeric_cols if c in fdf.columns]
    if len(avail_num) >= 2:
        corr = fdf[avail_num].corr()
        fig5 = px.imshow(
            corr, text_auto=".2f", aspect="auto",
            color_continuous_scale=[[0, "#180025"], [0.5, "#002880"], [1, "#00e5ff"]],
            zmin=-1, zmax=1
        )
        fig5.update_layout(**PLOT_BASE, height=480)
        fig5.update_traces(textfont=dict(family="Share Tech Mono", size=10, color="#c8e8ff"))
        st.plotly_chart(fig5, use_container_width=True)
        insight(
            "<b>📐 Pearson Correlation:</b> Values near ±1 = strong relationship. "
            "The Fuel–Payload link mathematically validates VIZ 01. "
            "Distance and Duration are highly correlated — deeper missions take longer."
        )
    else:
        st.info("Not enough numeric columns for heatmap.")

    # ── VIZ 6: Bonus ──
    if "Crew Size" in fdf.columns and "Scientific Yield" in fdf.columns:
        divider()
        section_tag("VISUALIZATION 06 · BONUS — CREW SIZE vs SCIENTIFIC YIELD")
        st.markdown("### Crew Size vs Scientific Yield")
        color_col6 = "Mission Type" if "Mission Type" in fdf.columns else None
        size_col6  = "Mission Cost"  if "Mission Cost"  in fdf.columns else None
        fig6 = px.scatter(
            fdf, x="Crew Size", y="Scientific Yield",
            color=color_col6, size=size_col6,
            hover_data=["Mission Name"] if "Mission Name" in fdf.columns else None,
            labels={"Crew Size": "Crew Size", "Scientific Yield": "Scientific Yield (pts)"},
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig6.update_layout(**PLOT_BASE)
        st.plotly_chart(fig6, use_container_width=True)
        insight("Bubble size = mission cost. Larger crews don't always yield more science — smaller focused research missions can outperform.")


# ══════════════════════════════════════════════
# SECTION 4 — SIMULATION
# ══════════════════════════════════════════════
elif "Simulation" in menu:
    section_tag("MODULE 04 · PHYSICS SIMULATION ENGINE")
    st.markdown("## ☄️ Rocket Launch Simulator")

    img_c, math_c = st.columns([1, 2])
    with img_c:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Falcon_Heavy_Demo_Mission_%2840126461851%29.jpg/800px-Falcon_Heavy_Demo_Mission_%2840126461851%29.jpg",
            caption="SpaceX Falcon Heavy — KSC, 2018",
            use_container_width=True
        )
    with math_c:
        st.markdown(
            "<div class='glass-card'>"
            "<div class='force-title'>📐 MATHEMATICAL FOUNDATION — EULER INTEGRATION</div>"
            "<table style='width:100%;border-collapse:collapse;font-family:Rajdhani,sans-serif;margin-top:0.8rem;'>"
            "<thead><tr>"
            "<th style='color:#00a8e8;padding:6px 12px;text-align:left;font-family:Orbitron,sans-serif;font-size:0.7rem;'>FORCE</th>"
            "<th style='color:#00a8e8;padding:6px 12px;text-align:left;font-family:Orbitron,sans-serif;font-size:0.7rem;'>EQUATION</th>"
            "<th style='color:#00a8e8;padding:6px 12px;text-align:left;font-family:Orbitron,sans-serif;font-size:0.7rem;'>DIR</th>"
            "</tr></thead><tbody>"
            "<tr><td style='padding:5px 12px;color:#c8e0f8;'>Thrust T</td>"
            "<td style='padding:5px 12px;color:#55aad8;font-family:Share Tech Mono,monospace;'>Constant (engine)</td>"
            "<td style='padding:5px 12px;color:#51cf66;'>↑</td></tr>"
            "<tr><td style='padding:5px 12px;color:#c8e0f8;'>Weight W</td>"
            "<td style='padding:5px 12px;color:#55aad8;font-family:Share Tech Mono,monospace;'>m_total × 9.81</td>"
            "<td style='padding:5px 12px;color:#ff6b6b;'>↓</td></tr>"
            "<tr><td style='padding:5px 12px;color:#c8e0f8;'>Drag D</td>"
            "<td style='padding:5px 12px;color:#55aad8;font-family:Share Tech Mono,monospace;'>½ρv²C_d A</td>"
            "<td style='padding:5px 12px;color:#ff6b6b;'>↓</td></tr>"
            "</tbody></table>"
            "<div style='font-family:Share Tech Mono,monospace;font-size:0.84rem;color:#00ddff;"
            "letter-spacing:0.04em;margin-top:1rem;line-height:1.9;'>"
            "a = (T − W − D) / m_total<br>"
            "ρ(h) = ρ₀ · exp(−h / 8500)<br>"
            "v += a·Δt &nbsp;|&nbsp; h += v·Δt &nbsp;|&nbsp; m_fuel −= ṁ·Δt"
            "</div></div>",
            unsafe_allow_html=True
        )

    divider()
    section_tag("FLIGHT PARAMETERS")

    st.sidebar.markdown(
        "<hr style='border-color:rgba(0,150,255,0.13);'>"
        "<div style='font-family:Orbitron,sans-serif;font-size:0.7rem;color:#00a8e8;"
        "letter-spacing:0.12em;margin-bottom:0.5rem;'>⚙ SIMULATION PARAMS</div>",
        unsafe_allow_html=True
    )
    initial_mass   = st.sidebar.number_input("Dry Mass (kg)",          min_value=1000, value=15000, step=1000)
    fuel_mass      = st.sidebar.number_input("Initial Fuel Mass (kg)", min_value=1000, value=25000, step=1000)
    payload_weight = st.sidebar.slider("Payload (kg)",     100,    10000,  2000)
    thrust         = st.sidebar.slider("Thrust (N)",       100000, 2000000, 600000, step=50000)
    drag_factor    = st.sidebar.slider("Drag Factor C_d",  0.1,    5.0,    0.8)
    burn_rate      = st.sidebar.slider("Burn Rate (kg/s)", 10,     500,    150)

    total_liftoff = initial_mass + fuel_mass + payload_weight
    twr           = thrust / (total_liftoff * 9.81)
    burn_time     = fuel_mass / burn_rate

    pa, pb, pc, pd_ = st.columns(4)
    for col, lbl, val in zip(
        [pa, pb, pc, pd_],
        ["Liftoff Mass", "Thrust/Weight", "Burn Duration", "Est. MECO"],
        [str(f"{total_liftoff:,}") + " kg", str(round(twr, 2)),
         str(int(burn_time)) + " s", "T+" + str(int(burn_time)) + "s"]
    ):
        with col:
            st.markdown(metric_card(val, lbl), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if twr < 1.0:
        st.error("⚠️ TWR = " + str(round(twr, 2)) + " — Insufficient thrust! Increase thrust or reduce mass.")
    else:
        st.success("✅ TWR = " + str(round(twr, 2)) + " — Trajectory nominal. Ready for ignition.")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀  IGNITE — BEGIN SIMULATION", use_container_width=True):
        t_list, alt_list, vel_list, acc_list, mass_list = [], [], [], [], []
        cur_alt  = 0.0
        cur_vel  = 0.0
        cur_fuel = float(fuel_mass)
        dt       = 0.5

        with st.spinner("▸ Running Euler integration..."):
            for t in np.arange(0, 300, dt):
                m_total  = initial_mass + payload_weight + cur_fuel
                rho      = 1.225 * np.exp(-cur_alt / 8500.0)
                w_force  = m_total * 9.81
                d_force  = 0.5 * rho * (cur_vel ** 2) * drag_factor * np.sign(cur_vel)
                thr      = float(thrust) if cur_fuel > 0 else 0.0
                if cur_fuel > 0:
                    cur_fuel = max(0.0, cur_fuel - burn_rate * dt)
                acc      = (thr - w_force - d_force) / m_total
                cur_vel += acc * dt
                cur_alt += cur_vel * dt
                if cur_alt < 0:
                    cur_alt, cur_vel = 0.0, 0.0
                    if t > 5:
                        break
                t_list.append(round(t, 2))
                alt_list.append(cur_alt)
                vel_list.append(cur_vel)
                acc_list.append(acc)
                mass_list.append(m_total)

        sim_df = pd.DataFrame({
            "Time (s)":           t_list,
            "Altitude (m)":       alt_list,
            "Velocity (m/s)":     vel_list,
            "Acceleration (m/s²)": acc_list,
            "Total Mass (kg)":    mass_list,
        })

        max_alt = max(alt_list)
        max_vel = max(vel_list)

        st.markdown(
            "<div class='glass-card' style='text-align:center;border-color:rgba(0,225,255,0.28);'>"
            "<span style='font-family:Share Tech Mono,monospace;font-size:0.78rem;color:#00ddff;letter-spacing:0.13em;'>"
            "◉ SIMULATION COMPLETE &nbsp;·&nbsp; "
            "MAX ALT: " + f"{max_alt:,.0f}" + " m &nbsp;·&nbsp; "
            "MAX VEL: " + f"{max_vel:,.1f}" + " m/s &nbsp;·&nbsp; "
            "MECO: T+" + str(int(burn_time)) + "s"
            "</span></div>",
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        for col, lbl, val in zip(
            [s1, s2, s3, s4],
            ["Max Altitude", "Max Velocity", "MECO Time", "Dry + Payload"],
            [f"{max_alt:,.0f} m", f"{max_vel:,.1f} m/s",
             str(int(burn_time)) + " s",
             str(f"{initial_mass + payload_weight:,}") + " kg"]
        ):
            with col:
                st.markdown(metric_card(val, lbl), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        COLORS = ["#00e5ff", "#ff6b6b", "#69db7c", "#cc5de8"]

        r1c1, r1c2 = st.columns(2)
        for col, y_col, title, color, ins_txt in zip(
            [r1c1, r1c2],
            ["Altitude (m)", "Velocity (m/s)"],
            ["🏔 Altitude Profile", "⚡ Velocity Profile"],
            [COLORS[0], COLORS[1]],
            ["Altitude climbs rapidly as fuel depletes and atmosphere thins. Orange dot = MECO.",
             "Velocity peaks at MECO then gravity decelerates ascent."]
        ):
            with col:
                fig = px.line(sim_df, x="Time (s)", y=y_col, title=title,
                              color_discrete_sequence=[color])
                fig.add_vline(x=burn_time, line_dash="dot", line_color="#ffd43b",
                              annotation_text="MECO", annotation_font_color="#ffd43b",
                              annotation_position="top right")
                fig.update_layout(**PLOT_BASE)
                st.plotly_chart(fig, use_container_width=True)
                insight(ins_txt)

        st.markdown("<br>", unsafe_allow_html=True)
        r2c1, r2c2 = st.columns(2)
        for col, y_col, title, color, ins_txt in zip(
            [r2c1, r2c2],
            ["Acceleration (m/s²)", "Total Mass (kg)"],
            ["📈 Acceleration Profile", "⚖ Mass Depletion"],
            [COLORS[2], COLORS[3]],
            ["Acceleration rises as mass drops. Goes negative post-MECO as gravity dominates.",
             "Fuel burns linearly. Post-MECO curve flattens — dry mass + payload remains."]
        ):
            with col:
                fig = px.line(sim_df, x="Time (s)", y=y_col, title=title,
                              color_discrete_sequence=[color])
                fig.add_vline(x=burn_time, line_dash="dot", line_color="#ffd43b",
                              annotation_text="MECO", annotation_font_color="#ffd43b",
                              annotation_position="top right")
                fig.update_layout(**PLOT_BASE)
                st.plotly_chart(fig, use_container_width=True)
                insight(ins_txt)

        divider()
        section_tag("RAW TELEMETRY DATA")
        st.dataframe(sim_df.round(3), use_container_width=True, height=300)
        st.download_button(
            "⬇  EXPORT TELEMETRY AS CSV",
            data=sim_df.to_csv(index=False).encode("utf-8"),
            file_name="aegis_telemetry.csv",
            mime="text/csv",
            use_container_width=True
        )