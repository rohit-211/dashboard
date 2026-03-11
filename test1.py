import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime
from streamlit_autorefresh import st_autorefresh

# ----------------------------------------------------
# AUTO REFRESH
# ----------------------------------------------------
st_autorefresh(interval=5000, key="dashboardrefresh")

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(page_title="AI Sustainability Dashboard", layout="wide")

st.title("🟢 Executive AI Sustainability Dashboard")
st.markdown("Monitor, analyze, and optimize corporate AI usage to reduce environmental impact.")
st.markdown("---")

# ----------------------------------------------------
# HERO METRICS
# ----------------------------------------------------
hero_metrics = {
    "Score": 85.8,
    "MSE": 93.3,
    "CFD": 0.85,
    "TUA": 80.0
}

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Corporate Sustainability Score", f"{hero_metrics['Score']} / 100", "Good")

with col2:
    st.metric("Model Selection Efficiency", f"{hero_metrics['MSE']}%", "+8.3% vs Last Month")

with col3:
    st.metric("Daily Carbon Footprint", f"{hero_metrics['CFD']} g CO2", "-0.2g vs Last Month")

with col4:
    st.metric("Time-of-Use Awareness", f"{hero_metrics['TUA']}%", "Peak Green Hours")

st.markdown("---")

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------
st.sidebar.header("⚙ AI Emission Controls")

deepseek = st.sidebar.slider("DeepSeek CO2 per Query (g)",0.01,10.0,5.0)
gpt4 = st.sidebar.slider("GPT-4 CO2 per Query (g)",0.01,5.0,0.5)
claude_opus = st.sidebar.slider("Claude 3 Opus CO2 per Query (g)",0.01,5.0,0.5)
gemini_ultra = st.sidebar.slider("Gemini Ultra CO2 per Query (g)",0.01,5.0,0.5)
gpt4o = st.sidebar.slider("GPT-4o CO2 per Query (g)",0.01,2.0,0.15)
gpt35 = st.sidebar.slider("GPT-3.5 CO2 per Query (g)",0.01,1.0,0.05)
gemini_pro = st.sidebar.slider("Gemini Pro CO2 per Query (g)",0.01,1.0,0.05)
claude_haiku = st.sidebar.slider("Claude Haiku CO2 per Query (g)",0.01,1.0,0.05)
gemini_flash = st.sidebar.slider("Gemini Flash CO2 per Query (g)",0.01,1.0,0.03)

st.sidebar.markdown("---")

queries = st.sidebar.slider("Total Daily AI Queries",100,10000,1000,step=100)

migration_pct = st.sidebar.slider(
"GPT-4 Queries Migrated → Gemini Flash (%)",
0,100,30,step=5
)

# ----------------------------------------------------
# QUERY DISTRIBUTION
# ----------------------------------------------------
gpt4_queries = queries * (1 - migration_pct/100)
gemini_flash_queries = queries * (migration_pct/100)

# ----------------------------------------------------
# TOTAL EMISSIONS
# ----------------------------------------------------
total_emissions = {
"DeepSeek":deepseek*queries*0.02,
"GPT-4":gpt4*gpt4_queries,
"Claude-3-Opus":claude_opus*queries*0.05,
"Gemini-Ultra":gemini_ultra*queries*0.05,
"GPT-4o":gpt4o*queries*0.08,
"GPT-3.5":gpt35*queries*0.2,
"Gemini-Pro":gemini_pro*queries*0.15,
"Claude-Haiku":claude_haiku*queries*0.1,
"Gemini-Flash":gemini_flash*gemini_flash_queries
}

model_emissions=pd.DataFrame({
"Model":list(total_emissions.keys()),
"Total CO2 (g)":list(total_emissions.values())
}).sort_values(by="Total CO2 (g)",ascending=True)

# ----------------------------------------------------
# DYNAMIC RADAR PARAMETERS
# ----------------------------------------------------
query_score=min(20,(queries/5000)*20)
model_score=min(25,(migration_pct/100)*25)
complexity_score=min(15,(gpt4+claude_opus+gemini_ultra)*2)
time_score=min(10,(hero_metrics["TUA"]/100)*10)
carbon_score=min(20,(hero_metrics["CFD"]/2)*20)
session_score=min(10,(migration_pct/100)*10)

user_performance=[
query_score,
model_score,
complexity_score,
time_score,
carbon_score,
session_score
]

parameters=[
'Query Frequency',
'Model Selection',
'Query Complexity',
'Time-of-Use',
'Daily Carbon',
'Session Efficiency'
]

weights=[20,25,15,10,20,10]

# ----------------------------------------------------
# MAIN VISUALIZATION
# ----------------------------------------------------
col_left,col_right=st.columns(2)

