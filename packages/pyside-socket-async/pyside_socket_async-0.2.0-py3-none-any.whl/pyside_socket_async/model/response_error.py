from pydantic import BaseModel


class ResponseError(BaseModel):
    status_code: int
    message: str
    text: str