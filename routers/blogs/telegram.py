from sqlalchemy import select
from datetime import datetime

from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


from routers.blogs.models import IsAdmin, Form
from database.config import settings
from database.database import new_session
from database.models import BlogsORM


router = Router()


@router.message(Command("create_post"), IsAdmin())
async def create_post_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.title)
    await message.answer(
        f"🌐 <b>Creating post.</b>\n1/2 Enter it's title",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Cancel"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@router.message(Form.title, IsAdmin())
async def proccess_content_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(Form.content)
    await message.answer(
        f"2/2 Enter it's content.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Cancel"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@router.message(Form.content, IsAdmin())
async def handle_content(message: Message, state: FSMContext) -> None:
    data = await state.update_data(content=message.text)
    await state.clear()
    await save_to_database(message=message, data=data)


@router.message(Command("cancel"), IsAdmin())
@router.message(F.text.casefold() == "cancel")
async def cancel_button_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


async def save_to_database(message: Message, data: Dict[str, Any]) -> None:
    title = data.get("title", "N/A")
    content = data.get("content", "N/A")

    async with new_session() as session:
        blog = BlogsORM(
            title=title,
            content=content,
            created_at=datetime.now().strftime("%Y/%m/%d %H:%M"),
        )
        session.add(blog)
        await session.commit()

    await message.answer(
        text=f"🌐 <b>Post created</b>\n\n<b>Title:</b>{title}\n<b>Content:</b>\n<b>{content}</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("remove_post"), IsAdmin())
async def remove_post_handler(message: Message, command: CommandObject) -> None:
    id: str = command.args

    if not id:
        return await message.answer("Post id not specified")

    async with new_session() as session:
        try:
            blog = await session.get(BlogsORM, id)
            await session.delete(blog)
            await session.flush()

            result = await session.execute(select(BlogsORM).order_by(BlogsORM.id))
            blogs = result.scalars().all()

            for index, blog in enumerate(blogs):
                blog.id = index + 1

            await session.commit()

        except (Exception, ExceptionGroup):
            return await message.answer("Post not found")

    await message.answer(
        text=f"<b>Post with id {id} removed</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("posts"), IsAdmin())
async def posts_handler(message: Message):
    async with new_session() as session:
        blogs = (await session.execute(select(BlogsORM))).scalars().all()
        await message.answer(
            text=(
                f"<b>Posts:</b>\n"
                + "\n".join([f"{blog.id} - {blog.title}" for blog in blogs])
                if blogs
                else "No posts"
            ),
            reply_markup=ReplyKeyboardRemove(),
        )


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
