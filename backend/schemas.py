from pydantic import BaseModel, ConfigDict


# full data of todo
class TodoData(BaseModel):
    id: int
    title: str
    status: bool
    model_config = ConfigDict(from_attributes=True)


# create todo
class TodoCreate(BaseModel):
    title: str


# update status
class UpdateStatus(BaseModel):
    id: int
    status: bool


# update title
class UpdateTitle(BaseModel):
    id: int
    title: str
