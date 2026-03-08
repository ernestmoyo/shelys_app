"""
Sales Dashboard - Interactive Analytics
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_customer_data, PRODUCTS, get_top_clients
from utils.charts import (
    territory_pie, category_bar, product_sales_bar,
    location_treemap, top_clients_bar, product_radar, sales_heatmap,
)

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .metric-card {
        background: white; padding: 1rem; border-radius: 10px;
        border-left: 4px solid #0066CC; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .metric-card h4 { color: #666; font-size: 0.8rem; margin: 0; }
    .metric-card h2 { color: #1a1a2e; margin: 0.2rem 0 0 0; }
</style>
""", unsafe_allow_html=True)

df = load_customer_data()
if df.empty:
    st.error("No data available.")
    st.stop()

st.title("Sales Dashboard")
st.markdown("Interactive analytics across territories, channels, products, and locations.")

# Filters
with st.sidebar:
    st.header("Filters")
    territories = st.multiselect("Territory", df["TERRITORY"].unique(), default=list(df["TERRITORY"].unique()))
    categories = st.multiselect("Channel", df["CATEGORY"].unique(), default=list(df["CATEGORY"].unique()))
    locations = st.multiselect("Location", sorted(df["LOCATION"].unique()), default=[])
    selected_products = st.multiselect("Products", PRODUCTS, default=PRODUCTS)

# Apply filters
filtered = df.copy()
if territories:
    filtered = filtered[filtered["TERRITORY"].isin(territories)]
if categories:
    filtered = filtered[filtered["CATEGORY"].isin(categories)]
if locations:
    filtered = filtered[filtered["LOCATION"].isin(locations)]

# Filtered KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Clients", f"{len(filtered):,}")
with col2:
    st.metric("Total Units", f"{filtered['Total Units'].sum():,}")
with col3:
    st.metric("Avg Units/Client", f"{filtered['Total Units'].mean():,.0f}")
with col4:
    st.metric("Locations", f"{filtered['LOCATION'].nunique()}")
with col5:
    best_product = max(selected_products, key=lambda p: filtered[p].sum()) if selected_products else "N/A"
    st.metric("Top Product", best_product)

st.markdown("---")

# Row 1: Territory & Category
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(territory_pie(filtered), use_container_width=True)
with col2:
    st.plotly_chart(category_bar(filtered), use_container_width=True)

# Row 2: Product performance
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(product_sales_bar(filtered, selected_products), use_container_width=True)
with col2:
    st.plotly_chart(product_radar(filtered, selected_products), use_container_width=True)

# Row 3: Location analysis
st.plotly_chart(location_treemap(filtered), use_container_width=True)

# Row 4: Heatmap & Top clients
col1, col2 = st.columns([1.2, 0.8])
with col1:
    st.plotly_chart(sales_heatmap(filtered, selected_products), use_container_width=True)
with col2:
    n_top = st.slider("Top N Clients", 5, 30, 15)
    st.plotly_chart(top_clients_bar(filtered, n_top), use_container_width=True)

# Data table
with st.expander("View Raw Data"):
    display_cols = ["Client ID", "CLIENT NAME", "LOCATION", "TERRITORY", "CATEGORY"] + selected_products + ["Total Units"]
    st.dataframe(
        filtered[display_cols].sort_values("Total Units", ascending=False),
        use_container_width=True,
        height=400,
    )
