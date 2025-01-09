from pydantic import BaseModel


class MessageForm(BaseModel):
    name: str
    message: str
