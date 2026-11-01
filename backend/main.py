
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analytics import router as analytics_router


app = FastAPI(
    title="Wind Forecast Intelligence API",
    description="UK wind generation forecast and accuracy analysis",
    version="1.0.0",
)

frontend_url = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_url,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "wind-forecast-api",
    }
