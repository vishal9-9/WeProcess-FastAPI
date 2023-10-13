from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    Column,
    Boolean,
    text,
    DateTime,
    ForeignKey,
    SmallInteger,
)
from sqlalchemy.orm import declarative_base

from models import client, user, masters

RegisterRecordsBase = declarative_base()


class FieldsMaster(RegisterRecordsBase):
    __tablename__ = "fields_master"

    id = Column(Integer, primary_key=True)
    field_name = Column(String(100), nullable=False)
    title = Column(String(100), nullable=True)
    regex = Column(String(300), nullable=True)
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RegistersMaster(RegisterRecordsBase):
    __tablename__ = "registers_master"

    id = Column(Integer, primary_key=True)
    state = Column(String(100), nullable=False)
    act = Column(String(300), nullable=False)
    type = Column(String(500), nullable=False)
    register_name = Column(String(300), nullable=False)
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RegisterFieldsMapping(RegisterRecordsBase):
    __tablename__ = "register_fields_master_mapping"

    id = Column(Integer, primary_key=True)
    register_id = Column(ForeignKey("registers_master.id"))
    field_id = Column(ForeignKey("fields_master.id"))
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class CategoryMaster(RegisterRecordsBase):
    __tablename__ = "category_master"

    id = Column(Integer, primary_key=True)
    category_name = Column(String(250), nullable=True)
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CategoryFieldsMapping(RegisterRecordsBase):
    __tablename__ = "category_fields_master_mapping"

    id = Column(Integer, primary_key=True)
    category_id = Column(ForeignKey("category_master.id"))
    field_id = Column(ForeignKey("fields_master.id"))
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class TemplatesMaster(RegisterRecordsBase):
    __tablename__ = "templates_master"

    id = Column(Integer, primary_key=True)
    template_name = Column(String(75), nullable=False)
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class TemplateFieldsMasterMapping(RegisterRecordsBase):
    __tablename__ = "template_fields_master_mapping"

    id = Column(Integer, primary_key=True)
    template_id = Column(ForeignKey("templates_master.id"))
    field_id = Column(ForeignKey("fields_master.id"))
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class TemplateFieldsToFieldsMasterMapping(RegisterRecordsBase):
    __tablename__ = "tempalte_fields_to_fields_master_mapping"

    id = Column(Integer, primary_key=True)
    template_id = Column(ForeignKey("templates_master.id"))
    field_id = Column(ForeignKey("fields_master.id"))
    excel_field_name = Column(String(100), nullable=False)
    excel_field_index = Column(Integer, nullable=False)
    month = Column(SmallInteger, nullable=False)
    year = Column(Integer, nullable=False)
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TemplateData(RegisterRecordsBase):
    __tablename__ = "template_data"

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey(client.Client.id), nullable=False)
    employee_id = Column(String(150), nullable=False)
    field_id = Column(ForeignKey("fields_master.id"))
    value = Column(String(500), nullable=False)
    month = Column(SmallInteger, nullable=False)
    year = Column(Integer, nullable=False)
    is_active = Column(Boolean, server_default=text("'1'"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
