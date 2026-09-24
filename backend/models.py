import enum
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class ComplianceStatus(str, enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"
    MANUAL_REVIEW = "MANUAL_REVIEW"

class ConnectionStatus(str, enum.Enum):
    CONNECTED = "CONNECTED"
    LOGIN_REQUIRED = "LOGIN_REQUIRED"
    LOGIN_FAILED = "LOGIN_FAILED"
    BLOCKED = "BLOCKED"
    CAPTCHA_REQUIRED = "CAPTCHA_REQUIRED"
    DATA_CHANGED = "DATA_CHANGED"
    TIMEOUT = "TIMEOUT"
    RATE_LIMITED = "RATE_LIMITED"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    DISABLED = "DISABLED"
    NOT_CONFIGURED = "NOT_CONFIGURED"

class Tender(Base):
    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True, index=True)
    tender_number = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    institution = Column(String, nullable=False)
    submission_deadline = Column(DateTime, nullable=True)
    status = Column(String, default="TASLAK")
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("TenderItem", back_populates="tender", cascade="all, delete-orphan")

class TenderItem(Base):
    __tablename__ = "tender_items"

    id = Column(Integer, primary_key=True, index=True)
    tender_id = Column(Integer, ForeignKey("tenders.id"), nullable=False)
    item_no = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, default="adet")

    tender = relationship("Tender", back_populates="items")
    requirements = relationship("Requirement", back_populates="item", cascade="all, delete-orphan")

class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("tender_items.id"), nullable=False)
    field = Column(String, nullable=False)
    operator = Column(String, nullable=False)
    value = Column(String, nullable=False)
    unit = Column(String, nullable=True)
    mandatory = Column(Boolean, default=True)

    item = relationship("TenderItem", back_populates="requirements")

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    base_url = Column(String, nullable=False)
    connection_status = Column(Enum(ConnectionStatus), default=ConnectionStatus.NOT_CONFIGURED)
    last_check = Column(DateTime, nullable=True)
    last_error = Column(Text, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = Column(String, default="4M1N Uzmanı")
    action = Column(String, nullable=False)
    details = Column(Text, nullable=False)