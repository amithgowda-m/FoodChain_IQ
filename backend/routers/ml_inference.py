from fastapi import APIRouter, Depends
from sqlmodel import Session
from .. import models, database, ML_model

router = APIRouter(prefix="/predict", tags=["Spoilage Prediction"])

@router.post("/")
async def predict_spoilage(data: models.SensorDataCreate, db: Session = Depends(database.get_db)):
    prediction = ML_model.predict_risk(
        product_id=data.product_id,
        temperature=data.temperature,
        humidity=data.humidity,
        shock_level=data.shock,
        duration_hours=0  # You can calculate or receive this value dynamically
    )

    # Optionally save prediction back to DB
    db_data = models.SensorData(**data.dict(), risk_prediction=prediction)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    return {"prediction": prediction}