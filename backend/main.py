from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import product, truck, sensors
from database import create_db  # ✅ Import DB setup function

app = FastAPI()

# ✅ Initialize the database tables
create_db()

# ✅ Enable CORS for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:3001"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include all route handlers
app.include_router(product.router)
app.include_router(truck.router)
app.include_router(sensors.router)

# ✅ Root test endpoint
@app.get("/")
def root():
    return {"message": "FastAPI backend is working fine 🔥"}
