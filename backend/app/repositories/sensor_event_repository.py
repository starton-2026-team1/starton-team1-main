from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.person import Person
from app.models.sensor_event import SensorEvent
from app.schemas.sensor_event import SensorEventCreate


async def create_sensor_event(
    session: AsyncSession, data: SensorEventCreate
) -> SensorEvent:
    event = SensorEvent(**data.model_dump())
    session.add(event)
    await session.flush()
    await session.refresh(event)
    return event


async def list_sensor_events(
    session: AsyncSession,
    user_id: int,
    person_id: int | None = None,
    limit: int = 100,
) -> list[SensorEvent]:
    query: Select[tuple[SensorEvent]] = (
        select(SensorEvent)
        .join(Person, Person.id == SensorEvent.person_id)
        .where(or_(Person.user_id == user_id, Person.user_id.is_(None)))
    )
    if person_id is not None:
        query = query.where(SensorEvent.person_id == person_id)
    query = query.order_by(SensorEvent.detected_at.desc()).limit(limit)
    result = await session.scalars(query)
    return list(result.all())
