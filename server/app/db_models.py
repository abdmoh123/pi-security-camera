"""File containing schemas of tables in the SQL database."""

from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, timezone


class Base(DeclarativeBase):
    """Exists to provide type hints to shutup mypy."""

    pass


camera_subscriptions_table = Table(
    "camera_subscriptions",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("camera_id", Integer, ForeignKey("cameras.id"), primary_key=True),
    Column("registered_at", DateTime, default=datetime.now(timezone.utc)),
)


# Association table (join table) for many-to-many relationship
video_user_association_table = Table(
    "video_user_association",
    Base.metadata,
    Column("video_id", Integer, ForeignKey("videos.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("added_at", DateTime, default=datetime.now(timezone.utc)),
)


class User(Base):
    """Schema for the user table."""

    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    cameras: Mapped[list[Camera]] = relationship(
        "Camera", secondary=camera_subscriptions_table, back_populates=__tablename__
    )
    videos: Mapped[list[Video]] = relationship(
        "Video", secondary=video_user_association_table, back_populates=__tablename__
    )


class Camera(Base):
    """Schema for the camera table."""

    __tablename__: str = "cameras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    host_address: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String)
    auth_key: Mapped[str] = mapped_column(String)
    mac_address: Mapped[str] = mapped_column(String)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    users: Mapped[list[User]] = relationship("User", secondary=camera_subscriptions_table, back_populates=__tablename__)


class Video(Base):
    """Schema for keeping a record of uploaded videos/recordings."""

    __tablename__: str = "videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    file_name: Mapped[str] = mapped_column(String)
    camera_id: Mapped[int | None] = mapped_column(
        ForeignKey(f"{Camera.__tablename__}.id"), primary_key=True, nullable=True
    )
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    users: Mapped[list[User]] = relationship(
        "User", secondary=video_user_association_table, back_populates=__tablename__
    )
