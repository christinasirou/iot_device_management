#!/usr/bin/env python3
"""
Sample data script for IoT Device Management API
This script creates sample device types, devices, and sensors for testing
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.database import SessionLocal, engine
from models import Base
from models.device_type import DeviceType
from models.device import Device
from models.sensor import Sensor, SensorType
from models.sensor_data import SensorData
from datetime import datetime, timedelta
import os
import random

# Create tables
Base.metadata.create_all(bind=engine)

def get_or_create_device_type(db: Session, name: str, **kwargs) -> DeviceType:
    existing = db.query(DeviceType).filter(DeviceType.name == name).first()
    if existing:
        return existing
    obj = DeviceType(name=name, **kwargs)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_or_create_device(db: Session, name: str, **kwargs) -> Device:
    existing = db.query(Device).filter(Device.name == name).first()
    if existing:
        return existing
    obj = Device(name=name, **kwargs)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_or_create_sensor(db: Session, sensor_id: str, **kwargs) -> Sensor:
    existing = db.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()
    if existing:
        return existing
    obj = Sensor(sensor_id=sensor_id, **kwargs)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_sample_data():
    db = SessionLocal()
    
    try:
        # Create device types (idempotent)
        dt_temp = get_or_create_device_type(db,
            name="Temperature Sensor",
            description="Digital temperature sensor",
            manufacturer="DHT22",
            model="DHT22",
            is_active=True
        )
        dt_hum = get_or_create_device_type(db,
            name="Humidity Sensor",
            description="Digital humidity sensor",
            manufacturer="DHT22",
            model="DHT22",
            is_active=True
        )
        dt_press = get_or_create_device_type(db,
            name="Pressure Sensor",
            description="Barometric pressure sensor",
            manufacturer="BMP280",
            model="BMP280",
            is_active=True
        )
        dt_motion = get_or_create_device_type(db,
            name="Motion Sensor",
            description="PIR motion detection sensor",
            manufacturer="HC-SR501",
            model="HC-SR501",
            is_active=True
        )
        
        # Create devices
        # Create devices (idempotent)
        d_lr = get_or_create_device(db,
            name="Living Room Sensor Hub",
            description="Main sensor hub in living room",
            location="Living Room",
            latitude=40.7128,
            longitude=-74.0060,
            is_active=True,
            is_online=True,
            last_seen=datetime.utcnow(),
            device_type_id=dt_temp.id
        )
        d_kt = get_or_create_device(db,
            name="Kitchen Temperature Monitor",
            description="Kitchen temperature monitoring",
            location="Kitchen",
            latitude=40.7129,
            longitude=-74.0061,
            is_active=True,
            is_online=True,
            last_seen=datetime.utcnow(),
            device_type_id=dt_temp.id
        )
        d_br = get_or_create_device(db,
            name="Bedroom Environment Sensor",
            description="Bedroom environment monitoring",
            location="Bedroom",
            latitude=40.7127,
            longitude=-74.0059,
            is_active=True,
            is_online=False,
            last_seen=datetime.utcnow() - timedelta(hours=2),
            device_type_id=dt_hum.id
        )
        d_gr = get_or_create_device(db,
            name="Garage Motion Detector",
            description="Garage motion detection system",
            location="Garage",
            latitude=40.7130,
            longitude=-74.0062,
            is_active=True,
            is_online=True,
            last_seen=datetime.utcnow(),
            device_type_id=dt_motion.id
        )
        
        # Create sensors
        # Create sensors (idempotent)
        s_lr_temp = get_or_create_sensor(db,
            sensor_id="TEMP_LR001",
            name="Living Room Temperature",
            sensor_type=SensorType.TEMPERATURE.value,
            unit="°C",
            min_value=-40,
            max_value=80,
            is_active=True,
            is_online=True,
            last_reading=datetime.utcnow(),
            device_id=d_lr.id
        )
        s_lr_hum = get_or_create_sensor(db,
            sensor_id="HUM_LR001",
            name="Living Room Humidity",
            sensor_type=SensorType.HUMIDITY.value,
            unit="%",
            min_value=0,
            max_value=100,
            is_active=True,
            is_online=True,
            last_reading=datetime.utcnow(),
            device_id=d_lr.id
        )
        s_kt_temp = get_or_create_sensor(db,
            sensor_id="TEMP_KT001",
            name="Kitchen Temperature",
            sensor_type=SensorType.TEMPERATURE.value,
            unit="°C",
            min_value=-40,
            max_value=80,
            is_active=True,
            is_online=True,
            last_reading=datetime.utcnow(),
            device_id=d_kt.id
        )
        s_br_hum = get_or_create_sensor(db,
            sensor_id="HUM_BR001",
            name="Bedroom Humidity",
            sensor_type=SensorType.HUMIDITY.value,
            unit="%",
            min_value=0,
            max_value=100,
            is_active=True,
            is_online=False,
            last_reading=datetime.utcnow() - timedelta(hours=2),
            device_id=d_br.id
        )
        s_gr_motion = get_or_create_sensor(db,
            sensor_id="MOT_GR001",
            name="Garage Motion",
            sensor_type=SensorType.MOTION.value,
            unit="",
            min_value=0,
            max_value=1,
            is_active=True,
            is_online=True,
            last_reading=datetime.utcnow(),
            device_id=d_gr.id
        )
        
        # Create sample sensor data
        sensor_data = []
        
        # Generate recent time-series data (configurable, default 24 hours)
        hours_to_generate = int(os.getenv("SAMPLE_HOURS", "24"))
        for i in range(hours_to_generate):
            timestamp = datetime.utcnow() - timedelta(hours=i)
            
            # Living room temperature (20-25°C range)
            temp_value = 22.5 + random.uniform(-2, 2) + random.uniform(-1, 1) * (i / 168)
            sensor_data.append(SensorData(
                sensor_id=s_lr_temp.id,
                value=round(temp_value, 1),
                unit="°C",
                timestamp=timestamp,
                quality_score=random.uniform(0.8, 1.0)
            ))
            
            # Kitchen temperature (18-28°C range, more variable)
            temp_value = 23.0 + random.uniform(-3, 3) + random.uniform(-2, 2) * (i / 168)
            sensor_data.append(SensorData(
                sensor_id=s_kt_temp.id,
                value=round(temp_value, 1),
                unit="°C",
                timestamp=timestamp,
                quality_score=random.uniform(0.7, 1.0)
            ))
            
            # Living room humidity (40-60% range)
            hum_value = 50 + random.uniform(-10, 10) + random.uniform(-5, 5) * (i / 168)
            sensor_data.append(SensorData(
                sensor_id=s_lr_hum.id,
                value=round(hum_value, 1),
                unit="%",
                timestamp=timestamp,
                quality_score=random.uniform(0.8, 1.0)
            ))

            # Bedroom humidity (35-65% range, slightly different baseline)
            br_hum_value = 52 + random.uniform(-12, 12) + random.uniform(-6, 6) * (i / 168)
            sensor_data.append(SensorData(
                sensor_id=s_br_hum.id,
                value=round(br_hum_value, 1),
                unit="%",
                timestamp=timestamp,
                quality_score=random.uniform(0.8, 1.0)
            ))
            
            # Motion sensor (0 or 1)
            motion_value = 1 if random.random() < 0.1 else 0  # 10% chance of motion
            sensor_data.append(SensorData(
                sensor_id=s_gr_motion.id,
                value=motion_value,
                unit="",
                timestamp=timestamp,
                quality_score=random.uniform(0.9, 1.0)
            ))
        
        # Add sensor data in batches
        for i in range(0, len(sensor_data), 100):
            batch = sensor_data[i:i+100]
            for data in batch:
                db.add(data)
            db.commit()
        
        print("Sample data created successfully!")
        # Summaries (query counts to avoid NameError and reflect actual DB state)
        dt_count = db.query(DeviceType).count()
        dev_count = db.query(Device).count()
        sen_count = db.query(Sensor).count()
        sd_count = db.query(SensorData).count()
        print(f"Device types in DB: {dt_count}")
        print(f"Devices in DB: {dev_count}")
        print(f"Sensors in DB: {sen_count}")
        print(f"Sensor data points added: {sd_count}")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
