from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.store import Store
from app.services.analysis_service import analyze_reviews_batch, get_analysis_summary

router = APIRouter()


@router.get("/summary/{store_id}")
def get_summary(store_id: str, db: Session = Depends(deps.get_db)):
    """업장 리뷰 분석 통계 요약"""
    store = db.query(Store).filter(Store.store_id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="등록되지 않은 업장입니다.")
    return get_analysis_summary(store_id, db)


@router.post("/run/{store_id}")
async def run_analysis(store_id: str, db: Session = Depends(deps.get_db)):
    """미분석 리뷰 AI 분석 실행"""
    store = db.query(Store).filter(Store.store_id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="등록되지 않은 업장입니다.")
    count = await analyze_reviews_batch(store_id, db)
    return {"analyzed_count": count, "message": f"{count}건 분석 완료"}
