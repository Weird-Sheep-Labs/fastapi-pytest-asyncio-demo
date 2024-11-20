import os

from faker import Faker
from polyfactory import SyncPersistenceProtocol
from polyfactory.factories.pydantic_factory import ModelFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Song

engine = create_engine(os.environ["DATABASE_URL"].replace("+asyncpg", ""))
session = scoped_session(sessionmaker(bind=engine))


class SyncPersistenceHandler[T](SyncPersistenceProtocol[T]):
    def save(self, data: T) -> T:
        session.add(data)
        session.commit()
        return data

    def save_many(self, data: list[T]) -> list[T]:
        session.add_all(data)
        session.commit()
        return data


class SongFactory(ModelFactory[Song]):
    __faker__ = Faker(locale="en_GB")
    __sync_persistence__ = SyncPersistenceHandler[Song]
