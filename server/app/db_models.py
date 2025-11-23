"""File containing schemas of tables in the SQL database."""

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone


class Base(DeclarativeBase):
    """Exists to provide type hints to shutup mypy."""

    pass


class User(Base):
    """Schema for the user table."""

    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))


class Camera(Base):
    """Schema for the camera table."""

    __tablename__: str = "cameras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    auth_key: Mapped[str] = mapped_column(String)
    mac_address: Mapped[str] = mapped_column(String)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))


class CameraSubscription(Base):
    """Schema for tracking cameras subscribed to users."""

    __tablename__: str = "camera_subscriptions"

    user_id: Mapped[int] = mapped_column(ForeignKey(f"{User.__tablename__}.id"), primary_key=True)
    camera_id: Mapped[int] = mapped_column(ForeignKey(f"{Camera.__tablename__}.id"), primary_key=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
