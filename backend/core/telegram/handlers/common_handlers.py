from datetime import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.telegram.models.models import AdminFilter, Form
from core.database.repositories.blog import BlogRepository
from core.telegram.handlers.callbacks import RemovePostCallback
from core.telegram import cancel_reply_markup, image_reply_markup


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
        reply_markup=cancel_reply_markup,
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
        '3/3 Enter image URL (or press "Skip" to skip this step):',
        reply_markup=image_reply_markup,
    )


@router.message(Form.image_uri, AdminFilter())
async def handle_image(message: Message, state: FSMContext) -> None:
    """
    Process the image URI of the post. Saves the post to the database if "Skip" is pressed or a valid URL is provided.

    :param message: The message object
    :param state: The FSM context
    :return: None
    """
    image_uri = None if message.text.lower() == "skip" else message.text

    data = await state.update_data(image_uri=image_uri)
    await state.clear()

    title: str = data.get("title", "Not Found")
    content: str = data.get("content", "Not Found")

    async with BlogRepository() as repository:
        await repository.add_one(
            title=title,
            content=content,
            image_uri=image_uri,
            created_at=datetime.now().strftime("%d/%m/%Y %H:%M"),
        )

    image = f'<a href="{image_uri}">🌐</a> ' if image_uri else ""

    await message.answer(
        text=(
            f"{image}<b>Post created</b>\n\n"
            f"<b>Title:</b> {title}\n"
            f"<b>Content:</b>\n{content}"
        ),
        reply_markup=None,
    )


@router.callback_query(RemovePostCallback.filter())
async def handle_remove_post(
    callback: CallbackQuery, callback_data: RemovePostCallback
) -> None:
    """
    Handles the removal of the post when a button is pressed.
    """

    async with BlogRepository() as repository:
        result = await repository.remove_one(id=callback_data.id)

    if "removed" in result:
        await callback.message.edit_text(
            f"✅ <b>{result}</b>\n\nUse /remove_post to manage other posts."
        )

    else:
        await callback.message.edit_text(f"❌ <b>{result}</b>")

    await callback.answer()
