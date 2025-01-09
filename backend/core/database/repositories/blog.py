from typing import Self, Type, Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.database.repositories.base import BaseRepository
from core.database import engine
from core.database.models.blog import BlogORM


class BlogRepository(BaseRepository):
    def __init__(self):
        self.session: async_sessionmaker

    async def __aenter__(self: Self) -> Self:
        self.session = async_sessionmaker(engine)
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:  # noqa
        return await self.session().close()

    async def get_one(self, **kwargs) -> Type[BlogORM] | None:
        """
        Get blog by it's id
        :param kwargs: id
        :return: BlogORM
        """
        id_ = kwargs.get("id")
        if not id_:
            raise ValueError("Blog id not specified")

        async with self.session() as session:
            return await session.get(BlogORM, id_)

    async def get_all(self) -> Sequence[BlogORM] | list[Any]:
        """
        Get all blogs
        :return: BlogORM
        """
        async with self.session() as session:
            if all_blogs := (await session.execute(select(BlogORM))).scalars().all():
                return all_blogs

            return []

    async def remove_one(self, **kwargs) -> ValueError | str:
        """
        Remove blog by it's id
        :param kwargs: id
        :return: ValueError or str
        """
        id_ = kwargs.get("id")
        if not id_:
            raise ValueError("Blog id not specified")

        async with self.session() as session:
            if not (blog := await session.get(BlogORM, id_)):
                return f"No blog with id {id_} found"

            await session.delete(blog)
            await session.flush()

            result = await session.execute(select(BlogORM).order_by(BlogORM.id))
            blogs = result.scalars().all()

            for index, blog in enumerate(blogs):
                blog.id = index + 1

            await session.commit()

            return f"Blog with id {id_} removed"

    async def add_one(self, **kwargs) -> str:
        """
        Add new post to blogs
        :param kwargs: title, content, image_uri
        :return: str
        """
        async with self.session() as session:
            blog = BlogORM(**kwargs)

            session.add(blog)
            await session.commit()

            return f"Post created. {', '.join(f'{key}={value}' for key, value in kwargs.items())}"
