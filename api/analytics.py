from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from models.database import get_db
from crud.analytics_crud import analytics_crud
from schemas.analytics_schema import AnalyticsResponse, TemperatureStats

router = APIRouter()


@router.get("/overview", response_model=AnalyticsResponse)
def get_analytics_overview(db: Session = Depends(get_db)):
    """Get comprehensive analytics overview"""
    return analytics_crud.get_analytics(db)


@router.get("/temperature", response_model=List[TemperatureStats])
def get_temperature_analytics(
    device_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get temperature analytics for all or specific device"""
    return analytics_crud.get_temperature_analytics(db, device_id)
