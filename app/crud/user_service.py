from sqlalchemy import select
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_by_telegram_id(session: AsyncSession, telegram_id: str) -> User | None:
    query = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def get_user_by_user_id(session: AsyncSession, user_id: str) -> User | None:
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, telegram_id: str, username: str) -> User:
    user = User(telegram_id=telegram_id, username=username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
