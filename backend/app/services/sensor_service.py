from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sensor import Sensor
from app.repositories.person_repository import get_person
from app.repositories.sensor_repository import (
    create_sensor,
    delete_sensor,
    get_sensor,
    update_sensor,
)
from app.schemas.sensor import SensorCreate, SensorUpdate


async def _ensure_person_exists(session: AsyncSession, person_id: int) -> None:
    if await get_person(session, person_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Person not found"
        )


async def register_sensor(session: AsyncSession, data: SensorCreate) -> Sensor:
    await _ensure_person_exists(session, data.person_id)
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
    if data.person_id is not None:
        await _ensure_person_exists(session, data.person_id)
    return await update_sensor(session, sensor, data)


async def remove_sensor(session: AsyncSession, sensor_id: int) -> None:
    sensor = await find_sensor_or_404(session, sensor_id)
    await delete_sensor(session, sensor)
