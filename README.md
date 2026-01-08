# 🌿 Smart Hydroponic Monitoring & Nutrient Prediction System

> **An IoT-enabled solution for precision agriculture using Machine Learning to predict nutrient levels.**

## 📌 Overview
Traditional hydroponic farming requires constant manual testing of water parameters. This project automates that process. It is a **Smart Hydroponic Monitoring System** that collects real-time data (pH, TDS, Turbidity) and uses **Machine Learning algorithms** to predict the exact concentration of essential nutrients (N, P, K, Ca, Mg, S).

The system features a live **Streamlit Dashboard** for visualization, threshold-based alerts for anomaly detection, and offline data logging to ensure reliability in remote agricultural environments.

## 🚀 Key Features
* **Real-time Monitoring:** Continuous tracking of critical environmental metrics (pH, TDS, Turbidity, Temp, Humidity).
* **AI-Driven Nutrient Prediction:** Utilizes **Random Forest & XGBoost** models to infer complex nutrient compositions (Nitrogen, Phosphorus, Potassium) based on raw sensor inputs.
* **Smart Alert System:** Instant threshold-based notifications when water quality drops or nutrient levels become critical.
* **Interactive Analytics:** A dynamic dashboard built with Streamlit to visualize historical trends and sensor health.
* **Offline Reliability:** Robust local data logging (SQLite/CSV) ensures no data is lost during internet outages.

## 🏗️ System Workflow
The system operates in three main stages:
1.  **Data Acquisition:** IoT sensors (pH, TDS, Turbidity) capture raw water quality parameters.
2.  **Processing & Prediction:** The microcontroller transmits data to the Python backend, where ML models analyze the inputs to predict nutrient concentrations.
3.  **Visualization:** The processed data is displayed on the Streamlit dashboard, providing farmers with actionable insights and alerts.

## 📸 Project Demo

### 1. Live Monitoring Dashboard
*Real-time visualization of sensor trends and live summary status.*
<img width="1909" height="982" alt="Screenshot 2025-05-11 220107" src="https://github.com/user-attachments/assets/48cb55bd-82fd-4a40-bf07-14d8ed4d093e" />

### 2. Nutrient Composition & Alerts
*ML-predicted nutrient breakdown and threshold alert system.*
<img width="1914" height="831" alt="Screenshot 2025-05-11 220146" src="https://github.com/user-attachments/assets/6731fef9-a240-44f2-a58d-b855e23e7f1c" />


### 3. Dataset & Training Data
*Sample of the dataset used to train the regression models.*
<img width="980" height="265" alt="Screenshot 2025-05-11 220353" src="https://github.com/user-attachments/assets/40aa57dc-5b89-4062-a9dd-17a34db8a2ee" />


## 🛠️ Tech Stack
* **Hardware:** ESP32/Arduino, Analog Water Quality Sensors.
* **Backend:** Python, Flask (API).
* **Machine Learning:** Scikit-Learn (Linear Regression, Random Forest, XGBoost).
* **Data Visualization:** Streamlit, Plotly, Altair.
* **Database:** SQLite / CSV (Offline Handling).

## 🔮 Future Scope
* **Automated Dosing:** Integrating peristaltic pumps to automatically correct nutrient levels based on ML predictions.
* **Cloud Integration:** Migrating data storage to AWS/Firebase for remote accessibility.
* **Mobile App:** Developing a Flutter-based mobile application for on-the-go monitoring.
