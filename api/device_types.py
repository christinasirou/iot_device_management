from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database import get_db
from crud.device_type_crud import device_type_crud
from schemas.device_type_schema import DeviceTypeCreate, DeviceTypeUpdate, DeviceTypeResponse

router = APIRouter()


@router.post("/", response_model=DeviceTypeResponse)
def create_device_type(device_type: DeviceTypeCreate, db: Session = Depends(get_db)):
    """Create a new device type"""
    # Check if name already exists
    existing_type = device_type_crud.get_device_type_by_name(db, device_type.name)
    if existing_type:
        raise HTTPException(status_code=400, detail="Device type name already exists")
    
    return device_type_crud.create_device_type(db, device_type)


@router.get("/", response_model=List[DeviceTypeResponse])
def get_device_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of device types with filtering options"""
    return device_type_crud.get_device_types(
        db, skip=skip, limit=limit, search=search, is_active=is_active
    )


@router.get("/{device_type_id}", response_model=DeviceTypeResponse)
def get_device_type(device_type_id: int, db: Session = Depends(get_db)):
    """Get a specific device type by ID"""
    device_type = device_type_crud.get_device_type(db, device_type_id)
    if not device_type:
        raise HTTPException(status_code=404, detail="Device type not found")
    return device_type


@router.put("/{device_type_id}", response_model=DeviceTypeResponse)
def update_device_type(device_type_id: int, device_type: DeviceTypeUpdate, db: Session = Depends(get_db)):
    """Update a device type"""
    updated_type = device_type_crud.update_device_type(db, device_type_id, device_type)
    if not updated_type:
        raise HTTPException(status_code=404, detail="Device type not found")
    return updated_type


@router.delete("/{device_type_id}")
def delete_device_type(device_type_id: int, db: Session = Depends(get_db)):
    """Delete a device type"""
    success = device_type_crud.delete_device_type(db, device_type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Device type not found")
    return {"message": "Device type deleted successfully"}
