from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class TemperatureStats(BaseModel):
    sensor_id: int
    sensor_name: str
    current_temp: float
    min_temp: float
    max_temp: float
    avg_temp: float
    temp_trend: str  # "rising", "falling", "stable"
    last_reading: datetime


class DeviceStats(BaseModel):
    device_id: int
    device_name: str
    total_sensors: int
    active_sensors: int
    online_sensors: int
    last_activity: Optional[datetime]
    temperature_sensors: List[TemperatureStats]


class AnalyticsResponse(BaseModel):
    total_devices: int
    total_sensors: int
    online_devices: int
    online_sensors: int
    device_stats: List[DeviceStats]
    temperature_summary: Dict[str, Any]
    data_points_today: int
    data_points_this_week: int
