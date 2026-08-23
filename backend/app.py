import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from db.engine import engine, SessionLocal
from db.database import Base
from db.helper import *

log = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    log.info("\nDB Session created...")
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/user-create/")
async def create_user(username: str, db: Session = Depends(get_db)):
    return add_user_helper(db, username)

@app.get("/user/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_helper(db, user_id)