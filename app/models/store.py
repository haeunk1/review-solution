from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from app.db.session import Base


class Store(Base):
    __tablename__ = "stores"

    store_id = Column(String, primary_key=True, index=True)  # 내부 고유 ID
    tenant_id = Column(String, index=True)  # SaaS 멀티테넌시용

    name = Column(String, nullable=False)
    business_type = Column(String)  # 음식점, 카페, 병원, 뷰티 등

    is_active = Column(Boolean, default=True)

    # 플랫폼별 고유 ID
    naver_place_id = Column(String)   # 네이버 플레이스 ID
    google_place_id = Column(String)  # 구글 맵 Place ID

    # 크롤링 주기 설정 (시간 단위: 1, 3, 6, 24)
    crawl_interval_hours = Column(Integer, default=6)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
