from typing import AsyncGenerator

from core.database.repositories.blog import BlogRepository
from core.database.repositories.visit import VisitRepository
from core.database.repositories.message import MessageRepository


async def get_blog_repository() -> AsyncGenerator[BlogRepository, None]:
    """
    Returns an instance of BlogRepository
    """
    async with BlogRepository() as repository:
        yield repository


async def get_visit_repository() -> AsyncGenerator[VisitRepository, None]:
    """
    Returns an instance of VisitRepository
    """
    async with VisitRepository() as repository:
        yield repository


async def get_message_repository() -> AsyncGenerator[MessageRepository, None]:
    """
    Returns an instance of VisitRepository
    """
    async with MessageRepository() as repository:
        yield repository
