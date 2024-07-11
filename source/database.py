from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from typing import Optional

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
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def get_count() -> Optional[int]:
    async with new_session() as session:
        counter = await session.get(CounterORM, 1)
        return counter.counter if counter else None


async def increment_count() -> None:
    async with new_session() as session:
        counter = await session.get(CounterORM, 1)
        if counter:
            counter.counter += 1
        else:
            counter = CounterORM(id=1, counter=1)
            session.add(counter)
        await session.commit()
