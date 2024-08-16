from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .. import router, reply_markup
from ..misc import proccess_post
from models.models import AdminFilter, Form


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
async def handle_image(message: Message, state: FSMContext) -> None:
    """
    Process the image URI of the post. Saves the post to the database.

    :param message: The message object
    :param state: The FSM context
    :return: None
    """
    data = await state.update_data(image_uri=message.text)
    await state.clear()

    await proccess_post(message=message, data=data)
