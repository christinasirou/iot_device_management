from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .device_type_schema import DeviceTypeResponse


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    location: Optional[str] = Field(None, max_length=200)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    is_active: bool = True
    device_type_id: int


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    location: Optional[str] = Field(None, max_length=200)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    is_active: Optional[bool] = None
    device_type_id: Optional[int] = None


class DeviceResponse(DeviceBase):
    id: int
    is_online: bool
    last_seen: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    device_type: Optional[DeviceTypeResponse] = None
    
    class Config:
        from_attributes = True


class DeviceList(BaseModel):
    devices: List[DeviceResponse]
    total: int
    page: int
    size: int
