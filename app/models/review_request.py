from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from app.db.session import Base
from app.models.review import Platform


class ReviewRequest(Base):
    """리뷰 요청 캠페인 (QR 코드 / 단축 URL)"""
    __tablename__ = "review_requests"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(String, ForeignKey("stores.store_id"), nullable=False, index=True)

    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    target_platform = Column(Enum(Platform), nullable=False)

    short_url = Column(String, unique=True)   # 단축 URL 코드 (예: rvhub.kr/abc12)
    qr_code_url = Column(String)              # QR 이미지 저장 경로 (S3 등)

    # 전환 통계
    click_count = Column(Integer, default=0)
    review_count = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ReviewAlert(Base):
    """부정 리뷰 위기 알림"""
    __tablename__ = "review_alerts"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(String, ForeignKey("stores.store_id"), nullable=False, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False)

    severity = Column(String, nullable=False)  # critical(1점) / warning(2점) / info(3점)
    is_read = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    is_blacklist = Column(Boolean, default=False)

    # AI 생성 위기 대응 답글
    suggested_reply = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
