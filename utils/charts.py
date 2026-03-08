"""
Reusable Plotly chart builders for the Malack Sales Suite.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

BRAND_COLORS = ["#0066CC", "#00B4D8", "#FF6B35", "#2EC4B6", "#E71D36", "#7209B7"]
PRODUCT_COLORS = {
    "Action": "#0066CC",
    "GMLT": "#00B4D8",
    "GMCT": "#FF6B35",
    "WWGW": "#2EC4B6",
    "BTZ": "#E71D36",
}


def _apply_layout(fig, title: str = "", height: int = 400):
    """Apply consistent layout styling."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#1A1A2E")),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=40, r=20, t=50, b=40),
        font=dict(family="Inter, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
    )
    return fig


def territory_pie(df: pd.DataFrame) -> go.Figure:
    """Pie chart of clients by territory."""
    data = df.groupby("TERRITORY")["Client ID"].count().reset_index()
    data.columns = ["Territory", "Clients"]
    fig = px.pie(data, values="Clients", names="Territory", color_discrete_sequence=BRAND_COLORS)
    return _apply_layout(fig, "Clients by Territory", 350)


def category_bar(df: pd.DataFrame) -> go.Figure:
    """Bar chart of clients by category."""
    data = df.groupby("CATEGORY")["Client ID"].count().reset_index()
    data.columns = ["Category", "Clients"]
    data = data.sort_values("Clients", ascending=True)
    fig = px.bar(data, x="Clients", y="Category", orientation="h", color_discrete_sequence=BRAND_COLORS)
    return _apply_layout(fig, "Clients by Channel", 350)


def product_sales_bar(df: pd.DataFrame, products: list) -> go.Figure:
    """Grouped bar chart of product sales by territory."""
    melted = df.melt(
        id_vars=["TERRITORY"],
        value_vars=products,
        var_name="Product",
        value_name="Units",
    )
    data = melted.groupby(["TERRITORY", "Product"])["Units"].sum().reset_index()
    fig = px.bar(
        data, x="Product", y="Units", color="TERRITORY",
        barmode="group", color_discrete_sequence=BRAND_COLORS,
    )
    return _apply_layout(fig, "Product Sales by Territory", 400)


def location_treemap(df: pd.DataFrame) -> go.Figure:
    """Treemap of sales by territory and location."""
    data = df.groupby(["TERRITORY", "LOCATION"]).agg(
        Units=("Total Units", "sum"),
        Clients=("Client ID", "count"),
    ).reset_index()
    fig = px.treemap(
        data, path=["TERRITORY", "LOCATION"], values="Units",
        color="Units", color_continuous_scale="Blues",
        custom_data=["Clients"],
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Units: %{value:,.0f}<br>Clients: %{customdata[0]}<extra></extra>"
    )
    return _apply_layout(fig, "Sales Distribution by Location", 500)


def top_clients_bar(df: pd.DataFrame, n: int = 15) -> go.Figure:
    """Horizontal bar chart of top clients."""
    top = df.nlargest(n, "Total Units").sort_values("Total Units")
    fig = px.bar(
        top, x="Total Units", y="CLIENT NAME", orientation="h",
        color="TERRITORY", color_discrete_sequence=BRAND_COLORS,
    )
    return _apply_layout(fig, f"Top {n} Clients by Total Units", max(350, n * 28))


def product_radar(df: pd.DataFrame, products: list) -> go.Figure:
    """Radar chart comparing product performance across territories."""
    fig = go.Figure()
    for territory in df["TERRITORY"].unique():
        t_data = df[df["TERRITORY"] == territory]
        values = [t_data[p].sum() for p in products]
        values.append(values[0])  # close the polygon
        fig.add_trace(go.Scatterpolar(
            r=values, theta=products + [products[0]],
            fill="toself", name=territory,
        ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
    return _apply_layout(fig, "Product Performance by Territory", 450)


def sales_heatmap(df: pd.DataFrame, products: list) -> go.Figure:
    """Heatmap of product sales by location."""
    data = df.groupby("LOCATION")[products].sum()
    top_locs = data.sum(axis=1).nlargest(20).index
    data = data.loc[top_locs]
    fig = px.imshow(
        data.values, labels=dict(x="Product", y="Location", color="Units"),
        x=products, y=list(data.index),
        color_continuous_scale="Blues", aspect="auto",
    )
    return _apply_layout(fig, "Product Sales Heatmap (Top 20 Locations)", 550)


def forecast_line(historical: pd.DataFrame, forecast: pd.DataFrame) -> go.Figure:
    """Line chart with historical and forecasted values."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=historical["Period"], y=historical["Units"],
        mode="lines+markers", name="Historical",
        line=dict(color=BRAND_COLORS[0], width=2),
    ))
    fig.add_trace(go.Scatter(
        x=forecast["Period"], y=forecast["Units"],
        mode="lines+markers", name="Forecast",
        line=dict(color=BRAND_COLORS[2], width=2, dash="dash"),
    ))
    if "Lower" in forecast.columns and "Upper" in forecast.columns:
        fig.add_trace(go.Scatter(
            x=list(forecast["Period"]) + list(forecast["Period"][::-1]),
            y=list(forecast["Upper"]) + list(forecast["Lower"][::-1]),
            fill="toself", fillcolor="rgba(255,107,53,0.15)",
            line=dict(color="rgba(255,107,53,0)"),
            showlegend=False, name="Confidence",
        ))
    return _apply_layout(fig, "Sales Forecast", 400)


def kpi_gauge(value: float, target: float, title: str) -> go.Figure:
    """Gauge chart for KPI tracking."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        delta={"reference": target, "relative": True, "valueformat": ".1%"},
        title={"text": title, "font": {"size": 14}},
        gauge={
            "axis": {"range": [0, target * 1.3]},
            "bar": {"color": BRAND_COLORS[0]},
            "steps": [
                {"range": [0, target * 0.5], "color": "#FFE0D0"},
                {"range": [target * 0.5, target * 0.8], "color": "#FFF3CD"},
                {"range": [target * 0.8, target], "color": "#D4EDDA"},
            ],
            "threshold": {
                "line": {"color": "#E71D36", "width": 3},
                "thickness": 0.8,
                "value": target,
            },
        },
    ))
    return _apply_layout(fig, "", 280)
