from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Optional

import aiohttp
from fastapi import Request


class IPManipulator:
    def __init__(self, request: Request) -> None:
        self.request: Request = request
        self.ip: Optional[str] = None

    async def get_client_ip(self) -> dict:
        """
        Retrieve the client's real IP address and location.
        """
        x_forwarded_for = self.request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            self.ip = x_forwarded_for.split(",")[0].strip()
        else:
            self.ip = self.request.headers.get("X-Real-IP", self.request.client.host)

        location = await self.get_ip_location()
        return {"ip": self.ip, "location": location}

    async def get_ip_location(self) -> dict:
        """
        Get the location of the IP address using an external API.
        """
        url = f"https://ipinfo.io/{self.ip}/json"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "city": data.get("city"),
                        "region": data.get("region"),
                        "country": data.get("country"),
                        "loc": data.get("loc"),
                    }
                else:
                    return {"error": "Could not retrieve location"}

    async def sum_location_info(self) -> str:
        client_info = await self.get_client_ip()
        user_ip = client_info["ip"]
        location = client_info["location"]

        if "error" in location:
            location_info = f"IP: {user_ip}"
        else:
            country = location.get("country", "")
            city = location.get("city", "")
            region = location.get("region", "")
            loc = location.get("loc", "")

            location_info = (
                f"IP: {user_ip}, Location: {country}, {city}, {region}, {loc}"
            )

        return location_info


class CustomRateLimiter:
    def __init__(self, limit: int, period: timedelta):
        self.limit = limit
        self.period = period
        self.requests = defaultdict(list)

    async def is_allowed(self, key: str) -> bool:
        now = datetime.now(timezone.utc)
        period_start = now - self.period
        self.cleanup(key, period_start)

        if len(self.requests[key]) < self.limit:
            self.requests[key].append(now)
            return True
        return False

    def cleanup(self, key: str, period_start: datetime):
        self.requests[key] = [
            timestamp for timestamp in self.requests[key] if timestamp > period_start
        ]
