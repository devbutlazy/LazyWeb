from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import BaseFilter


class Form(StatesGroup):
    title = State()
    content = State()


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == 6456054542

