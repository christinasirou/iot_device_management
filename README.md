# IoT Device Management API

A comprehensive FastAPI microservice for managing IoT devices, sensors, and data collection with real-time analytics and monitoring capabilities.

## Features

- **Device Management**: Create, read, update, and delete IoT devices
- **Sensor Management**: Manage various types of sensors (temperature, humidity, pressure, etc.)
- **Data Collection**: Store and retrieve sensor data with timestamps
- **Analytics**: Real-time analytics and statistics
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Data Validation**: Pydantic models for request/response validation
- **Database Migrations**: Alembic for database schema management

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **PostgreSQL**: Primary database
- **Alembic**: Database migration tool
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application

## Project Structure

```
iot_device_management/
├── alembic/                    # Database migrations
│   ├── versions/              # Migration files
│   ├── env.py                 # Alembic environment
│   └── script.py.mako         # Migration template
├── api/                       # API endpoints
│   ├── __init__.py
│   ├── devices.py            # Device endpoints
│   ├── sensors.py            # Sensor endpoints
│   ├── sensor_data.py        # Sensor data endpoints
│   ├── device_types.py       # Device type endpoints
│   └── analytics.py          # Analytics endpoints
├── crud/                      # Database operations
│   ├── __init__.py
│   ├── device_crud.py
│   ├── sensor_crud.py
│   ├── sensor_data_crud.py
│   ├── device_type_crud.py
│   └── analytics_crud.py
├── models/                    # Database models
│   ├── __init__.py
│   ├── database.py           # Database configuration
│   ├── device.py             # Device model
│   ├── sensor.py             # Sensor model
│   ├── sensor_data.py        # Sensor data model
│   └── device_type.py        # Device type model
├── schemas/                   # Pydantic schemas
│   ├── __init__.py
│   ├── device_schema.py
│   ├── sensor_schema.py
│   ├── sensor_data_schema.py
│   ├── device_type_schema.py
│   └── analytics_schema.py
├── main.py                   # FastAPI application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── alembic.ini              # Alembic configuration
└── README.md                # This file
```

## Requirements

