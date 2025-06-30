from fastapi import APIRouter

router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"]
)

@router.get("/")
def get_readings():
    return [
        {"id": 1, "temperature": 24.5, "humidity": 62},
        {"id": 2, "temperature": 25.2, "humidity": 59}
    ]
