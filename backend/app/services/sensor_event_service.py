from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sensor_event import SensorEvent
from app.repositories.person_repository import get_owned_person
from app.repositories.sensor_event_repository import create_sensor_event
from app.repositories.sensor_repository import get_owned_sensor
from app.schemas.sensor_event import SensorEventCreate


async def record_sensor_event(
    session: AsyncSession, user_id: int, data: SensorEventCreate
) -> SensorEvent:
    if await get_owned_person(session, data.person_id, user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Person not found"
        )
    if data.sensor_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found"
        )
    sensor = await get_owned_sensor(session, data.sensor_id, user_id)
    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found"
        )
    if sensor.person_id != data.person_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sensor is not assigned to the person",
        )
    return await create_sensor_event(session, data)
