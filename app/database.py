from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


# Создаем асинхронный движок 
engine = create_async_engine(
        "postgresql+asyncpg://postgres:Tow0ZG5K63@localhost:5432/postgres",  # пример: "postgresql+asyncpg://user:password@localhost/dbname"
    echo=False,  # можно включить True для отладки SQL-запросов
)

# Создаем сессионный класс
async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Базовый класс моделей
class Base(DeclarativeBase):
    pass

# Зависимость для получения сессии
async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
