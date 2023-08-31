from pydantic import BaseModel


class MessagesSchemas(BaseModel):
    id: int
    message: str
