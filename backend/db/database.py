from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import text

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(
        Integer,
        autoincrement=True,
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String,
        nullable = False
    )
    # notification_schedule: Mapped[list["NotificationSchedule"]] = relationship(
    #     back_populates="user",
    #     lazy="selectin"
    # )

class NotificationSchedule(Base):
    __tablename__ = "notification_schedule"

    notification_id: Mapped[int] = mapped_column(
        Integer,
        autoincrement=True,
        primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.user_id"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(
        String,
        nullable = False
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable = True
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    is_notified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false")
    )
    # user: Mapped["User"] = relationship(
    #     back_populates="notification_schedule",
    # )