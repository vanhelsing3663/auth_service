from functools import partial
from typing import AsyncIterable
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from adapters.sqlalchemy_adapter.connect import create_session_maker

async def new_session(session_maker) -> AsyncIterable[AsyncSession]:
    session = session_maker()

    async with session:
        yield session

def init_dependencies(app: FastAPI):
    session_maker = create_session_maker()

    app.dependency_overrides[AsyncSession] = partial(new_session, session_maker)