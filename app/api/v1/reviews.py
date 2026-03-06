from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.review import Review
from app.schemas.reviews import ReviewResponse
from app.services.scraper_service import scraper_service

router = APIRouter()

@router.get("/", response_model=list[ReviewResponse])
def read_reviews(db: Session = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    # 스프링의 Service.findAll() 호출과 유사
    reviews = db.query(Review).all()
    return reviews


@router.post("/collect/{hospital_id}")
async def collect_hospital_reviews(hospital_id: str, db: Session = Depends(deps.get_db)):
    # 1. 크롤링 시작
    reviews_data = await scraper_service.get_naver_reviews(hospital_id)
    
    if not reviews_data:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없거나 수집에 실패했습니다.")

    # 2. DB 저장 (Bulk Insert 방식이 좋지만 일단 하나씩)
    for data in reviews_data:
        db_review = Review(**data) # 딕셔너리를 모델 객체로 변환
        db.add(db_review)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB 저장 오류: {str(e)}")

    return {"status": "success", "collected_count": len(reviews_data)}