import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(DATABASE_URL, echo=True, future=True, pool_pre_ping=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, autocommit=False, autoflush=False
    )
    async with async_session() as session:
        yield session
