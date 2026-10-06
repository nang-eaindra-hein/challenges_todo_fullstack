from contextlib import asynccontextmanager

from litestar import Litestar, post, get
from litestar.di import Provide
from litestar.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, engine, SessionLocal


async def provide_db_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(app: Litestar):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@get("/home")
async def home() -> dict:
    return {"message": "Litestar auth app is running!"}
