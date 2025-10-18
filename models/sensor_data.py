from sqlalchemy import Column, Integer, Float, DateTime, Text, ForeignKey, Index, String
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from config import settings


class SensorData(Base):
	__tablename__ = "sensor_data"
	__table_args__ = (
		Index('idx_sensor_timestamp', 'sensor_id', 'timestamp'),
		Index('idx_timestamp', 'timestamp'),
		{"schema": settings.db_schema},
	)
	
	id = Column(Integer, primary_key=True, index=True)
	sensor_id = Column(Integer, ForeignKey(f"{settings.db_schema}.sensors.id"), nullable=False)
	value = Column(Float, nullable=False)
	unit = Column(String(20))
	timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
	meta = Column(Text)  # JSON string for additional data
	quality_score = Column(Float)  # Data quality indicator (0-1)
	
	# Relationships
	sensor = relationship("Sensor", back_populates="sensor_data")
