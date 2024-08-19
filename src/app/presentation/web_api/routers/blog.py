from fastapi import APIRouter, Depends
from async_lru import alru_cache

from ....infrastructure.database.repositories.blog import BlogRepository
from ..dependencies.depends import get_blog_repository

router = APIRouter()


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
