import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
import datetime
import time
from streamlit_autorefresh import st_autorefresh

# ----------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------
st.set_page_config(page_title="AI Sustainability Dashboard", layout="wide")

# ----------------------------------------------------
# AUTO REFRESH
# ----------------------------------------------------
st_autorefresh(interval=3000, key="realtime_refresh")

# ----------------------------------------------------
# LIVE CARBON INTENSITY API
# ----------------------------------------------------
def get_live_carbon():
    try:
        url = "https://api.carbonintensity.org.uk/intensity"
        res = requests.get(url).json()
        return res["data"][0]["intensity"]["actual"]
    except:
        return 300

live_carbon = get_live_carbon()

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.title("🟢 Executive AI Sustainability Dashboard")
st.markdown("🔴 **LIVE AI Sustainability Monitoring System**")
st.markdown("---")

# ----------------------------------------------------
# SIDEBAR CONTROLS
# ----------------------------------------------------
st.sidebar.header("⚙ AI Emission Controls")

deepseek = st.sidebar.slider("DeepSeek CO2 per Query (g)", 0.01, 10.0, 5.0)
gpt4 = st.sidebar.slider("GPT-4 CO2 per Query (g)", 0.01, 5.0, 0.5)
claude_opus = st.sidebar.slider("Claude 3 Opus CO2 per Query (g)", 0.01, 5.0, 0.5)
gemini_ultra = st.sidebar.slider("Gemini Ultra CO2 per Query (g)", 0.01, 5.0, 0.5)
gpt4o = st.sidebar.slider("GPT-4o CO2 per Query (g)", 0.01, 2.0, 0.15)
gpt35 = st.sidebar.slider("GPT-3.5 CO2 per Query (g)", 0.01, 1.0, 0.05)
gemini_pro = st.sidebar.slider("Gemini Pro CO2 per Query (g)", 0.01, 1.0, 0.05)
claude_haiku = st.sidebar.slider("Claude Haiku CO2 per Query (g)", 0.01, 1.0, 0.05)
gemini_flash = st.sidebar.slider("Gemini Flash CO2 per Query (g)", 0.01, 1.0, 0.03)

queries = st.sidebar.slider("Total Daily AI Queries", 100, 10000, 1000, step=100)

migration_pct = st.sidebar.slider(
    "GPT-4 Queries Migrated → Gemini Flash (%)",
    0,
    100,
    30,
    step=5
)

# ----------------------------------------------------
# REAL TIME QUERY LOGGER
# ----------------------------------------------------
models = [
    "GPT-4",
    "GPT-4o",
    "GPT-3.5",
    "Gemini-Pro",
    "Gemini-Flash",
    "Claude-Haiku"
]

if "query_logs" not in st.session_state:
    st.session_state.query_logs = []

model_used = np.random.choice(models)
timestamp = datetime.datetime.now()

co2_lookup = {
    "GPT-4": gpt4,
    "GPT-4o": gpt4o,
    "GPT-3.5": gpt35,
    "Gemini-Pro": gemini_pro,
    "Gemini-Flash": gemini_flash,
    "Claude-Haiku": claude_haiku
}

co2_emission = co2_lookup[model_used]

new_log = {
    "Time": timestamp.strftime("%H:%M:%S"),
    "Model": model_used,
    "CO2 (g)": round(co2_emission, 3)
}

st.session_state.query_logs.append(new_log)

if len(st.session_state.query_logs) > 100:
    st.session_state.query_logs.pop(0)

query_df = pd.DataFrame(st.session_state.query_logs)

# ----------------------------------------------------
# LIVE SUSTAINABILITY SCORE
# ----------------------------------------------------
live_total_emissions = query_df["CO2 (g)"].sum()
sustainability_score = max(0, 100 - (live_total_emissions * 0.5))

# ----------------------------------------------------
# HERO METRICS
# ----------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Corporate Sustainability Score", f"{sustainability_score:.2f}")

with col2:
    st.metric("Live Grid Carbon Intensity", f"{live_carbon} gCO2/kWh")

with col3:
    st.metric("Total CO2 Emissions", f"{live_total_emissions:.2f} g")

