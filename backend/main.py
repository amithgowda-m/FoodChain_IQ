from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # CORS middleware import
from routers.predict import router as predict_router

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include the prediction router
app.include_router(predict_router, prefix="/api/v1")