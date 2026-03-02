from pydantic import BaseModel
from datetime import datetime

# 생성할 때 받는 데이터 (Request Body)
class ReviewCreate(BaseModel):
    review_id: str
    hospital_id: str
    body: str

# 결과로 돌려줄 때 데이터 (Response Body)
class ReviewResponse(BaseModel):
    review_id: str
    hospital_id: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True # SQLAlchemy 객체를 자동으로 DTO로 변환