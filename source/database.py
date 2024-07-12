from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from source.config import settings

engine = create_async_engine(
    f"sqlite+aiosqlite:///{settings.DB_NAME}.db",
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class CounterORM(Model):
    __tablename__ = "counter"

    id: Mapped[int] = mapped_column(primary_key=True)
    counter: Mapped[int] = mapped_column(default=0)


async def create_tables() -> None:
    """
    Create database tables

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
