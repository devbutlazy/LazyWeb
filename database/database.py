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


async def drop_table_by_name(table_name: str) -> None:
    """
    Drop a specific table by its name.

    :param engine: SQLAlchemy AsyncEngine instance.
    :param base: SQLAlchemy DeclarativeMeta instance (Base).
    :param table_name: Name of the table to drop.
    :return: None
    """
    async with engine.begin() as conn:
        table = Base.metadata.tables.get(table_name)

        if table != None:
            await conn.run_sync(table.drop)
            print("Dropped table '%s'." % table_name)
        else:
            print(f"Table '{table_name}' does not exist.")
