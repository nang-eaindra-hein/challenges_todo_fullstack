from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
from .schemas import TodoStatusEnum
from sqlalchemy import Enum as SQLEnum


class Todos(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True, index=True)
    status: Mapped[bool] = mapped_column(
        SQLEnum(TodoStatusEnum), default=TodoStatusEnum.ACTIVE
    )
