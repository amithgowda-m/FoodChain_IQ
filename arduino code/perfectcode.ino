#include <WiFi.h>
#include <DHT.h>
#include <Wire.h>
#include "MPU6050_tockn.h"

// === Wi-Fi Credentials ===
const char* ssid = "  ";     // Replace with your Wi-Fi name
const char* password = " ";      // Replace with your Wi-Fi password

// === DHT22 Sensor Setup ===
#define DHTPIN 18         // GPIO pin connected to DHT22
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// === MPU6050 Sensor Setup ===
TwoWire I2Cone = TwoWire(0);  
MPU6050 mpu(I2Cone);


const char* server = "192.168.110.177";  
const int port = 8000;
const char* endpoint = "/api/v1/sensor-data";

WiFiClient client;


float calculateShockLevel() {
  mpu.update();
  float ax = abs(mpu.getAccX());
  float ay = abs(mpu.getAccY());
  float az = abs(mpu.getAccZ());
  return ax + ay + az;  
}


String buildJsonPayload(float temperature, float humidity, float shock_level) {
  return String("{\"temperature\":") +
         String(temperature, 2) + "," +
         "\"humidity\":" + String(humidity, 2) + "," +
         "\"shock_level\":" + String(shock_level, 2) +
         "}";
}


void testConnection() {
  Serial.println("📡 Testing connection to backend...");

  if (client.connect(server, port)) {
    Serial.println(" Connected to server!");
    client.print(String("GET / HTTP/1.1\r\n") +
                 "Host: " + String(server) + "\r\n" +
                 "Connection: close\r\n\r\n");
    delay(1000);

    while (client.available()) {
      String line = client.readStringUntil('\r');
      Serial.print(line);
    }

    client.stop();
  } else {
    Serial.println(" Failed to connect to server!");
  }
}


void setup() {
  Serial.begin(115200);
  delay(1000);

  
  dht.begin();

  
  I2Cone.begin(21, 22, 400000); 
  mpu.begin();
  mpu.calcGyroOffsets(true);  
  Serial.println("MPU6050 initialized");

 
  Serial.print(" Connecting to WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 20) {
    delay(500);
    Serial.print(".");
    retries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected");
    Serial.print(" IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n WiFi connection failed!");
    return;
  }

  testConnection();  
}


void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(5000);
    return;
  }

  float shock_level = calculateShockLevel();

  // Log to serial
  Serial.printf(" Temp: %.2f°C | Humidity: %.2f%% |  Shock Level: %.2f g\n",
                temperature, humidity, shock_level);

  
  String jsonPayload = buildJsonPayload(temperature, humidity, shock_level);

  
  if (client.connect(server, port)) {
    client.print(String("POST ") + endpoint + " HTTP/1.1\r\n" +
                 "Host: " + server + "\r\n" +
                 "Content-Type: application/json\r\n" +
                 "Content-Length: " + jsonPayload.length() + "\r\n\r\n" +
                 jsonPayload);

    Serial.println(" Data sent:");
    Serial.println(jsonPayload);
    client.stop();
  } else {
    Serial.println(" Failed to connect to backend server!");
  }

  delay(5000);  
}