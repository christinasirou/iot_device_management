from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from models.device import Device
from models.sensor import Sensor
from models.sensor_data import SensorData
from schemas.analytics_schema import AnalyticsResponse, TemperatureStats, DeviceStats


class AnalyticsCRUD:
    def get_analytics(self, db: Session) -> AnalyticsResponse:
        # Get basic counts
        total_devices = db.query(Device).count()
        total_sensors = db.query(Sensor).count()
        online_devices = db.query(Device).filter(Device.is_online == True).count()
        online_sensors = db.query(Sensor).filter(Sensor.is_online == True).count()
        
        # Get device stats
        devices = db.query(Device).all()
        device_stats = []
        
        for device in devices:
            sensors = db.query(Sensor).filter(Sensor.device_id == device.id).all()
            active_sensors = db.query(Sensor).filter(
                and_(Sensor.device_id == device.id, Sensor.is_active == True)
            ).count()
            online_sensors_count = db.query(Sensor).filter(
                and_(Sensor.device_id == device.id, Sensor.is_online == True)
            ).count()
            
            # Get temperature sensors for this device
            temp_sensors = db.query(Sensor).filter(
                and_(
                    Sensor.device_id == device.id,
                    Sensor.sensor_type == 'temperature'
                )
            ).all()
            
            temperature_stats = []
            for sensor in temp_sensors:
                latest_data = db.query(SensorData).filter(
                    SensorData.sensor_id == sensor.id
                ).order_by(desc(SensorData.timestamp)).first()
                
                if latest_data:
                    # Get stats for this sensor
                    stats = db.query(
                        func.min(SensorData.value).label('min_temp'),
                        func.max(SensorData.value).label('max_temp'),
                        func.avg(SensorData.value).label('avg_temp')
                    ).filter(SensorData.sensor_id == sensor.id).first()
                    
                    if stats:
                        temperature_stats.append(TemperatureStats(
                            sensor_id=sensor.id,
                            sensor_name=sensor.name,
                            current_temp=latest_data.value,
                            min_temp=float(stats.min_temp),
                            max_temp=float(stats.max_temp),
                            avg_temp=float(stats.avg_temp),
                            temp_trend="stable",  # Could be calculated based on recent data
                            last_reading=latest_data.timestamp
                        ))
            
            # Get last activity
            last_activity = db.query(SensorData.timestamp).join(Sensor).filter(
                Sensor.device_id == device.id
            ).order_by(desc(SensorData.timestamp)).first()
            
            device_stats.append(DeviceStats(
                device_id=device.id,
                device_name=device.name,
                total_sensors=len(sensors),
                active_sensors=active_sensors,
                online_sensors=online_sensors_count,
                last_activity=last_activity.timestamp if last_activity else None,
                temperature_sensors=temperature_stats
            ))
        
        # Get temperature summary
        temp_sensors = db.query(Sensor).filter(Sensor.sensor_type == 'temperature').all()
        temp_summary = {}
        
        if temp_sensors:
            temp_values = []
            for sensor in temp_sensors:
                latest = db.query(SensorData).filter(
                    SensorData.sensor_id == sensor.id
                ).order_by(desc(SensorData.timestamp)).first()
                if latest:
                    temp_values.append(latest.value)
            
            if temp_values:
                temp_summary = {
                    "current_avg": sum(temp_values) / len(temp_values),
                    "min_current": min(temp_values),
                    "max_current": max(temp_values),
                    "sensors_count": len(temp_values)
                }
        
        # Get data points for today and this week
        today = datetime.utcnow().date()
        start_today = datetime.combine(today, datetime.min.time())
        end_today = datetime.combine(today, datetime.max.time())
        
        week_start = today - timedelta(days=today.weekday())
        start_week = datetime.combine(week_start, datetime.min.time())
        
        data_points_today = db.query(SensorData).filter(
            and_(
                SensorData.timestamp >= start_today,
                SensorData.timestamp <= end_today
            )
        ).count()
        
        data_points_this_week = db.query(SensorData).filter(
            SensorData.timestamp >= start_week
        ).count()
        
        return AnalyticsResponse(
            total_devices=total_devices,
            total_sensors=total_sensors,
            online_devices=online_devices,
            online_sensors=online_sensors,
            device_stats=device_stats,
            temperature_summary=temp_summary,
            data_points_today=data_points_today,
            data_points_this_week=data_points_this_week
        )

    def get_temperature_analytics(self, db: Session, device_id: Optional[int] = None) -> List[TemperatureStats]:
        query = db.query(Sensor).filter(Sensor.sensor_type == 'temperature')
        
        if device_id:
            query = query.filter(Sensor.device_id == device_id)
        
        sensors = query.all()
        temperature_stats = []
        
        for sensor in sensors:
            latest_data = db.query(SensorData).filter(
                SensorData.sensor_id == sensor.id
            ).order_by(desc(SensorData.timestamp)).first()
            
            if latest_data:
                stats = db.query(
                    func.min(SensorData.value).label('min_temp'),
                    func.max(SensorData.value).label('max_temp'),
                    func.avg(SensorData.value).label('avg_temp')
                ).filter(SensorData.sensor_id == sensor.id).first()
                
                if stats:
                    temperature_stats.append(TemperatureStats(
                        sensor_id=sensor.id,
                        sensor_name=sensor.name,
                        current_temp=latest_data.value,
                        min_temp=float(stats.min_temp),
                        max_temp=float(stats.max_temp),
                        avg_temp=float(stats.avg_temp),
                        temp_trend="stable",
                        last_reading=latest_data.timestamp
                    ))
        
        return temperature_stats


analytics_crud = AnalyticsCRUD()
