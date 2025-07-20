from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..models import SensorData, SensorDataCreate, SensorDataRead
from ..database import get_db
from ..ML_model import predict_risk

import smtplib
from email.message import EmailMessage

# ✅ Email settings
SENDER_EMAIL = "foodchainiq@gmail.com"
SENDER_PASSWORD = "1234Abcd"  # Use an app password (for Gmail with 2FA)
RECIPIENT_EMAIL = "amithgowdam.cs24@rvce.edu.in"

router = APIRouter(prefix="/predict", tags=["Spoilage Prediction"])

def send_email_alert(risk_level, data):
    subject = "⚠️ FoodChain IQ Spoilage Alert"
    body = (
        f"Food spoilage has been detected.\n\n"
        f"Prediction: {risk_level.upper()}\n"
        f"Temperature: {data.temperature}°C\n"
        f"Humidity: {data.humidity}%\n"
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
            print("Email alert sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

@router.post("/risk")
def predict_spoilage(data: SensorDataCreate, db: Session = Depends(get_db)) -> dict:
    try:
        risk_level = predict_risk(data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # ✅ Send email alert after prediction
    send_email_alert(risk_level, data)

    # ✅ Save result in DB
    db_data = SensorData(**data.dict(), risk_prediction=risk_level)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return {"risk_level": risk_level}
