from pydantic import BaseModel, ConfigDict


class MetaWordSchema(BaseModel):
    word_id: int
    word_type: int
    word: str

    model_config = ConfigDict(from_attributes=True)
