from datetime import datetime
from typing import Annotated, Optional, Union
from pydantic import BaseModel, ConfigDict, Field

from schemas.sections import Section
from schemas.tags import Tag


class PostBase(BaseModel):
    title: Annotated[str, Field(..., max_length=60, min_length=6)]
    body: str
    tags: list[str] = []


class PostCreate(PostBase):
    section_id: int


class PostUpdate(PostBase):
    title: Annotated[Union[str, None], Field(max_length=60)] = None
    body: Union[str, None] = None
    section_id: Union[int, None] = None
    tags: list[str] = []


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: Union[datetime, None] = None
    section: Section
    tags: list[Tag] = []

    model_config = ConfigDict(from_attributes=True)


class FilterPosts(BaseModel):
    title: Union[str, None] = None
    # TODO:  add more filters

class PostUpdatePUT(BaseModel):
    title: str
    body:str
    section_id: int
    tags: Optional[list[int]] = Field(default_factory=list)

class PostUpdatePATCH(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    section_id: Optional[int] = None
    tags: Optional[list[int]] = None

class config:
    orm_mode = True

class PostFilter(BaseModel):
    section_id: Optional[int] = None
    tags: list[str] = Field(default_factory=list)
    created_at_gt: Optional[datetime] = None
    created_at_lt: Optional[datetime] = None