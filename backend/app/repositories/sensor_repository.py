from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate, SensorUpdate


async def create_sensor(session: AsyncSession, data: SensorCreate) -> Sensor:
    sensor = Sensor(**data.model_dump())
    session.add(sensor)
    await session.flush()
    await session.refresh(sensor)
    return sensor


async def list_sensors(session: AsyncSession) -> list[Sensor]:
    result = await session.scalars(select(Sensor).order_by(Sensor.id))
    return list(result.all())


async def get_sensor(session: AsyncSession, sensor_id: int) -> Sensor | None:
    return await session.get(Sensor, sensor_id)


async def update_sensor(session: AsyncSession, sensor: Sensor, data: SensorUpdate) -> Sensor:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(sensor, key, value)
    await session.flush()
    await session.refresh(sensor)
    return sensor


async def delete_sensor(session: AsyncSession, sensor: Sensor) -> None:
    await session.delete(sensor)
