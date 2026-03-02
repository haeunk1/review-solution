from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.review import Review
from app.schemas.reviews import ReviewResponse

router = APIRouter()

@router.get("/", response_model=list[ReviewResponse])
def read_reviews(db: Session = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    # 스프링의 Service.findAll() 호출과 유사
    reviews = db.query(Review).all()
    return reviews