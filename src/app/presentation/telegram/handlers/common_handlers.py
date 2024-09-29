from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from src.app.presentation.telegram.models.models import AdminFilter, Form

from src.app.presentation.telegram import reply_markup
from src.app.infrastructure.database.repositories.blog import BlogRepository

router = Router()


@router.message(Form.title, AdminFilter())
async def handle_title(message: Message, state: FSMContext) -> None:
    """
    Process the title of the post. Sets the state to `Form.content`.

    :param message: The message object
    :param state: The FSM context
    :return: None
    """
    await state.update_data(title=message.text)
    await state.set_state(Form.content)

    await message.answer(
        "2/3 Enter post content (Markdown syntax is supported):",
        reply_markup=reply_markup,
    )


@router.message(Form.content, AdminFilter())
async def handle_content(message: Message, state: FSMContext) -> None:
    """
    Process the content of the post. Sets the state to `Form.image_uri`.

    :param message: The message object
    :param state: The FSM context
    :return: None
    """
    await state.update_data(content=message.text)
    await state.set_state(Form.image_uri)

    await message.answer(
        '3/3 Enter image URL (or type "skip" to skip this step):',
        reply_markup=reply_markup,
    )


@router.message(Form.image_uri, AdminFilter())
async def handle_image(message: Message, state: FSMContext) -> Message:
    """
    Process the image URI of the post. Saves the post to the database.

    :param message: The message object
    :param state: The FSM context
    :return: None
    """
    data = await state.update_data(image_uri=message.text)
    await state.clear()

    title: str = data.get("title", "N/A")
    content: str = data.get("content", "N/A")
    image_uri: str = data.get("image_uri", "N/A")

    async with BlogRepository() as repository:
        if _ := (
            await repository.add_one(
                title=title,
                content=content,
                image_uri=image_uri,
                created_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
            )
        ):
            return await message.answer(
                text=(
                    f'<a href="{image_uri}">🌐</a> <b>Post created</b>\n\n'
                    f"<b>Title:</b> {title}\n"
                    f"<b>Content:</b>\n{content}"
                )
            )

        return await message.answer("An error occurred while adding a post")
