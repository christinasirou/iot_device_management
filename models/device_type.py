from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from config import settings


class DeviceType(Base):
	__tablename__ = "device_types"
	__table_args__ = {"schema": settings.db_schema}
	
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(100), unique=True, nullable=False, index=True)
	description = Column(Text)
	manufacturer = Column(String(100))
	model = Column(String(100))
	is_active = Column(Boolean, default=True)
	created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
	updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
	
	# Relationships
	devices = relationship("Device", back_populates="device_type")
