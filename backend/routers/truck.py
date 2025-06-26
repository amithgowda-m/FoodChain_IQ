from fastapi import APIRouter

router = APIRouter(
    prefix="/trucks",
    tags=["Trucks"]
)

@router.get("/")
def get_trucks():
    return [
        {"id": 1, "driver": "Ramesh", "location": "Bangalore"},
        {"id": 2, "driver": "Suresh", "location": "Mysore"}
    ]
