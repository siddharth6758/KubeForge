import logging
import redis
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import FileResponse
from config.settings import settings
from db.engine import engine, get_db
from db.database import Base
from db.helper import *
from typing import Optional
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

log = logging.getLogger(__name__)
FRONTEND_FILE = Path(__file__).parent / "templates" / "index.html"

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)

redis_conn = redis.Redis(
    host="redis",
    port=6379,
    password=settings.redis_password,
    decode_responses=True
)
log.info("Redis Server setup complete!")

@app.get("/")
async def root():
    return FileResponse(FRONTEND_FILE)

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

@app.delete("/notification/{notification_id}")
async def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    resp = delete_notification_helper(db, notification_id)
    if not resp:
        raise HTTPException(status_code=404, detail="Notification not found")
    return resp

@app.post("/notification/")
async def create_notification(user_id: int = Body(...), title: str = Body(...), description: str = Body(...), scheduled_at: datetime = Body(...), db: Session = Depends(get_db)):
    notification = add_notification(db, user_id, title, description, scheduled_at)
    if notification:
        reminder_id = f"U{user_id}_N{notification.notification_id}"
        scheduled_at_unix = convert_to_unix(notification.scheduled_at)
        redis_conn.zadd(
            "reminders",
            {f"reminder:{reminder_id}": scheduled_at_unix}
        )
        log.info(f"Added to Redis sorted set: {reminder_id}")
        return notification
    else:
        return {
            "status": 500,
            "message": "Internal Server Error"
        }

@app.patch("/notification-update/{notification_id}")
async def update_notified_notification(notification_id: int, title: Optional[str] = Body(None), description: Optional[str] = Body(None), scheduled_at: Optional[datetime] = Body(None), db: Session = Depends(get_db)):
    notification = db.get(NotificationSchedule, notification_id)
    if notification:
        is_notified = False
        if scheduled_at:
            scheduled_at = scheduled_at.astimezone(IST)
            is_notified = True if notification.scheduled_at >= scheduled_at else False
            reminder_id = f"U{notification.user_id}_N{notification.notification_id}"
            scheduled_at_unix = convert_to_unix(scheduled_at)
            redis_conn.zadd(
                "reminders",
                {f"reminder:{reminder_id}": scheduled_at_unix}
            )
            log.info(f"Updated to redis sorted set: {reminder_id}")
        return update_notification_sent(db, notification, title, description, scheduled_at, is_notified)
    else:
        raise HTTPException(status_code=404, detail="Notification not found")