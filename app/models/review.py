from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from app.db.session import Base
from sqlalchemy.sql import func

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(String, ForeignKey("hospitals.hospital_id")) # 외래키
    review_text = Column(Text, nullable=False) # 리뷰 내용
    rating = Column(String) # 별점 또는 '좋아요'
    visitor_name = Column(String) # 방문자명
    visited_date = Column(String) # 방문일
    created_at = Column(DateTime(timezone=True), server_default=func.now())