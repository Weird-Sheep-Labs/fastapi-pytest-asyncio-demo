import uuid

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi_filter import FilterDepends
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session
from filters import SongFilter
from models import Song, SongBase, SongBasePartial, SongList, SongRead

song_router = APIRouter(prefix="/songs")


@song_router.get("", response_model=LimitOffsetPage[SongList])
async def list_songs(
    filter: SongFilter = FilterDepends(SongFilter),
    session: AsyncSession = Depends(get_session),
):
    query = select(Song)
    query = filter.sort(filter.filter(query))
    return await paginate(session, query)  # type: ignore


@song_router.get("/{id}", response_model=SongRead)
async def get_song(id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    if _song := await session.get(Song, id):
        return _song
    raise HTTPException(status_code=404, detail="Item not found")


@song_router.post("")
async def add_song(song: SongBase, session: AsyncSession = Depends(get_session)):
    _song = Song(**song.model_dump(exclude_unset=True))
    session.add(_song)
    try:
        await session.commit()
        await session.refresh(_song)
        return _song
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail=exc.orig.args)  # type: ignore


@song_router.patch("/{id}")
async def update_song(
    song: SongBasePartial,
    id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    if _song := await session.get(Song, id):
        for k, v in song.model_dump(exclude_unset=True).items():
            setattr(_song, k, v)
        try:
            await session.commit()
            await session.refresh(_song)
            return _song
        except IntegrityError as exc:
            raise HTTPException(status_code=400, detail=exc.orig.args)  # type: ignore
    raise HTTPException(status_code=404, detail="Item not found")
