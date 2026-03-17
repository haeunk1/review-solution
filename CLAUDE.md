# 프로젝트 컨텍스트: AI 리뷰 통합 관리 솔루션 (Review Solution)

## 1. 프로젝트 개요
- **목적:** 네이버, 구글, 강남언니 등 외부 플랫폼의 리뷰를 통합 수집하고, AI를 통해 감성 분석 및 자동 답글 생성을 제공하는 대시보드 서비스.
- **핵심 가치:** 리뷰 관리 효율화, 고객 경험 개선, 데이터 기반 인사이트 제공.

## 2. 기술 스택 (Tech Stack)
- **Backend:** Python 3.13+, FastAPI
- **Database:** PostgreSQL (SQLAlchemy 2.0+, Alembic)
- **AI/LLM:** Claude API (또는 GPT)를 활용한 리뷰 분석 및 답글 생성
- **Authentication:** JWT (python-jose, passlib)
- **Environment:** Pydantic Settings (BaseSettings) 기반 환경 설정

## 3. 개발 원칙 (Development Rules)
- **Async First:** FastAPI의 이점을 살려 모든 I/O 작업(DB, API 호출)은 `async/await`를 기본으로 함.
- **Migration:** DB 스키마 변경 시 반드시 `alembic`을 활용하며, 마이그레이션 파일명은 명확한 의도를 담을 것.
- **Type Hinting:** 모든 함수와 클래스에는 파이썬 Type Hint를 철저히 적용할 것.
- **Security:** 외부 리뷰 데이터 처리 시 XSS 방지 및 개인정보 비식별화 처리를 고려할 것.

## 4. 도메인 특화 가이드 (Domain Specifics)
- **Multi-Platform:** 네이버, 구글, 강남언니 등 각 플랫폼마다 다른 데이터 구조를 표준화된 리포맷(Standard Schema)으로 변환하는 로직을 중시함.
- **AI Tone & Manner:** - AI 답글 생성 시, 해당 업체(병원, 식당 등)의 브랜드 이미지에 맞는 친절하고 전문적인 톤을 유지해야 함.
  - 부정적 리뷰(악플)에 대해서는 공감하되 방어적인 태도를 지양하는 가이드라인을 준수할 것.
- **Performance:** 대량의 리뷰 데이터를 대시보드에 렌더링하므로, SQL 쿼리 최적화 및 인덱스 활용을 우선시함.

## 5. 지시 사항 (Instructions for Claude)
- 코드 제안 시 위 기술 스택을 준수할 것.
- 새로운 라이브러리 추가가 필요할 경우 반드시 사전에 제안하고 승인받을 것.
- 에러 처리 시 사용자에게 명확한 메시지를 전달하는 예외 처리 패턴을 사용할 것.