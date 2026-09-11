from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.person import Person
from app.repositories.person_repository import (
    create_person,
    delete_person,
    get_person,
    update_person,
)
from app.schemas.person import PersonCreate, PersonUpdate


async def register_person(session: AsyncSession, data: PersonCreate) -> Person:
    return await create_person(session, data)


async def find_person_or_404(session: AsyncSession, person_id: int) -> Person:
    person = await get_person(session, person_id)
    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Person not found"
        )
    return person


async def update_registered_person(
    session: AsyncSession, person_id: int, data: PersonUpdate
) -> Person:
    person = await find_person_or_404(session, person_id)
    return await update_person(session, person, data)


async def remove_person(session: AsyncSession, person_id: int) -> None:
    person = await find_person_or_404(session, person_id)
    await delete_person(session, person)
