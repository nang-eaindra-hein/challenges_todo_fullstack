from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Todos(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(unique=True, index=True)
    status: Mapped[bool] = mapped_column(default=False)
