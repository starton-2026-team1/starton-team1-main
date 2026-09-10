from fastapi import APIRouter

from app.api.v1.sensors import router as sensors_router

api_router = APIRouter()
api_router.include_router(sensors_router, prefix="/sensors", tags=["Sensors"])
