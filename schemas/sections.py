from typing import Annotated, Union
from pydantic import BaseModel, ConfigDict, Field


class SectionBase(BaseModel):
    name: Annotated[str , Field(..., max_length=25, min_length=5)]  #min and max length must be defined!!


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    pass


class Section(SectionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
