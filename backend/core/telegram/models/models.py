from aiogram.filters import BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from config.config import settings


class Form(StatesGroup):
    """
    States group for the blog post form, including title, content, and image URI.
    """

    title: State = State()
    content: State = State()
    image_uri: State = State()


class AdminFilter(BaseFilter):
    """
    A filter to check if the user has administrative privileges.
    """

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == settings.BOT_ADMIN_ID
