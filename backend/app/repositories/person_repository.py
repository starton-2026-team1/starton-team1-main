from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.person import Person
from app.schemas.person import PersonCreate, PersonUpdate


async def create_person(session: AsyncSession, data: PersonCreate) -> Person:
    person = Person(**data.model_dump())
    session.add(person)
    await session.flush()
    await session.refresh(person)
    return person


async def list_people(session: AsyncSession) -> list[Person]:
    result = await session.scalars(select(Person).order_by(Person.id))
    return list(result.all())


async def get_person(session: AsyncSession, person_id: int) -> Person | None:
    return await session.get(Person, person_id)


async def update_person(session: AsyncSession, person: Person, data: PersonUpdate) -> Person:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(person, key, value)
    await session.flush()
    await session.refresh(person)
    return person


async def delete_person(session: AsyncSession, person: Person) -> None:
    await session.delete(person)
