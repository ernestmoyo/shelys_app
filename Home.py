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

# Page config
st.set_page_config(
    page_title="Malack Sales Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    /* Global */
    .block-container { padding-top: 1.5rem; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1628 0%, #1a2744 100%);
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li {
        color: #e0e0e0 !important;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #0066CC 0%, #0052a3 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,102,204,0.3);
    }
    .kpi-card h3 { margin: 0; font-size: 0.85rem; opacity: 0.85; font-weight: 400; }
    .kpi-card h1 { margin: 0.3rem 0 0 0; font-size: 2rem; font-weight: 700; }

    .kpi-card-green {
        background: linear-gradient(135deg, #2EC4B6 0%, #1a9e92 100%);
        padding: 1.2rem; border-radius: 12px; color: white;
        text-align: center; box-shadow: 0 4px 15px rgba(46,196,182,0.3);
    }
    .kpi-card-green h3 { margin: 0; font-size: 0.85rem; opacity: 0.85; font-weight: 400; }
    .kpi-card-green h1 { margin: 0.3rem 0 0 0; font-size: 2rem; font-weight: 700; }

    .kpi-card-orange {
        background: linear-gradient(135deg, #FF6B35 0%, #e05520 100%);
        padding: 1.2rem; border-radius: 12px; color: white;
        text-align: center; box-shadow: 0 4px 15px rgba(255,107,53,0.3);
    }
    .kpi-card-orange h3 { margin: 0; font-size: 0.85rem; opacity: 0.85; font-weight: 400; }
    .kpi-card-orange h1 { margin: 0.3rem 0 0 0; font-size: 2rem; font-weight: 700; }

    .kpi-card-purple {
        background: linear-gradient(135deg, #7209B7 0%, #5c0796 100%);
        padding: 1.2rem; border-radius: 12px; color: white;
        text-align: center; box-shadow: 0 4px 15px rgba(114,9,183,0.3);
    }
    .kpi-card-purple h3 { margin: 0; font-size: 0.85rem; opacity: 0.85; font-weight: 400; }
    .kpi-card-purple h1 { margin: 0.3rem 0 0 0; font-size: 2rem; font-weight: 700; }

    /* Welcome banner */
    .welcome-banner {
        background: linear-gradient(135deg, #0a1628 0%, #1a3a5c 50%, #0066CC 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    .welcome-banner h1 { font-size: 2.2rem; margin-bottom: 0.3rem; }
    .welcome-banner p { opacity: 0.85; font-size: 1.05rem; }

    /* Nav cards */
    .nav-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e8ecf1;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: all 0.2s;
        height: 100%;
    }
    .nav-card:hover {
        box-shadow: 0 6px 20px rgba(0,102,204,0.15);
        border-color: #0066CC;
    }
    .nav-card h3 { color: #0066CC; margin-bottom: 0.5rem; }
    .nav-card p { color: #555; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

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
