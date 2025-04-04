from flask import Flask, request, jsonify
import pickle
import sqlite3
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_config import EMAIL_ADDRESS, EMAIL_PASSWORD, TO_EMAIL

app = Flask(__name__)

# Load scaler and models
with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("models/nitrogen_model.pkl", "rb") as f:
    model_nitrogen = pickle.load(f)

with open("models/phosphorus_model.pkl", "rb") as f:
    model_phosphorus = pickle.load(f)

with open("models/potassium_model.pkl", "rb") as f:
    model_potassium = pickle.load(f)

with open("models/calcium_model.pkl", "rb") as f:
    model_calcium = pickle.load(f)

with open("models/magnesium_model.pkl", "rb") as f:
    model_magnesium = pickle.load(f)

with open("models/sulfur_model.pkl", "rb") as f:
    model_sulfur = pickle.load(f)

# Initialize database connection
db_conn = sqlite3.connect("hydroponics.db", check_same_thread=False)

# Nutrient thresholds
NUTRIENT_THRESHOLDS = {
    "Nitrogen": (1000, 2000),
    "Phosphorus": (3, 10),
    "Potassium": (50, 100),
    "Calcium": (40, 80),
    "Magnesium": (30, 60),
    "Sulfur": (1, 5),
}

def check_thresholds_and_alert(nutrients):
    alerts = []
    for nutrient, value in nutrients.items():
        min_val, max_val = NUTRIENT_THRESHOLDS[nutrient]
        if value < min_val or value > max_val:
            alerts.append(f"{nutrient}: {value:.2f} (Out of range {min_val}-{max_val})")

    if alerts:
        send_email_alert(alerts)

def send_email_alert(alerts):
    subject = "🚨 Hydroponics Alert: Nutrient Threshold Breached"
    body = "The following nutrient levels are outside the safe range:\n\n" + "\n".join(alerts)

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("📧 Alert email sent.")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

@app.route('/sensor-data', methods=['POST'])
def sensor_data():
    try:
        data = request.get_json()
        print(f"📅 Received Sensor Data: {data}")

        cursor = db_conn.cursor()
        cursor.execute("""
            INSERT INTO sensor_readings (pH, TDS, Turbidity, Temperature, Humidity, Light_Intensity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["pH"], data["TDS"], data["Turbidity"],
            data["Temperature"], data["Humidity"], data["Light_Intensity"]
        ))
        db_conn.commit()
        return jsonify({"message": "Sensor data stored successfully."}), 200

    except Exception as e:
        print(f"🔥 Error in /sensor-data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        sensor_data = request.get_json()
        print(f"📅 Received Sensor Data: {sensor_data}")

        # Rename to match training column names
        input_data = {
            "pH": sensor_data["pH"],
            "TDS (ppm)": sensor_data["TDS"],
            "Turbidity (NTU)": sensor_data["Turbidity"],
            "Temperature (°C)": sensor_data["Temperature"],
            "Humidity (%)": sensor_data["Humidity"],
            "Light Intensity (lux)": sensor_data["Light_Intensity"]
        }

        input_df = pd.DataFrame([input_data])
        scaled_input = scaler.transform(input_df)

        prediction = {
            "Nitrogen": model_nitrogen.predict(scaled_input)[0],
            "Phosphorus": model_phosphorus.predict(scaled_input)[0],
            "Potassium": model_potassium.predict(scaled_input)[0],
            "Calcium": model_calcium.predict(scaled_input)[0],
            "Magnesium": model_magnesium.predict(scaled_input)[0],
            "Sulfur": model_sulfur.predict(scaled_input)[0]
        }

        print(f"🔮 Predicted Nutrients: {prediction}")

        # Store predictions in DB
        cursor = db_conn.cursor()
        cursor.execute("""
            INSERT INTO nutrient_predictions (Nitrogen, Phosphorus, Potassium, Calcium, Magnesium, Sulfur)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            prediction["Nitrogen"], prediction["Phosphorus"], prediction["Potassium"],
            prediction["Calcium"], prediction["Magnesium"], prediction["Sulfur"]
        ))
        db_conn.commit()

        # Alert if out of threshold
        check_thresholds_and_alert(prediction)

        return jsonify(prediction), 200

    except Exception as e:
        print(f"🔥 Error in /predict: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
