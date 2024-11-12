
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    name: Annotated[str, Field(..., max_length=25, min_length=5)]  # TODO: min and max length must be defined!!


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class TagsWithPostCount(BaseModel):
    id: int
    name: str
    post_count: int

    class Config:
        orm_mode = True
