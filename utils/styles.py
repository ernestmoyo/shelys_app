"""
Shared CSS styles for the Malack Sales Suite.
All UI/UX audit fixes applied here.
"""

GLOBAL_CSS = """
<style>
/* ── GLOBAL RESET & TYPOGRAPHY ─────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Source Sans 3', sans-serif !important;
}

.block-container { padding-top: 1.5rem; }

/* ── MAIN APP BACKGROUND ────────────────────────────────── */
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #F4F6FA !important;
}

/* ── SIDEBAR – FIX CONTRAST ISSUE ──────────────────────── */
[data-testid="stSidebar"] {
    background-image: linear-gradient(180deg, #0A1628 0%, #1A2744 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}

[data-testid="stSidebar"] * {
    color: #E8EDF5 !important;
}

[data-testid="stSidebar"] a {
    color: #FFFFFF !important;
    text-decoration: none !important;
    transition: color 0.2s ease !important;
}

[data-testid="stSidebar"] a:hover {
    color: #5BA3F5 !important;
}

[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
}

/* ── WELCOME BANNER ─────────────────────────────────────── */
.welcome-banner {
    background: linear-gradient(135deg, #0A1628 0%, #1B3A5C 45%, #0D5FBF 100%) !important;
    border-radius: 16px !important;
    padding: 2.5rem 2rem !important;
    box-shadow: 0 8px 32px rgba(13,95,191,0.25) !important;
    border: 1px solid rgba(91,163,245,0.2) !important;
    color: white;
    margin-bottom: 1.5rem;
}
.welcome-banner h1 { font-size: 2.2rem; margin-bottom: 0.3rem; color: white !important; }
.welcome-banner p { opacity: 0.85; font-size: 1.05rem; color: white !important; }

/* ── KPI CARDS – FIX NUMBER WRAPPING ───────────────────── */
.kpi-card,
.kpi-card-green,
.kpi-card-orange,
.kpi-card-purple {
    border-radius: 16px !important;
    padding: 1.5rem 1rem !important;
    text-align: center !important;
    min-width: 140px !important;
    width: 100% !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    overflow: hidden !important;
    color: white;
}

.kpi-card:hover,
.kpi-card-green:hover,
.kpi-card-orange:hover,
.kpi-card-purple:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.2) !important;
}

.kpi-card h1,
.kpi-card-green h1,
.kpi-card-orange h1,
.kpi-card-purple h1 {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    line-height: 1.2 !important;
    margin: 0.5rem 0 !important;
    letter-spacing: -0.5px !important;
    color: white !important;
}

.kpi-card h3,
.kpi-card-green h3,
.kpi-card-orange h3,
.kpi-card-purple h3 {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    opacity: 0.85 !important;
    margin: 0 0 0.25rem 0 !important;
    color: white !important;
}

/* Harmonised colour palette */
.kpi-card {
    background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%) !important;
    box-shadow: 0 6px 20px rgba(21,101,192,0.35) !important;
}
.kpi-card-green {
    background: linear-gradient(135deg, #00897B 0%, #00695C 100%) !important;
    box-shadow: 0 6px 20px rgba(0,137,123,0.35) !important;
}
.kpi-card-orange {
    background: linear-gradient(135deg, #E65100 0%, #BF360C 100%) !important;
    box-shadow: 0 6px 20px rgba(230,81,0,0.35) !important;
}
.kpi-card-purple {
    background: linear-gradient(135deg, #5E35B1 0%, #4527A0 100%) !important;
    box-shadow: 0 6px 20px rgba(94,53,177,0.35) !important;
}

/* ── SECTION HEADINGS ───────────────────────────────────── */
[data-testid="stMain"] h2,
[data-testid="stMain"] h3 {
    color: #0D1B2A !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px !important;
}

/* ── QUICK NAVIGATION CARDS ─────────────────────────────── */
.nav-card {
    background: #FFFFFF !important;
    border: 1px solid #DCE4F0 !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
    box-shadow: 0 2px 12px rgba(13,27,42,0.07) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
    cursor: pointer !important;
    height: 100%;
}
.nav-card:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 8px 24px rgba(13,95,191,0.15) !important;
    border-color: #5BA3F5 !important;
}
.nav-card h3 {
    color: #1565C0 !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem !important;
    line-height: 1.3 !important;
}
.nav-card p {
    color: #4A5568 !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
    margin: 0 !important;
}

/* ── TARGET CARDS (Forecasting) ──────────────────────────── */
.target-card {
    background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%) !important;
    padding: 1.2rem; border-radius: 14px;
    border-left: 4px solid #1565C0;
    margin-bottom: 0.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.target-card h4 { color: #1565C0 !important; margin: 0; font-weight: 600; }
.target-card p { margin: 0.3rem 0 0 0; font-size: 1.4rem; font-weight: 700; color: #0D1B2A !important; }

/* ── REPORT CARDS ────────────────────────────────────────── */
.report-card {
    background: #FFFFFF !important;
    padding: 1.5rem;
    border-radius: 14px;
    border: 1px solid #DCE4F0;
    box-shadow: 0 2px 12px rgba(13,27,42,0.07);
    text-align: center;
    height: 100%;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.report-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(13,95,191,0.12);
}
.report-card h3 { color: #1565C0 !important; font-weight: 700; }
.report-card p { color: #4A5568 !important; font-size: 0.9rem; line-height: 1.6; }

/* ── CLIENT CARDS (CRM) ─────────────────────────────────── */
.client-card {
    background: #FFFFFF; padding: 1.2rem; border-radius: 14px;
    border: 1px solid #DCE4F0; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 0.8rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.client-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}
.client-card h4 { color: #1565C0 !important; margin: 0 0 0.3rem 0; font-weight: 700; }
.client-card p { margin: 0.1rem 0; color: #4A5568; font-size: 0.9rem; }

.tag {
    display: inline-block; padding: 0.2rem 0.7rem; border-radius: 20px;
    font-size: 0.75rem; font-weight: 600; margin-right: 0.3rem;
}
.tag-pharmacy { background: #e3f2fd; color: #1565C0; }
.tag-dldm { background: #e8f5e9; color: #2e7d32; }
.tag-shop { background: #fff3e0; color: #e65100; }
.tag-supermarket { background: #fce4ec; color: #c62828; }
.tag-dsm { background: #f3e5f5; color: #5E35B1; }
.tag-tanga { background: #e0f2f1; color: #00695c; }

/* ── METRIC CARD (Dashboard) ─────────────────────────────── */
.metric-card {
    background: #FFFFFF; padding: 1rem; border-radius: 12px;
    border-left: 4px solid #1565C0; box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
.metric-card h4 { color: #4A5568; font-size: 0.8rem; margin: 0; }
.metric-card h2 { color: #0D1B2A; margin: 0.2rem 0 0 0; }

/* ── SCROLLBAR STYLING ───────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F4F6FA; }
::-webkit-scrollbar-thumb { background: #C5CEE0; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #5BA3F5; }

/* ── STREAMLIT OVERRIDES ─────────────────────────────────── */
[data-testid="stHeader"] {
    background-color: transparent !important;
    border-bottom: none !important;
}
[data-testid="stBottom"] {
    background-color: #F4F6FA !important;
}
footer, .reportview-container .main footer {
    color: #8896A5 !important;
    font-size: 0.8rem !important;
}
[data-testid="baseButton-secondary"] {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

/* ── PRODUCT PORTFOLIO CARDS – Fix number wrap ──────────── */
[data-testid="stMain"] [style*="padding: 1rem"] h1 {
    font-size: 1.5rem !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
</style>
"""


def inject_css():
    """Inject global CSS into the Streamlit page."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
