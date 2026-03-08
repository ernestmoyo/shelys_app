"""
Malack Sales Suite - Main Entry Point
Shelys Pharmaceuticals (Aspen Pharma) | DSM & Tanga Region
"""

import streamlit as st
import sys
from pathlib import Path

# Add app root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.data_loader import load_customer_data, PRODUCTS
from utils.styles import inject_css

# Page config
st.set_page_config(
    page_title="Malack Sales Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# Sidebar
with st.sidebar:
    st.markdown("### Malack Sales Suite")
    st.markdown("**Shelys Pharmaceuticals**")
    st.markdown("*(Aspen Pharma)*")
    st.markdown("---")
    st.markdown("**Malack A. Tweve**")
    st.markdown("DSM & Tanga Region")
    st.markdown("---")
    st.markdown("##### Navigation")
    st.markdown("""
    - **Home** - Overview & KPIs
    - **Dashboard** - Interactive Analytics
    - **CRM** - Client Management
    - **Forecasting** - Sales Projections
    - **Reports** - Export & PDF
    """)

# Load data
df = load_customer_data()

if df.empty:
    st.error("Could not load customer data. Please check the data files.")
    st.stop()

# Welcome banner
st.markdown("""
<div class="welcome-banner">
    <h1>Malack Sales Suite</h1>
    <p>Shelys Pharmaceuticals (Aspen Pharma) &mdash; DSM & Tanga Regional Sales Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# KPI Row
total_clients = len(df)
total_units = df["Total Units"].sum()
dsm_count = len(df[df["TERRITORY"] == "DSM"])
tanga_count = len(df[df["TERRITORY"] == "Tanga"])
avg_units = df["Total Units"].mean()
num_locations = df["LOCATION"].nunique()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <h3>Total Clients</h3>
        <h1>{total_clients:,}</h1>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="kpi-card-green">
        <h3>Total Product Units</h3>
        <h1>{total_units:,}</h1>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="kpi-card-orange">
        <h3>Avg Units / Client</h3>
        <h1>{avg_units:,.0f}</h1>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="kpi-card-purple">
        <h3>Active Locations</h3>
        <h1>{num_locations}</h1>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Territory split
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <h3>DSM Territory</h3>
        <h1>{dsm_count} clients</h1>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="kpi-card-green">
        <h3>Tanga Territory</h3>
        <h1>{tanga_count} clients</h1>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Quick product overview
st.markdown("### Product Portfolio Overview")
prod_cols = st.columns(len(PRODUCTS))
colors = ["kpi-card", "kpi-card-green", "kpi-card-orange", "kpi-card-purple", "kpi-card"]
for i, product in enumerate(PRODUCTS):
    with prod_cols[i]:
        total = df[product].sum()
        st.markdown(f"""
        <div class="{colors[i % len(colors)]}" style="padding: 1rem;">
            <h3>{product}</h3>
            <h1 style="font-size: 1.5rem;">{total:,}</h1>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Navigation cards
st.markdown("### Quick Navigation")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="nav-card">
        <h3>📊 Sales Dashboard</h3>
        <p>Interactive charts, territory analysis, product performance, and location insights.</p>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="nav-card">
        <h3>👥 Client CRM</h3>
        <p>Search, filter, and manage your 427 clients. Track contacts and categories.</p>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="nav-card">
        <h3>📈 Forecasting</h3>
        <p>2026 sales projections, growth targets, and territory potential analysis.</p>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="nav-card">
        <h3>📄 Reports</h3>
        <p>Generate PDF summaries and Excel exports for management reporting.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Malack Sales Suite v1.0 | Built for Shelys Pharmaceuticals (Aspen Pharma)")
