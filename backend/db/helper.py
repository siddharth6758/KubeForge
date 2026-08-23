from sqlalchemy.orm import Session
from db.database import User, NotificationSchedule

def add_user_helper(db: Session, username: str):
    db_item = User(username=username)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user_helper(db: Session, user_id: int):
    return db.get(User, user_id)