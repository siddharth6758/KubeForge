from datetime import datetime
from zoneinfo import ZoneInfo

# from sqlalchemy import update
from sqlalchemy.orm import Session
from db.database import User, NotificationSchedule

IST = ZoneInfo("Asia/Kolkata")

def convert_to_unix(scheduled_at: datetime):
    dt_timestamp = scheduled_at.timestamp()
    return dt_timestamp

def add_user_helper(db: Session, username: str):
    db_item = User(username=username)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user_helper(db: Session, user_id: int):
    return db.get(User, user_id)

def add_notification(db: Session, user_id: int, title: str, description: str, scheduled_at: datetime):
    scheduled_at_ist = scheduled_at.astimezone(IST)
    db_item = NotificationSchedule(user_id=user_id, title=title, description=description, scheduled_at=scheduled_at_ist)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_notification_helper(db: Session, notification_id: int):
    return db.get(NotificationSchedule, notification_id)

def get_pending_notifications(db: Session, user_id: int):
    return db.query(NotificationSchedule).filter(
            NotificationSchedule.user_id == user_id,
            NotificationSchedule.is_notified == False
        ).all()

def delete_notification_helper(db: Session, notification_id: int):
    item = db.get(NotificationSchedule, notification_id)
    if not item:
        return None
    db.delete(item)
    db.commit()
    return {"status": 200, "message": "Notifcation deleted successfully"}

def update_notification_sent(db: Session, notification: NotificationSchedule, title: str|None, description: str|None, scheduled_at: datetime|None, is_notified: bool):
    if notification:
        if title is not None:
            notification.title = title

        if description is not None:
            notification.description = description

        if scheduled_at is not None:
            notification.scheduled_at = scheduled_at

        notification.is_notified = is_notified
        db.commit()
        db.refresh(notification)
        return notification
    else:
        return {"status": 404, "message": f"Notification not found: {notification.notification_id}"}