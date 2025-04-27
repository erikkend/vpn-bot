from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.server import Server


async def select_server_by_region(session: AsyncSession, region) -> Server | None:
    query = select(Server).where(Server.region == region, Server.is_active == True)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def select_server_by_id(session: AsyncSession, server_id) -> Server | None:
    query = select(Server).where(Server.id == server_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()