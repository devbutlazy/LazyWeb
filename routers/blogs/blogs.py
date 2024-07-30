from fastapi import APIRouter
from sqlalchemy import select

from database.database import new_session
from database.models import BlogsORM
from async_lru import alru_cache

router = APIRouter()


@alru_cache()
@router.get("/get_blogs")
async def get_blogs():
    """
    Get blogs counter

    :return: blogs counter
    """
    async with new_session() as session:
        blogs = (await session.execute(select(BlogsORM))).scalars().all()
        return {"blogs": blogs}
