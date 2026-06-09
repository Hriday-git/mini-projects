import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/wildlife_tracking_2024_expanded.csv")

    df = df.rename(columns={
        "forest": "region",
        "motion_type": "behavior"
    })

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Create risk_level if missing
    if "risk_level" not in df.columns:
        df["risk_level"] = 0
        df.loc[df["heart_rate"] > 110, "risk_level"] = 2
        df.loc[(df["heart_rate"] >= 90) & (df["temperature"] > 36), "risk_level"] = 1

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
# Page Title
# -------------------------------
st.title("🔴 Risk Analytics")
st.divider()

# -------------------------------
# 1️⃣ Risk Distribution (Donut)
# -------------------------------
# CREATE risk_counts FIRST
risk_counts = filtered_df["risk_level"].value_counts().reset_index()
risk_counts.columns = ["risk_level", "count"]

# Map labels
risk_labels = {
    0: "Normal",
    1: "Medium Risk",
    2: "High Risk"
}

risk_counts["risk_label"] = risk_counts["risk_level"].map(risk_labels)

# Plot

fig1 = px.pie(
    risk_counts,
    names="risk_label",
    values="count",
    title="Risk Level Distribution",
    hole=0.4,
    template="plotly_white",
    color="risk_label",
    color_discrete_map={
        "Normal": "#4CAF50",       # green
        "Medium Risk": "#FFA726",  # orange
        "High Risk": "#EF5350"     # red
    }
)

fig1.update_traces(
    textposition="outside",   # 🔥 key fix
    textinfo="percent+label"
)

st.plotly_chart(fig1, use_container_width=True)
st.write("")

# -------------------------------
# 2️⃣ High Risk Alerts by Region
# -------------------------------
st.subheader("High Risk Alerts by Region")

high_risk_df = filtered_df[filtered_df["risk_level"] == 2]

region_risk = high_risk_df["region"].value_counts().reset_index()
region_risk.columns = ["region", "count"]

fig2 = px.bar(
    region_risk,
    x="region",
    y="count",
    title="High Risk Cases by Region",
    template="plotly_white",
    color="count",
    color_continuous_scale="Reds"
)

fig2.update_layout(xaxis_tickangle=-30)

st.plotly_chart(fig2, use_container_width=True)

st.write("")

# -------------------------------
# 3️⃣ Top High-Risk Species
# -------------------------------
st.subheader("Top High-Risk Species")

species_risk = high_risk_df["species"].value_counts().reset_index()
species_risk.columns = ["species", "count"]

fig3 = px.bar(
    species_risk.head(10),
    x="species",
    y="count",
    title="Top 10 High-Risk Species",
    template="plotly_white",
    color="count",
    color_continuous_scale="Purples"
)

fig3.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig3, use_container_width=True)