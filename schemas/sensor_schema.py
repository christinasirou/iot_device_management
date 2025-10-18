from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from typing import Literal


class SensorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    sensor_id: str = Field(..., min_length=1, max_length=50)
    sensor_type: Literal[
        "temperature","humidity","pressure","light","motion","sound","vibration","proximity","gas","other"
    ]
    unit: Optional[str] = Field(None, max_length=20)
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    is_active: bool = True
    device_id: int


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    sensor_id: Optional[str] = Field(None, min_length=1, max_length=50)
    sensor_type: Optional[
        Literal[
            "temperature","humidity","pressure","light","motion","sound","vibration","proximity","gas","other"
        ]
    ] = None
    unit: Optional[str] = Field(None, max_length=20)
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    is_active: Optional[bool] = None
    device_id: Optional[int] = None


class SensorResponse(SensorBase):
    id: int
    is_online: bool
    last_reading: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SensorList(BaseModel):
    sensors: List[SensorResponse]
    total: int
    page: int
    size: int
