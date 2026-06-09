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
st.title("🟠 Species & Health Analysis")
st.divider()

# -------------------------------
# Layout
# -------------------------------


# -------------------------------
# 1️⃣ Top Species per Region (Stacked Bar)
# -------------------------------
st.subheader("Top Species per Region")

# Get top 5 species overall (reduces clutter)
top_species_list = filtered_df["species"].value_counts().head(5).index

filtered_top = filtered_df[filtered_df["species"].isin(top_species_list)]

species_region = (
    filtered_top.groupby(["region", "species"])
    .size()
    .reset_index(name="count")
)

fig1 = px.bar(
    species_region,
    x="region",
    y="count",
    color="species",
    title="Top 5 Species per Region",
    template="plotly_white"
)

fig1.update_layout(
    xaxis_tickangle=-30,
    legend_title_text="Species"
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 2️⃣ Avg Heart Rate per Region (Horizontal Bar)
# -------------------------------
st.subheader("Average Heart Rate per Region")

avg_hr = (
    filtered_df.groupby("region")["heart_rate"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    avg_hr,
    x="heart_rate",
    y="region",
    orientation="h",
    title="Average Heart Rate per Region",
    template="plotly_white",
    color="heart_rate",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -------------------------------
# 3️⃣ Top Species Overall
# -------------------------------
st.subheader("🐾 Top Species Overall")

top_species = (
    filtered_df["species"]
    .value_counts()
    .reset_index()
)

top_species.columns = ["species", "count"]

fig3 = px.bar(
    top_species.head(10),
    x="species",
    y="count",
    title="Top 10 Species",
    template="plotly_white",
    color="count",
    color_continuous_scale="Viridis"
)

fig3.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig3, use_container_width=True)