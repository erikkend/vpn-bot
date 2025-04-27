from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vpn_key import VPNKey
from app.models.subscription import Subscription

async def deactivate_expired_configs(session: AsyncSession):
    now = datetime.now()

    query = (
        select(VPNKey)
        .join(Subscription)
        .where(
            Subscription.expires_at < now,
            VPNKey.is_active == True
        )
    )
    result = await session.execute(query)
    expired_configs = result.scalars().all()

    for config in expired_configs:
        config.is_active = False

    await session.commit()
