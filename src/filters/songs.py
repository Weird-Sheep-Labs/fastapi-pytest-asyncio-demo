from datetime import date
from typing import Optional

from fastapi_filter.contrib.sqlalchemy.filter import Filter

from models import Song


class SongFilter(Filter):
    name: Optional[str] = None
    artist: Optional[str] = None
    artist__ilike: Optional[str] = None
    streams__gte: Optional[float] = None
    streams__lte: Optional[float] = None
    released_on__gte: Optional[date] = None
    released_on__lte: Optional[date] = None
    order_by: Optional[list[str]] = None

    class Constants(Filter.Constants):
        model = Song
