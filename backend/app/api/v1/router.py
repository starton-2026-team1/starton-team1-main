from fastapi import APIRouter

from app.api.v1.people import router as people_router
from app.api.v1.sensor_events import router as sensor_events_router
from app.api.v1.sensors import router as sensors_router

api_router = APIRouter()
api_router.include_router(people_router, prefix="/people", tags=["People"])
api_router.include_router(sensors_router, prefix="/sensors", tags=["Sensors"])
api_router.include_router(
    sensor_events_router, prefix="/sensor-events", tags=["Sensor Events"]
)
