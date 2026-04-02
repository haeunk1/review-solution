import json
import google.generativeai as genai
from collections import Counter
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.models.review import Review, Sentiment

GEMINI_MODEL = "gemini-2.0-flash-lite"


def _get_model() -> genai.GenerativeModel:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return genai.GenerativeModel(GEMINI_MODEL)


async def analyze_reviews_batch(store_id: str, db: Session) -> int:
    """미분석 리뷰를 Gemini API로 배치 분석하여 DB에 저장. 분석된 건수 반환."""
    unanalyzed = (
        db.query(Review)
        .filter(Review.store_id == store_id, Review.sentiment.is_(None))
        .all()
    )
    if not unanalyzed:
        return 0

    model = _get_model()
    updated = 0
    batch_size = 5

    for i in range(0, len(unanalyzed), batch_size):
        batch = unanalyzed[i : i + batch_size]
        numbered = "\n".join(
            f"{j+1}. {r.review_text[:300]}" for j, r in enumerate(batch)
        )
        prompt = f"""다음은 업장(음식점, 카페, 병원 등) 리뷰들입니다. 각 리뷰를 분석해서 JSON 배열로 반환해줘.

리뷰:
{numbered}

각 항목 형식:
{{
  "sentiment": "positive" | "negative" | "neutral",
  "keywords": ["키워드1", "키워드2", "키워드3"]
}}

반드시 리뷰 순서대로 {len(batch)}개의 JSON 객체 배열만 반환해줘. 마크다운 없이 JSON만."""

        response = model.generate_content(prompt)
        raw = response.text.strip()

        # JSON 배열 추출 (마크다운 코드블록 대응)
        start, end = raw.find("["), raw.rfind("]") + 1
        if start == -1 or end == 0:
            raise ValueError(f"Gemini 응답에서 JSON 배열을 찾을 수 없습니다: {raw[:200]}")
        results = json.loads(raw[start:end])

        for review, result in zip(batch, results):
            sentiment_val = result.get("sentiment", "neutral")
            try:
                review.sentiment = Sentiment(sentiment_val)
            except ValueError:
                review.sentiment = Sentiment.neutral
            review.keywords = json.dumps(result.get("keywords", []), ensure_ascii=False)
            updated += 1

        db.commit()

    return updated


def get_analysis_summary(store_id: str, db: Session) -> dict:
    """병원의 분석 통계 요약 반환."""
    reviews = db.query(Review).filter(Review.store_id == store_id).all()
    if not reviews:
        return _empty_summary()

    total = len(reviews)
    analyzed = [r for r in reviews if r.sentiment is not None]
    replied = [r for r in reviews if r.reply_text is not None]
    pending = [r for r in reviews if r.reply_text is None]

    # 감성 분포
    sentiment_counts = Counter(r.sentiment for r in analyzed)
    pos = sentiment_counts.get(Sentiment.positive, 0)
    neg = sentiment_counts.get(Sentiment.negative, 0)
    neu = sentiment_counts.get(Sentiment.neutral, 0)
    analyzed_total = len(analyzed)

    def pct(n: int) -> float:
        return round(n / analyzed_total * 100, 1) if analyzed_total else 0.0

    # 키워드 빈도 (감성별 분리)
    pos_kw: Counter = Counter()
    neg_kw: Counter = Counter()
    for r in analyzed:
        if not r.keywords:
            continue
        try:
            kws = json.loads(r.keywords)
        except Exception:
            continue
        if r.sentiment == Sentiment.positive:
            pos_kw.update(kws)
        elif r.sentiment == Sentiment.negative:
            neg_kw.update(kws)

    # 월별 트렌드 (최근 6개월)
    six_months_ago = datetime.now(timezone.utc) - timedelta(days=180)
    monthly: dict[str, int] = {}
    for r in reviews:
        if not r.created_at:
            continue
        created = r.created_at
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        if created >= six_months_ago:
            key = created.strftime("%Y-%m")
            monthly[key] = monthly.get(key, 0) + 1

    trend = [{"month": k, "count": v} for k, v in sorted(monthly.items())]

    return {
        "total_reviews": total,
        "analyzed_count": analyzed_total,
        "reply_rate": round(len(replied) / total * 100, 1) if total else 0.0,
        "pending_count": len(pending),
        "sentiment": {
            "positive": pos,
            "negative": neg,
            "neutral": neu,
            "positive_pct": pct(pos),
            "negative_pct": pct(neg),
            "neutral_pct": pct(neu),
        },
        "top_positive_keywords": [kw for kw, _ in pos_kw.most_common(10)],
        "top_negative_keywords": [kw for kw, _ in neg_kw.most_common(10)],
        "monthly_trend": trend,
    }


def _empty_summary() -> dict:
    return {
        "total_reviews": 0,
        "analyzed_count": 0,
        "reply_rate": 0.0,
        "pending_count": 0,
        "sentiment": {
            "positive": 0, "negative": 0, "neutral": 0,
            "positive_pct": 0.0, "negative_pct": 0.0, "neutral_pct": 0.0,
        },
        "top_positive_keywords": [],
        "top_negative_keywords": [],
        "monthly_trend": [],
    }
