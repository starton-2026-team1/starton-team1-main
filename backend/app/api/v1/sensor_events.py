from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repositories.sensor_event_repository import list_sensor_events
from app.schemas.sensor_event import SensorEventCreate, SensorEventResponse
from app.services.sensor_event_service import record_sensor_event

router = APIRouter()


@router.post("", response_model=SensorEventResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor_event(
    data: SensorEventCreate, session: AsyncSession = Depends(get_db_session)
) -> SensorEventResponse:
    return await record_sensor_event(session, data)


@router.get("", response_model=list[SensorEventResponse])
async def get_sensor_events(
    person_id: int | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
) -> list[SensorEventResponse]:
    return await list_sensor_events(session, person_id, limit)


@router.get("/people/{person_id}/timeline", response_model=list[SensorEventResponse])
async def get_person_timeline(
    person_id: int,
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
) -> list[SensorEventResponse]:
    return await list_sensor_events(session, person_id, limit)
