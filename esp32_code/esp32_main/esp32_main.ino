#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>
#include <ArduinoJson.h>

// WiFi Credentials
const char* ssid = "PRAVIN CHAUDHARI";  // 🔹 Change this
const char* password = "7057964544";    // 🔹 Change this

// Flask API URLs
const char* serverURL = "http://192.168.137.43:5000/sensor-data";
const char* predictURL = "http://192.168.137.43:5000/predict";

// Sensor Pins
#define ONE_WIRE_BUS 4
#define DHTPIN 15
#define DHTTYPE DHT11
#define TDS_PIN 34

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature waterTempSensor(&oneWire);
DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

float aref = 5.0;
float ecCalibration = 7.5;
float conversionFactor = 0.90;

void setup() {
    Serial.begin(115200);
    lcd.init();
    lcd.backlight();

    dht.begin();
    waterTempSensor.begin();

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Connecting WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected!");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("WiFi Connected!");
    delay(2000);
}

void loop() {
    waterTempSensor.requestTemperatures();
    float waterTempC = waterTempSensor.getTempCByIndex(0);
    float airTempC = dht.readTemperature();
    float humidity = dht.readHumidity();

    float rawVoltage = analogRead(TDS_PIN) * aref / 4095.0;
    float ec = rawVoltage * ecCalibration;
    int tds = (133.42 * pow(ec, 3) - 255.86 * ec * ec + 857.39 * ec) * conversionFactor;

    float pH = 6.5;
    float turbidity = 10.0;
    float lightIntensity = 300.0;

    StaticJsonDocument<200> jsonDoc;
    jsonDoc["pH"] = pH;
    jsonDoc["TDS"] = tds;
    jsonDoc["Turbidity"] = turbidity;
    jsonDoc["Temperature"] = waterTempC;
    jsonDoc["Humidity"] = humidity;
    jsonDoc["Light_Intensity"] = lightIntensity;

    String jsonString;
    serializeJson(jsonDoc, jsonString);

    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;

        http.begin(serverURL);
        http.addHeader("Content-Type", "application/json");
        int httpResponseCode = http.POST(jsonString);
        Serial.print("📤 Sent Data - Response: ");
        Serial.println(httpResponseCode);
        http.end();

        http.begin(predictURL);
        http.addHeader("Content-Type", "application/json");
        httpResponseCode = http.POST(jsonString);
        Serial.print("🔮 Prediction Response: ");
        Serial.println(httpResponseCode);

        if (httpResponseCode == 200) {
            String response = http.getString();
            Serial.print("Predicted Nutrients: ");
            Serial.println(response);
        }

        http.end();
    } else {
        Serial.println("WiFi Disconnected!");
    }

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Water Temp: ");
    lcd.print(waterTempC);
    lcd.print("C");
    lcd.setCursor(0, 1);
    lcd.print("Air Temp: ");
    lcd.print(airTempC);
    lcd.print("C");
    delay(2000);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Humidity: ");
    lcd.print(humidity);
    lcd.print("%");
    delay(2000);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("TDS: ");
    lcd.print(tds);
    lcd.print("ppm");
    lcd.setCursor(0, 1);
    lcd.print("pH: ");
    lcd.print(pH);
    delay(2000);

    delay(10000);
}
