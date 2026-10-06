from pydantic import BaseModel, EmailStr


class TodosData(BaseModel):
    id: int
    title: str
    description: str
    status: bool
