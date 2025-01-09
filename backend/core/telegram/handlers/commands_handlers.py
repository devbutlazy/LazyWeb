from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from core.telegram.models.models import AdminFilter, Form
from core.telegram.handlers.callbacks import RemovePostCallback
from core.telegram import cancel_reply_markup
from core.database.repositories.blog import BlogRepository
from core.database.repositories.visit import VisitRepository

router = Router()


@router.message(Command("create_post"), AdminFilter())
async def handle_create_post(message: Message, state: FSMContext) -> None:
    """
    Start the process of creating a new post. Sets the state to `Form.title`.

    :param message: The message object from the user interaction.
    :param state: The FSM context to manage states in the finite state machine.
    :return: None
    """
    await state.set_state(Form.title)

    await message.answer(
        "🌐 <b>Creating post.</b>\n1/3 Enter post title (Markdown syntax is supported):",
        reply_markup=cancel_reply_markup,
    )


@router.message(Command("remove_post"))
async def list_posts(message: Message) -> None:
    """
    Fetches all posts and displays them as buttons.
    If no posts are found, notifies the user.
    """
    async with BlogRepository() as repository:
        posts = await repository.get_all()

    if not posts:
        return await message.answer("❌ <b>No posts available to remove.</b>")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{index + 1}. {post.title[:30]}",
                    callback_data=RemovePostCallback(id=post.id).pack(),
                )
            ]
            for index, post in enumerate(posts)
        ]
    )

    await message.answer("Select a post to remove:", reply_markup=keyboard)


@router.message(Command("posts"), AdminFilter())
async def posts_handler(message: Message) -> None:
    """
    Display all existing blog posts with their IDs and titles.

    :param message: The message object from the user interaction.
    :return: None
    """

    async with BlogRepository() as repository:
        all_blogs = await repository.get_all()
        await message.answer(
            text=(
                f"<b>Posts:</b>\n"
                + "\n".join([f"{blog.id}. {blog.title}" for blog in all_blogs])
                if all_blogs
                else "❌ <b>No posts</b>"
            ),
            reply_markup=ReplyKeyboardRemove(),
        )


@router.message(Command("set_visits"), AdminFilter())
async def set_visits_handler(message: Message, command: CommandObject) -> None:
    """
    Set the number of blog post views to 0.

    :param message: The message object from the user interaction.
    :return: None
    """

    count: str = command.args

    if not count:
        return await message.answer("❌ <b>Visits count not specified</b>")  # type: ignore

    async with VisitRepository() as repository:
        await repository.set_vistis(counter=int(count))

        return await message.answer(f"✅ <b>Visits count set to {count}</b>")
