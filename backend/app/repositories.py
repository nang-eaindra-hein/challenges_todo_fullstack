from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import select
from .models import Todos


class TodoRepository(SQLAlchemyAsyncRepository[Todos]):
    model_type = Todos

    async def get_by_title(self, title: str) -> Todos | None:
        statement = select(Todos).where(Todos.title == title)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()
