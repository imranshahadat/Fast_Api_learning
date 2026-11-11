from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.init_db import create_tables
from app.routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(title="User CRUD API", lifespan=lifespan)

app.include_router(user_router)


@app.get("/")
async def home():
    return {"message": "Welcome to FastAPI"}
