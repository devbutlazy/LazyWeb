import aiohttp
from fastapi import Request

async def get_client_ip(request: Request) -> dict:
    """
    Retrieve the client's real IP address and location.
    """
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.headers.get("X-Real-IP", request.client.host)

    location = await get_ip_location(ip)
    return {"ip": ip, "location": location}


async def get_ip_location(ip: str) -> dict:
    """
    Get the location of the IP address using an external API.
    """
    url = f"https://ipinfo.io/{ip}/json"

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

async def sum_location_info(request):
    client_info = await get_client_ip(request)
    user_ip = client_info["ip"]
    location = client_info["location"]

    if "error" in location:
        location_info = f"IP: {user_ip}"
    else:
        country = location.get("country", "")
        city = location.get("city", "")
        region = location.get("region", "")
        loc = location.get("loc", "")

        location_info = f"IP: {user_ip}, Location: {country}, {city}, {region}, {loc}"

    return location_info