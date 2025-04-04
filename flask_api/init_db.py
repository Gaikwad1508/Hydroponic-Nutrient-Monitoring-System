import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("hydroponics.db")
cursor = conn.cursor()

# 🚰 Create table for sensor readings
cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pH REAL,
    TDS REAL,
    Turbidity REAL,
    Temperature REAL,
    Humidity REAL,
    Light_Intensity REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# 🌿 Create table for nutrient predictions
cursor.execute("""
CREATE TABLE IF NOT EXISTS nutrient_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nitrogen REAL,
    Phosphorus REAL,
    Potassium REAL,
    Calcium REAL,
    Magnesium REAL,
    Sulfur REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("✅ Database initialized successfully.")
