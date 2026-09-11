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
    # 이벤트 생성 시점에는 sensor_id가 항상 있어야 한다.
    # (sensor_id가 NULL로 남는 경우는 이후 센서가 삭제됐을 때뿐)
    if data.sensor_id is None or await get_sensor(session, data.sensor_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found"
        )
    return await create_sensor_event(session, data)
