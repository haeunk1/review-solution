from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.api import deps
from app.models.review import Review, ReplyStyle, ReplyStatus
from app.services.reply_service import generate_reply

router = APIRouter()


class ReplyGenerateRequest(BaseModel):
    style: Optional[str] = None  # formal | friendly | positive


class ReplySubmitRequest(BaseModel):
    reply_text: str


@router.post("/generate/{review_id}")
async def generate_review_reply(
    review_id: int,
    body: ReplyGenerateRequest = ReplyGenerateRequest(),
    db: Session = Depends(deps.get_db),
):
    """특정 리뷰에 대한 AI 답글 생성"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

    style: Optional[ReplyStyle] = None
    if body.style:
        try:
            style = ReplyStyle(body.style)
        except ValueError:
            raise HTTPException(status_code=400, detail="유효하지 않은 스타일입니다.")

    reply_text = generate_reply(
        review_text=review.review_text,
        visitor_name=review.visitor_name,
        sentiment=review.sentiment,
        style=style,
    )
    return {"reply_text": reply_text}


@router.post("/submit/{review_id}")
def submit_review_reply(
    review_id: int,
    body: ReplySubmitRequest,
    db: Session = Depends(deps.get_db),
):
    """사용자가 확인/수정한 답글을 저장 (approved 상태로 변경)"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

    review.reply_text = body.reply_text
    review.reply_status = ReplyStatus.approved
    db.commit()
    return {"status": "success", "message": "답글이 등록되었습니다."}