with col_left:

    st.subheader("Algorithm Parameter Breakdown")

    fig_radar=go.Figure()

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
    polar=dict(radialaxis=dict(visible=True,range=[0,30])),
    template="plotly_white"
    )

    st.plotly_chart(fig_radar,use_container_width=True)

with col_right:

    st.subheader("Total CO2 Emissions by AI Model")

    fig_bar=px.bar(
    model_emissions,
    x="Total CO2 (g)",
    y="Model",
    orientation='h',
    color="Total CO2 (g)",
    color_continuous_scale="RdYlGn_r",
    text="Total CO2 (g)"
    )

    st.plotly_chart(fig_bar,use_container_width=True)

st.markdown("---")

# ----------------------------------------------------
# RISK GAUGE
# ----------------------------------------------------
st.subheader("AI Sustainability Risk Indicator")

fig=go.Figure(go.Indicator(
mode="gauge+number",
value=hero_metrics["Score"],
title={'text':"Sustainability Score"},
gauge={
'axis':{'range':[0,100]},
'steps':[
{'range':[0,60],'color':"red"},
{'range':[60,80],'color':"yellow"},
{'range':[80,100],'color':"lightgreen"}
]
}
))

st.plotly_chart(fig,use_container_width=True)

st.markdown("---")

# ----------------------------------------------------
# TEMPORAL CARBON ANALYSIS (FIXED)
# ----------------------------------------------------
col_bottom_left,col_bottom_right=st.columns(2)

with col_bottom_left:

    st.subheader("Temporal Carbon Intensity")

    hours=list(range(24))

    base_queries=queries/24

    query_volume=[
    int(base_queries*(1+0.6*np.sin(h/3)))
    for h in hours
    ]

    grid_carbon=[
    300+100*np.sin((h-6)/4)
    for h in hours
    ]

    df_temporal=pd.DataFrame({
    "Hour":hours,
    "Query Volume":query_volume,
    "Grid Carbon":grid_carbon
    })

    fig_area=go.Figure()

    fig_area.add_trace(go.Scatter(
    x=df_temporal["Hour"],
    y=df_temporal["Grid Carbon"],
    fill='tozeroy',
    name="Grid Carbon Intensity",
    line=dict(width=3)
    ))

    fig_area.add_trace(go.Scatter(
    x=df_temporal["Hour"],
    y=df_temporal["Query Volume"],
    mode='lines+markers',
    name="AI Queries",
    line=dict(width=3)
    ))

    fig_area.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Intensity / Queries",
    template="plotly_white"
    )

    st.plotly_chart(fig_area,use_container_width=True)

# ----------------------------------------------------
# STRATEGY SIMULATOR
# ----------------------------------------------------
with col_bottom_right:

    st.subheader("Strategy Simulator")

    original_emissions=queries*gpt4

    new_emissions=(gpt4_queries*gpt4+gemini_flash_queries*gemini_flash)

    savings=original_emissions-new_emissions

    st.info(f"Predicted Daily Carbon Savings: **{savings:.2f} g CO2**")

    efficiency_gain=migration_pct*0.15

    st.success(f"Projected Model Efficiency Increase: **+{efficiency_gain:.2f}%**")

    st.metric("Total Queries Analysed",queries)

st.markdown("---")

# ----------------------------------------------------
# REAL TIME MONITORING
# ----------------------------------------------------
st.header("🔴 Real-Time AI Monitoring System")

models=["GPT-4","GPT-4o","GPT-3.5","Gemini-Pro","Gemini-Flash","Claude-Haiku"]

if "logs" not in st.session_state:
    st.session_state.logs=[]

model=np.random.choice(models)
timestamp=datetime.datetime.now().strftime("%H:%M:%S")
co2=np.random.uniform(0.02,0.5)

st.session_state.logs.append({
"Time":timestamp,
"Model":model,
"CO2":co2
})

if len(st.session_state.logs)>50:
    st.session_state.logs.pop(0)

log_df=pd.DataFrame(st.session_state.logs)

st.subheader("Live AI Query Feed")
st.dataframe(log_df,use_container_width=True)

st.subheader("Live Model Usage")

usage=log_df["Model"].value_counts().reset_index()
usage.columns=["Model","Queries"]

fig_usage=px.bar(usage,x="Model",y="Queries",color="Queries")
st.plotly_chart(fig_usage,use_container_width=True)

st.subheader("Live CO2 Emission Distribution")

emissions=log_df.groupby("Model")["CO2"].sum().reset_index()

fig_pie=px.pie(emissions,names="Model",values="CO2")
st.plotly_chart(fig_pie,use_container_width=True)

total_live_co2=log_df["CO2"].sum()
live_score=max(0,100-total_live_co2*5)

st.metric("Dynamic Sustainability Score",round(live_score,2))

if len(log_df)>40:
    st.error("⚠ High AI traffic detected")
else:
    st.success("🌱 AI usage within sustainable limits")
