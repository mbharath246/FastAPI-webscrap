from fastapi import FastAPI

from src.database import schemas
from src.database.connection import engine
from src.endpoints.user import users
from src.auth import authentication
from src.endpoints.webscrap import hackernews_router

app = FastAPI()

schemas.Base.metadata.create_all(bind = engine)

app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(hackernews_router.router)