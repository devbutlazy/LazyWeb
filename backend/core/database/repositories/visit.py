from typing import Self

from sqlalchemy.ext.asyncio import async_sessionmaker

from core.database.repositories.base import BaseRepository
from core.database import engine
from core.database.models.visit import VisitORM


class VisitRepository(BaseRepository):
    def __init__(self):
        self.session: async_sessionmaker = async_sessionmaker(engine)

    async def __aenter__(self: Self) -> Self:
        self.session = async_sessionmaker(engine)
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:  # noqa
        return await self.session().close()

    async def get_one(self, **kwargs):
        async with self.session() as session:
            return await session.get(VisitORM, 1)

    async def add_one(self, **kwargs):
        async with self.session() as session:
            counter = await session.get(VisitORM, 1)
            if counter:
                counter.counter += 1
            else:
                counter = VisitORM(id=1, counter=1)
                session.add(counter)

            await session.commit()

    async def remove_one(self, **kwargs):
        async with self.session() as session:
            counter = await session.get(VisitORM, 1)
            if counter:
                counter.counter -= 1
            else:
                counter = VisitORM(id=1, counter=1)
                session.add(counter)

            await session.commit()

    async def set_vistis(self, **kwargs):
        async with self.session() as session:
            counter = await session.get(VisitORM, 1)
            if counter:
                counter.counter = kwargs.get("counter")
            else:
                counter = VisitORM(id=1, counter=kwargs.get("counter"))
                session.add(counter)

            await session.commit()
