from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from config import settings


class Device(Base):
	__tablename__ = "devices"
	__table_args__ = {"schema": settings.db_schema}

	# Expose primary key as device_id in the ORM while keeping underlying column name 'id'
	id = Column("id", Integer, primary_key=True, index=True)
	name = Column(String(100), nullable=False, index=True)
	description = Column(Text)
	location = Column(String(200))
	latitude = Column(Float)
	longitude = Column(Float)
	is_active = Column(Boolean, default=True)
	is_online = Column(Boolean, default=False)
	last_seen = Column(DateTime(timezone=True))
	device_type_id = Column(Integer, ForeignKey(f"{settings.db_schema}.device_types.id"))
	created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
	updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

	# Relationships
	device_type = relationship("DeviceType", back_populates="devices")
	sensors = relationship("Sensor", back_populates="device", cascade="all, delete-orphan")
