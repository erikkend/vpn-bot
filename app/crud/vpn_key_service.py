from app.models.vpn_key import VPNKey

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


async def get_vpn_key_by_user_id(session: AsyncSession, user_id: str) -> list[VPNKey]:
    query = select(VPNKey).options(selectinload(VPNKey.subscription), selectinload(VPNKey.server)).where(VPNKey.user_id == user_id, VPNKey.is_active == True)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def create_vpn_key(session: AsyncSession, user_id: str, created_key: str, key_uuid: str, key_email: str) -> VPNKey:
    # временно key_email и key_sub_id одинаковые
    vpn_key = VPNKey(user_id=user_id, full_key_data=created_key, key_uuid=key_uuid, key_email=key_email, key_sub_id=key_email)
    session.add(vpn_key)
    await session.commit()
    await session.refresh(vpn_key)
    return vpn_key
