from typing import Generator
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from fastapi import  Depends

# 1. DB 세션 주입용
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db  # API 컨트롤러에서 이 db 객체를 사용하게 됨
    finally:
        db.close() # API 응답이 끝나면 자동으로 DB 연결을 해제 (Spring의 Open Session In View와 유사)

# 2. 현재 사용자 주입용 (임시 Mock 버전)
def get_current_user(db: Session = Depends(get_db)):
    mock_user = {
        "id":1,
        "username":"admin",
        "email":"admin@example.com",
        "is_active":True
    }
    return mock_user
