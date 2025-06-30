from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..models import SensorData, SensorDataCreate, SensorDataRead
from ..database import get_db
from ..ML_model import predict_risk

router = APIRouter(prefix="/predict", tags=["Spoilage Prediction"])

@router.post("/risk")
def predict_spoilage(data: SensorDataCreate, db: Session = Depends(get_db)) -> dict:
    try:
        risk_level = predict_risk(data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Optional: Save result back to database
    db_data = SensorData(**data.dict(), risk_prediction=risk_level)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return {"risk_level": risk_level}