from typing import Self, Dict, Any

from datetime import timedelta

from aiohttp import ClientSession
from fastapi import Request, HTTPException

from config.config import settings
from core.api.services.cooldown import CustomRateLimiter
from core.api.services.ip_handler import IPAddressHandler


class MessageRepository:
    daily_limiter = CustomRateLimiter(limit=2, period=timedelta(days=1))

    def __init__(self):
        self.url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"
        self.session: ClientSession = ClientSession()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        await self.session.close()

    async def send_message(
        self, request: Request, name: str, message: str
    ) -> Dict[str, Any]:
        ip_handler = IPAddressHandler(request)
        ip_address = (await ip_handler.get_client_ip())["ip"]
        key = f"rate_limit:{ip_address}"

        if not await MessageRepository.daily_limiter.is_allowed(key):
            raise HTTPException(
                status_code=429, detail="Rate limit exceeded. Try again tomorrow."
            )

        location_info = await ip_handler.summarize_location()

        params = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": f"‼️ Message from {name}\n\n{message}\n\n{location_info}",
        }

        async with self.session.get(self.url, params=params) as response:
            return await response.json()
