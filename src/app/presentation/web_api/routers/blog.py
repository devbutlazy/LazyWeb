from typing import AsyncGenerator

from fastapi import APIRouter, Depends
from async_lru import alru_cache

from ....infrastructure.database.repositories.blog import BlogRepository

router = APIRouter()

async def get_blog_repository() -> AsyncGenerator[BlogRepository, None]:
    async with BlogRepository() as repository:
        yield repository

@alru_cache()
async def cached_get_blogs(repository: BlogRepository) -> dict:
    """
    Get blogs counter

    :return: blogs counter
    """
    return {"status": 200, "blogs": await repository.get_all()}


@alru_cache()
@router.get("/get_blogs")
async def get_blogs(repository: BlogRepository = Depends(get_blog_repository)):
    """
    Get blogs counter

    :return: blogs counter
    """
    return await cached_get_blogs(repository)