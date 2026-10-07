from contextlib import asynccontextmanager

from litestar import Litestar, post, get, put, delete

from sqlalchemy import select, func, delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Todos
from .database import Base, engine, SessionLocal
from .schemas import (
    TodoData,
    UpdateStatus,
    UpdateTitle,
    TodoCreate,
    TodoLists,
    TodoStatusEnum,
)
from .repositories import TodoRepository


async def provide_db_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def provide_todo_repo(
    db_session: AsyncSession,
) -> TodoRepository:

    return TodoRepository(session=db_session)


@asynccontextmanager
async def lifespan(app: Litestar):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


# get lists and count
@get("/todos")
async def get_todos(todo_repo: TodoRepository, type: str | None) -> TodoLists:

    if type == TodoStatusEnum.ACTIVE:
        lists_statement = await todo_repo.list(
            statement=select(Todos).where(Todos.status == TodoStatusEnum.ACTIVE)
        )
        # active lists(false)
    elif type == TodoStatusEnum.COMPLETED:
        lists_statement = await todo_repo.list(
            statement=select(Todos).where(Todos.status == TodoStatusEnum.COMPLETED)
        )  # completed lists(true)
    else:
        lists_statement = await todo_repo.list()  # all lists

    # count
    count_statement = len(lists_statement)

    list_data: list[TodoData] = [
        TodoData.model_validate(todo) for todo in lists_statement
    ]

    return {"items": list_data, "count": count_statement}


# create todo
@post("/todo")
async def create_todo(
    todo_repo: TodoRepository,
    data: TodoCreate,
) -> TodoData:

    todo = Todos(title=data.title)

    todo = await todo_repo.add(todo)

    await todo_repo.session.commit()

    return TodoData.model_validate(todo)


# update status
@put("/todo-status/{todo_id:int}")
async def update_status(
    todo_id: int, todo_repo: TodoRepository, data: UpdateStatus
) -> TodoData:

    todo = await todo_repo.get(todo_id)

    todo.status = data.status

    todo = await todo_repo.update(todo)
    await todo_repo.session.commit()

    return TodoData.model_validate(todo)


# update title
@put("/todo-title/{todo_id:int}")
async def update_title(
    todo_id: int, todo_repo: TodoRepository, data: UpdateTitle
) -> TodoData:

    todo = await todo_repo.get(todo_id)

    todo.title = data.title

    todo = await todo_repo.update(todo)
    await todo_repo.session.commit()

    return TodoData.model_validate(todo)


# delete bt id
@delete("/{todo_id:int}")
async def delete_todo(todo_id: int, todo_repo: TodoRepository) -> None:

    await todo_repo.delete(todo_id)
    await todo_repo.session.commit()


# delete all lists
@delete("/delete-todos")
async def delete_todos(todo_repo: TodoRepository) -> None:

    todos = await todo_repo.list()

    await todo_repo.delete_many([todo.id for todo in todos])
    await todo_repo.session.commit()
