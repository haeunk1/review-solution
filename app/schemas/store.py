from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StoreCreate(BaseModel):
    store_id: str
    name: str
    business_type: Optional[str] = None
    tenant_id: Optional[str] = None
    naver_place_id: Optional[str] = None
    google_place_id: Optional[str] = None
    crawl_interval_hours: Optional[int] = 6


class StoreResponse(BaseModel):
    store_id: str
    name: str
    business_type: Optional[str]
    tenant_id: Optional[str]
    naver_place_id: Optional[str]
    google_place_id: Optional[str]
    crawl_interval_hours: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
