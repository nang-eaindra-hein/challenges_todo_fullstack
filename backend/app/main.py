from litestar import Litestar
from litestar.di import Provide
from .methods import (
    lifespan,
    provide_db_session,
    provide_todo_repo,
    get_todos,
    create_todo,
    update_status,
    update_title,
    delete_todo,
    delete_todos,
)

app = Litestar(
    route_handlers=[
        get_todos,
        create_todo,
        update_status,
        update_title,
        delete_todo,
        delete_todos,
    ],
    dependencies={
        "db_session": Provide(provide_db_session),
        "todo_repo": Provide(provide_todo_repo),
    },
    lifespan=[lifespan],
    debug=True,
)
