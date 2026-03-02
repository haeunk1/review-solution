from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class Hospital(Base):
    __tablename__ = "hospitals"

    hospital_id = Column(String, primary_key=True, index=True) # 네이버 ID
    name = Column(String, nullable=False)
    category = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())