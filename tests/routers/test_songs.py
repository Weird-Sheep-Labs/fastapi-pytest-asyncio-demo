import datetime
import os
from urllib.parse import urlencode

import pytest

from ..factories import SongFactory


@pytest.mark.asyncio(loop_scope="class")
class TestSongRouter:
    @classmethod
    def setup_class(cls) -> None:
        with open(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "fixtures",
                "spotify_top_100_20241119.csv",
            )
        ) as f:
            for line in f.readlines():
                args = line.split(",")
                SongFactory.create_sync(
                    name=args[0],
                    artist=args[1],
                    streams=float(args[2]),
                    released_on=datetime.datetime.strptime(args[3].strip(), "%d %B %Y"),
                )

    async def test_list_songs(self, async_client):
        """
        Tests that the songs are listed correctly.
        """
        resp = await async_client.get("/v1/songs")
        assert resp.status_code == 200
        assert resp.json()["limit"] == 50
        assert resp.json()["offset"] == 0
        assert resp.json()["total"] == 100

    async def test_oldest_song(self, async_client):
        """
        Tests that the oldest song is correctly retrieved.
        """
        resp = await async_client.get("/v1/songs?order_by=released_on&limit=1")
        song = resp.json()["items"][0]
        assert song["name"] == "Bohemian Rhapsody"
        assert song["artist"] == "Queen"

    async def test_dua_lipa_number(self, async_client):
        """
        Tests that the number of Dua Lipa songs (including collabs) is correctly retrieved.
        """
        resp = await async_client.get(
            f"/v1/songs?{urlencode({'artist__ilike': '%dua lipa%'})}"
        )
        print(resp.json()["items"])
        assert resp.json()["total"] == 5
