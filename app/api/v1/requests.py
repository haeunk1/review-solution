import random
import string
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.models.review_request import ReviewRequest
from app.schemas.review_request import ReviewRequestCreate, ReviewRequestResponse

router = APIRouter()


def _generate_short_code(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


@router.get("/", response_model=list[ReviewRequestResponse])
def list_requests(
    store_id: str = Query(...),
    db: Session = Depends(deps.get_db),
):
    return (
        db.query(ReviewRequest)
        .filter(ReviewRequest.store_id == store_id, ReviewRequest.is_active == True)
        .order_by(ReviewRequest.created_at.desc())
        .all()
    )


@router.post("/", response_model=ReviewRequestResponse)
def create_request(
    data: ReviewRequestCreate,
    db: Session = Depends(deps.get_db),
):
    # 단축 URL 코드 생성 (중복 방지)
    for _ in range(5):
        code = _generate_short_code()
        if not db.query(ReviewRequest).filter(ReviewRequest.short_url == code).first():
            break

    req = ReviewRequest(
        store_id=data.store_id,
        title=data.title,
        message=data.message,
        target_platform=data.target_platform,
        short_url=code,
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


@router.delete("/{request_id}")
def delete_request(request_id: int, db: Session = Depends(deps.get_db)):
    req = db.query(ReviewRequest).filter(ReviewRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다.")
    req.is_active = False
    db.commit()
    return {"status": "deleted"}


@router.get("/{request_id}/qr")
def get_qr(request_id: int, db: Session = Depends(deps.get_db)):
    req = db.query(ReviewRequest).filter(ReviewRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다.")
    # TODO: QR 이미지 생성 서비스 연동 (qrcode 라이브러리)
    qr_url = req.qr_code_url or f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://rvhub.kr/{req.short_url}"
    return {"qr_url": qr_url}


@router.post("/{request_id}/regenerate-url")
def regenerate_url(request_id: int, db: Session = Depends(deps.get_db)):
    req = db.query(ReviewRequest).filter(ReviewRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다.")
    req.short_url = _generate_short_code()
    db.commit()
    return {"short_url": req.short_url}


@router.post("/{request_id}/send-sms")
def send_sms(request_id: int, payload: dict, db: Session = Depends(deps.get_db)):
    """SMS / 카카오 알림톡 발송 — 외부 API 연동 예정"""
    req = db.query(ReviewRequest).filter(ReviewRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다.")
    phones = payload.get("phones", [])
    # TODO: 카카오 알림톡 API 또는 SMS 게이트웨이 연동
    return {"status": "queued", "count": len(phones)}


@router.get("/{request_id}/stats")
def get_stats(request_id: int, db: Session = Depends(deps.get_db)):
    req = db.query(ReviewRequest).filter(ReviewRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="캠페인을 찾을 수 없습니다.")
    return {
        "clicks": req.click_count,
        "reviews": req.review_count,
        "conversion_rate": round(req.review_count / max(req.click_count, 1) * 100, 1),
    }
