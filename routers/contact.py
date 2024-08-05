import aiohttp
from fastapi import Form, HTTPException, Request, APIRouter
from slowapi import Limiter
from slowapi.util import get_remote_address

from database.config import settings

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.post("/send_message")
@limiter.limit("5/minute")
async def send_message(request: Request, name: str = Form(...), message: str = Form(...)) -> dict:
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
