from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Tuple
from datetime import datetime, timedelta
from models.sensor_data import SensorData
from schemas.sensor_data_schema import SensorDataCreate, SensorDataStats


class SensorDataCRUD:
    def create_sensor_data(self, db: Session, sensor_data: SensorDataCreate) -> SensorData:
        db_sensor_data = SensorData(**sensor_data.dict())
        db.add(db_sensor_data)
        db.commit()
        db.refresh(db_sensor_data)
        return db_sensor_data

    def get_sensor_data(
        self, 
        db: Session, 
        sensor_id: int,
        skip: int = 0, 
        limit: int = 100,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[SensorData]:
        query = db.query(SensorData).filter(SensorData.sensor_id == sensor_id)
        
        if start_time:
            query = query.filter(SensorData.timestamp >= start_time)
        
        if end_time:
            query = query.filter(SensorData.timestamp <= end_time)
        
        return query.order_by(desc(SensorData.timestamp)).offset(skip).limit(limit).all()

    def get_latest_sensor_data(self, db: Session, sensor_id: int) -> Optional[SensorData]:
        return db.query(SensorData).filter(
            SensorData.sensor_id == sensor_id
        ).order_by(desc(SensorData.timestamp)).first()

    def get_sensor_data_stats(
        self, 
        db: Session, 
        sensor_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Optional[SensorDataStats]:
        query = db.query(SensorData).filter(SensorData.sensor_id == sensor_id)
        
        if start_time:
            query = query.filter(SensorData.timestamp >= start_time)
        
        if end_time:
            query = query.filter(SensorData.timestamp <= end_time)
        
        stats = query.with_entities(
            func.count(SensorData.id).label('count'),
            func.min(SensorData.value).label('min_value'),
            func.max(SensorData.value).label('max_value'),
            func.avg(SensorData.value).label('avg_value')
        ).first()
        
        if not stats or stats.count == 0:
            return None
        
        latest_data = self.get_latest_sensor_data(db, sensor_id)
        
        return SensorDataStats(
            sensor_id=sensor_id,
            count=stats.count,
            min_value=float(stats.min_value),
            max_value=float(stats.max_value),
            avg_value=float(stats.avg_value),
            latest_value=latest_data.value if latest_data else 0.0,
            latest_timestamp=latest_data.timestamp if latest_data else datetime.utcnow()
        )

    def get_sensor_data_count(
        self, 
        db: Session, 
        sensor_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> int:
        query = db.query(SensorData).filter(SensorData.sensor_id == sensor_id)
        
        if start_time:
            query = query.filter(SensorData.timestamp >= start_time)
        
        if end_time:
            query = query.filter(SensorData.timestamp <= end_time)
        
        return query.count()

    def get_temperature_data(
        self, 
        db: Session, 
        device_id: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[SensorData]:
        from models.sensor import Sensor
        
        query = db.query(SensorData).join(Sensor).filter(
            Sensor.sensor_type == 'temperature'
        )
        
        if device_id:
            query = query.filter(Sensor.device_id == device_id)
        
        if start_time:
            query = query.filter(SensorData.timestamp >= start_time)
        
        if end_time:
            query = query.filter(SensorData.timestamp <= end_time)
        
        return query.order_by(desc(SensorData.timestamp)).all()

    def get_data_today(self, db: Session) -> int:
        today = datetime.utcnow().date()
        start_time = datetime.combine(today, datetime.min.time())
        end_time = datetime.combine(today, datetime.max.time())
        
        return db.query(SensorData).filter(
            and_(
                SensorData.timestamp >= start_time,
                SensorData.timestamp <= end_time
            )
        ).count()

    def get_data_this_week(self, db: Session) -> int:
        today = datetime.utcnow().date()
        week_start = today - timedelta(days=today.weekday())
        start_time = datetime.combine(week_start, datetime.min.time())
        end_time = datetime.utcnow()
        
        return db.query(SensorData).filter(
            and_(
                SensorData.timestamp >= start_time,
                SensorData.timestamp <= end_time
            )
        ).count()


sensor_data_crud = SensorDataCRUD()
