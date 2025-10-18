from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database import get_db
from crud.device_crud import device_crud
from schemas.device_schema import DeviceCreate, DeviceUpdate, DeviceResponse, DeviceList

router = APIRouter()


@router.post("/", response_model=DeviceResponse)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """Create a new IoT device"""
    return device_crud.create_device(db, device)


@router.get("/", response_model=DeviceList)
def get_devices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    device_type_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    is_online: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of IoT devices with filtering options"""
    devices = device_crud.get_devices(
        db, skip=skip, limit=limit, search=search,
        device_type_id=device_type_id, is_active=is_active, is_online=is_online
    )
    total = device_crud.get_devices_count(
        db, search=search, device_type_id=device_type_id,
        is_active=is_active, is_online=is_online
    )
    
    return DeviceList(
        devices=devices,
        total=total,
        page=skip // limit + 1,
        size=len(devices)
    )


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    """Get a specific device by ID"""
    device = device_crud.get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(device_id: int, device: DeviceUpdate, db: Session = Depends(get_db)):
    """Update a device"""
    updated_device = device_crud.update_device(db, device_id, device)
    if not updated_device:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated_device


@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """Delete a device"""
    success = device_crud.delete_device(db, device_id)
    if not success:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}


@router.patch("/{device_id}/status")
def update_device_status(
    device_id: int, 
    is_online: bool, 
    db: Session = Depends(get_db)
):
    """Update device online status"""
    device = device_crud.update_device_status(db, device_id, is_online)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": f"Device status updated to {'online' if is_online else 'offline'}"}
