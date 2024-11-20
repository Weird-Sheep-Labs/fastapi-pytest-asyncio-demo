import uuid
from datetime import date, datetime
from typing import Optional

from sqlmodel import SQLModel

from models.base import BaseModel


class SongBase(SQLModel):
    name: str
    artist: str
    streams: float
    released_on: date


class Song(SongBase, BaseModel, table=True):
    pass


class SongBasePartial(SQLModel):
    name: Optional[str] = None
    artist: Optional[str] = None
    streams: Optional[float] = None
    released_on: Optional[date] = None


class SongRead(SongBase):
    id: uuid.UUID


class SongList(SongRead):
    created_at: datetime
