from pydantic import BaseModel
from datetime import datetime

# 생성할 때 받는 데이터 (Request Body)
class HospitalCreate(BaseModel):
    hospital_id: str
    name: str
    category: str | None = None

# 결과로 돌려줄 때 데이터 (Response Body)
class HospitalResponse(BaseModel):
    hospital_id: str
    name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True # SQLAlchemy 객체를 자동으로 DTO로 변환