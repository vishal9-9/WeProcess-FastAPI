from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    Column,
    Boolean,
    text,
    DateTime,
)
from sqlalchemy.orm import declarative_base

ClientBase = declarative_base()


class Client(ClientBase):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
