from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from config import settings
import enum


class SensorType(enum.Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    LIGHT = "light"
    MOTION = "motion"
    SOUND = "sound"
    VIBRATION = "vibration"
    PROXIMITY = "proximity"
    GAS = "gas"
    OTHER = "other"


class Sensor(Base):
    __tablename__ = "sensors"
    __table_args__ = {"schema": settings.db_schema}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    sensor_id = Column(String(50), unique=True, nullable=False, index=True)
    # Store as plain string in DB to avoid DB enum type
    sensor_type = Column(String(50), nullable=False)
    unit = Column(String(20))  # e.g., "°C", "%", "Pa", "lux"
    min_value = Column(Float)
    max_value = Column(Float)
    is_active = Column(Boolean, default=True)
    is_online = Column(Boolean, default=False)
    last_reading = Column(DateTime(timezone=True))
    device_id = Column(Integer, ForeignKey(f"{settings.db_schema}.devices.id"))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    device = relationship("Device", back_populates="sensors")
    sensor_data = relationship("SensorData", back_populates="sensor", cascade="all, delete-orphan")
