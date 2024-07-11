from fastapi import APIRouter, Form, HTTPException
from source.config import settings
import requests

router = APIRouter()


@router.post("/send_message")
async def send_message(name: str = Form(...), message: str = Form(...)):
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage",
            params={
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": f"‼️ Повідомлення від {name}\n\n{message}",
            },
        )
        response.raise_for_status()
        return {"message": "Повідомлення надіслано"}
    except requests.RequestException as error:
        raise HTTPException(
            status_code=500, 
            detail=f"Помилка відправки повідомлення: {str(error)}"
        )
