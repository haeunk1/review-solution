from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate, HospitalResponse

router = APIRouter()

# 병원 등록 (POST)
@router.post("/", response_model=HospitalResponse)
def create_hospital(hospital_in: HospitalCreate, db: Session = Depends(deps.get_db)):
    # 중복 체크
    db_hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_in.hospital_id).first()
    if db_hospital:
        raise HTTPException(status_code=400, detail="이미 등록된 병원 ID입니다.")
    
    # 데이터 삽입 (Save)
    new_hospital = Hospital(**hospital_in.model_dump())
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital) # 저장된 후 자동 생성된 값(날짜 등)을 반영
    return new_hospital

# 병원 목록 조회 (GET)
@router.get("/", response_model=list[HospitalResponse])
def get_hospitals(db: Session = Depends(deps.get_db)):
    return db.query(Hospital).all()
