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
st.title("🟡 Behaviour & Region Analysis")
st.divider()

# -------------------------------
# 1️⃣ Behavior Distribution (Full Width)
# -------------------------------
st.subheader("Behavior Distribution")

behavior_counts = filtered_df["behavior"].value_counts().reset_index()
behavior_counts.columns = ["behavior", "count"]

fig1 = px.bar(
    behavior_counts,
    x="behavior",
    y="count",
    title="Behavior Distribution",
    template="plotly_white",
    color="count",
    color_continuous_scale="Blues"
)

fig1.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(fig1, use_container_width=True)

st.write("")

# -------------------------------
# 2️⃣ Region Activity (Pie - FIXED)
# -------------------------------
st.subheader("Region-wise Activity")

region_counts = filtered_df["region"].value_counts().reset_index()
region_counts.columns = ["region", "count"]

if region_counts.empty:
    st.warning("No data available for selected filters.")
else:
    fig2 = px.pie(
        region_counts,
        names="region",
        values="count",
        title="Region-wise Activity",
        hole=0.4,
        template="plotly_white"
    )

    fig2.update_traces(
        textposition="outside",   # 🔥 FIX visibility
        textinfo="percent+label"
    )

    fig2.update_layout(
        showlegend=True
    )

    st.plotly_chart(fig2, use_container_width=True)