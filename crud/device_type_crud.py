from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from models.device_type import DeviceType
from schemas.device_type_schema import DeviceTypeCreate, DeviceTypeUpdate


class DeviceTypeCRUD:
    def create_device_type(self, db: Session, device_type: DeviceTypeCreate) -> DeviceType:
        db_device_type = DeviceType(**device_type.dict())
        db.add(db_device_type)
        db.commit()
        db.refresh(db_device_type)
        return db_device_type

    def get_device_type(self, db: Session, device_type_id: int) -> Optional[DeviceType]:
        return db.query(DeviceType).filter(DeviceType.id == device_type_id).first()

    def get_device_type_by_name(self, db: Session, name: str) -> Optional[DeviceType]:
        return db.query(DeviceType).filter(DeviceType.name == name).first()

    def get_device_types(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[DeviceType]:
        query = db.query(DeviceType)
        
        if search:
            query = query.filter(
                or_(
                    DeviceType.name.ilike(f"%{search}%"),
                    DeviceType.manufacturer.ilike(f"%{search}%"),
                    DeviceType.model.ilike(f"%{search}%")
                )
            )
        
        if is_active is not None:
            query = query.filter(DeviceType.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()

    def update_device_type(self, db: Session, device_type_id: int, device_type: DeviceTypeUpdate) -> Optional[DeviceType]:
        db_device_type = self.get_device_type(db, device_type_id)
        if db_device_type:
            update_data = device_type.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_device_type, field, value)
            db.commit()
            db.refresh(db_device_type)
        return db_device_type

    def delete_device_type(self, db: Session, device_type_id: int) -> bool:
        db_device_type = self.get_device_type(db, device_type_id)
        if db_device_type:
            db.delete(db_device_type)
            db.commit()
            return True
        return False

    def get_device_types_count(
        self, 
        db: Session, 
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        query = db.query(DeviceType)
        
        if search:
            query = query.filter(
                or_(
                    DeviceType.name.ilike(f"%{search}%"),
                    DeviceType.manufacturer.ilike(f"%{search}%"),
                    DeviceType.model.ilike(f"%{search}%")
                )
            )
        
        if is_active is not None:
            query = query.filter(DeviceType.is_active == is_active)
        
        return query.count()


device_type_crud = DeviceTypeCRUD()
