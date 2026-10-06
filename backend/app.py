from litestar import Litestar
from litestar.di import Provide
from methods import (
    lifespan,
    provide_db_session,
    getTodos,
    createTodo,
    updateStatus,
    updateTitle,
    deleteTodo,
    deleteTodos,
    countTodos,
)

app = Litestar(
    route_handlers=[
        getTodos,
        createTodo,
        updateStatus,
        updateTitle,
        deleteTodo,
        countTodos,
        deleteTodos,
    ],
    dependencies={"db_session": Provide(provide_db_session)},
    lifespan=[lifespan],
)
