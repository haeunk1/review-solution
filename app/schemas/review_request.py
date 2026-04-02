from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewRequestCreate(BaseModel):
    store_id: str
    title: str
    message: str
    target_platform: str


class ReviewRequestResponse(BaseModel):
    id: int
    store_id: str
    title: str
    message: str
    target_platform: str
    short_url: Optional[str] = None
    qr_code_url: Optional[str] = None
    click_count: int = 0
    review_count: int = 0
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewAlertResponse(BaseModel):
    id: int
    store_id: str
    review_id: int
    severity: str
    is_read: bool
    is_resolved: bool
    is_blacklist: bool
    suggested_reply: Optional[str] = None
    created_at: datetime

    # 리뷰 정보 (JOIN)
    author: Optional[str] = None
    rating: Optional[float] = None
    content: Optional[str] = None
    platform: Optional[str] = None
    review_date: Optional[str] = None

    class Config:
        from_attributes = True


class AlertStats(BaseModel):
    critical: int
    warning: int
    info: int
    unread: int


class MonthlyReportResponse(BaseModel):
    id: str
    store_id: str
    period: str
    total_reviews: int
    new_reviews: int
    avg_rating: float
    rating_change: float
    positive_rate: float
    negative_rate: float
    neutral_rate: float
    reply_rate: float
    top_positive_keywords: list[str]
    top_negative_keywords: list[str]
    platform_breakdown: list[dict]
    monthly_trend: list[dict]
    generated_at: str
    pdf_url: Optional[str] = None
