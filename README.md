# 🚀 Space Mission Launch Path Explorer

**Student Name:** Aditya Jitendra Kumar Sahani  
**Student ID:** 1000414  
**Course:** Artificial Intelligence  
**Focus:** Mathematics for AI-I
**Assessment Type:** Submative Assessment  (SA)  

## 📌 Project Overview

This Streamlit web application provides an interactive dashboard for visualizing and analyzing **500 real-world space mission records**. The app applies **mathematical and statistical reasoning** — including Newton's Second Law, differential equations, and correlation analysis — to explore how factors like fuel, payload, cost, and crew size influence mission success.

Built as part of **Scenario 1: Rocket Launch Path Visualization**, the app mirrors real-world aerospace data science workflows used by engineers and mission planners.

---

## 🌐 Live Web App
> **🔗 [[Click here to open the live Streamlit ap](https://idai104-1000414-aditya-jitendra-kumar-sahani-sa.streamlit.app/)](#)**  
---

## 🎯 What Does This App Visualise?

| Section | Visualisations |
|---|---|
| 📊 Overview & EDA | Box Plot (Success by Mission Type), Bar Chart (Launch Vehicles), Correlation Heatmap |
| 🔥 Fuel & Payload | Scatter Plot (Payload vs Fuel), Scatter + Trendline (Distance vs Duration), Bar (Fuel Efficiency) |
| 💰 Cost Analysis | Scatter (Cost vs Success), Bar (Avg Cost by Category), Line Plot (Scientific Yield over Time) |
| 🛸 Simulation | Live Rocket Launch Simulation using differential equations (altitude, velocity, acceleration) |
| 🧠 Insights & Report | Key findings, Dataset Explorer, Mission Type Distribution Pie Chart |

---

## 🔬 Research Context — Newton's Second Law Applied

Rockets follow **F = ma**, where:
- **Thrust** (engine force, upward) 
- **Gravity** = mass × 9.81 m/s² (downward)  
- **Drag** = air resistance (decreases at altitude as air gets thinner)
- As **fuel burns → mass decreases → acceleration increases**

**Differential equation used in simulation:**
```
a(t) = [Thrust − m(t)×g − 0.5×Cd×ρ(h)×v(t)²×A] / m(t)
v(t+1) = v(t) + a(t) × Δt
h(t+1) = h(t) + v(t) × Δt
m(t+1) = m(t) − fuel_burn_rate × Δt
```

---

## 📁 Repository Structure

```
📦 IDAI104-1000414-ADITYA-JITENDRA-KUMAR-SAHANI-SA
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── space_missions_dataset__1_.csv  # Dataset (500 missions)
└── README.md                       # This file
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone this repository
git clone https://github.com/IDAI104-1000414-ADITYA-JITENDRA-KUMAR-SAHANI-SA
cd IDAI104-1000414-ADITYA-JITENDRA-KUMAR-SAHANI-SA

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## ☁️ How to Deploy on Streamlit Cloud

1. Push all files to your GitHub repository
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **"Deploy an app"**
4. Select your GitHub repo and set `app.py` as the main file
5. Click **Deploy** — your live link will be generated!

---

## 🧠 Key Insights from the Data

1. **Heavier Payloads → More Fuel Consumed** — Confirms Newton's Second Law: greater mass requires greater thrust and fuel.
2. **High Cost ≠ High Success** — No strong correlation between mission budget and success rate.
3. **Distance Drives Duration** — Farther targets require proportionally longer missions and more fuel.
4. **Launch Vehicle Matters** — Starship handles heavier payloads; Falcon Heavy excels in fuel efficiency.
5. **Research Missions Deliver Most Scientific Value** — Highest average scientific yield across all mission types.

---

## 🛠️ Technologies Used

| Tool | Purpose |
|---|---|
| `Streamlit` | Interactive web dashboard |
| `Pandas` | Data loading, cleaning & analysis |
| `NumPy` | Numerical simulation (differential equations) |
| `Plotly` | Interactive charts (scatter, bar, box, line) |
| `Seaborn` | Statistical heatmap & line plots |
| `Matplotlib` | Supporting static charts |
| `Statsmodels` | Trendline (OLS regression) in scatter plots |

---

## 📋 Assessment Checklist

- [x] Problem Understanding & Research (Newton's Law, rocket dynamics)
- [x] Data Preprocessing & Cleaning (date conversion, type casting, null handling)
- [x] 5+ Compulsory Visualisations (scatter, bar, line, box, heatmap)
- [x] Rocket Launch Simulation (differential equations, step-by-step)
- [x] Interactive Streamlit controls (sliders, dropdowns, multiselects)
- [x] GitHub Repository with README & requirements.txt
- [x] Streamlit Cloud Deployment

---


*🌌 Aerospace Data Insights | Mathematics for AI-I Summative Assessment*

