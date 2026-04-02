from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.db.session import Base
from app.models.review import Platform, Sentiment


class Competitor(Base):
    """경쟁사 업체 정보"""
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(String, ForeignKey("stores.store_id"), nullable=False, index=True)

    name = Column(String, nullable=False)
    platform = Column(Enum(Platform), nullable=False)
    platform_place_id = Column(String, nullable=False)  # 구글 Place ID 또는 네이버 플레이스 ID
    address = Column(String)

    # 집계 캐시 (주기적으로 업데이트)
    avg_rating = Column(Float)
    total_reviews = Column(Integer, default=0)
    positive_keywords = Column(Text)  # JSON 배열
    negative_keywords = Column(Text)  # JSON 배열

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_collected_at = Column(DateTime(timezone=True))


class CompetitorReview(Base):
    """경쟁사 리뷰"""
    __tablename__ = "competitor_reviews"

    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"), nullable=False, index=True)

    platform = Column(Enum(Platform), nullable=False)
    platform_review_id = Column(String, index=True)  # 중복 방지

    author = Column(String)
    rating = Column(Float)
    content = Column(Text, nullable=False)
    visited_date = Column(String)

    sentiment = Column(Enum(Sentiment))
    keywords = Column(Text)  # JSON 배열

    created_at = Column(DateTime(timezone=True), server_default=func.now())
