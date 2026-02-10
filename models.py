from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_url = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    logs = relationship("AccessLog", back_populates="url")

class AccessLog(Base):
    __tablename__ = "access_logs"
    id = Column(Integer, primary_key=True, index=True)
    short_url = Column(String, ForeignKey("urls.short_url"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)

    url = relationship("URL", back_populates="logs")