with col4:
    st.metric("Total Queries Logged", len(query_df))

st.markdown("---")

# ----------------------------------------------------
# LIVE AI ACTIVITY FEED
# ----------------------------------------------------
st.subheader("🔴 Live AI Activity Feed")

st.dataframe(
    query_df.sort_index(ascending=False),
    use_container_width=True
)

st.markdown("---")

# ----------------------------------------------------
# MODEL USAGE TRACKER
# ----------------------------------------------------
st.subheader("Live Model Usage Distribution")

usage = query_df["Model"].value_counts().reset_index()
usage.columns = ["Model", "Queries"]

fig_usage = px.bar(
    usage,
    x="Model",
    y="Queries",
    color="Queries"
)

st.plotly_chart(fig_usage, use_container_width=True)

# ----------------------------------------------------
# REAL TIME EMISSION TRACKER
# ----------------------------------------------------
st.subheader("Real-Time CO2 Emission Distribution")

emission_df = query_df.groupby("Model")["CO2 (g)"].sum().reset_index()

fig_emission = px.pie(
    emission_df,
    names="Model",
    values="CO2 (g)"
)

st.plotly_chart(fig_emission, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------
# RADAR ANALYTICS
# ----------------------------------------------------
parameters = [
    'Query Frequency',
    'Model Selection',
    'Query Complexity',
    'Time-of-Use',
    'Daily Carbon',
    'Session Efficiency'
]

weights = [20, 25, 15, 10, 20, 10]

user_performance = [
    min(20, len(query_df)/5),
    migration_pct/4,
    14,
    8,
    max(5, 20 - live_total_emissions/100),
    8
]

st.subheader("Algorithm Parameter Breakdown")

fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=weights,
    theta=parameters,
    fill='toself',
    name='Max Allocation'
))

fig_radar.add_trace(go.Scatterpolar(
    r=user_performance,
    theta=parameters,
    fill='toself',
    name='Current Performance'
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 30]))
)

st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------
# SUSTAINABILITY GAUGE
# ----------------------------------------------------
st.subheader("AI Sustainability Risk Indicator")

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=sustainability_score,
    title={'text': "Sustainability Score"},
    gauge={
        'axis': {'range': [0,100]},
        'steps': [
            {'range': [0,60], 'color': "red"},
            {'range': [60,80], 'color': "yellow"},
            {'range': [80,100], 'color': "lightgreen"}
        ],
    }
))

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------
# PEAK USAGE ALERT SYSTEM
# ----------------------------------------------------
st.subheader("AI Load Monitoring")

current_queries = len(query_df)

if current_queries > 80:
    st.error("⚠ High AI traffic detected — emissions rising")

elif current_queries > 40:
    st.warning("⚡ Moderate AI usage")

else:
    st.success("🌱 AI usage within sustainable limits")

st.markdown("---")

# ----------------------------------------------------
# STRATEGY SIMULATOR
# ----------------------------------------------------
st.subheader("Strategy Simulator")

gpt4_queries = queries * (1 - migration_pct/100)
gemini_flash_queries = queries * (migration_pct/100)

original_emissions = queries * gpt4

new_emissions = (
    gpt4_queries * gpt4 +
    gemini_flash_queries * gemini_flash
)

savings = original_emissions - new_emissions

st.info(f"Predicted Daily Carbon Savings: **{savings:.2f} g CO2**")

efficiency_gain = migration_pct * 0.15

st.success(f"Projected Model Efficiency Increase: **+{efficiency_gain:.2f}%**")

st.metric("Total Queries Analysed", queries)

st.markdown("---")

# ----------------------------------------------------
# AI RECOMMENDATION ENGINE
# ----------------------------------------------------
st.subheader("AI Sustainability Recommendations")

if migration_pct < 40:
    st.warning("⚠ Increase lightweight model migration to reduce emissions.")

if queries > 5000:
    st.info("💡 High AI usage detected. Consider batching requests or lighter models.")

if savings > 200:
    st.success("✅ Current strategy significantly reduces carbon emissions.")

if sustainability_score > 80:
    st.success("🌱 Your AI infrastructure is operating sustainably.")
