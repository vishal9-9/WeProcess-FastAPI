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

MastersBase = declarative_base()


class RoleMaster(MastersBase):
    __tablename__ = "role_master"
    id = Column(Integer, primary_key=True)
    role = Column(String(100), nullable=False)
    is_custom = Column(Boolean, server_default=text("'0'"))
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class CountryMaster(MastersBase):
    __tablename__ = "country_master"

    id = Column(Integer, primary_key=True, index=True)
    country_name = Column(String(255))


class StateMaster(MastersBase):
    __tablename__ = "state_master"

    id = Column(Integer, primary_key=True, index=True)
    state_name = Column(String(255))
    country_id = Column(ForeignKey("country_master.id"), nullable=False)
