import redis
import time
import logging

from notifypy import Notify
from db.engine import SessionLocal
from config.settings import settings
from db.helper import get_notification_helper
from fastapi import FastAPI

log = logging.getLogger(__name__)

redis_app = FastAPI()

r = redis.Redis(
    host="localhost",
    port=6753,
    password=settings.redis_password,
    decode_responses=True
)

@redis_app.get('/healthcheck')
async def healthcheck_worker():
    return {"status":200, "message": "ok"}

while True:
    now = time.time()
    reminders = r.zrangebyscore(
        "reminders",
        "-inf",
        now
    )

    db = SessionLocal()

    log.info(f"[WORKER] info running at: {now}")

    notification = Notify()

    for reminder in reminders:
        log.debug(f"Processing the notification: {reminder}")

        notification_id = reminder.split('N')[-1]
        print(f'------>Notification:{notification_id}')

        notification = get_notification_helper(db, notification_id)

        notification.title = notification.title
        notification.message = notification.description
        notification.send()

        r.zrem("reminders", reminder)
