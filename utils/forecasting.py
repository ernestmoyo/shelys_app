"""
Sales forecasting utilities using linear regression and growth modeling.
Based on 2026 targets from the Shelys Sales Plan.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# 2026 Targets from the sales plan
TARGETS = {
    "revenue_growth": 0.25,  # 25% revenue growth
    "new_clients": 85,       # 85 new clients
    "retention_rate": 0.95,  # 95% retention
    "target_clients": 512,   # Target 512 total clients
    "current_clients": 427,
}

QUARTERLY_WEIGHTS = {
    "Q1": 0.20,
    "Q2": 0.25,
    "Q3": 0.28,
    "Q4": 0.27,
}


def generate_quarterly_targets(df: pd.DataFrame, products: list) -> pd.DataFrame:
    """Generate quarterly sales targets based on 2026 plan."""
    current_totals = {p: df[p].sum() for p in products}
    target_totals = {p: int(v * (1 + TARGETS["revenue_growth"])) for p, v in current_totals.items()}

    rows = []
    for quarter, weight in QUARTERLY_WEIGHTS.items():
        row = {"Quarter": quarter}
        for p in products:
            row[f"{p}_Target"] = int(target_totals[p] * weight)
            row[f"{p}_Current"] = int(current_totals[p] * weight)
        row["Total_Target"] = sum(row[f"{p}_Target"] for p in products)
        row["Total_Current"] = sum(row[f"{p}_Current"] for p in products)
        rows.append(row)

    return pd.DataFrame(rows)


def generate_monthly_forecast(df: pd.DataFrame, months: int = 12) -> pd.DataFrame:
    """Generate monthly sales forecast using linear growth model."""
    total_current = df["Total Units"].sum()
    total_target = total_current * (1 + TARGETS["revenue_growth"])
    monthly_growth = (total_target / total_current) ** (1 / months) - 1

    periods = []
    units = []
    lower = []
    upper = []

    for i in range(months):
        month_label = f"2026-{i+1:02d}"
        base = total_current / months
        projected = base * (1 + monthly_growth) ** (i + 1)

        # Add seasonal variation
        seasonal = 1.0 + 0.05 * np.sin(2 * np.pi * (i + 1) / 12)
        projected *= seasonal

        noise_pct = 0.05 + (i * 0.01)
        periods.append(month_label)
        units.append(int(projected))
        lower.append(int(projected * (1 - noise_pct)))
        upper.append(int(projected * (1 + noise_pct)))

    return pd.DataFrame({
        "Period": periods,
        "Units": units,
        "Lower": lower,
        "Upper": upper,
    })


def generate_historical_baseline(df: pd.DataFrame, months: int = 6) -> pd.DataFrame:
    """Generate simulated historical baseline (last 6 months of 2025)."""
    total = df["Total Units"].sum()
    monthly_base = total / 12

    periods = []
    units = []
    for i in range(months):
        month = 12 - months + i + 1
        period = f"2025-{month:02d}"
        seasonal = 1.0 + 0.03 * np.sin(2 * np.pi * month / 12)
        variation = 1.0 + np.random.uniform(-0.03, 0.03)
        periods.append(period)
        units.append(int(monthly_base * seasonal * variation))

    return pd.DataFrame({"Period": periods, "Units": units})


def client_growth_forecast() -> pd.DataFrame:
    """Forecast client growth through 2026."""
    current = TARGETS["current_clients"]
    target = TARGETS["target_clients"]
    monthly_new = TARGETS["new_clients"] / 12
    churn_rate = (1 - TARGETS["retention_rate"]) / 12

    rows = []
    clients = current
    for i in range(12):
        month = f"2026-{i+1:02d}"
        new = int(monthly_new * (1 + 0.1 * np.sin(2 * np.pi * (i + 1) / 12)))
        churned = int(clients * churn_rate)
        clients = clients + new - churned
        rows.append({
            "Month": month,
            "Total Clients": clients,
            "New Clients": new,
            "Churned": churned,
            "Net Growth": new - churned,
            "Target": target,
        })

    return pd.DataFrame(rows)


def territory_growth_potential(df: pd.DataFrame, products: list) -> pd.DataFrame:
    """Analyze growth potential by territory and location."""
    location_stats = df.groupby(["TERRITORY", "LOCATION"]).agg(
        Clients=("Client ID", "count"),
        Avg_Units=("Total Units", "mean"),
        Total_Units=("Total Units", "sum"),
    ).reset_index()

    overall_avg = df["Total Units"].mean()
    location_stats["Performance_Index"] = (
        location_stats["Avg_Units"] / overall_avg * 100
    ).round(1)
    location_stats["Growth_Potential"] = location_stats["Performance_Index"].apply(
        lambda x: "High" if x < 80 else ("Medium" if x < 110 else "Low")
    )

    return location_stats.sort_values("Performance_Index")
