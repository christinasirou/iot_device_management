from fastapi import APIRouter
from .devices import router as devices_router
from .sensors import router as sensors_router
from .sensor_data import router as sensor_data_router
from .device_types import router as device_types_router
from .analytics import router as analytics_router

api_router = APIRouter()

api_router.include_router(devices_router, prefix="/devices", tags=["devices"])
api_router.include_router(sensors_router, prefix="/sensors", tags=["sensors"])
api_router.include_router(sensor_data_router, prefix="/sensor-data", tags=["sensor-data"])
api_router.include_router(device_types_router, prefix="/device-types", tags=["device-types"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
