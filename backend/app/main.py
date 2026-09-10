from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import (
    check_database_connection,
    close_database_connection,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await check_database_connection()
    yield
    await close_database_connection()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


class SensorCreate(BaseModel):
    name: str
    location: str
    device_id: str
    status: str


sensors = []


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/sensors")
def create_sensor(sensor: SensorCreate):
    new_sensor = {
        "id": len(sensors) + 1,
        "name": sensor.name,
        "location": sensor.location,
        "device_id": sensor.device_id,
        "status": sensor.status,
    }

    sensors.append(new_sensor)

    return new_sensor