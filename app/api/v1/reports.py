from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from typing import Optional
from app.api import deps
from app.models.review import Review, Sentiment, Platform
from app.models.store import Store
from app.schemas.review_request import MonthlyReportResponse

router = APIRouter()


def _build_report(store_id: str, period: str, db: Session) -> MonthlyReportResponse:
    """period: '2026-03' 형식"""
    year, month = period.split("-")
    year_i, month_i = int(year), int(month)

    # 해당 월 리뷰
    reviews = (
        db.query(Review)
        .filter(
            Review.store_id == store_id,
            extract("year", Review.created_at) == year_i,
            extract("month", Review.created_at) == month_i,
        )
        .all()
    )

    total = len(reviews)
    if total == 0:
        raise HTTPException(status_code=404, detail=f"{period} 리뷰 데이터가 없습니다.")

    # 이전 달 평균 평점
    prev_month = month_i - 1 if month_i > 1 else 12
    prev_year = year_i if month_i > 1 else year_i - 1
    prev_reviews = (
        db.query(Review)
        .filter(
            Review.store_id == store_id,
            extract("year", Review.created_at) == prev_year,
            extract("month", Review.created_at) == prev_month,
        )
        .all()
    )
    prev_avg = sum(float(r.rating) for r in prev_reviews if r.rating) / max(len(prev_reviews), 1)
    cur_avg = sum(float(r.rating) for r in reviews if r.rating) / max(total, 1)

    # 감성 분포
    pos = sum(1 for r in reviews if r.sentiment == Sentiment.positive)
    neg = sum(1 for r in reviews if r.sentiment == Sentiment.negative)
    neu = total - pos - neg
    pos_pct = round(pos / total * 100)
    neg_pct = round(neg / total * 100)
    neu_pct = 100 - pos_pct - neg_pct

    # 답변율
    replied = sum(1 for r in reviews if r.reply_text)
    reply_rate = round(replied / total * 100)

    # 플랫폼 분포
    platform_counts: dict = {}
    platform_ratings: dict = {}
    for r in reviews:
        p = r.platform.value if r.platform else "unknown"
        platform_counts[p] = platform_counts.get(p, 0) + 1
        if r.rating:
            platform_ratings.setdefault(p, []).append(float(r.rating))

    platform_breakdown = []
    for p, cnt in platform_counts.items():
        ratings = platform_ratings.get(p, [])
        avg_r = sum(ratings) / len(ratings) if ratings else 0.0
        platform_breakdown.append({
            "platform": p,
            "count": cnt,
            "avg_rating": round(avg_r, 2),
            "percentage": round(cnt / total * 100),
        })

    # 월별 트렌드 (최근 6개월)
    monthly_trend = []
    for i in range(5, -1, -1):
        m = month_i - i
        y = year_i
        while m <= 0:
            m += 12
            y -= 1
        month_str = f"{y:04d}-{m:02d}"
        month_reviews = [
            r for r in db.query(Review).filter(
                Review.store_id == store_id,
                extract("year", Review.created_at) == y,
                extract("month", Review.created_at) == m,
            ).all()
        ]
        cnt = len(month_reviews)
        avg_r = sum(float(r.rating) for r in month_reviews if r.rating) / max(cnt, 1)
        monthly_trend.append({"month": month_str, "count": cnt, "avg_rating": round(avg_r, 2)})

    # 키워드 (분석된 리뷰에서 추출)
    import json, collections
    pos_kw_all: list[str] = []
    neg_kw_all: list[str] = []
    for r in reviews:
        if r.keywords:
            try:
                kws = json.loads(r.keywords)
                if r.sentiment == Sentiment.positive:
                    pos_kw_all.extend(kws)
                elif r.sentiment == Sentiment.negative:
                    neg_kw_all.extend(kws)
            except Exception:
                pass

    top_pos = [kw for kw, _ in collections.Counter(pos_kw_all).most_common(10)]
    top_neg = [kw for kw, _ in collections.Counter(neg_kw_all).most_common(5)]

    return MonthlyReportResponse(
        id=f"{store_id}-{period}",
        store_id=store_id,
        period=period,
        total_reviews=db.query(Review).filter(Review.store_id == store_id).count(),
        new_reviews=total,
        avg_rating=round(cur_avg, 2),
        rating_change=round(cur_avg - prev_avg, 2),
        positive_rate=pos_pct,
        negative_rate=neg_pct,
        neutral_rate=neu_pct,
        reply_rate=reply_rate,
        top_positive_keywords=top_pos,
        top_negative_keywords=top_neg,
        platform_breakdown=platform_breakdown,
        monthly_trend=monthly_trend,
        generated_at=datetime.now().strftime("%Y-%m-%d"),
    )


@router.get("/", response_model=list[MonthlyReportResponse])
def list_reports(
    store_id: str = Query(...),
    db: Session = Depends(deps.get_db),
):
    """최근 6개월 리포트 목록"""
    now = datetime.now()
    reports = []
    for i in range(6):
        m = now.month - i
        y = now.year
        while m <= 0:
            m += 12
            y -= 1
        period = f"{y:04d}-{m:02d}"
        try:
            reports.append(_build_report(store_id, period, db))
        except HTTPException:
            pass
    return reports


@router.get("/latest/{store_id}", response_model=MonthlyReportResponse)
def latest_report(store_id: str, db: Session = Depends(deps.get_db)):
    now = datetime.now()
    period = f"{now.year:04d}-{now.month:02d}"
    return _build_report(store_id, period, db)


@router.get("/{store_id}/{period}", response_model=MonthlyReportResponse)
def get_report(store_id: str, period: str, db: Session = Depends(deps.get_db)):
    """특정 월 리포트 조회"""
    return _build_report(store_id, period, db)


@router.post("/generate", response_model=MonthlyReportResponse)
def generate_report(payload: dict, db: Session = Depends(deps.get_db)):
    """리포트 생성 (AI 분석 후 반환)"""
    store_id = payload.get("store_id")
    period = payload.get("period")
    if not store_id or not period:
        raise HTTPException(status_code=400, detail="store_id와 period가 필요합니다.")
    return _build_report(store_id, period, db)


@router.get("/{report_id}/pdf")
def get_pdf_url(report_id: str):
    """PDF 다운로드 URL 발급 — 실제 구현 시 S3 presigned URL 사용"""
    return {
        "pdf_url": f"https://storage.reviewhub.kr/reports/{report_id}.pdf",
        "expires_at": "2026-12-31T23:59:59Z",
    }
