from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.api import deps
from app.models.review_request import ReviewAlert
from app.models.review import Review
from app.schemas.review_request import ReviewAlertResponse, AlertStats

router = APIRouter()


@router.get("/", response_model=list[ReviewAlertResponse])
def list_alerts(
    store_id: str = Query(...),
    severity: Optional[str] = Query(None),
    is_resolved: Optional[bool] = Query(None),
    db: Session = Depends(deps.get_db),
):
    """부정 리뷰 알림 목록 조회"""
    q = db.query(ReviewAlert, Review).join(
        Review, ReviewAlert.review_id == Review.id
    ).filter(ReviewAlert.store_id == store_id)

    if severity:
        q = q.filter(ReviewAlert.severity == severity)
    if is_resolved is not None:
        q = q.filter(ReviewAlert.is_resolved == is_resolved)

    results = q.order_by(ReviewAlert.created_at.desc()).all()

    alerts = []
    for alert, review in results:
        item = ReviewAlertResponse(
            id=alert.id,
            store_id=alert.store_id,
            review_id=alert.review_id,
            severity=alert.severity,
            is_read=alert.is_read,
            is_resolved=alert.is_resolved,
            is_blacklist=alert.is_blacklist,
            suggested_reply=alert.suggested_reply,
            created_at=alert.created_at,
            author=review.visitor_name,
            rating=float(review.rating) if review.rating else None,
            content=review.review_text,
            platform=review.platform.value if review.platform else None,
            review_date=review.created_at.strftime("%Y-%m-%d") if review.created_at else None,
        )
        alerts.append(item)
    return alerts


@router.get("/stats/{store_id}", response_model=AlertStats)
def get_alert_stats(store_id: str, db: Session = Depends(deps.get_db)):
    """알림 통계 (심각도별 카운트)"""
    base = db.query(ReviewAlert).filter(
        ReviewAlert.store_id == store_id,
        ReviewAlert.is_resolved == False,
    )
    return AlertStats(
        critical=base.filter(ReviewAlert.severity == "critical").count(),
        warning=base.filter(ReviewAlert.severity == "warning").count(),
        info=base.filter(ReviewAlert.severity == "info").count(),
        unread=db.query(ReviewAlert).filter(
            ReviewAlert.store_id == store_id,
            ReviewAlert.is_read == False,
        ).count(),
    )


@router.patch("/{alert_id}/read")
def mark_read(alert_id: int, db: Session = Depends(deps.get_db)):
    """알림 읽음 처리"""
    alert = db.query(ReviewAlert).filter(ReviewAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="알림을 찾을 수 없습니다.")
    alert.is_read = True
    db.commit()
    return {"status": "ok"}


@router.patch("/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(deps.get_db)):
    """알림 해결 처리"""
    alert = db.query(ReviewAlert).filter(ReviewAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="알림을 찾을 수 없습니다.")
    alert.is_resolved = True
    alert.is_read = True
    db.commit()
    return {"status": "resolved"}


@router.post("/{alert_id}/generate-reply")
async def generate_crisis_reply(
    alert_id: int,
    payload: dict,
    db: Session = Depends(deps.get_db),
):
    """AI 위기 대응 답글 생성"""
    from app.services.reply_service import reply_service

    alert = db.query(ReviewAlert).filter(ReviewAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="알림을 찾을 수 없습니다.")

    review = db.query(Review).filter(Review.id == alert.review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

    style = payload.get("style", "formal")
    reply_text = await reply_service.generate_reply(review.review_text, style=style)

    alert.suggested_reply = reply_text
    db.commit()
    return {"reply_text": reply_text}


@router.post("/{alert_id}/blacklist")
def report_blacklist(
    alert_id: int,
    payload: dict,
    db: Session = Depends(deps.get_db),
):
    """블랙컨슈머 신고"""
    alert = db.query(ReviewAlert).filter(ReviewAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="알림을 찾을 수 없습니다.")
    alert.is_blacklist = True
    db.commit()
    return {"status": "reported", "reason": payload.get("reason", "")}
