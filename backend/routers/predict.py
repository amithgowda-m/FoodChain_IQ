from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
import os
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

router = APIRouter()

# -----------------------------
# ✨ Initialize SQLite DB
# -----------------------------
def init_db():
    conn = sqlite3.connect('foodchain.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  temperature REAL,
                  humidity REAL,
                  shock_level REAL,
                  product_type TEXT,
                  prediction TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# -----------------------------
# Load Model, Scaler, Columns
# -----------------------------
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))  # /backend/routers
    model_path = os.path.join(base_dir, "..", "ML_model", "rf_spoilage_model.pkl")
    scaler_path = os.path.join(base_dir, "..", "ML_model", "scaler.pkl")
    columns_path = os.path.join(base_dir, "..", "ML_model", "X_train_columns.pkl")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    X_train_columns = joblib.load(columns_path)
except Exception as e:
    raise Exception("Model or scaler not found. Make sure to train first.") from e

# -----------------------------
# Email Alert Settings
# -----------------------------
SENDER_EMAIL = "foodchainiq@gmail.com"
SENDER_PASSWORD = "bnte halh rgpn ehgo"  # App password (not Gmail login)
RECEIVER_EMAIL = "gowdaamithm@gmail.com"

def send_email_alert(temperature, humidity, shock_level, product_type):
    print("📧 Attempting to send email alert...")
    
    subject = "🚨 FoodChain IQ: Spoilage Alert from FoodChain IQ"
    body = f"""ALERT: Spoiled product detected.

Product Type: {product_type}
Temperature: {temperature}°C
Humidity: {humidity}%
Shock Level: {shock_level}g

Please take immediate action."""

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.set_debuglevel(1)  # 🔍 Enable SMTP debug output
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("✅ Email alert sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)

# -----------------------------
# Global Sensor State
# -----------------------------
latest_sensor_data = {
    "temperature": None,
    "humidity": None,
    "shock_level": None
}

# -----------------------------
# Pydantic Schemas
# -----------------------------
class ProductTypeRequest(BaseModel):
    product_type: str

class SensorDataRequest(BaseModel):
    temperature: float
    humidity: float
    shock_level: float

# -----------------------------
# Save Prediction
# -----------------------------
def save_prediction(temperature, humidity, shock_level, product_type, prediction):
    conn = sqlite3.connect('foodchain.db')
    c = conn.cursor()
    c.execute('''INSERT INTO predictions 
                 (temperature, humidity, shock_level, product_type, prediction)
                 VALUES (?, ?, ?, ?, ?)''',
              (temperature, humidity, shock_level, product_type, prediction))
    conn.commit()
    conn.close()

# -----------------------------
# Route: Receive Sensor Data
# -----------------------------
@router.post("/sensor-data")
async def receive_sensor_data(data: SensorDataRequest):
    global latest_sensor_data
    try:
        latest_sensor_data.update({
            "temperature": data.temperature,
            "humidity": data.humidity,
            "shock_level": data.shock_level
        })
        return {
            "status": "success",
            "message": "Sensor data updated successfully",
            "received": latest_sensor_data
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail="Invalid sensor data format")

# -----------------------------
# Route: Predict Spoilage
# -----------------------------
@router.post("/predict")
async def predict(request: ProductTypeRequest):
    try:
        temperature = latest_sensor_data["temperature"]
        humidity = latest_sensor_data["humidity"]
        shock_level = latest_sensor_data["shock_level"]
        product_type = request.product_type

        if None in (temperature, humidity, shock_level):
            temperature = 25.0
            humidity = 60.0
            shock_level = 0.5
            print("⚠️ No live sensor data — using fallback values")

        df = pd.DataFrame([{
            "Product_Type": product_type,
            "Temperature (°C)": temperature,
            "Humidity (%)": humidity,
            "Shock Level (g)": shock_level
        }])

        product_dummies = pd.get_dummies(df[['Product_Type']], prefix='Product')
        df_encoded = pd.concat([
            product_dummies,
            df[['Temperature (°C)', 'Humidity (%)', 'Shock Level (g)']]
        ], axis=1)

        df_encoded = df_encoded.reindex(columns=X_train_columns, fill_value=0)
        scaled_features = scaler.transform(df_encoded)
        prediction = model.predict(scaled_features)[0]
        risk_level = "Safe" if prediction == 0 else "Spoiled"

        print(f"📊 Prediction result: {risk_level}")

        # Save to DB
        save_prediction(temperature, humidity, shock_level, product_type, risk_level)

        # Email alert only if risk is "Spoiled"
        if risk_level == "Spoiled":
            print("🚨 Spoiled detected. Triggering email alert...")
            send_email_alert(temperature, humidity, shock_level, product_type)

        return {
            "prediction": risk_level,
            "sensor_data": latest_sensor_data,
            "product_type": product_type
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# -----------------------------
# Route: Get Prediction History
# -----------------------------
@router.get("/history")
async def get_prediction_history(limit: int = 10):
    try:
        conn = sqlite3.connect('foodchain.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(f"SELECT * FROM predictions ORDER BY timestamp DESC LIMIT {limit}")
        rows = c.fetchall()
        conn.close()

        history = [dict(row) for row in rows]
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")
