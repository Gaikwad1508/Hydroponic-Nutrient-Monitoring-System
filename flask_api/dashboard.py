import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
import plotly.express as px

# -----------------------------
# 📦 DATABASE CONNECTION
# -----------------------------
conn = sqlite3.connect('hydroponics.db')
cursor = conn.cursor()

# -----------------------------
# 📋 PAGE SETUP
# -----------------------------
st.set_page_config(page_title="Hydroponics Dashboard", layout="wide")
st.title("🌿 Hydroponics Monitoring Dashboard")

# -----------------------------
# 📡 FETCH DATA
# -----------------------------
sensor_df = pd.read_sql_query("SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 50", conn)
prediction_df = pd.read_sql_query("SELECT * FROM nutrient_predictions ORDER BY timestamp DESC LIMIT 1", conn)

# Parse timestamp to datetime for chart compatibility
sensor_df['timestamp'] = pd.to_datetime(sensor_df['timestamp'])
latest_sensor = sensor_df.iloc[0]

# -----------------------------
# ✅ THRESHOLDS (Tweak as needed)
# -----------------------------
THRESHOLDS = {
    "Temperature": (20, 30),
    "pH": (5.5, 6.5),
    "TDS": (500, 1800),
    "Humidity": (50, 75),
    "Nitrogen": (200, 1500),
    "Phosphorus": (10, 100),
    "Potassium": (40, 200),
    "Calcium": (20, 150),
    "Magnesium": (10, 80),
    "Sulfur": (5, 50),
}

# -----------------------------
# 📊 SUMMARY METRIC CARDS
# -----------------------------
st.markdown("### ✅ Live Sensor Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Temperature (°C)", latest_sensor['Temperature'], help="Ideal: 20–30°C")
col2.metric("💧 pH", latest_sensor['pH'], help="Ideal: 5.5–6.5")
col3.metric("🧪 TDS (ppm)", latest_sensor['TDS'], help="Ideal: 500–1800 ppm")
col4.metric("🌫️ Humidity (%)", latest_sensor['Humidity'], help="Ideal: 50–75%")

# -----------------------------
# ⚠️ ALERT PANEL
# -----------------------------
st.markdown("### ⚠️ Threshold Alerts")
alerts = []

for param in ["Temperature", "pH", "TDS", "Humidity"]:
    val = latest_sensor[param]
    low, high = THRESHOLDS[param]
    if val < low:
        alerts.append(f"🔻 {param} is too LOW: {val}")
    elif val > high:
        alerts.append(f"🔺 {param} is too HIGH: {val}")

if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("✅ All sensor parameters are within safe thresholds.")

# -----------------------------
# 📈 SENSOR TREND CHARTS
# -----------------------------
st.markdown("### 📈 Sensor Trends Over Time")

line_chart = alt.Chart(sensor_df).transform_fold(
    ["Temperature", "pH", "TDS", "Humidity"],
    as_=["Parameter", "Value"]
).mark_line(point=True).encode(
    x=alt.X('timestamp:T', title='Timestamp'),
    y=alt.Y('Value:Q', title='Value'),
    color=alt.Color('Parameter:N', title="Parameter"),
    tooltip=['timestamp:T', 'Parameter:N', 'Value:Q']
).properties(
    width=900,
    height=300
)

st.altair_chart(line_chart, use_container_width=True)

# -----------------------------
# 🧪 NUTRIENT PREDICTIONS CHART
# -----------------------------
st.markdown("### 🧪 Nutrient Levels")
if not prediction_df.empty:
    nutrient_vals = prediction_df.iloc[0].drop('timestamp').to_dict()

    # Alert on nutrient levels
    st.markdown("#### ⚠️ Nutrient Alerts")
    for key, val in nutrient_vals.items():
        low, high = THRESHOLDS.get(key, (0, float('inf')))
        if val < low:
            st.warning(f"🟡 {key} is too LOW: {val:.2f}")
        elif val > high:
            st.error(f"🔴 {key} is too HIGH: {val:.2f}")

    # Horizontal bar chart
    nutrient_chart = px.bar(
        x=list(nutrient_vals.values()),
        y=list(nutrient_vals.keys()),
        orientation='h',
        color=list(nutrient_vals.values()),
        color_continuous_scale='YlGnBu',
        labels={"x": "Value", "y": "Nutrient"}
    )
    st.plotly_chart(nutrient_chart, use_container_width=True)

# -----------------------------
# 🗃️ DATA TABLES + DOWNLOAD
# -----------------------------
st.markdown("### 🗃️ Sensor & Nutrient Raw Data")
tab1, tab2 = st.tabs(["📊 Sensor Data", "🔮 Nutrient Predictions"])

with tab1:
    st.dataframe(sensor_df)
    st.download_button("⬇ Download Sensor Data CSV", sensor_df.to_csv(index=False).encode(), file_name="sensor_data.csv")

with tab2:
    prediction_history = pd.read_sql_query("SELECT * FROM nutrient_predictions ORDER BY timestamp DESC LIMIT 50", conn)
    st.dataframe(prediction_history)
    st.download_button("⬇ Download Prediction Data CSV", prediction_history.to_csv(index=False).encode(), file_name="nutrient_predictions.csv")

# Close DB
conn.close()
