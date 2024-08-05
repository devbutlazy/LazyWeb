from aiogram.filters import BaseFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message


class Form(StatesGroup):
    title = State()
    content = State()
    image_uri = State()


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == 6456054542

