"""
Data loader module for Malack/Shelys customer database.
Loads, cleans, and caches Excel data for the application.
"""

import os
import pandas as pd
import streamlit as st
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PRODUCTS = ["Action", "GMLT", "GMCT", "WWGW", "BTZ"]

MAIN_FILE = "MALACK_CUSTOMER_DATABASE_2025_UPDATED-6.12.2025 (1).xlsx"
NORMALIZED_FILE = "MALACK_CUSTOMER_DATABASE_2025_UPDATED-6.12.2025_other (1).xlsx"


def _clean_location(loc: str) -> str:
    """Normalize location names: strip whitespace, title case."""
    if pd.isna(loc):
        return "Unknown"
    return " ".join(str(loc).strip().split()).title()


def _clean_category(cat: str) -> str:
    """Normalize category names."""
    if pd.isna(cat):
        return "Other"
    cat = str(cat).strip().title()
    mapping = {
        "Ph": "Pharmacy",
        "Pharmacy": "Pharmacy",
        "Dldm": "DLDM",
        "Shop": "Shop",
        "Supermarket": "Supermarket",
    }
    return mapping.get(cat, cat)


def _clean_territory(ter: str) -> str:
    """Normalize territory names."""
    if pd.isna(ter):
        return "Unknown"
    ter = str(ter).strip().upper()
    if "DSM" in ter or "DAR" in ter:
        return "DSM"
    if "TANGA" in ter:
        return "Tanga"
    return ter.title()


@st.cache_data(ttl=3600)
def load_customer_data() -> pd.DataFrame:
    """Load and clean the main customer database (wide format)."""
    filepath = DATA_DIR / MAIN_FILE
    if not filepath.exists():
        st.error(f"Data file not found: {filepath}")
        return pd.DataFrame()

    df = pd.read_excel(filepath, sheet_name="Customer Database", engine="openpyxl")

    # Standardize column names
    df.columns = df.columns.str.strip()

    # Clean text columns
    df["LOCATION"] = df["LOCATION"].apply(_clean_location)
    df["CATEGORY"] = df["CATEGORY"].apply(_clean_category)
    df["TERRITORY"] = df["TERRITORY"].apply(_clean_territory)
    df["CLIENT NAME"] = df["CLIENT NAME"].astype(str).str.strip().str.title()
    df["CONTACT"] = df["CONTACT"].astype(str).str.strip().replace("nan", "N/A")

    # Ensure numeric product columns
    for col in PRODUCTS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Add total sales column
    df["Total Units"] = df[PRODUCTS].sum(axis=1)

    # Add client ID if not present
    if "NS" in df.columns:
        df["Client ID"] = df["NS"]
    else:
        df["Client ID"] = range(1, len(df) + 1)

    return df


@st.cache_data(ttl=3600)
def load_summary_data() -> dict:
    """Load summary sheet data."""
    filepath = DATA_DIR / MAIN_FILE
    if not filepath.exists():
        return {}

    df = pd.read_excel(filepath, sheet_name="Summary", engine="openpyxl")
    summary = {}
    for _, row in df.iterrows():
        key = str(row.iloc[0]).strip()
        val = row.iloc[1]
        summary[key] = val
    return summary


@st.cache_data(ttl=3600)
def load_product_totals() -> pd.DataFrame:
    """Load product totals from Sheet4."""
    filepath = DATA_DIR / MAIN_FILE
    if not filepath.exists():
        return pd.DataFrame()

    df = pd.read_excel(filepath, sheet_name="Sheet4", engine="openpyxl")
    df.columns = ["Product", "Total Units"]
    return df


def get_territory_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generate territory-level summary."""
    return df.groupby("TERRITORY").agg(
        Clients=("Client ID", "count"),
        **{p: (p, "sum") for p in PRODUCTS},
        Total_Units=("Total Units", "sum"),
    ).reset_index()


def get_location_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generate location-level summary."""
    return df.groupby(["TERRITORY", "LOCATION"]).agg(
        Clients=("Client ID", "count"),
        Total_Units=("Total Units", "sum"),
    ).reset_index().sort_values("Total_Units", ascending=False)


def get_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generate category-level summary."""
    return df.groupby("CATEGORY").agg(
        Clients=("Client ID", "count"),
        **{p: (p, "sum") for p in PRODUCTS},
        Total_Units=("Total Units", "sum"),
    ).reset_index()


def get_top_clients(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Get top N clients by total units."""
    return df.nlargest(n, "Total Units")[
        ["Client ID", "CLIENT NAME", "LOCATION", "TERRITORY", "CATEGORY", "Total Units"]
    ]
