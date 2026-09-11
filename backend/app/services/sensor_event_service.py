from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sensor_event import SensorEvent
from app.repositories.person_repository import get_person
from app.repositories.sensor_event_repository import create_sensor_event
from app.repositories.sensor_repository import get_sensor
from app.schemas.sensor_event import SensorEventCreate


async def record_sensor_event(
    session: AsyncSession, data: SensorEventCreate
) -> SensorEvent:
    if await get_person(session, data.person_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Person not found"
        )
    if await get_sensor(session, data.sensor_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found"
        )
    return await create_sensor_event(session, data)
