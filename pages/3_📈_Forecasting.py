"""
Sales Forecasting - 2026 Projections & Growth Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_customer_data, PRODUCTS
from utils.forecasting import (
    TARGETS, generate_quarterly_targets, generate_monthly_forecast,
    generate_historical_baseline, client_growth_forecast,
    territory_growth_potential,
)
from utils.charts import BRAND_COLORS, forecast_line, kpi_gauge, _apply_layout

st.set_page_config(page_title="Sales Forecasting", page_icon="📈", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .target-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.2rem; border-radius: 12px; border-left: 4px solid #0066CC;
        margin-bottom: 0.5rem;
    }
    .target-card h4 { color: #0066CC; margin: 0; }
    .target-card p { margin: 0.3rem 0 0 0; font-size: 1.4rem; font-weight: 700; color: #1a1a2e; }
</style>
""", unsafe_allow_html=True)

df = load_customer_data()
if df.empty:
    st.error("No data available.")
    st.stop()

st.title("Sales Forecasting")
st.markdown("2026 projections based on the Shelys Sales & Marketing Plan targets.")

# 2026 Targets overview
st.markdown("### 2026 Strategic Targets")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="target-card">
        <h4>Revenue Growth</h4>
        <p>{TARGETS['revenue_growth']*100:.0f}%</p>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="target-card">
        <h4>New Clients</h4>
        <p>{TARGETS['new_clients']}</p>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="target-card">
        <h4>Retention Rate</h4>
        <p>{TARGETS['retention_rate']*100:.0f}%</p>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="target-card">
        <h4>Target Clients</h4>
        <p>{TARGETS['target_clients']}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# KPI Gauges
st.markdown("### Progress Tracking")
col1, col2, col3 = st.columns(3)
with col1:
    fig = kpi_gauge(len(df), TARGETS["target_clients"], "Client Base")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    current_units = df["Total Units"].sum()
    target_units = int(current_units * (1 + TARGETS["revenue_growth"]))
    fig = kpi_gauge(current_units, target_units, "Total Units")
    st.plotly_chart(fig, use_container_width=True)
with col3:
    avg_units = df["Total Units"].mean()
    target_avg = avg_units * 1.15
    fig = kpi_gauge(avg_units, target_avg, "Avg Units/Client")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Monthly Forecast
st.markdown("### Monthly Sales Forecast")
historical = generate_historical_baseline(df)
forecast = generate_monthly_forecast(df)
st.plotly_chart(forecast_line(historical, forecast), use_container_width=True)

# Quarterly Targets
st.markdown("### Quarterly Targets Breakdown")
quarterly = generate_quarterly_targets(df, PRODUCTS)

col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=quarterly["Quarter"], y=quarterly["Total_Current"],
        name="Current Pace", marker_color=BRAND_COLORS[1],
    ))
    fig.add_trace(go.Bar(
        x=quarterly["Quarter"], y=quarterly["Total_Target"],
        name="2026 Target", marker_color=BRAND_COLORS[0],
    ))
    fig.update_layout(barmode="group", title="Quarterly: Current vs Target")
    _apply_layout(fig, "Quarterly: Current vs Target", 400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Product-level quarterly
    product_q = []
    for _, row in quarterly.iterrows():
        for p in PRODUCTS:
            product_q.append({
                "Quarter": row["Quarter"],
                "Product": p,
                "Target": row[f"{p}_Target"],
            })
    pq_df = pd.DataFrame(product_q)
    fig = px.bar(pq_df, x="Quarter", y="Target", color="Product",
                 color_discrete_sequence=BRAND_COLORS, title="Product Targets by Quarter")
    _apply_layout(fig, "Product Targets by Quarter", 400)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Client Growth Forecast
st.markdown("### Client Growth Projection")
growth = client_growth_forecast()

col1, col2 = st.columns([1.5, 1])
with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=growth["Month"], y=growth["Total Clients"],
        mode="lines+markers", name="Projected Clients",
        line=dict(color=BRAND_COLORS[0], width=3),
    ))
    fig.add_trace(go.Scatter(
        x=growth["Month"], y=growth["Target"],
        mode="lines", name="Target (512)",
        line=dict(color=BRAND_COLORS[4], width=2, dash="dash"),
    ))
    _apply_layout(fig, "Client Base Growth", 400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=growth["Month"], y=growth["New Clients"],
                         name="New", marker_color=BRAND_COLORS[3]))
    fig.add_trace(go.Bar(x=growth["Month"], y=-growth["Churned"],
                         name="Churned", marker_color=BRAND_COLORS[4]))
    _apply_layout(fig, "Monthly New vs Churned", 400)
    fig.update_layout(barmode="relative")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Territory Growth Potential
st.markdown("### Territory Growth Potential Analysis")
potential = territory_growth_potential(df, PRODUCTS)

col1, col2 = st.columns([1.5, 1])
with col1:
    fig = px.scatter(
        potential, x="Clients", y="Avg_Units",
        size="Total_Units", color="Growth_Potential",
        hover_name="LOCATION",
        color_discrete_map={"High": "#E71D36", "Medium": "#FF6B35", "Low": "#2EC4B6"},
        title="Location Growth Matrix",
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### High Growth Locations")
    high_growth = potential[potential["Growth_Potential"] == "High"].sort_values("Performance_Index")
    for _, row in high_growth.head(10).iterrows():
        st.markdown(
            f"**{row['LOCATION']}** ({row['TERRITORY']}) — "
            f"{row['Clients']} clients, Index: {row['Performance_Index']}"
        )

    st.markdown("#### Top Performing Locations")
    top_perf = potential[potential["Growth_Potential"] == "Low"].sort_values("Performance_Index", ascending=False)
    for _, row in top_perf.head(5).iterrows():
        st.markdown(
            f"**{row['LOCATION']}** ({row['TERRITORY']}) — "
            f"{row['Clients']} clients, Index: {row['Performance_Index']}"
        )
