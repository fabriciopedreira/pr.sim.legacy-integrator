from pydantic import BaseModel


class DefaultResponse(BaseModel):
    data: list
