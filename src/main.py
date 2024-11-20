from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi_pagination import add_pagination

from routers import song_router

app = FastAPI(openapi_url="/v1/openapi.json", docs_url="/v1/docs")

# Add routers
router = APIRouter(prefix="/v1")
router.include_router(song_router)

app.include_router(router)

# Add pagination for list views
add_pagination(app)


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
