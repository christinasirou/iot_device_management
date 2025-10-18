from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models.database import engine, get_db
from models import Base
from api import api_router
from config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IoT Device Management API",
    description="A comprehensive FastAPI microservice for managing IoT devices, sensors, and data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes with configurable prefix
app.include_router(api_router, prefix=f"/{settings.api_prefix}/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
