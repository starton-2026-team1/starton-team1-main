from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sensor import Sensor
from app.repositories.sensor_repository import (
    create_sensor,
    delete_sensor,
    get_sensor,
    update_sensor,
)
from app.schemas.sensor import SensorCreate, SensorUpdate


async def register_sensor(session: AsyncSession, data: SensorCreate) -> Sensor:
    try:
        return await create_sensor(session, data)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="device_id is already registered",
        ) from exc


async def find_sensor_or_404(session: AsyncSession, sensor_id: int) -> Sensor:
    sensor = await get_sensor(session, sensor_id)
    if sensor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return sensor


async def update_registered_sensor(
    session: AsyncSession, sensor_id: int, data: SensorUpdate
) -> Sensor:
    sensor = await find_sensor_or_404(session, sensor_id)
    return await update_sensor(session, sensor, data)


async def remove_sensor(session: AsyncSession, sensor_id: int) -> None:
    sensor = await find_sensor_or_404(session, sensor_id)
    await delete_sensor(session, sensor)
