from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.api import deps
from app.models.hospital import Hospital
from app.models.review import Review
from app.schemas.reviews import ReviewResponse
from app.services.scraper_service import scraper_service
from app.services.scheduler_service import collect_reviews_for_hospital

router = APIRouter()


@router.get("/", response_model=list[ReviewResponse])
def read_reviews(
    hospital_id: Optional[str] = Query(None),
    platform: Optional[str] = Query(None),
    reply_status: Optional[str] = Query(None),
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
):
    q = db.query(Review)
    if hospital_id:
        q = q.filter(Review.hospital_id == hospital_id)
    if platform:
        q = q.filter(Review.platform == platform)
    if reply_status:
        q = q.filter(Review.reply_status == reply_status)
    return q.order_by(Review.created_at.desc()).all()


@router.post("/collect/{hospital_id}")
async def collect_hospital_reviews(
    hospital_id: str,
    db: Session = Depends(deps.get_db),
):
    """특정 병원의 리뷰를 즉시 수집 (수동 트리거)"""
    hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="등록되지 않은 병원입니다.")

    await collect_reviews_for_hospital(hospital_id)
    return {"status": "success", "message": f"{hospital.name} 리뷰 수집 완료"}
