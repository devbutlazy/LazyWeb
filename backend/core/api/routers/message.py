from fastapi import APIRouter, Request, Depends

from core.api.schemas.schemas import MessageForm
from core.api.dependencies.depends import get_message_repository

router = APIRouter()


@router.post("/send_message")
async def send_user(
    request: Request, form: MessageForm, repository=Depends(get_message_repository)
):
    if await repository.send_message(
        request=request, name=form.name, message=form.message
    ):
        return {"status": 200, "message": "Message sent"}

    return {"status": 500, "message": "Internal server error"}
