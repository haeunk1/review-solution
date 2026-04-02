from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.api import deps
from app.models.store import Store
from app.models.review import Review
from app.schemas.reviews import ReviewResponse
from app.services.scraper_service import scraper_service
from app.services.scheduler_service import collect_reviews_for_store

router = APIRouter()


@router.get("/", response_model=list[ReviewResponse])
def read_reviews(
    store_id: Optional[str] = Query(None),
    platform: Optional[str] = Query(None),
    reply_status: Optional[str] = Query(None),
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_user),
):
    q = db.query(Review)
    if store_id:
        q = q.filter(Review.store_id == store_id)
    if platform:
        q = q.filter(Review.platform == platform)
    if reply_status:
        q = q.filter(Review.reply_status == reply_status)
    return q.order_by(Review.created_at.desc()).all()


@router.post("/collect/{store_id}")
async def collect_store_reviews(
    store_id: str,
    db: Session = Depends(deps.get_db),
):
    """특정 업장의 리뷰를 즉시 수집 (수동 트리거)"""
    store = db.query(Store).filter(Store.store_id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="등록되지 않은 업장입니다.")

    await collect_reviews_for_store(store_id)
    return {"status": "success", "message": f"{store.name} 리뷰 수집 완료"}
