from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
import os

router = APIRouter()

# -----------------------------
# 1. Load Model, Scaler, and Training Columns
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
# 2. Global Variable for Latest Sensor Data
# -----------------------------
latest_sensor_data = {
    "temperature": None,
    "humidity": None,
    "shock_level": None
}

# -----------------------------
# 3. Pydantic Models for Validation
# -----------------------------
class ProductTypeRequest(BaseModel):
    product_type: str

class SensorDataRequest(BaseModel):
    temperature: float
    humidity: float
    shock_level: float

# -----------------------------
# 4. Route: Receive Sensor Data from ESP32
# -----------------------------
@router.post("/sensor-data")
async def receive_sensor_data(data: SensorDataRequest):  # ✅ fixed here
    global latest_sensor_data
    try:
        print("📥 Raw POST Data:", data.dict())  # 👈 Debug what's being sent
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
        print("🚨 Error parsing sensor data:", str(e))
        raise HTTPException(status_code=422, detail="Invalid sensor data format")

# -----------------------------
# 5. Route: Predict Spoilage Risk Based on Product Type
# -----------------------------
@router.post("/predict")
async def predict(request: ProductTypeRequest):
    try:
        # Get the latest sensor values
        temperature = latest_sensor_data["temperature"]
        humidity = latest_sensor_data["humidity"]
        shock_level = latest_sensor_data["shock_level"]
        product_type = request.product_type

        # Use fallback values if no live data yet
        if None in (temperature, humidity, shock_level):
            temperature = 25.0
            humidity = 60.0
            shock_level = 0.5
            print("⚠️ No live sensor data — using fallback values")

        # Create input dataframe
        df = pd.DataFrame([{
            "Product_Type": product_type,
            "Temperature (°C)": temperature,
            "Humidity (%)": humidity,
            "Shock Level (g)": shock_level
        }])

        # One-hot encode product type
        product_dummies = pd.get_dummies(df[['Product_Type']], prefix='Product')
        df_encoded = pd.concat([
            product_dummies,
            df[['Temperature (°C)', 'Humidity (%)', 'Shock Level (g)']]
        ], axis=1)

        # Reindex to match training columns
        df_encoded = df_encoded.reindex(columns=X_train_columns, fill_value=0)

        # Scale numerical features
        scaled_features = scaler.transform(df_encoded)

        # Make prediction
        prediction = model.predict(scaled_features)[0]
        risk_level = "Safe" if prediction == 0 else "Spoiled"

        return {
            "prediction": risk_level,
            "sensor_data": latest_sensor_data,
            "product_type": product_type
        }

    except Exception as e:
        print("🚨 Prediction error:", str(e))
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
