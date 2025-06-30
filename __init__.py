import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
from typing import Dict

# Load trained model and encoder
model = joblib.load("ML_model/spoilage_model.txt")
label_encoder = joblib.load("ML_model/product_encoder.pkl")

def predict_risk(data: Dict) -> int:
    """
    Predict spoilage risk from raw sensor data.
    
    Args:
        data: Dict containing product_id, temperature, humidity, shock
        
    Returns:
        int: Risk level - 0 (Safe), 1 (At Risk), 2 (Spoiled)
    """
    # Encode product_id
    try:
        encoded_product = label_encoder.transform([data["product_id"]])[0]
    except ValueError:
        raise ValueError(f"Product ID {data['product_id']} not seen during training.")

    # Hardcode duration_hours for now; you can enhance this later using timestamp diff
    duration_hours = 0

    # Prepare input features in correct order
    features = np.array([
        [encoded_product, data["temperature"], data["humidity"], data["shock"], duration_hours]
    ])

    # Run inference
    prediction = model.predict(features)[0]

    return int(prediction)