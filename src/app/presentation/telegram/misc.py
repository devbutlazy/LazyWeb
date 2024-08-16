from datetime import datetime, timezone
from typing import Dict, Any

from aiogram.types import Message

from ...infrastructure.database import new_session
from ...infrastructure.database.models.blog import BlogORM


async def proccess_post(message: Message, data: Dict[str, Any]) -> None:
    """
    Save a blog post to the database.

    :param message: The message object from the user interaction.
    :param data: A dictionary containing the blog post data with keys 'title', 'content', and 'image_uri'.
    :return: None
    """
    title: str = data.get("title", "N/A")
    content: str = data.get("content", "N/A")
    image_uri: str = data.get("image_uri", "N/A")

    try:
        async with new_session() as session:
            post = BlogORM(
                title=title,
                content=content,
                created_at=datetime.now(timezone.utc),
                image_uri=image_uri,
            )
            session.add(post)
            await session.commit()

        await message.answer(
            text=(
                f'<a href="{image_uri}">🌐</a> <b>Post created</b>\n\n'
                f"<b>Title:</b> {title}\n"
                f"<b>Content:</b>\n{content}"
            )
        )
    except BaseException as error:
        await message.answer(text=f"An error occurred while saving the post: {error}")
