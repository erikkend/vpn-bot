import asyncio
import logging

from app.models.user import User
from app.models.server import Server
from app.models.vpn_key import VPNKey
from app.models.subscription import Subscription
from app.models.order import Order

from app.database import Base, engine  # подставь правильный путь к своим файлам!

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_all_tables():
    async with engine.begin() as conn:
        logger.info("Создаю таблицы в базе данных...")
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Все таблицы успешно созданы!")

if __name__ == "__main__":
    asyncio.run(create_all_tables())
