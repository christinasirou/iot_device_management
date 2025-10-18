from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from models.device import Device
from schemas.device_schema import DeviceCreate, DeviceUpdate


class DeviceCRUD:
    def create_device(self, db: Session, device: DeviceCreate) -> Device:
        db_device = Device(**device.dict())
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device

    def get_device(self, db: Session, device_id: int) -> Optional[Device]:
        return db.query(Device).filter(Device.id == device_id).first()

    def get_device_by_device_id(self, db: Session, device_id: int) -> Optional[Device]:
        return db.query(Device).filter(Device.id == device_id).first()

    def get_devices(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None,
        device_type_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        is_online: Optional[bool] = None
    ) -> List[Device]:
        query = db.query(Device)
        
        if search:
            query = query.filter(
                or_(
                    Device.name.ilike(f"%{search}%"),
                    Device.location.ilike(f"%{search}%")
                )
            )
        
        if device_type_id is not None:
            query = query.filter(Device.device_type_id == device_type_id)
        
        if is_active is not None:
            query = query.filter(Device.is_active == is_active)
        
        if is_online is not None:
            query = query.filter(Device.is_online == is_online)
        
        return query.offset(skip).limit(limit).all()

    def update_device(self, db: Session, device_id: int, device: DeviceUpdate) -> Optional[Device]:
        db_device = self.get_device(db, device_id)
        if db_device:
            update_data = device.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_device, field, value)
            db.commit()
            db.refresh(db_device)
        return db_device

    def delete_device(self, db: Session, device_id: int) -> bool:
        db_device = self.get_device(db, device_id)
        if db_device:
            db.delete(db_device)
            db.commit()
            return True
        return False

    def update_device_status(self, db: Session, device_id: int, is_online: bool) -> Optional[Device]:
        db_device = self.get_device(db, device_id)
        if db_device:
            db_device.is_online = is_online
            if is_online:
                from datetime import datetime
                db_device.last_seen = datetime.utcnow()
            db.commit()
            db.refresh(db_device)
        return db_device

    def get_devices_count(
        self, 
        db: Session, 
        search: Optional[str] = None,
        device_type_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        is_online: Optional[bool] = None
    ) -> int:
        query = db.query(Device)
        
        if search:
            query = query.filter(
                or_(
                    Device.name.ilike(f"%{search}%"),
                    Device.location.ilike(f"%{search}%")
                )
            )
        
        if device_type_id is not None:
            query = query.filter(Device.device_type_id == device_type_id)
        
        if is_active is not None:
            query = query.filter(Device.is_active == is_active)
        
        if is_online is not None:
            query = query.filter(Device.is_online == is_online)
        
        return query.count()


device_crud = DeviceCRUD()
