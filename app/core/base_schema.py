from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    ok: bool = Field(description="성공유무")
    message: str = Field(description="성공 실패 메시지")
