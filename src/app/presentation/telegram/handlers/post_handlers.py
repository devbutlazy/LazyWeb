from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.app.presentation.telegram.models.models import AdminFilter, Form
from src.app.presentation.telegram import reply_markup
from src.app.infrastructure.database.repositories.blog import BlogRepository

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer("Test.")


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
async def remove_post_handler(message: Message, command: CommandObject) -> Message:
    """
    Handle the removal of a blog post by ID.

    :param message: The message object from the user interaction.
    :param command: The command object containing the post ID as an argument.
    :return: None
    """
    id_: str = command.args

    if not id_:
        return await message.answer("Post id not specified")  # type: ignore

    async with BlogRepository() as repository:
        if await repository.remove_one(id=id_):
            return await message.answer(
                text=f"<b>Post with id {id_} removed</b>",
                reply_markup=ReplyKeyboardRemove(),
            )

        return await message.answer(f"Blog with id {id_} not found")


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
                + "\n".join([f"{blog.id} - {blog.title}" for blog in all_blogs])
                if all_blogs
                else "No posts"
            ),
            reply_markup=ReplyKeyboardRemove(),
        )
