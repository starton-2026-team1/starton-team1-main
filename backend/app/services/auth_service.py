from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import create_user, get_user_by_email, update_user
from app.schemas.auth import AuthResponse, LoginRequest, SignUpRequest, UserUpdate


def build_auth_response(user: User) -> AuthResponse:
    return AuthResponse(
        access_token=create_access_token(user.id),
        user=user,
    )


async def sign_up(session: AsyncSession, data: SignUpRequest) -> AuthResponse:
    if await get_user_by_email(session, str(data.email)) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )
    try:
        user = await create_user(
            session,
            str(data.email),
            hash_password(data.password),
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        ) from exc
    return build_auth_response(user)


async def log_in(session: AsyncSession, data: LoginRequest) -> AuthResponse:
    user = await get_user_by_email(session, str(data.email))
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return build_auth_response(user)


async def update_account(
    session: AsyncSession, user: User, data: UserUpdate
) -> User:
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect",
        )

    new_email = str(data.email) if data.email is not None else None
    if new_email is not None:
        existing = await get_user_by_email(session, new_email)
        if existing is not None and existing.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )
    try:
        return await update_user(
            session,
            user,
            email=new_email,
            password_hash=(
                hash_password(data.new_password) if data.new_password else None
            ),
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        ) from exc
