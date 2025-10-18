from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from models.database import get_db
from crud.sensor_data_crud import sensor_data_crud
from schemas.sensor_data_schema import SensorDataCreate, SensorDataResponse, SensorDataList, SensorDataStats

router = APIRouter()


@router.post("/", response_model=SensorDataResponse)
def create_sensor_data(sensor_data: SensorDataCreate, db: Session = Depends(get_db)):
    """Create new sensor data"""
    return sensor_data_crud.create_sensor_data(db, sensor_data)


@router.get("/sensor/{sensor_id}", response_model=SensorDataList)
def get_sensor_data(
    sensor_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get sensor data for a specific sensor"""
    data = sensor_data_crud.get_sensor_data(
        db, sensor_id, skip=skip, limit=limit,
        start_time=start_time, end_time=end_time
    )
    total = sensor_data_crud.get_sensor_data_count(
        db, sensor_id, start_time=start_time, end_time=end_time
    )
    
    return SensorDataList(
        data=data,
        total=total,
        page=skip // limit + 1,
        size=len(data)
    )


@router.get("/sensor/{sensor_id}/latest", response_model=SensorDataResponse)
def get_latest_sensor_data(sensor_id: int, db: Session = Depends(get_db)):
    """Get the latest sensor data for a specific sensor"""
    data = sensor_data_crud.get_latest_sensor_data(db, sensor_id)
    if not data:
        raise HTTPException(status_code=404, detail="No data found for this sensor")
    return data


@router.get("/sensor/{sensor_id}/stats", response_model=SensorDataStats)
def get_sensor_data_stats(
    sensor_id: int,
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get statistics for sensor data"""
    stats = sensor_data_crud.get_sensor_data_stats(db, sensor_id, start_time, end_time)
    if not stats:
        raise HTTPException(status_code=404, detail="No data found for this sensor")
    return stats


@router.get("/temperature", response_model=List[SensorDataResponse])
def get_temperature_data(
    device_id: Optional[int] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get temperature sensor data"""
    return sensor_data_crud.get_temperature_data(db, device_id, start_time, end_time)


@router.get("/stats/overview")
def get_data_overview(db: Session = Depends(get_db)):
    """Get overview of data collection statistics"""
    today_count = sensor_data_crud.get_data_today(db)
    week_count = sensor_data_crud.get_data_this_week(db)
    
    return {
        "data_points_today": today_count,
        "data_points_this_week": week_count,
        "timestamp": datetime.utcnow()
    }
