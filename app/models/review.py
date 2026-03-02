from sqlalchemy import Column, String, Text, Boolean, JSON, ForeignKey
from app.db.session import Base

class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(String, primary_key=True)
    hospital_id = Column(String, ForeignKey("hospitals.hospital_id"))
    body = Column(Text)
    ai_reply_draft = Column(Text)
    is_approved = Column(Boolean, default=False)
    raw_data = Column(JSON)