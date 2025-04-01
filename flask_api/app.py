from flask import Flask, request, jsonify
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load Models & Scaler
models = {}
for nutrient in ["Nitrogen", "Phosphorus", "Potassium", "Calcium", "Magnesium", "Sulfur"]:
    with open(f"{nutrient}_model.pkl", "rb") as f:
        models[nutrient] = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Store latest sensor readings
latest_data = {}

@app.route('/')
def home():
    return "🚀 Flask API is running! Use POST /predict to get predictions."

# New API: Receive Sensor Data from ESP32
@app.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    global latest_data
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be in JSON format"}), 400
        
        data = request.json  
        required_features = ["pH", "TDS", "Turbidity", "Temperature", "Humidity", "Light_Intensity"]

        # Validate input data
        if not all(feature in data for feature in required_features):
            return jsonify({"error": f"Missing one or more required features: {required_features}"}), 400

        latest_data = data  # Store latest readings

        # ✅ Print received data for debugging
        print("Received Sensor Data:", latest_data)

        return jsonify({"message": "Data received successfully!", "data": latest_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API to fetch the latest sensor data (for website)
@app.route('/latest-data', methods=['GET'])
def get_latest_data():
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  # Host on local network
