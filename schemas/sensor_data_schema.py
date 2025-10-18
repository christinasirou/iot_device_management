from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SensorDataBase(BaseModel):
    sensor_id: int
    value: float
    unit: Optional[str] = Field(None, max_length=20)
    meta: Optional[str] = None
    quality_score: Optional[float] = Field(None, ge=0, le=1)


class SensorDataCreate(SensorDataBase):
    timestamp: Optional[datetime] = None


class SensorDataResponse(SensorDataBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class SensorDataList(BaseModel):
    data: List[SensorDataResponse]
    total: int
    page: int
    size: int


class SensorDataStats(BaseModel):
    sensor_id: int
    count: int
    min_value: float
    max_value: float
    avg_value: float
    latest_value: float
    latest_timestamp: datetime
