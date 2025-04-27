from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subscription import Subscription


async def create_subscription(session: AsyncSession, vpn_id, expire_date) -> Subscription:
    subscription = Subscription(vpn_key_id=vpn_id, expires_at=expire_date)
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)
    return subscription

async def get_subscription_by_vpn_id(session: AsyncSession, vpn_id) -> Subscription | None:
    query = select(Subscription).where(Subscription.vpn_key_id == vpn_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def update_vpn_expire_time(session: AsyncSession, vpn_id, new_date):
    query = update(Subscription).where(Subscription.vpn_key_id == vpn_id).values(expires_at=new_date)
    await session.execute(query)
    await session.commit()
