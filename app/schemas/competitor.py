from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CompetitorCreate(BaseModel):
    store_id: str
    name: str
    platform: str
    platform_place_id: str
    address: Optional[str] = None


class CompetitorReviewResponse(BaseModel):
    id: int
    competitor_id: int
    platform: str
    author: Optional[str] = None
    rating: Optional[float] = None
    content: str
    visited_date: Optional[str] = None
    sentiment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CompetitorResponse(BaseModel):
    id: int
    store_id: str
    name: str
    platform: str
    platform_place_id: str
    address: Optional[str] = None
    avg_rating: Optional[float] = None
    total_reviews: Optional[int] = 0
    positive_keywords: Optional[str] = None   # JSON 문자열
    negative_keywords: Optional[str] = None   # JSON 문자열
    created_at: datetime
    last_collected_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompetitorMyStore(BaseModel):
    name: str
    avg_rating: float
    total_reviews: int
    positive_rate: float
    top_keywords: List[str]


class CompetitorComparisonItem(BaseModel):
    name: str
    avg_rating: float
    total_reviews: int
    positive_rate: float
    top_keywords: List[str]


class CompetitorComparison(BaseModel):
    my_store: CompetitorMyStore
    competitors: List[CompetitorComparisonItem]
