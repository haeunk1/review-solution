from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base

class Hospital(Base):
    __tablename__ = "hospitals"

    hospital_id = Column(String, primary_key=True, index=True)  # 내부 고유 ID
    tenant_id = Column(String, index=True)  # SaaS 멀티테넌시용 (클리닉 구분)

    name = Column(String, nullable=False)
    category = Column(String)  # 피부과, 성형외과 등
    is_active = Column(Boolean, default=True)

    # 플랫폼별 고유 ID
    naver_place_id = Column(String)       # 네이버 플레이스 ID
    google_place_id = Column(String)      # 구글 맵 Place ID
    gangnamunni_id = Column(String)       # 강남언니 병원 ID

    # 크롤링 주기 설정 (시간 단위: 1, 3, 6, 24)
    crawl_interval_hours = Column(Integer, default=6)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
