from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.review import Platform, Sentiment, ReplyStatus, ReplyStyle


class ReviewResponse(BaseModel):
    id: int
    hospital_id: str
    platform: Platform
    platform_review_id: Optional[str]
    review_text: str
    rating: Optional[str]
    visitor_name: Optional[str]
    visited_date: Optional[str]
    sentiment: Optional[Sentiment]
    keywords: Optional[str]
    reply_text: Optional[str]
    reply_status: Optional[ReplyStatus]
    reply_style: Optional[ReplyStyle]
    created_at: datetime

    class Config:
        from_attributes = True
