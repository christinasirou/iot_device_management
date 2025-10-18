from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from models.sensor import Sensor
from schemas.sensor_schema import SensorCreate, SensorUpdate


class SensorCRUD:
    def create_sensor(self, db: Session, sensor: SensorCreate) -> Sensor:
        db_sensor = Sensor(**sensor.dict())
        db.add(db_sensor)
        db.commit()
        db.refresh(db_sensor)
        return db_sensor

    def get_sensor(self, db: Session, sensor_id: int) -> Optional[Sensor]:
        return db.query(Sensor).filter(Sensor.id == sensor_id).first()

    def get_sensor_by_sensor_id(self, db: Session, sensor_id: str) -> Optional[Sensor]:
        return db.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()

    def get_sensors(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None,
        device_id: Optional[int] = None,
        sensor_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_online: Optional[bool] = None
    ) -> List[Sensor]:
        query = db.query(Sensor)
        
        if search:
            query = query.filter(
                or_(
                    Sensor.name.ilike(f"%{search}%"),
                    Sensor.sensor_id.ilike(f"%{search}%")
                )
            )
        
        if device_id is not None:
            query = query.filter(Sensor.device_id == device_id)
        
        if sensor_type:
            query = query.filter(Sensor.sensor_type == sensor_type)
        
        if is_active is not None:
            query = query.filter(Sensor.is_active == is_active)
        
        if is_online is not None:
            query = query.filter(Sensor.is_online == is_online)
        
        return query.offset(skip).limit(limit).all()

    def update_sensor(self, db: Session, sensor_id: int, sensor: SensorUpdate) -> Optional[Sensor]:
        db_sensor = self.get_sensor(db, sensor_id)
        if db_sensor:
            update_data = sensor.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_sensor, field, value)
            db.commit()
            db.refresh(db_sensor)
        return db_sensor

    def delete_sensor(self, db: Session, sensor_id: int) -> bool:
        db_sensor = self.get_sensor(db, sensor_id)
        if db_sensor:
            db.delete(db_sensor)
            db.commit()
            return True
        return False

    def update_sensor_status(self, db: Session, sensor_id: int, is_online: bool) -> Optional[Sensor]:
        db_sensor = self.get_sensor(db, sensor_id)
        if db_sensor:
            db_sensor.is_online = is_online
            if is_online:
                from datetime import datetime
                db_sensor.last_reading = datetime.utcnow()
            db.commit()
            db.refresh(db_sensor)
        return db_sensor

    def get_sensors_count(
        self, 
        db: Session, 
        search: Optional[str] = None,
        device_id: Optional[int] = None,
        sensor_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_online: Optional[bool] = None
    ) -> int:
        query = db.query(Sensor)
        
        if search:
            query = query.filter(
                or_(
                    Sensor.name.ilike(f"%{search}%"),
                    Sensor.sensor_id.ilike(f"%{search}%")
                )
            )
        
        if device_id is not None:
            query = query.filter(Sensor.device_id == device_id)
        
        if sensor_type:
            query = query.filter(Sensor.sensor_type == sensor_type)
        
        if is_active is not None:
            query = query.filter(Sensor.is_active == is_active)
        
        if is_online is not None:
            query = query.filter(Sensor.is_online == is_online)
        
        return query.count()


sensor_crud = SensorCRUD()
