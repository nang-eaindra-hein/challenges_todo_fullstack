from pydantic import BaseModel, ConfigDict
from enum import Enum


# status eum
class TodoStatusEnum(str, Enum):
    ACTIVE = "Active"  # false
    COMPLETED = "Completed"  # true


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


# update todo
class UpdateTodo(BaseModel):
    title: str | None = None
    status: TodoStatusEnum | None = None
