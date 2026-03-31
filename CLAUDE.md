# CLAUDE.md

이 파일은 Claude Code(claude.ai/code)가 이 저장소에서 작업할 때 참고하는 가이드입니다.

## 프로젝트 개요

한국 의료 시설을 위한 AI 기반 리뷰 통합 관리 대시보드. 네이버 플레이스, 구글 맵스, 강남언니의 리뷰를 수집하고 Gemini API를 통해 감성 분석 및 자동 답글 생성을 제공합니다.

## 개발 명령어

### 백엔드 (FastAPI)
```bash
# 의존성 설치
pip install -r requirements.txt

# DB 마이그레이션 적용
alembic upgrade head

# 백엔드 서버 실행 (포트 8001)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# 모델 변경 후 새 마이그레이션 생성
alembic revision --autogenerate -m "변경_내용_설명"
```

### 프론트엔드 (Vue 3 + Vite)
```bash
cd frontend

npm install
npm run dev      # 개발 서버 포트 3000 (/api 요청은 localhost:8081로 프록시)
npm run build    # TypeScript 검사 + 프로덕션 빌드
```

> **주의:** Vite 프록시 대상이 `http://localhost:8081`로 설정되어 있습니다. 백엔드를 8081 포트로 실행하거나, `frontend/vite.config.ts`의 프록시 설정을 백엔드 포트에 맞게 수정하세요.

### 환경 설정
`.env.example`을 복사하여 값을 채워 넣습니다:
```
DATABASE_URL=postgresql://postgres:1234@localhost:5432/review_db
GEMINI_API_KEY=...
SECRET_KEY=...
```

## 아키텍처

### 백엔드 (`app/`)

**계층 구조:** `api/v1/` 라우터 → `services/` (비즈니스 로직) → `models/` (SQLAlchemy ORM) + `schemas/` (Pydantic DTO)

| 라우터 | 경로 | 역할 |
|---|---|---|
| `reviews.py` | `/api/v1/reviews` | 리뷰 목록 조회, 수동 수집 트리거 |
| `hospitals.py` | `/api/v1/hospitals` | 병원 CRUD |
| `analysis.py` | `/api/v1/analysis` | 감성 분석, 통계 요약 |
| `replies.py` | `/api/v1/replies` | AI 답글 생성 및 저장 |

**주요 서비스:**
- `scraper_service.py` — Playwright 기반 플랫폼별 스크래퍼. 모든 스크래퍼는 `BaseScraper`를 상속하며 표준화된 `ReviewData` 데이터클래스를 반환합니다. 새 플랫폼 스크래퍼는 반드시 이 패턴을 따라야 합니다.
- `analysis_service.py` — 감성 분석 및 키워드 추출 시 리뷰 5개씩 묶어 Gemini API를 호출합니다.
- `reply_service.py` — Gemini로 답글을 생성하며 감성에 따라 톤을 자동 선택합니다 (부정=격식체, 긍정=긍정적, 중립=친근체). 답글은 한국어 100~200자로 제한됩니다.
- `scheduler_service.py` — APScheduler가 병원별 수집 작업을 설정된 주기로 실행합니다. `platform_review_id`로 중복을 제거하며, 기존 리뷰가 5개 연속으로 감지되면 조기 종료합니다.

**인증 참고사항:** JWT 설정이 `app/core/config.py`와 `app/api/deps.py`에 존재하지만, `get_current_user()`는 현재 하드코딩된 목업 유저를 반환합니다 — 아직 실제로 적용되지 않았습니다.

### 프론트엔드 (`frontend/src/`)

- **Vue Router** 가드가 `localStorage`에 `hospital_id`가 없으면 `/login`으로 리다이렉트합니다.
- **`src/api/`** — 도메인별 Axios 클라이언트 (hospitals, reviews, analysis). 기본 URL은 `/api/v1`.
- **`src/composables/useReviews.ts`** — 리뷰 목록과 선택된 리뷰의 중앙 상태 관리. 피처 컴포넌트는 API를 직접 호출하지 않고 이 컴포저블을 사용해야 합니다.
- **`src/types/review.ts`** — Review, StatsData 및 Enum 타입의 표준 TypeScript 타입. 백엔드 Pydantic 스키마와 항상 동기화를 유지해야 합니다.

### 데이터베이스

핵심 테이블: `hospitals`, `reviews`. 주요 인덱스 컬럼: `platform_review_id`(중복 제거), `hospital_id`(FK), `tenant_id`(향후 멀티테넌시). 스키마 변경은 반드시 Alembic을 사용하며 직접 테이블을 수정하지 않습니다.

## 개발 원칙

- **Async 우선:** 모든 DB 및 외부 API 호출은 반드시 `async/await`를 사용합니다.
- **플랫폼 정규화:** 새로운 플랫폼 스크래퍼는 반드시 `ReviewData`(표준화 스키마)를 반환해야 합니다. 플랫폼 고유 필드가 하위 서비스로 유출되지 않도록 합니다.
- **AI LLM:** 현재 **Google Gemini** (`gemini-2.0-flash-lite`)를 사용합니다. `OPENAI_API_KEY` 설정 필드는 존재하지만 사용되지 않습니다. 별도 논의 없이 OpenAI 호출을 추가하지 않습니다.
- **마이그레이션:** 모든 모델 변경에는 Alembic 마이그레이션이 필요합니다. 마이그레이션 메시지는 명확하게 작성합니다.
- **새 라이브러리:** `requirements.txt` 또는 `package.json`에 추가하기 전에 반드시 먼저 제안합니다.
