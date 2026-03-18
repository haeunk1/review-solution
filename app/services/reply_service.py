import google.generativeai as genai
from app.core.config import settings
from app.models.review import Sentiment, ReplyStyle

GEMINI_MODEL = "gemini-2.0-flash-lite"

_STYLE_GUIDE: dict[str, str] = {
    ReplyStyle.formal: "정중하고 공식적인 어투로, 고객의 불편을 공감하며 개선 의지를 표현합니다.",
    ReplyStyle.friendly: "친근하고 따뜻한 어투로, 고객과 가깝게 소통하는 느낌을 줍니다.",
    ReplyStyle.positive: "긍정적이고 감사한 어투로, 고객의 좋은 경험을 함께 기뻐합니다.",
}


def _get_model() -> genai.GenerativeModel:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return genai.GenerativeModel(GEMINI_MODEL)


def _auto_style(sentiment: str | None) -> ReplyStyle:
    if sentiment == Sentiment.negative:
        return ReplyStyle.formal
    if sentiment == Sentiment.positive:
        return ReplyStyle.positive
    return ReplyStyle.friendly


def generate_reply(
    review_text: str,
    visitor_name: str | None,
    sentiment: str | None,
    style: ReplyStyle | None = None,
) -> str:
    """Gemini API로 리뷰 답글 생성."""
    if style is None:
        style = _auto_style(sentiment)

    style_guide = _STYLE_GUIDE.get(style, _STYLE_GUIDE[ReplyStyle.friendly])
    name_hint = f"리뷰 작성자: {visitor_name}\n" if visitor_name else ""

    prompt = f"""피부과/성형외과 병원의 리뷰 답글을 작성해줘.

{name_hint}리뷰 내용:
{review_text}

답글 스타일: {style_guide}

요구사항:
- 한국어로 작성
- 100~200자 내외로 간결하게
- 병원 이름 언급 금지
- 과도한 마케팅 문구 금지
- 자연스럽고 진정성 있게
- 답글 텍스트만 반환 (설명 없이)"""

    model = _get_model()
    response = model.generate_content(prompt)
    return response.text.strip()
