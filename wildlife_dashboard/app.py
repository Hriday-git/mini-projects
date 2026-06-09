import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# -------------------------------
# GLOBAL STYLE (UI POLISH)
# -------------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0B0F19;
}

/* Headings */
h1, h2, h3 {
    color: #E5E7EB;
}

/* KPI Cards */
.kpi-card {
    padding: 18px;
    border-radius: 14px;
    background: linear-gradient(145deg, #111827, #1F2937);
    border: 1px solid #1F2937;
    transition: 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
}

/* Text */
p, span {
    color: #9CA3AF;
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 18px;
    font-weight: 600;
}

/* Reduce top padding */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

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
# KPI Calculations
# -------------------------------
total_records = len(df)
high_risk = len(df[df["risk_level"] == 2])
most_active_region = df["region"].value_counts().idxmax()
dominant_species = df["species"].value_counts().idxmax()

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<h1 style="font-size:40px;">🌿 Wildlife Monitoring Dashboard</h1>
<p style="font-size:16px; color:#9CA3AF;">
IoT-Based Wildlife Tracking & Risk Analytics System
</p>
""", unsafe_allow_html=True)

st.write("")

# -------------------------------
# KPI CARDS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f'''
<div class="kpi-card">
    <h5>📊 Total Records</h5>
    <h2 style="color:#60A5FA;">{total_records}</h2>
</div>
''', unsafe_allow_html=True)

col2.markdown(f'''
<div class="kpi-card">
    <h5>⚠️ High Risk</h5>
    <h2 style="color:#EF4444;">{high_risk}</h2>
</div>
''', unsafe_allow_html=True)

col3.markdown(f'''
<div class="kpi-card">
    <h5>🌍 Active Region</h5>
    <h2 style="color:#34D399;">{most_active_region}</h2>
</div>
''', unsafe_allow_html=True)

col4.markdown(f'''
<div class="kpi-card">
    <h5>🐾 Dominant Species</h5>
    <h2 style="color:#FBBF24;">{dominant_species}</h2>
</div>
''', unsafe_allow_html=True)

st.write("")
st.write("")

# -------------------------------
# EXPANDABLE INSIGHTS
# -------------------------------
with st.expander("🔍 View Key Insights"):
    st.markdown("### Key Insights")

    st.write("1. Congo Basin and Amazon regions show the highest wildlife activity, indicating dense animal movement and habitat richness.")
    st.write("2. Majority of observations fall under the Normal category, while High Risk cases are relatively low but critical.")
    st.write("3. Certain species consistently appear in high-risk conditions, suggesting vulnerability to environmental or physiological stress.")
    st.write("4. Peak activity is observed during specific hours of the day, indicating strong temporal behavior patterns across species.")

st.write("")

# -------------------------------
# EXPANDABLE OVERVIEW
# -------------------------------
with st.expander("🌍 View Dashboard Overview"):
    st.markdown("### Dashboard Overview")

    st.write("1. This dashboard analyzes wildlife data using IoT-based parameters such as heart rate, temperature, motion, and location.")
    st.write("2. It provides multi-dimensional insights across behavior, region, species health, risk levels, and time-based activity.")
    st.write("3. Risk levels are derived using rule-based logic simulating machine learning classification.")
    st.write("4. Interactive filters allow dynamic exploration of data by region and species for better monitoring and decision-making.")