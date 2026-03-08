# Sales Suite

A regional sales intelligence platform built with [Streamlit](https://streamlit.io/) for interactive analytics, client management, forecasting, and automated reporting.

---

## Features

### Sales Dashboard
- Territory, channel, and product analytics
- Interactive treemaps, heatmaps, and radar charts
- Filterable by territory, channel, location, and product
- Top client rankings

### Client CRM
- Search and filter across your client base
- Card view and table view with contact details
- Per-client product breakdown
- Channel and location analytics

### Sales Forecasting
- Quarterly and monthly sales projections
- Client growth modeling
- Territory growth potential analysis
- KPI gauges tracking progress against targets

### Automated Reports
- Executive summary PDF with KPIs, charts, and tables
- Excel export of full client database
- Forecast workbook with quarterly targets
- Custom filtered reports by territory and channel

---

## Tech Stack

- **Streamlit** — UI framework
- **Pandas** — Data processing
- **Plotly** — Interactive charts
- **scikit-learn** — Forecasting models
- **FPDF2** — PDF report generation
- **XlsxWriter** — Excel exports

---

## Setup

```bash
pip install -r requirements.txt
streamlit run Home.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Project Structure

```
├── Home.py                  # Landing page
├── pages/
│   ├── 1_📊_Dashboard.py   # Sales analytics
│   ├── 2_👥_CRM.py         # Client manager
│   ├── 3_📈_Forecasting.py # Sales projections
│   └── 4_📄_Reports.py     # Report generator
├── utils/
│   ├── data_loader.py       # Data loading & cleaning
│   ├── charts.py            # Plotly chart builders
│   ├── forecasting.py       # Growth models
│   └── report_generator.py  # PDF & Excel generators
├── data/                    # Customer database files
├── .streamlit/config.toml   # Theme config
└── requirements.txt
```
