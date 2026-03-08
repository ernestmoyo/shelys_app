"""
CRM - Client Relationship Manager
Search, filter, manage, and analyze clients.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_customer_data, PRODUCTS
from utils.charts import BRAND_COLORS
from utils.styles import inject_css
import plotly.express as px

st.set_page_config(page_title="Client CRM", page_icon="👥", layout="wide")
inject_css()

df = load_customer_data()
if df.empty:
    st.error("No data available.")
    st.stop()

st.title("Client CRM")
st.markdown("Search, filter, and manage your client portfolio.")

# Search and filter bar
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    search = st.text_input("Search clients", placeholder="Type a client name, location, or contact...")
with col2:
    territory_filter = st.selectbox("Territory", ["All"] + list(df["TERRITORY"].unique()))
with col3:
    category_filter = st.selectbox("Channel", ["All"] + list(df["CATEGORY"].unique()))
with col4:
    sort_by = st.selectbox("Sort by", ["Total Units (High)", "Total Units (Low)", "Name (A-Z)", "Name (Z-A)"])

# Apply filters
filtered = df.copy()
if search:
    search_lower = search.lower()
    filtered = filtered[
        filtered["CLIENT NAME"].str.lower().str.contains(search_lower, na=False) |
        filtered["LOCATION"].str.lower().str.contains(search_lower, na=False) |
        filtered["CONTACT"].str.lower().str.contains(search_lower, na=False)
    ]
if territory_filter != "All":
    filtered = filtered[filtered["TERRITORY"] == territory_filter]
if category_filter != "All":
    filtered = filtered[filtered["CATEGORY"] == category_filter]

# Sort
sort_map = {
    "Total Units (High)": ("Total Units", False),
    "Total Units (Low)": ("Total Units", True),
    "Name (A-Z)": ("CLIENT NAME", True),
    "Name (Z-A)": ("CLIENT NAME", False),
}
sort_col, sort_asc = sort_map[sort_by]
filtered = filtered.sort_values(sort_col, ascending=sort_asc)

# Results summary
st.markdown(f"**{len(filtered):,}** clients found")
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs(["Client List", "Client Cards", "Analytics"])

with tab1:
    # Interactive data table
    display_cols = [
        "Client ID", "CLIENT NAME", "LOCATION", "CONTACT",
        "CATEGORY", "TERRITORY",
    ] + PRODUCTS + ["Total Units"]

    st.dataframe(
        filtered[display_cols],
        use_container_width=True,
        height=500,
        column_config={
            "Client ID": st.column_config.NumberColumn("ID", width="small"),
            "CLIENT NAME": st.column_config.TextColumn("Client Name", width="medium"),
            "CONTACT": st.column_config.TextColumn("Contact", width="medium"),
            "Total Units": st.column_config.ProgressColumn(
                "Total Units", min_value=0, max_value=int(df["Total Units"].max()),
                format="%d",
            ),
        },
    )

with tab2:
    # Card view
    page_size = 20
    total_pages = max(1, (len(filtered) - 1) // page_size + 1)
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    start = (page - 1) * page_size
    end = start + page_size

    for _, row in filtered.iloc[start:end].iterrows():
        cat_class = f"tag-{row['CATEGORY'].lower()}"
        ter_class = f"tag-{row['TERRITORY'].lower()}"
        st.markdown(f"""
        <div class="client-card">
            <h4>{row['CLIENT NAME']}</h4>
            <p>📍 {row['LOCATION']} &nbsp;|&nbsp; 📞 {row['CONTACT']}</p>
            <p>
                <span class="tag {cat_class}">{row['CATEGORY']}</span>
                <span class="tag {ter_class}">{row['TERRITORY']}</span>
            </p>
            <p style="margin-top: 0.5rem; font-weight: 600;">
                Total: {row['Total Units']:,} units &nbsp;|&nbsp;
                Action: {row['Action']:,} &nbsp; GMLT: {row['GMLT']:,} &nbsp;
                GMCT: {row['GMCT']:,} &nbsp; WWGW: {row['WWGW']:,} &nbsp; BTZ: {row['BTZ']:,}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.caption(f"Page {page} of {total_pages}")

with tab3:
    # Analytics for filtered set
    st.markdown("### Filtered Client Analytics")

    col1, col2 = st.columns(2)
    with col1:
        # Category distribution
        cat_counts = filtered["CATEGORY"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig = px.pie(cat_counts, values="Count", names="Category",
                     color_discrete_sequence=BRAND_COLORS, title="Channel Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Units distribution
        fig = px.histogram(filtered, x="Total Units", nbins=25,
                          color_discrete_sequence=BRAND_COLORS, title="Units Distribution")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Product comparison for filtered clients
    product_totals = {p: filtered[p].sum() for p in PRODUCTS}
    prod_df = pd.DataFrame(list(product_totals.items()), columns=["Product", "Units"])
    fig = px.bar(prod_df, x="Product", y="Units", color="Product",
                 color_discrete_map={
                     "Action": BRAND_COLORS[0], "GMLT": BRAND_COLORS[1],
                     "GMCT": BRAND_COLORS[2], "WWGW": BRAND_COLORS[3], "BTZ": BRAND_COLORS[4],
                 },
                 title="Product Sales for Filtered Clients")
    st.plotly_chart(fig, use_container_width=True)

    # Top locations in filtered set
    loc_stats = filtered.groupby("LOCATION").agg(
        Clients=("Client ID", "count"), Units=("Total Units", "sum")
    ).reset_index().sort_values("Units", ascending=False).head(15)

    fig = px.bar(loc_stats, x="Units", y="LOCATION", orientation="h",
                 color_discrete_sequence=BRAND_COLORS, title="Top Locations")
    fig.update_layout(yaxis=dict(autorange="reversed"), height=450)
    st.plotly_chart(fig, use_container_width=True)

# Client detail view
st.markdown("---")
st.markdown("### Client Detail View")
client_names = filtered["CLIENT NAME"].tolist()
if client_names:
    selected_client = st.selectbox("Select a client", client_names)
    client = filtered[filtered["CLIENT NAME"] == selected_client].iloc[0]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        **{client['CLIENT NAME']}**
        - **Location:** {client['LOCATION']}
        - **Territory:** {client['TERRITORY']}
        - **Channel:** {client['CATEGORY']}
        - **Contact:** {client['CONTACT']}
        - **Total Units:** {client['Total Units']:,}
        """)
    with col2:
        client_products = pd.DataFrame({
            "Product": PRODUCTS,
            "Units": [client[p] for p in PRODUCTS],
        })
        fig = px.bar(client_products, x="Product", y="Units",
                     color="Product", color_discrete_sequence=BRAND_COLORS,
                     title=f"Product Breakdown - {client['CLIENT NAME']}")
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
