from pydantic import BaseModel, ConfigDict
from enum import Enum


# full data of todo
class TodoData(BaseModel):
    id: int
    title: str
    status: TodoStatusEnum
    model_config = ConfigDict(from_attributes=True)


class TodoLists(BaseModel):
    items: list[TodoData]
    count: int


# create todo
class TodoCreate(BaseModel):
    title: str


# update status
class UpdateStatus(BaseModel):
    status: TodoStatusEnum


# update title
class UpdateTitle(BaseModel):
    title: str


# status eum
class TodoStatusEnum(str, Enum):
    ACTIVE = "Active"  # false
    COMPLETED = "Completed"  # true
