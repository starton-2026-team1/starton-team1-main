from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repositories.sensor_repository import list_sensors
from app.schemas.sensor import SensorCreate, SensorResponse, SensorUpdate
from app.services.sensor_service import (
    find_sensor_or_404,
    register_sensor,
    remove_sensor,
    update_registered_sensor,
)

router = APIRouter()


@router.post("", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor(
    data: SensorCreate, session: AsyncSession = Depends(get_db_session)
) -> SensorResponse:
    return await register_sensor(session, data)


@router.get("", response_model=list[SensorResponse])
async def get_sensors(session: AsyncSession = Depends(get_db_session)) -> list[SensorResponse]:
    return await list_sensors(session)


@router.get("/{sensor_id}", response_model=SensorResponse)
async def get_sensor(sensor_id: int, session: AsyncSession = Depends(get_db_session)) -> SensorResponse:
    return await find_sensor_or_404(session, sensor_id)


@router.patch("/{sensor_id}", response_model=SensorResponse)
async def patch_sensor(
    sensor_id: int,
    data: SensorUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> SensorResponse:
    return await update_registered_sensor(session, sensor_id, data)


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sensor(sensor_id: int, session: AsyncSession = Depends(get_db_session)) -> Response:
    await remove_sensor(session, sensor_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
