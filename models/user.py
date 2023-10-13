from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    Column,
    Boolean,
    text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base

from models import client, masters

UserBase = declarative_base()


class User(UserBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    salt = Column(String(150), nullable=False)
    mobile = Column(String(50), nullable=False)
    role_id = Column(ForeignKey(masters.RoleMaster.id))
    client_id = Column(ForeignKey(client.Client.id))
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
