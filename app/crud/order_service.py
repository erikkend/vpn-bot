from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order


async def create_order(session: AsyncSession, user_id: str, amount: float, currency: str, month_c, region) -> Order:
    order = Order(user_id=user_id, amount=amount, currency=currency, expires_at=Order.generate_expire_time(), month_count=month_c, server_region=region)
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order

async def get_order_by_id(session: AsyncSession, order_id) -> Order | None:
    query = select(Order).where(Order.id == order_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

async def update_order_info(session: AsyncSession, order_id, order_uuid):
    query = update(Order).where(Order.id == order_id).values(order_uuid=order_uuid)
    await session.execute(query)
    await session.commit()