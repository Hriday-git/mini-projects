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
st.title("🔵 Time Analysis")
st.divider()

# -------------------------------
# Prepare Time Features
# -------------------------------
filtered_df["hour"] = filtered_df["timestamp"].dt.hour

# -------------------------------
# 1️⃣ Activity by Hour
# -------------------------------
st.subheader("Activity by Hour")

hourly_activity = (
    filtered_df.groupby("hour")
    .size()
    .reset_index(name="count")
)

fig1 = px.line(
    hourly_activity,
    x="hour",
    y="count",
    title="Animal Activity Across Hours",
    template="plotly_white"
)

fig1.update_traces(line=dict(color="#1E88E5"))  # Blue tone

st.plotly_chart(fig1, use_container_width=True)

st.write("")

# -------------------------------
# 2️⃣ Risk Trend Over Time
# -------------------------------
st.subheader("Risk Trend Over Time")

risk_time = (
    filtered_df.groupby("hour")["risk_level"]
    .mean()
    .reset_index()
)

fig2 = px.line(
    risk_time,
    x="hour",
    y="risk_level",
    title="Average Risk Level Over Time",
    template="plotly_white"
)

fig2.update_traces(line=dict(color="#8E24AA"))  # Purple tone

st.plotly_chart(fig2, use_container_width=True)