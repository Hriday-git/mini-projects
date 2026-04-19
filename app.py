import streamlit as st
import pandas as pd

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Wildlife Dashboard", layout="wide")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/wildlife_tracking_2024_expanded.csv")

    # Fix column names (important)
    df = df.rename(columns={
        "forest": "region",
        "motion_type": "behavior"
    })

    # Fix timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return df

df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.title("🔎 Filters")

region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + sorted(df["region"].dropna().unique())
)

species = st.sidebar.selectbox(
    "Select Species",
    ["All"] + sorted(df["species"].dropna().unique())
)

# Apply filters
filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[filtered_df["region"] == region]

if species != "All":
    filtered_df = filtered_df[filtered_df["species"] == species]

# -------------------------------
# Header
# -------------------------------
st.title("🌿 Wildlife Monitoring Dashboard")
st.caption("IoT-Based Wildlife Tracking & Risk Analytics System")

st.markdown("---")

# -------------------------------
# KPI Section
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("📊 Total Records", len(filtered_df))

high_risk = len(filtered_df[filtered_df["risk_level"] == 2])
col2.metric("⚠️ High Risk Count", high_risk)

if not filtered_df.empty:
    top_region = filtered_df["region"].value_counts().idxmax()
else:
    top_region = "N/A"

col3.metric("🌍 Most Active Region", top_region)

st.markdown("---")

# -------------------------------
# Quick Preview Charts
# -------------------------------
col1, col2 = st.columns(2)

col1.subheader("Behavior Distribution")
col1.bar_chart(filtered_df["behavior"].value_counts())

col2.subheader("Region Activity")
col2.bar_chart(filtered_df["region"].value_counts())

st.markdown("---")

# -------------------------------
# Info + Raw Data
# -------------------------------
st.info("Use sidebar filters and navigate pages for detailed insights 👈")

with st.expander("🔍 View Data"):
    st.dataframe(filtered_df.head(100))

st.success("Dashboard Loaded Successfully ✅")
