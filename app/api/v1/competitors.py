from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import json
from app.api import deps
from app.models.competitor import Competitor, CompetitorReview
from app.models.review import Review, Sentiment
from app.models.store import Store
from app.schemas.competitor import (
    CompetitorCreate, CompetitorResponse, CompetitorReviewResponse,
    CompetitorComparison, CompetitorMyStore, CompetitorComparisonItem,
)

router = APIRouter()


@router.get("/", response_model=list[CompetitorResponse])
def list_competitors(
    store_id: str = Query(...),
    db: Session = Depends(deps.get_db),
):
    return db.query(Competitor).filter(Competitor.store_id == store_id).all()


@router.post("/", response_model=CompetitorResponse)
def create_competitor(
    data: CompetitorCreate,
    db: Session = Depends(deps.get_db),
):
    # 중복 체크
    existing = db.query(Competitor).filter(
        Competitor.store_id == data.store_id,
        Competitor.platform == data.platform,
        Competitor.platform_place_id == data.platform_place_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 경쟁사입니다.")

    comp = Competitor(**data.model_dump())
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp


@router.delete("/{competitor_id}")
def remove_competitor(competitor_id: int, db: Session = Depends(deps.get_db)):
    comp = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="경쟁사를 찾을 수 없습니다.")
    db.delete(comp)
    db.commit()
    return {"status": "deleted"}


@router.get("/{competitor_id}/reviews", response_model=list[CompetitorReviewResponse])
def get_competitor_reviews(
    competitor_id: int,
    limit: int = Query(10),
    db: Session = Depends(deps.get_db),
):
    return (
        db.query(CompetitorReview)
        .filter(CompetitorReview.competitor_id == competitor_id)
        .order_by(CompetitorReview.created_at.desc())
        .limit(limit)
        .all()
    )


@router.post("/{competitor_id}/collect")
async def collect_competitor(competitor_id: int, db: Session = Depends(deps.get_db)):
    """경쟁사 리뷰 수집 (수동 트리거) — 스크래퍼 구현 예정"""
    comp = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="경쟁사를 찾을 수 없습니다.")
    # TODO: 스크래퍼 연동
    return {"status": "queued", "competitor": comp.name}


@router.post("/collect-all/{store_id}")
async def collect_all_competitors(store_id: str, db: Session = Depends(deps.get_db)):
    """모든 경쟁사 리뷰 일괄 수집"""
    competitors = db.query(Competitor).filter(Competitor.store_id == store_id).all()
    return {"status": "queued", "count": len(competitors)}


@router.get("/comparison/{store_id}", response_model=CompetitorComparison)
def get_comparison(store_id: str, db: Session = Depends(deps.get_db)):
    """내 업장 vs 경쟁사 비교 분석"""
    store = db.query(Store).filter(Store.store_id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="업장을 찾을 수 없습니다.")

    # 내 업장 통계
    my_reviews = db.query(Review).filter(Review.store_id == store_id).all()
    my_total = len(my_reviews)
    my_avg_rating = sum(float(r.rating) for r in my_reviews if r.rating) / max(my_total, 1)
    my_positive = sum(1 for r in my_reviews if r.sentiment == Sentiment.positive)
    my_positive_rate = round(my_positive / max(my_total, 1) * 100, 1)

    my_store_data = CompetitorMyStore(
        name=store.name,
        avg_rating=round(my_avg_rating, 2),
        total_reviews=my_total,
        positive_rate=my_positive_rate,
        top_keywords=[],
    )

    # 경쟁사 통계
    competitors = db.query(Competitor).filter(Competitor.store_id == store_id).all()
    comp_items = []
    for comp in competitors:
        kws = json.loads(comp.positive_keywords or "[]")
        comp_items.append(CompetitorComparisonItem(
            name=comp.name,
            avg_rating=comp.avg_rating or 0.0,
            total_reviews=comp.total_reviews or 0,
            positive_rate=0.0,
            top_keywords=kws[:5],
        ))

    return CompetitorComparison(my_store=my_store_data, competitors=comp_items)
