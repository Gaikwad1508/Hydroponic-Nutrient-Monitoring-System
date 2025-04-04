import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("hydroponics.db")

# Read sensor readings
print("📊 Sensor Readings:")
sensor_df = pd.read_sql_query("SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 5", conn)
print(sensor_df)

# Read nutrient predictions
print("\n🔮 Nutrient Predictions:")
prediction_df = pd.read_sql_query("SELECT * FROM nutrient_predictions ORDER BY timestamp DESC LIMIT 5", conn)
print(prediction_df)

conn.close()
