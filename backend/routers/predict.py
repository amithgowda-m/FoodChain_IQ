from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np

router = APIRouter()

# Load the trained model and scaler
model = joblib.load("ML_model/rf_spoilage_model.pkl")
scaler = joblib.load("ML_model/scaler.pkl")

# Simulated X_train columns (must match what was used during training)
X_train_columns = ['Temperature (°C)', 'Humidity (%)', 'Shock Level (g)',
                   'Product_Vegetables', 'Product_Fruits', 'Product_Dairy']
X_train = pd.DataFrame(columns=X_train_columns)

# Global variable to store latest sensor data
latest_sensor_data = {
    "temperature": 25.0,
    "humidity": 60.0,
    "shock_level": 0.5
}

# Pydantic models for validation
class ProductTypeRequest(BaseModel):
    product_type: str

class SensorDataRequest(BaseModel):
    temperature: float
    humidity: float
    shock_level: float

# --- ROUTE 1: Receive sensor data from ESP32 ---
@router.post("/sensor-data")
async def receive_sensor_data(data: SensorDataRequest):
    global latest_sensor_data
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

# --- ROUTE 2: Predict spoilage based on product type + latest sensor data ---
@router.post("/predict")
async def predict(request: ProductTypeRequest):
    try:
        # Get latest sensor values
        temperature = latest_sensor_data["temperature"]
        humidity = latest_sensor_data["humidity"]
        shock_level = latest_sensor_data["shock_level"]
        product_type = request.product_type

        # Create DataFrame with input features
        df = pd.DataFrame([{
            "Product_Type": product_type,
            "Temperature (°C)": temperature,
            "Humidity (%)": humidity,
            "Shock Level (g)": shock_level
        }])

        # One-hot encode product type
        product_dummies = pd.get_dummies(df[['Product_Type']], prefix='Product', drop_first=True)
        df_encoded = pd.concat([
            product_dummies,
            df[['Temperature (°C)', 'Humidity (%)', 'Shock Level (g)']]
        ], axis=1)

        # Ensure all columns are present (to match training)
        missing_cols = set(X_train.columns) - set(df_encoded.columns)
        for col in missing_cols:
            df_encoded[col] = 0
        df_encoded = df_encoded[X_train.columns]

        # Scale the features
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
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")