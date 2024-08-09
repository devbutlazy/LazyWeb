from datetime import timedelta

import aiohttp
from fastapi import Form, Request, APIRouter, HTTPException
from slowapi.util import get_remote_address

from database.config import settings
from routers.misc import IPManipulator, CustomRateLimiter

daily_limiter = CustomRateLimiter(limit=2, period=timedelta(days=1))
router = APIRouter()


@router.post("/send_message")
async def send_message(
    request: Request, name: str = Form(...), message: str = Form(...)
) -> dict:
    """
    Send message to telegram chat
    :param name: name of the sender
    :param message: message text
    :return: success message
    """
    ip_address = get_remote_address(request)
    key = f"rate_limit:{ip_address}"

    if not await daily_limiter.is_allowed(key):
        # Return an HTTP 429 Too Many Requests error with a custom message
        raise HTTPException(
            status_code=429, detail="Rate limit exceeded. Try again tomorrow."
        )

    location_info = await IPManipulator(request).sum_location_info()

    async with aiohttp.ClientSession() as session:
        await session.get(
            f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage",
            params={
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": f"‼️ Message from {name}\n\n{message}\n\n{location_info}",
            },
        )

    return {"message": "Message sent"}
