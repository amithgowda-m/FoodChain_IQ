from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..models import SensorData, SensorDataCreate, SensorDataRead
from ..database import get_db
from ..ML_model import predict_risk

# ✅ Twilio for SMS
from twilio.rest import Client

# ✅ Twilio credentials (replace with your actual info)
ACCOUNT_SID = 'YOUR_TWILIO_SID'
AUTH_TOKEN = 'YOUR_TWILIO_AUTH'
TWILIO_FROM = '+1234567890'       # Your Twilio phone number
TO_NUMBER = '+91XXXXXXXXXX'       # Recipient number

router = APIRouter(prefix="/predict", tags=["Spoilage Prediction"])

def send_sms_alert(risk_level, data):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    msg = (
        f"⚠️ FoodChain IQ Alert:\n"
        f"Prediction: {risk_level.upper()}.\n"
        f"Temp: {data.temperature}°C, Humidity: {data.humidity}%"
    )

    try:
        message = client.messages.create(
            body=msg,
            from_=TWILIO_FROM,
            to=TO_NUMBER
        )
        print(f"SMS sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

@router.post("/risk")
def predict_spoilage(data: SensorDataCreate, db: Session = Depends(get_db)) -> dict:
    try:
        risk_level = predict_risk(data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # ✅ Send SMS alert after prediction
    send_sms_alert(risk_level, data)

    # ✅ Save to DB
    db_data = SensorData(**data.dict(), risk_prediction=risk_level)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return {"risk_level": risk_level}
