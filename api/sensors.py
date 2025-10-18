from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database import get_db
from crud.sensor_crud import sensor_crud
from schemas.sensor_schema import SensorCreate, SensorUpdate, SensorResponse, SensorList

router = APIRouter()


@router.post("/", response_model=SensorResponse)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    """Create a new sensor"""
    # Check if sensor_id already exists
    existing_sensor = sensor_crud.get_sensor_by_sensor_id(db, sensor.sensor_id)
    if existing_sensor:
        raise HTTPException(status_code=400, detail="Sensor ID already exists")
    
    return sensor_crud.create_sensor(db, sensor)


@router.get("/", response_model=SensorList)
def get_sensors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    device_id: Optional[int] = Query(None),
    sensor_type: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    is_online: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of sensors with filtering options"""
    sensors = sensor_crud.get_sensors(
        db, skip=skip, limit=limit, search=search,
        device_id=device_id, sensor_type=sensor_type,
        is_active=is_active, is_online=is_online
    )
    total = sensor_crud.get_sensors_count(
        db, search=search, device_id=device_id,
        sensor_type=sensor_type, is_active=is_active, is_online=is_online
    )
    
    return SensorList(
        sensors=sensors,
        total=total,
        page=skip // limit + 1,
        size=len(sensors)
    )


@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    """Get a specific sensor by ID"""
    sensor = sensor_crud.get_sensor(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.put("/{sensor_id}", response_model=SensorResponse)
def update_sensor(sensor_id: int, sensor: SensorUpdate, db: Session = Depends(get_db)):
    """Update a sensor"""
    updated_sensor = sensor_crud.update_sensor(db, sensor_id, sensor)
    if not updated_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return updated_sensor


@router.delete("/{sensor_id}")
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)):
    """Delete a sensor"""
    success = sensor_crud.delete_sensor(db, sensor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"message": "Sensor deleted successfully"}


@router.patch("/{sensor_id}/status")
def update_sensor_status(
    sensor_id: int, 
    is_online: bool, 
    db: Session = Depends(get_db)
):
    """Update sensor online status"""
    sensor = sensor_crud.update_sensor_status(db, sensor_id, is_online)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"message": f"Sensor status updated to {'online' if is_online else 'offline'}"}
