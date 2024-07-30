from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.config import settings
from database.models import Base

engine = create_async_engine(
    f"sqlite+aiosqlite:///{settings.DB_NAME}.db",
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables() -> None:
    """
    Create database tables

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    """
    Create database tables

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
