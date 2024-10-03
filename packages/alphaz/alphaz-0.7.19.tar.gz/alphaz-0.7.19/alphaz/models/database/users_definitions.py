# MODULES
import datetime

# SQLALCHEMY
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint,
    Float,
    BLOB,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.sqltypes import Boolean
from marshmallow import Schema, fields

# MODELS
from .models import (
    AlphaTable,
    AlphaTableId,
    AlphaColumn,
    AlphaTableIdUpdateDate,
    AlphaTableIdPrimary,
    AlphaTableUpdateDate,
)

# CORE
from core import core

db = core.db
ma = core.ma

BIND = core.config.get("user_mgt/bind", "USERS")


class UserSession(db.Model, AlphaTableUpdateDate):
    __bind_key__ = BIND
    __tablename__ = "user_session"

    user_id = AlphaColumn(Integer, primary_key=True)
    token = AlphaColumn(String(500))
    ip = AlphaColumn(String(50))
    expire = AlphaColumn(DateTime)


class UserRole(db.Model, AlphaTableUpdateDate):
    __bind_key__ = BIND
    __tablename__ = "user_role"

    user_id = AlphaColumn(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    role_name = AlphaColumn(
        String(200),
        ForeignKey("role.name", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    activated = AlphaColumn(Boolean, default=True)


class User(db.Model, AlphaTable):
    __bind_key__ = BIND
    __tablename__ = "user"

    id = AlphaColumn(Integer, autoincrement=True, primary_key=True)
    username = AlphaColumn(String(30), unique=True)
    mail = AlphaColumn(String(40), default="-")
    password = AlphaColumn(String(100))
    pass_reset_token = AlphaColumn(String(100))
    pass_reset_token_exp = AlphaColumn(DateTime)
    telegram_id = AlphaColumn(String(100))
    # icon = AlphaColumn(String(100))
    role = AlphaColumn(Integer)

    expire = AlphaColumn(DateTime)
    date_registred = AlphaColumn(DateTime)
    registration_token = AlphaColumn(String(100))
    registration_code = AlphaColumn(String(255))
    infos = AlphaColumn(String(500))
    last_activity = AlphaColumn(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )

    roles = relationship(
        "Role",
        secondary=UserRole.__table__,
        cascade="all, delete",
    )


class RolePermission(db.Model, AlphaTableUpdateDate):
    __bind_key__ = BIND
    __tablename__ = "role_permission"

    role_name = AlphaColumn(
        String(200),
        ForeignKey("role.name", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    permission_key = AlphaColumn(
        String(200),
        ForeignKey("permission.key", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    activated = AlphaColumn(Boolean, default=True)


class Role(db.Model, AlphaTableUpdateDate):
    __bind_key__ = BIND
    __tablename__ = "role"

    name = AlphaColumn(String(200), primary_key=True)
    description = AlphaColumn(String(1000))
    activated = AlphaColumn(Boolean, default=True)

    id_app = AlphaColumn(
        Integer,
        ForeignKey("application.id", ondelete="CASCADE"),
    )

    application = relationship(
        "Application",
        backref=backref(__tablename__ + "s", lazy=True, cascade="all, delete-orphan"),
    )

    permissions = relationship(
        "Permission",
        secondary=RolePermission.__table__,
        cascade="all,delete",
    )


class Permission(db.Model, AlphaTableUpdateDate):
    __bind_key__ = BIND
    __tablename__ = "permission"

    key = AlphaColumn(String(200), primary_key=True)
    description = AlphaColumn(String(1000))
    activated = AlphaColumn(Boolean, default=True)

    roles = relationship(
        "Role", secondary=RolePermission.__table__, cascade="all,delete"
    )  # TODO: remove overlaps="permissions" and fix the warning


class Notification(db.Model, AlphaTableUpdateDate):
    __bind_key__ = BIND
    __tablename__ = "notification"

    user_id = AlphaColumn(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    user = relationship(
        "User",
        backref=backref(__tablename__ + "s", lazy=True, cascade="all, delete-orphan"),
    )

    user_from = AlphaColumn(Integer, nullable=False, primary_key=True)

    element_type = AlphaColumn(String(30))
    element_action = AlphaColumn(String(20))
    element_id = AlphaColumn(Integer)


class Application(db.Model, AlphaTableUpdateDate):
    __bind_key__ = BIND
    __tablename__ = "application"

    id = AlphaColumn(Integer, primary_key=True)
    name = AlphaColumn(String(20), nullable=False)

    description = AlphaColumn(String(255))
