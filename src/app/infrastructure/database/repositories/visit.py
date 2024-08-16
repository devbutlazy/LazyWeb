from sqlalchemy.ext.asyncio import async_sessionmaker

from .base import BaseRepository
from .. import engine


class VisitRepository(BaseRepository):
    def __init__(self):
        self.session: async_sessionmaker = async_sessionmaker(engine)

    ...
