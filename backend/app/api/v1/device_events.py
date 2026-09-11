from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import verify_device_api_key
from app.core.database import get_db_session
from app.schemas.sensor_event import DeviceEventCreate, DeviceEventResponse
from app.services.device_event_service import record_device_event

router = APIRouter(dependencies=[Depends(verify_device_api_key)])


@router.post("", response_model=DeviceEventResponse, status_code=status.HTTP_201_CREATED)
async def create_device_event(
    data: DeviceEventCreate,
    response: Response,
    session: AsyncSession = Depends(get_db_session),
) -> DeviceEventResponse:
    event, created = await record_device_event(session, data)
    if not created:
        response.status_code = status.HTTP_200_OK
    return event
