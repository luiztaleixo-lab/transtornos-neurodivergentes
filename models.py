from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def utc_now():
    return datetime.now(timezone.utc)

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    bio = db.Column(db.String(500), default="")
    avatar_color = db.Column(db.String(20), default="#4a6b5d")
    created_at = db.Column(db.DateTime, default=utc_now)

    forum_messages = db.relationship("ForumMessage", back_populates="user", lazy="dynamic")
    created_rooms = db.relationship("ForumRoom", back_populates="creator", lazy="dynamic")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "bio": self.bio,
            "avatar_color": self.avatar_color,
            "created_at": self.created_at.strftime("%d/%m/%Y") if self.created_at else ""
        }


class ForumRoom(db.Model):
    __tablename__ = "forum_rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), default="")
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    creator = db.relationship("User", back_populates="created_rooms")
    messages = db.relationship("ForumMessage", back_populates="room", cascade="all, delete-orphan", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.creator.username if self.creator else "Sistema",
            "created_at": self.created_at.strftime("%d/%m/%Y %H:%M") if self.created_at else "",
            "messages_count": self.messages.count()
        }


class ForumMessage(db.Model):
    __tablename__ = "forum_messages"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("forum_rooms.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now, index=True)

    user = db.relationship("User", back_populates="forum_messages")
    room = db.relationship("ForumRoom", back_populates="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "user_id": self.user_id,
            "username": self.user.username if self.user else "Desconhecido",
            "avatar_color": self.user.avatar_color if self.user else "#4a6b5d",
            "content": self.content,
            "created_at": self.created_at.strftime("%H:%M") if self.created_at else ""
        }


class PrivateMessage(db.Model):
    __tablename__ = "private_messages"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now, index=True)

    sender = db.relationship("User", foreign_keys=[sender_id])
    recipient = db.relationship("User", foreign_keys=[recipient_id])

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "sender_username": self.sender.username if self.sender else "Desconhecido",
            "sender_avatar_color": self.sender.avatar_color if self.sender else "#4a6b5d",
            "content": self.content,
            "created_at": self.created_at.strftime("%H:%M") if self.created_at else ""
        }
