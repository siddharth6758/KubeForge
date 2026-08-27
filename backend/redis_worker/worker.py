import redis
import time
import logging
import asyncio

from notifypy import Notify
from db.engine import SessionLocal
from config.settings import settings
from db.helper import get_notification_helper
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

log = logging.getLogger(__name__)

redis_app = FastAPI()

r = redis.Redis(
    host="redis",
    port=6379,
    password=settings.redis_password,
    decode_responses=True
)

@redis_app.get('/healthcheck')
async def healthcheck_worker():
    return {"status":200, "message": "ok"}

async def get_processing():
    db = SessionLocal()
    while True:
        try:
            now = time.time()
            reminders = r.zrangebyscore(
                "reminders",
                "-inf",
                now
            )

            # log.info(f"[WORKER] info running at: {now}")

            notify = Notify()

            try:
                for reminder in reminders:
                    log.debug(f"Processing the notification: {reminder}")

                    notification_id = reminder.split('N')[-1]

                    notification = get_notification_helper(db, notification_id)

                    if notification is None:
                        log.warning(
                            "Notification %s not found",
                            notification_id,
                        )
                        r.zrem("reminders", reminder)
                        continue

                    notify.title = notification.title
                    notify.message = notification.description
                    notify.send()

                    r.zrem("reminders", reminder)
            finally:
                db.close()

        except Exception as e:
            log.exception(f"[WORKER] Worker loop failed: {str(e)}")

        await asyncio.sleep(0.5)

@redis_app.on_event("startup")
async def startup():
    asyncio.create_task(get_processing())