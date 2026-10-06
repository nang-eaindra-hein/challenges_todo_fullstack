from contextlib import asynccontextmanager

from litestar import Litestar, post, get, put, delete

from sqlalchemy import select, func, delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import Todos
from database import Base, engine, SessionLocal
from schemas import TodoData, UpdateStatus, UpdateTitle, TodoCreate


async def provide_db_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(app: Litestar):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@get("/todos")
async def getTodos(db_session: AsyncSession) -> list[TodoData]:
    statement = select(Todos)

    result = await db_session.execute(statement)
    todos = result.scalars().all()

    return [TodoData.model_validate(todo) for todo in todos]


@get("/todos_count")
async def countTodos(db_session: AsyncSession) -> int:
    statement = select(func.count()).select_from(Todos)

    result = await db_session.execute(statement)

    return result.scalar_one()


@post("/todo")
async def createTodo(db_session: AsyncSession, data: TodoCreate) -> TodoData:

    todo = Todos(title=data.title)

    db_session.add(todo)

    await db_session.commit()

    await db_session.refresh(todo)

    return TodoData.model_validate(todo)


@put("/{todo_id:int}/todo_status")
async def updateStatus(
    todo_id: int, db_session: AsyncSession, data: UpdateStatus
) -> list[TodoData]:

    todo = await db_session.get(Todos, todo_id)

    todo.status = data.status

    await db_session.commit()

    await db_session.refresh(todo)

    return TodoData.model_validate(todo)


@put("/{todo_id:int}/todo_title")
async def updateTitle(
    todo_id: int, db_session: AsyncSession, data: UpdateTitle
) -> list[TodoData]:

    todo = await db_session.get(Todos, todo_id)

    todo.title = data.title

    await db_session.commit()

    await db_session.refresh(todo)

    return TodoData.model_validate(todo)


@delete("/{todo_id:int}")
async def deleteTodo(todo_id: int, db_session: AsyncSession) -> None:
    todo = await db_session.get(Todos, todo_id)

    await db_session.delete(todo)

    await db_session.commit()


@delete("/delete_todos")
async def deleteTodos(db_session: AsyncSession) -> None:

    await db_session.execute(sqlalchemy_delete(Todos))
    await db_session.commit()
