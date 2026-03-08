"""
Automated PDF and Excel report generator for Malack Sales Suite.
"""

import io
import pandas as pd
from datetime import datetime
from fpdf import FPDF


class SalesReport(FPDF):
    """Custom PDF report for Malack/Shelys sales data."""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(0, 102, 204)
        self.cell(0, 8, "Malack Tweve - Shelys Pharmaceuticals", ln=True, align="L")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}", ln=True, align="L")
        self.line(10, self.get_y() + 2, 200, self.get_y() + 2)
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(26, 26, 46)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def sub_title(self, title: str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(0, 102, 204)
        self.cell(0, 8, title, ln=True)
        self.ln(1)

    def body_text(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def kpi_row(self, label: str, value: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.cell(80, 7, label, border=0)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 102, 204)
        self.cell(0, 7, str(value), ln=True)

    def add_table(self, headers: list, data: list, col_widths: list = None):
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)

        # Header row
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 102, 204)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, str(h), border=1, fill=True, align="C")
        self.ln()

        # Data rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(50, 50, 50)
        for row_idx, row in enumerate(data):
            if row_idx % 2 == 0:
                self.set_fill_color(245, 247, 250)
            else:
                self.set_fill_color(255, 255, 255)
            for i, val in enumerate(row):
                self.cell(col_widths[i], 6, str(val), border=1, fill=True, align="C")
            self.ln()
        self.ln(4)


def generate_executive_summary(df: pd.DataFrame, products: list) -> bytes:
    """Generate executive summary PDF report."""
    pdf = SalesReport()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(26, 26, 46)
    pdf.cell(0, 15, "Executive Sales Summary", ln=True, align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 8, "Malack Tweve Regional Analysis - DSM & Tanga", ln=True, align="C")
    pdf.ln(10)

    # KPIs
    pdf.section_title("Key Performance Indicators")
    total_clients = len(df)
    total_units = df["Total Units"].sum()
    avg_units = df["Total Units"].mean()
    dsm_clients = len(df[df["TERRITORY"] == "DSM"])
    tanga_clients = len(df[df["TERRITORY"] == "Tanga"])

    pdf.kpi_row("Total Active Clients:", f"{total_clients:,}")
    pdf.kpi_row("Total Product Units:", f"{total_units:,}")
    pdf.kpi_row("Average Units per Client:", f"{avg_units:,.0f}")
    pdf.kpi_row("DSM Territory Clients:", f"{dsm_clients:,}")
    pdf.kpi_row("Tanga Territory Clients:", f"{tanga_clients:,}")
    pdf.ln(5)

    # Product Performance
    pdf.section_title("Product Performance")
    headers = ["Product", "Total Units", "% of Total", "Avg/Client"]
    data = []
    for p in products:
        total = df[p].sum()
        pct = f"{total / total_units * 100:.1f}%"
        avg = f"{df[p].mean():,.0f}"
        data.append([p, f"{total:,}", pct, avg])
    pdf.add_table(headers, data, [50, 50, 45, 45])

    # Territory Breakdown
    pdf.section_title("Territory Breakdown")
    for territory in ["DSM", "Tanga"]:
        t_data = df[df["TERRITORY"] == territory]
        pdf.sub_title(f"{territory} Territory")
        pdf.kpi_row("  Clients:", f"{len(t_data):,}")
        pdf.kpi_row("  Total Units:", f"{t_data['Total Units'].sum():,}")
        pdf.kpi_row("  Avg Units/Client:", f"{t_data['Total Units'].mean():,.0f}")
        pdf.ln(2)

    # Category Analysis
    pdf.add_page()
    pdf.section_title("Channel Distribution")
    cat_headers = ["Channel", "Clients", "Total Units", "Avg Units"]
    cat_data = []
    for cat in df["CATEGORY"].unique():
        c_data = df[df["CATEGORY"] == cat]
        cat_data.append([
            cat, f"{len(c_data):,}",
            f"{c_data['Total Units'].sum():,}",
            f"{c_data['Total Units'].mean():,.0f}",
        ])
    pdf.add_table(cat_headers, cat_data, [50, 45, 50, 45])

    # Top 20 Clients
    pdf.section_title("Top 20 Clients")
    top = df.nlargest(20, "Total Units")
    top_headers = ["#", "Client", "Location", "Territory", "Units"]
    top_data = []
    for i, (_, row) in enumerate(top.iterrows(), 1):
        name = str(row["CLIENT NAME"])[:25]
        top_data.append([
            str(i), name, str(row["LOCATION"])[:15],
            row["TERRITORY"], f"{row['Total Units']:,}",
        ])
    pdf.add_table(top_headers, top_data, [15, 65, 45, 30, 35])

    # Location Analysis
    pdf.add_page()
    pdf.section_title("Top Locations by Sales")
    loc_data = df.groupby(["TERRITORY", "LOCATION"]).agg(
        Clients=("Client ID", "count"),
        Units=("Total Units", "sum"),
    ).reset_index().nlargest(15, "Units")
    loc_headers = ["Location", "Territory", "Clients", "Total Units"]
    loc_rows = []
    for _, row in loc_data.iterrows():
        loc_rows.append([
            str(row["LOCATION"])[:20], row["TERRITORY"],
            str(row["Clients"]), f"{row['Units']:,}",
        ])
    pdf.add_table(loc_headers, loc_rows, [60, 40, 40, 50])

    return pdf.output()


def generate_client_list_excel(df: pd.DataFrame, products: list) -> bytes:
    """Generate Excel export of client data with formatting."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Main client list
        export_cols = ["Client ID", "CLIENT NAME", "LOCATION", "CONTACT",
                       "CATEGORY", "TERRITORY"] + products + ["Total Units"]
        df[export_cols].to_excel(writer, sheet_name="Client Database", index=False)

        # Territory summary
        territory_summary = df.groupby("TERRITORY").agg(
            Clients=("Client ID", "count"),
            **{p: (p, "sum") for p in products},
            Total_Units=("Total Units", "sum"),
        ).reset_index()
        territory_summary.to_excel(writer, sheet_name="Territory Summary", index=False)

        # Location summary
        location_summary = df.groupby(["TERRITORY", "LOCATION"]).agg(
            Clients=("Client ID", "count"),
            Total_Units=("Total Units", "sum"),
        ).reset_index().sort_values("Total_Units", ascending=False)
        location_summary.to_excel(writer, sheet_name="Location Summary", index=False)

        # Category summary
        category_summary = df.groupby("CATEGORY").agg(
            Clients=("Client ID", "count"),
            **{p: (p, "sum") for p in products},
            Total_Units=("Total Units", "sum"),
        ).reset_index()
        category_summary.to_excel(writer, sheet_name="Channel Summary", index=False)

        # Formatting
        workbook = writer.book
        header_fmt = workbook.add_format({
            "bold": True, "bg_color": "#0066CC", "font_color": "white",
            "border": 1, "align": "center",
        })
        number_fmt = workbook.add_format({"num_format": "#,##0", "border": 1})

        for sheet_name in writer.sheets:
            ws = writer.sheets[sheet_name]
            ws.set_column("A:A", 10)
            ws.set_column("B:B", 25)
            ws.set_column("C:C", 18)
            ws.set_column("D:D", 15)

    output.seek(0)
    return output.getvalue()
