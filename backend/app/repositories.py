from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from .models import Todos


class TodoRepository(SQLAlchemyAsyncRepository[Todos]):
    model_type = Todos
