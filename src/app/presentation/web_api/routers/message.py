from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel

from ....infrastructure.database.repositories.message import MessageRepository
from ..dependencies.depends import get_message_repository

router = APIRouter()


class MessageForm(BaseModel):
    name: str
    message: str


@router.post("/send_message")
async def send_user(
    request: Request, form: MessageForm, repository=Depends(get_message_repository)
):
    if await repository.send_message(
        request=request, name=form.name, message=form.message
    ):
        return {"status": 200, "message": "Message sent"}

    return {"status": 500, "message": "Internal server error"}
