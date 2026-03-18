from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.hospital import Hospital
from app.services.analysis_service import analyze_reviews_batch, get_analysis_summary

router = APIRouter()


@router.get("/summary/{hospital_id}")
def get_summary(hospital_id: str, db: Session = Depends(deps.get_db)):
    """병원 리뷰 분석 통계 요약"""
    hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="등록되지 않은 병원입니다.")
    return get_analysis_summary(hospital_id, db)


@router.post("/run/{hospital_id}")
async def run_analysis(hospital_id: str, db: Session = Depends(deps.get_db)):
    """미분석 리뷰 AI 분석 실행"""
    hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="등록되지 않은 병원입니다.")
    count = await analyze_reviews_batch(hospital_id, db)
    return {"analyzed_count": count, "message": f"{count}건 분석 완료"}
