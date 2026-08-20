from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db.engine import engine
from .db.database import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}