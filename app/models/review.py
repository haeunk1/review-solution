from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Enum
from app.db.session import Base
from sqlalchemy.sql import func
import enum

class Platform(str, enum.Enum):
    naver = "naver"
    google = "google"
    gangnamunni = "gangnamunni"

class Sentiment(str, enum.Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class ReplyStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    posted = "posted"

class ReplyStyle(str, enum.Enum):
    formal = "formal"       # 정중한/공식적
    friendly = "friendly"   # 친근한/따뜻한
    positive = "positive"   # 긍정적/지지하는

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(String, ForeignKey("hospitals.hospital_id"), nullable=False, index=True)

    # 플랫폼 정보
    platform = Column(Enum(Platform), nullable=False, default=Platform.naver)
    platform_review_id = Column(String, index=True)  # 플랫폼별 고유 ID (중복 방지)

    # 리뷰 내용
    review_text = Column(Text, nullable=False)
    rating = Column(String)
    visitor_name = Column(String)
    visited_date = Column(String)

    # AI 분석 결과
    sentiment = Column(Enum(Sentiment))
    keywords = Column(Text)  # JSON 문자열로 저장 (["키워드1", "키워드2"])

    # AI 답글
    reply_text = Column(Text)
    reply_status = Column(Enum(ReplyStatus), default=ReplyStatus.pending)
    reply_style = Column(Enum(ReplyStyle))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
