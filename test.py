import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Sustainability Dashboard", layout="wide")

# --- MOCK DATA BASED ON ALGORITHM DOCUMENT ---
# User A - Sustainable Profile Example
hero_metrics = {
    "Score": 85.8,
    "MSE": 93.3,
    "CFD": 0.85,
    "TUA": 80.0
}

# CO2 Emissions per Query by Model (in grams)
model_emissions = pd.DataFrame({
    "Model": ["DeepSeek", "GPT-4", "Claude-3-Opus", "Gemini-Ultra", "GPT-4o", "GPT-3.5", "Gemini-Pro", "Claude-Haiku", "Gemini-Flash"],
    "CO2 (g)": [5.0, 0.5, 0.5, 0.5, 0.15, 0.05, 0.05, 0.05, 0.03]
}).sort_values(by="CO2 (g)", ascending=True)

# Parameter Weights for Radar Chart
parameters = ['Query Frequency (QF)', 'Model Selection (MSE)', 'Query Complexity (QCS)', 
              'Time-of-Use (TUA)', 'Daily Carbon (CFD)', 'Session Efficiency (SDE)']
weights = [20, 25, 15, 10, 20, 10]
user_performance = [18, 23, 14, 8, 17, 8] # Simulated user component scores out of their max weights

# --- DASHBOARD HEADER ---
st.title("🟢 Executive AI Sustainability Dashboard")
st.markdown("Monitor, analyze, and optimize corporate AI usage to reduce environmental impact.")
st.markdown("---")

# --- HERO METRICS (TOP ROW) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Corporate Sustainability Score", value=f"{hero_metrics['Score']} / 100", delta="Good", delta_color="normal")
with col2:
    st.metric(label="Model Selection Efficiency (MSE)", value=f"{hero_metrics['MSE']}%", delta="+8.3% vs Last Month")
with col3:
    st.metric(label="Daily Carbon Footprint (CFD)", value=f"{hero_metrics['CFD']}g CO2", delta="-0.2g vs Last Month", delta_color="inverse")
with col4:
    st.metric(label="Time-of-Use Awareness (TUA)", value=f"{hero_metrics['TUA']}%", delta="Peak Green Hours")

st.markdown("---")

# --- STRATEGIC VISUALIZATIONS (MIDDLE ROW) ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Algorithm Parameter Breakdown")
    # Radar Chart
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=weights,
        theta=parameters,
        fill='toself',
        name='Max Weight Allocation',
        line_color='lightgrey'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=user_performance,
        theta=parameters,
        fill='toself',
        name='Current Corporate Performance',
        line_color='green'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 30])), showlegend=True)
    st.plotly_chart(fig_radar, use_container_width=True)

with col_right:
    st.subheader("CO2 Emissions per Query by AI Model")
    # Horizontal Bar Chart
    fig_bar = px.bar(model_emissions, x="CO2 (g)", y="Model", orientation='h',
                     color="CO2 (g)", color_continuous_scale="RdYlGn_r",
                     text="CO2 (g)")
    fig_bar.update_layout(xaxis_title="CO2 (grams/query)", yaxis_title="AI Model")
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# --- PREDICTIVE ANALYTICS (BOTTOM ROW) ---
col_bottom_left, col_bottom_right = st.columns(2)

with col_bottom_left:
    st.subheader("Temporal Carbon Intensity")
    st.markdown("AI query volume overlaid with regional renewable energy availability.")
    
    # Simulated time-series data
    hours = list(range(24))
    query_volume = np.random.normal(50, 15, 24).astype(int)
    grid_carbon = [abs(np.sin(h/4) * 100) for h in hours] # Simulating low carbon mid-day
    
    df_temporal = pd.DataFrame({"Hour": hours, "Query Volume": query_volume, "Grid Carbon Intensity": grid_carbon})
    
    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(x=df_temporal["Hour"], y=df_temporal["Grid Carbon Intensity"], 
                                  fill='tozeroy', name="Carbon Intensity", line_color='lightcoral'))
    fig_area.add_trace(go.Scatter(x=df_temporal["Hour"], y=df_temporal["Query Volume"], 
                                  name="AI Queries", line_color='blue', mode='lines+markers'))
    fig_area.update_layout(xaxis_title="Hour of Day (0-23)", yaxis_title="Volume / Intensity")
    st.plotly_chart(fig_area, use_container_width=True)

with col_bottom_right:
    st.subheader("Strategy Simulator: Migration Impact")
    st.markdown("Estimate the impact of shifting heavy model usage to lightweight models.")
    
    migration_pct = st.slider("Percentage of GPT-4 queries migrated to Gemini-Flash:", min_value=0, max_value=100, value=30, step=5)
    
    # Simple calculation for simulation
    original_emissions = 1000 * 0.5  # Assume 1000 GPT-4 queries
    new_emissions = ((1000 * (1 - migration_pct/100)) * 0.5) + ((1000 * (migration_pct/100)) * 0.03)
    savings = original_emissions - new_emissions
    
    st.info(f"**Predicted Daily Carbon Savings:** {savings:.1f} grams of CO2")
    st.success(f"**Projected MSE Increase:** +{migration_pct * 0.15:.1f}%")