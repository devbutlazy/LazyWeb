import aiohttp
from fastapi import APIRouter, Form, HTTPException

from database.config import settings

router = APIRouter()


@router.post("/send_message")
async def send_message(name: str = Form(...), message: str = Form(...)) -> dict:
    """
    Send message to telegram chat

    :param name: name of the sender
    :param message: message text
    :return: success message
    """

    try:
        async with aiohttp.ClientSession() as session:
            await session.get(
                f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage",
                params={
                    "chat_id": settings.TELEGRAM_CHAT_ID,
                    "text": f"‼️ Message from {name}\n\n{message}",
                },
            )
            return {"message": "Message sent"}
    except aiohttp.ClientError as error:
        raise HTTPException(
            status_code=500, detail=f"Error while sending message: {str(error)}"
        )
