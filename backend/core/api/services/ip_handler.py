from typing import Dict, Optional

import aiohttp
from fastapi import Request


class IPAddressHandler:
    def __init__(self, request: Request) -> None:
        """
        Initialize the IPAddressHandler with the given request.

        :param request: The FastAPI Request object.
        """
        self.request = request
        self.ip: Optional[str] = None

    async def get_client_ip(self) -> Dict[str, Optional[str]]:
        """
        Retrieve the client's IP address and its location.

        :return: A dictionary containing 'ip' and 'location'.
        """
        self.ip = self._extract_ip_from_headers()
        location = await self._fetch_ip_location()
        return {"ip": self.ip, "location": location}

    def _extract_ip_from_headers(self) -> str:
        """
        Extract the client's IP address from request headers.

        :return: The client's IP address.
        """
        x_forwarded_for = self.request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        
        return self.request.headers.get("X-Real-IP", self.request.client.host)

    async def _fetch_ip_location(self) -> Dict[str, Optional[str]]:
        """
        Fetch the location of the IP address using an external API.

        :return: A dictionary containing location information or an error message.
        """
        url = f"https://ipinfo.io/{self.ip}/json"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if not response.status == 200:
                    return {"error": "Unable to retrieve location"}

                data = await response.json()
                return {
                    "city": data.get("city"),
                    "region": data.get("region"),
                    "country": data.get("country"),
                    "loc": data.get("loc"),
                }

    async def summarize_location(self) -> str:
        """
        Summarize the location information in a human-readable format.

        :return: A string summarizing the IP address and its location.
        """
        client_info = await self.get_client_ip()
        user_ip = client_info["ip"]
        location = client_info["location"]

        if (not isinstance(location, dict)) and ("error" in location):
            return f"IP: {user_ip}"

        country = location.get("country", "")
        city = location.get("city", "")
        region = location.get("region", "")
        loc = location.get("loc", "")

        return f"IP: {user_ip}, Location: {country}, {city}, {region}, {loc}"
