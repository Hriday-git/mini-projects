
import pandas as pd
import plotly.express as px

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("wildlife_tracking_2024_expanded.csv")

# ==============================
# 1. BEHAVIOR DISTRIBUTION
# ==============================
behavior = df['motion_type'].value_counts().reset_index()
behavior.columns = ['motion_type', 'count']

fig1 = px.bar(behavior, x='motion_type', y='count',
              title="Behavior Distribution")
fig1.write_html("behavior.html")

# ==============================
# 2. REGION ACTIVITY
# ==============================
region = df['forest'].value_counts().reset_index()
region.columns = ['forest', 'count']

fig2 = px.pie(region, names='forest', values='count',
              title="Region-wise Activity")
fig2.write_html("region.html")

# ==============================
# 3. SPECIES PER REGION
# ==============================

species_region = df.groupby(['forest', 'species']).size().reset_index(name='count')
top_species = species_region.sort_values(['forest','count'], ascending=[True, False]) \
                           .groupby('forest').head(5)

fig3 = px.bar(
    top_species,
    x='forest',
    y='count',
    color='species',
    barmode='group',
    title="Top 5 Species per Region",
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig3.write_html("species.html")

# ==============================
# 4. AVG HEART RATE
# ==============================
heart = df.groupby('forest')['heart_rate'].mean().reset_index()

fig4 = px.bar(heart,
              x='heart_rate',
              y='forest',
              orientation='h',
              title="Average Heart Rate per Region")
fig4.write_html("heart.html")

# ==============================
# 5. RISK DISTRIBUTION
# ==============================
def risk_logic(row):
    if row['heart_rate'] > 110 and row['motion_type'] in ["Running","Swimming","Flying","Jumping","Climbing"]:
        return "High Risk"
    elif row['heart_rate'] >= 90:
        return "Medium Risk"
    else:
        return "Normal"

df['risk_flag'] = df.apply(risk_logic, axis=1)

risk = df['risk_flag'].value_counts().reset_index()
risk.columns = ['risk', 'count']

fig5 = px.pie(risk, names='risk', values='count',
              hole=0.4,
              title="Risk Distribution")
fig5.write_html("risk.html")

# ==============================
# 6. HEATMAP
# ==============================
heat = df.groupby(['forest', 'risk_flag']).size().reset_index(name='count')

# Convert to percentage
heat['percentage'] = heat.groupby('forest')['count'].transform(lambda x: x / x.sum())

fig6 = px.density_heatmap(
    heat,
    x='forest',
    y='risk_flag',
    z='percentage',
    color_continuous_scale='Viridis',
    title="Risk Distribution by Region (%)"
)

fig6.write_html("heatmap.html")

# ==============================
# 7. TIME SERIES
# ==============================
df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True)
df['hour'] = df['timestamp'].dt.hour

time = df.groupby('hour').size().reset_index(name='count')

fig7 = px.line(time,
               x='hour',
               y='count',
               title="Activity by Hour")
fig7.write_html("time.html")

# ==============================
# ==============================
# HIGH RISK ALERTS BY REGION
# ==============================

alert = df[df['risk_flag'] == "High Risk"] \
        .groupby('forest') \
        .size() \
        .reset_index(name='high_risk_count')

fig_alert = px.bar(
    alert,
    x='forest',
    y='high_risk_count',
    color='forest',
    title="High Risk Alerts by Region"
)

fig_alert.write_html("alerts.html")

# ==============================
# RISK TREND OVER TIME
# ==============================

# Ensure hour column exists
df['timestamp'] = pd.to_datetime(df['timestamp'], dayfirst=True)
df['hour'] = df['timestamp'].dt.hour

risk_time = df.groupby(['hour', 'risk_flag']) \
              .size() \
              .reset_index(name='count')

fig_trend = px.line(
    risk_time,
    x='hour',
    y='count',
    color='risk_flag',
    title="Risk Trend Over Time"
)

fig_trend.write_html("trend.html")

# ==============================
# TOP HIGH-RISK SPECIES
# ==============================

risk_species = df[df['risk_flag'] == "High Risk"] \
                .groupby('species') \
                .size() \
                .reset_index(name='count') \
                .sort_values(by='count', ascending=False) \
                .head(5)

fig_species = px.bar(
    risk_species,
    x='species',
    y='count',
    color='species',
    title="Top 5 High-Risk Species"
)

fig_species.write_html("top_species.html")