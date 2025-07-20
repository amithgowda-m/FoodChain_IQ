from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.predict import router as predict_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include prediction router
app.include_router(predict_router, prefix="/api/v1")

# ✅ Add this new route
@app.get("/")
def read_root():
    return {"message": "Welcome to Food Spoilage Prediction API"}