- Python 3.11
- PostgreSQL 17

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd iot_device_management
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv # or if you have py launcher: py -3.11 -m venv venv
   venv\Scripts\activate  # On Linux: source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   - Create a database
   - Update the `.env` file with your database credentials

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   python start.py
   # or
   python main.py
   ```

## API Endpoints

Base URL
- http://{API_HOST}:{API_PORT}/{API_PREFIX}/api/v1

### Devices
- `GET /{API_PREFIX}/api/v1/devices` - List devices
- `POST /{API_PREFIX}/api/v1/devices` - Create device
- `GET /{API_PREFIX}/api/v1/devices/{device_id}` - Get device
- `PUT /{API_PREFIX}/api/v1/devices/{device_id}` - Update device
- `DELETE /{API_PREFIX}/api/v1/devices/{device_id}` - Delete device
- `PATCH /{API_PREFIX}/api/v1/devices/{device_id}/status?is_online=true|false` - Update status

Request body (device):
```json
{
  "name": "Living Room Sensor Hub",
  "description": "Main sensor hub",
  "location": "Living Room",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "is_active": true,
  "device_type_id": 1
}
```

### Sensors
- `GET /{API_PREFIX}/api/v1/sensors` - List sensors
- `POST /{API_PREFIX}/api/v1/sensors` - Create sensor
- `GET /{API_PREFIX}/api/v1/sensors/{sensor_id}` - Get sensor
- `PUT /{API_PREFIX}/api/v1/sensors/{sensor_id}` - Update sensor
- `DELETE /{API_PREFIX}/api/v1/sensors/{sensor_id}` - Delete sensor
- `PATCH /{API_PREFIX}/api/v1/sensors/{sensor_id}/status?is_online=true|false` - Update status

Request body (sensor):
```json
{
  "name": "Temperature Sensor 1",
  "sensor_id": "TEMP001",
  "sensor_type": "temperature",
  "unit": "°C",
  "min_value": -40,
  "max_value": 80,
  "is_active": true,
  "device_id": 1
}
```

### Sensor Data
- `POST /{API_PREFIX}/api/v1/sensor-data` - Create sensor data
- `GET /{API_PREFIX}/api/v1/sensor-data/sensor/{sensor_id}` - List sensor data
- `GET /{API_PREFIX}/api/v1/sensor-data/sensor/{sensor_id}/latest` - Latest reading
- `GET /{API_PREFIX}/api/v1/sensor-data/sensor/{sensor_id}/stats` - Statistics
- `GET /{API_PREFIX}/api/v1/sensor-data/temperature` - Temperature data
- `GET /{API_PREFIX}/api/v1/sensor-data/stats/overview` - Overview counts

Request body (sensor data):
```json
{
  "sensor_id": 1,
  "value": 22.5,
  "unit": "°C",
  "timestamp": "2025-10-05T12:00:00Z",
  "meta": null,
  "quality_score": 0.95
}
```

### Device Types
- `GET /{API_PREFIX}/api/v1/device-types` - List device types
- `POST /{API_PREFIX}/api/v1/device-types` - Create device type
- `GET /{API_PREFIX}/api/v1/device-types/{device_type_id}` - Get device type
- `PUT /{API_PREFIX}/api/v1/device-types/{device_type_id}` - Update device type
- `DELETE /{API_PREFIX}/api/v1/device-types/{device_type_id}` - Delete device type

Request body (device type):
```json
{
  "name": "Temperature Sensor",
  "description": "Digital temperature sensor",
  "manufacturer": "DHT22",
  "model": "DHT22",
  "is_active": true
}
```

### Analytics
- `GET /{API_PREFIX}/api/v1/analytics/overview` - Analytics overview
- `GET /{API_PREFIX}/api/v1/analytics/temperature` - Temperature analytics

## Database Schema

### Device Types
- Device type definitions (thermometer, humidity sensor, etc.)
- Manufacturer and model information

### Devices
- IoT device instances
- Location information (latitude/longitude)
- Online/offline status
- Device type relationships

### Sensors
- Individual sensors on devices
- Sensor types (temperature, humidity, pressure, etc.)
- Min/max value ranges
- Online/offline status

### Sensor Data
- Time-series sensor readings
- Value, unit, timestamp
- Data quality scores
- Metadata for additional information

## Usage Examples

### Create a Device Type
```bash
curl -X POST "http://localhost:9000/api/v1/device-types" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Temperature Sensor",
    "description": "Digital temperature sensor",
    "manufacturer": "DHT22",
    "model": "DHT22"
  }'
```

### Create a Device
```bash
curl -X POST "http://localhost:9000/api/v1/devices" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Living Room Sensor",
    "device_id": "LR001",
    "description": "Living room temperature sensor",
    "location": "Living Room",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "device_type_id": 1
  }'
```

### Create a Sensor
```bash
curl -X POST "http://localhost:9000/api/v1/sensors" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Temperature Sensor 1",
    "sensor_id": "TEMP001",
    "sensor_type": "temperature",
    "unit": "°C",
    "min_value": -40,
    "max_value": 80,
    "device_id": 1
  }'
```

### Submit Sensor Data
```bash
curl -X POST "http://localhost:9000/api/v1/sensor-data" \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": 1,
    "value": 22.5,
    "unit": "°C",
    "quality_score": 0.95
  }'
```

### Get Analytics
```bash
curl -X GET "http://localhost:9000/api/v1/analytics/overview"
```

## Configuration

The application uses environment variables for configuration. Update the `.env` file with your settings:

```bash
# API host and port
API_HOST=localhost
API_PORT=9000

# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=iot_manager
DB_USER=postgres
DB_PASS=your_password_here
DB_SCHEMA=iot_manager

# Security configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:9000/docs
- **ReDoc**: http://localhost:9000/redoc

## License

This project is licensed under the MIT License.
