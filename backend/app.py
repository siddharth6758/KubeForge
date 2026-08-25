import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Body
from db.engine import engine, SessionLocal
from db.database import Base
from db.helper import *
from typing import Optional
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

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
async def create_user(username: str = Body(...), db: Session = Depends(get_db)):
    return add_user_helper(db, username)

@app.get("/user/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_helper(db, user_id)

@app.get("/notification/{notification_id}")
async def get_notification(notification_id: int, db: Session = Depends(get_db)):
    return get_notification_helper(db, notification_id)

@app.get("/pending-notification/{user_id}")
async def user_pending_notification(user_id: int, db: Session = Depends(get_db)):
    return get_pending_notifications(db, user_id)

@app.post("/notification/")
async def create_notification(user_id: int = Body(...), title: str = Body(...), description: str = Body(...), scheduled_at: datetime = Body(...), db: Session = Depends(get_db)):
    return add_notification(db, user_id, title, description, scheduled_at)

@app.patch("/notification-update/{notification_id}")
async def update_notified_notification(notification_id: int, title: Optional[str] = Body(None), description: Optional[str] = Body(None), scheduled_at: Optional[datetime] = Body(None), db: Session = Depends(get_db)):
    notification = db.get(NotificationSchedule, notification_id)
    if notification:
        is_notified = False
        scheduled_at = scheduled_at.astimezone(IST)
        if scheduled_at is not None and scheduled_at > notification.scheduled_at:
            is_notified = True
        return update_notification_sent(db, notification, title, description, scheduled_at, is_notified)
    else:
        raise HTTPException(status_code=404, detail="Notification not found")