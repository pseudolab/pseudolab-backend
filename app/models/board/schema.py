from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BoardSchema(BaseModel):
    title: str
    content: str
    password: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
