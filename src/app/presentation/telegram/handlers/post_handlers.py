from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from sqlalchemy import select

from .. import router, reply_markup
from models.models import AdminFilter, Form
from ....infrastructure.database import new_session
from ....infrastructure.database.models.blog import BlogORM


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
        reply_markup=reply_markup,
    )


@router.message(Command("remove_post"), AdminFilter())
async def remove_post_handler(message: Message, command: CommandObject) -> None:
    """
    Handle the removal of a blog post by ID.

    :param message: The message object from the user interaction.
    :param command: The command object containing the post ID as an argument.
    :return: None
    """
    id_: str = command.args

    if not id_:
        return await message.answer("Post id not specified")  # type: ignore

    async with new_session() as session:
        try:
            blog = await session.get(BlogORM, id_)
            if blog:
                await session.delete(blog)
                await session.flush()

                result = await session.execute(select(BlogORM).order_by(BlogORM.id_))
                blogs = result.scalars().all()

                for index, blog in enumerate(blogs):
                    blog.id = index + 1

                await session.commit()
            else:
                raise Exception("Blog not found")
        except Exception as e:
            return await message.answer(f"An error occurred: {e}")  # type: ignore

    await message.answer(
        text=f"<b>Post with id {id_} removed</b>",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("posts"), AdminFilter())
async def posts_handler(message: Message) -> None:
    """
    Display all existing blog posts with their IDs and titles.

    :param message: The message object from the user interaction.
    :return: None
    """
    async with new_session() as session:
        blogs = (await session.execute(select(BlogORM))).scalars().all()
        await message.answer(
            text=(
                f"<b>Posts:</b>\n"
                + "\n".join([f"{blog.id} - {blog.title}" for blog in blogs])
                if blogs
                else "No posts"
            ),
            reply_markup=ReplyKeyboardRemove(),
        )
