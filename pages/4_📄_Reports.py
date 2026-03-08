"""
Reports - Generate PDF & Excel exports.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_customer_data, PRODUCTS
from utils.report_generator import generate_executive_summary, generate_client_list_excel
from utils.forecasting import (
    generate_quarterly_targets, client_growth_forecast,
    territory_growth_potential, TARGETS,
)

st.set_page_config(page_title="Reports", page_icon="📄", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .report-card {
        background: white; padding: 1.5rem; border-radius: 12px;
        border: 1px solid #e8ecf1; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center; height: 100%;
    }
    .report-card h3 { color: #0066CC; }
    .report-card p { color: #555; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

df = load_customer_data()
if df.empty:
    st.error("No data available.")
    st.stop()

st.title("Report Generator")
st.markdown("Export professional reports for management and fieldwork.")

st.markdown("---")

# Report options
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="report-card">
        <h3>📊 Executive Summary</h3>
        <p>Full PDF report with KPIs, product performance, territory breakdown, top clients, and location analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("Generate Executive PDF", use_container_width=True, type="primary"):
        with st.spinner("Generating PDF report..."):
            pdf_bytes = generate_executive_summary(df, PRODUCTS)
            st.download_button(
                label="Download Executive Summary PDF",
                data=pdf_bytes,
                file_name="Malack_Executive_Summary_2026.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        st.success("Report generated successfully!")

with col2:
    st.markdown("""
    <div class="report-card">
        <h3>📋 Client Database Export</h3>
        <p>Complete Excel workbook with client list, territory summary, location breakdown, and channel analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("Generate Excel Export", use_container_width=True, type="primary"):
        with st.spinner("Generating Excel workbook..."):
            excel_bytes = generate_client_list_excel(df, PRODUCTS)
            st.download_button(
                label="Download Client Database Excel",
                data=excel_bytes,
                file_name="Malack_Client_Database_2026.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        st.success("Export generated successfully!")

with col3:
    st.markdown("""
    <div class="report-card">
        <h3>📈 Forecast Report</h3>
        <p>Excel workbook with quarterly targets, client growth projections, and territory potential analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("Generate Forecast Excel", use_container_width=True, type="primary"):
        with st.spinner("Generating forecast report..."):
            import io
            import pandas as pd

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                # Quarterly targets
                quarterly = generate_quarterly_targets(df, PRODUCTS)
                quarterly.to_excel(writer, sheet_name="Quarterly Targets", index=False)

                # Client growth
                growth = client_growth_forecast()
                growth.to_excel(writer, sheet_name="Client Growth", index=False)

                # Territory potential
                potential = territory_growth_potential(df, PRODUCTS)
                potential.to_excel(writer, sheet_name="Growth Potential", index=False)

                # Targets summary
                targets_df = pd.DataFrame([
                    {"Metric": "Revenue Growth Target", "Value": f"{TARGETS['revenue_growth']*100:.0f}%"},
                    {"Metric": "New Clients Target", "Value": str(TARGETS["new_clients"])},
                    {"Metric": "Retention Rate Target", "Value": f"{TARGETS['retention_rate']*100:.0f}%"},
                    {"Metric": "Total Client Target", "Value": str(TARGETS["target_clients"])},
                    {"Metric": "Current Clients", "Value": str(TARGETS["current_clients"])},
                ])
                targets_df.to_excel(writer, sheet_name="2026 Targets", index=False)

            output.seek(0)
            st.download_button(
                label="Download Forecast Excel",
                data=output.getvalue(),
                file_name="Malack_Forecast_2026.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        st.success("Forecast report generated successfully!")

st.markdown("---")

# Custom filtered report
st.markdown("### Custom Filtered Report")
st.markdown("Generate reports for specific territories, channels, or locations.")

col1, col2, col3 = st.columns(3)
with col1:
    report_territory = st.multiselect("Territory", df["TERRITORY"].unique(), default=list(df["TERRITORY"].unique()))
with col2:
    report_category = st.multiselect("Channel", df["CATEGORY"].unique(), default=list(df["CATEGORY"].unique()))
with col3:
    report_format = st.selectbox("Format", ["PDF Summary", "Excel Export"])

# Apply filters
report_df = df.copy()
if report_territory:
    report_df = report_df[report_df["TERRITORY"].isin(report_territory)]
if report_category:
    report_df = report_df[report_df["CATEGORY"].isin(report_category)]

st.info(f"Selected: **{len(report_df):,}** clients across **{report_df['LOCATION'].nunique()}** locations")

if st.button("Generate Custom Report", use_container_width=True):
    with st.spinner("Generating custom report..."):
        if report_format == "PDF Summary":
            pdf_bytes = generate_executive_summary(report_df, PRODUCTS)
            territory_label = "_".join(report_territory) if report_territory else "All"
            st.download_button(
                label="Download Custom PDF",
                data=pdf_bytes,
                file_name=f"Malack_Report_{territory_label}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            excel_bytes = generate_client_list_excel(report_df, PRODUCTS)
            territory_label = "_".join(report_territory) if report_territory else "All"
            st.download_button(
                label="Download Custom Excel",
                data=excel_bytes,
                file_name=f"Malack_Report_{territory_label}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
    st.success("Custom report generated!")

st.markdown("---")

# Quick data preview
with st.expander("Preview Report Data"):
    tab1, tab2, tab3 = st.tabs(["Client Summary", "Territory Summary", "Product Summary"])

    with tab1:
        st.dataframe(
            report_df[["Client ID", "CLIENT NAME", "LOCATION", "TERRITORY", "CATEGORY", "Total Units"]]
            .sort_values("Total Units", ascending=False),
            use_container_width=True, height=400,
        )

    with tab2:
        territory_summary = report_df.groupby("TERRITORY").agg(
            Clients=("Client ID", "count"),
            Total_Units=("Total Units", "sum"),
            Avg_Units=("Total Units", "mean"),
        ).reset_index()
        territory_summary["Avg_Units"] = territory_summary["Avg_Units"].round(0)
        st.dataframe(territory_summary, use_container_width=True)

    with tab3:
        import pandas as pd
        product_summary = pd.DataFrame({
            "Product": PRODUCTS,
            "Total Units": [report_df[p].sum() for p in PRODUCTS],
            "Avg/Client": [report_df[p].mean().round(0) for p in PRODUCTS],
            "Max": [report_df[p].max() for p in PRODUCTS],
            "Min": [report_df[p].min() for p in PRODUCTS],
        })
        st.dataframe(product_summary, use_container_width=True)
