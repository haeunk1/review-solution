from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.api import deps
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate, HospitalResponse

router = APIRouter()


class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    naver_place_id: Optional[str] = None
    google_place_id: Optional[str] = None
    gangnamunni_id: Optional[str] = None
    crawl_interval_hours: Optional[int] = None
    is_active: Optional[bool] = None


@router.post("/", response_model=HospitalResponse)
def create_hospital(hospital_in: HospitalCreate, db: Session = Depends(deps.get_db)):
    db_hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_in.hospital_id).first()
    if db_hospital:
        raise HTTPException(status_code=400, detail="이미 등록된 병원 ID입니다.")
    new_hospital = Hospital(**hospital_in.model_dump())
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)
    return new_hospital


@router.get("/", response_model=list[HospitalResponse])
def get_hospitals(db: Session = Depends(deps.get_db)):
    return db.query(Hospital).all()


@router.get("/info/{hospital_id}", response_model=HospitalResponse)
def get_hospital(hospital_id: str, db: Session = Depends(deps.get_db)):
    hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="등록되지 않은 병원입니다.")
    return hospital


@router.patch("/{hospital_id}", response_model=HospitalResponse)
def update_hospital(hospital_id: str, hospital_in: HospitalUpdate, db: Session = Depends(deps.get_db)):
    hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="병원을 찾을 수 없습니다.")
    for field, value in hospital_in.model_dump(exclude_none=True).items():
        setattr(hospital, field, value)
    db.commit()
    db.refresh(hospital)
    return hospital
