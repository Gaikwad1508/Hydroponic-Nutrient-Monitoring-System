#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>
#include <ArduinoJson.h>

// WiFi Credentials
const char* ssid = "PRAVIN CHAUDHARI";  // 🔹 Change this   //YOUR_WIFI_SSID
const char* password = "7057964544";  // 🔹 Change this     //YOUR_WIFI_PASSWORD

// Flask Server Address
const char* serverURL = "http://192.168.137.129:5000/sensor-data";      // 🔹 Replace with your PC's local IP   //http://YOUR_PC_IP:5000/sensor-data

// Define Sensor Pins
#define ONE_WIRE_BUS 4       // DS18B20 Water Temperature
#define DHTPIN 15            // DHT11 Air Temperature & Humidity
#define DHTTYPE DHT11
#define TDS_PIN 34           // TDS Sensor (ADC Pin)

// Sensor Instances
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature waterTempSensor(&oneWire);
DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Constants for TDS & EC Calibration
float aref = 5.0;
float ecCalibration = 7.5;
float conversionFactor = 0.90;

void setup() {
    Serial.begin(115200);
    lcd.init();
    lcd.backlight();
    dht.begin();
    waterTempSensor.begin();

    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected!");
}

void loop() {
    // ✅ Read Water Temperature
    waterTempSensor.requestTemperatures();
    float waterTempC = waterTempSensor.getTempCByIndex(0);

    // ✅ Read Air Temperature & Humidity
    float airTempC = dht.readTemperature();
    float humidity = dht.readHumidity();

    // ✅ Read TDS (Simulated for now)
    float rawVoltage = analogRead(TDS_PIN) * aref / 4095.0;
    float ec = rawVoltage * ecCalibration;
    int tds = (133.42 * pow(ec, 3) - 255.86 * ec * ec + 857.39 * ec) * conversionFactor;

    // ✅ Dummy Values for pH, Turbidity, Light Intensity
    float pH = 6.5; // Temporary value until sensor is connected
    float turbidity = 10.0; // Temporary value
    float lightIntensity = 300.0; // Temporary value

    // ✅ Create JSON Object
    StaticJsonDocument<200> jsonDoc;
    jsonDoc["pH"] = pH;
    jsonDoc["TDS"] = tds;
    jsonDoc["Turbidity"] = turbidity;
    jsonDoc["Temperature"] = waterTempC;
    jsonDoc["Humidity"] = humidity;
    jsonDoc["Light_Intensity"] = lightIntensity;

    // ✅ Serialize JSON
    String jsonString;
    serializeJson(jsonDoc, jsonString);

    // ✅ Send Data to Flask API
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverURL);
        http.addHeader("Content-Type", "application/json");

        int httpResponseCode = http.POST(jsonString);
        Serial.print("HTTP Response Code: ");
        Serial.println(httpResponseCode);

        http.end();
    } else {
        Serial.println("WiFi Disconnected!");
    }

    // ✅ LCD Display (Page 1)
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Water T: "); lcd.print(waterTempC); lcd.print("C");
    lcd.setCursor(0, 1);
    lcd.print("Air T: "); lcd.print(airTempC); lcd.print("C");
    delay(2000);

    // ✅ LCD Display (Page 2)
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Humidity: ");
    lcd.setCursor(0, 1);
    lcd.print(humidity); lcd.print("%");
    delay(2000);

    // ✅ LCD Display (Page 3)
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("TDS: "); lcd.print(tds); lcd.print("ppm");
    lcd.setCursor(0, 1);
    lcd.print("pH: "); lcd.print(pH);
    delay(2000);

    delay(10000); // 🔄 Send Data Every 10 Seconds
}
