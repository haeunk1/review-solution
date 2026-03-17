from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.hospital import Hospital
from app.models.review import Review, Platform
from app.services.scraper_service import scraper_service
import traceback

scheduler = AsyncIOScheduler()


async def collect_reviews_for_hospital(hospital_id: str):
    """특정 병원의 모든 플랫폼 리뷰를 수집하고 DB에 저장"""
    db: Session = SessionLocal()
    try:
        hospital = db.query(Hospital).filter(
            Hospital.hospital_id == hospital_id,
            Hospital.is_active == True,
        ).first()

        if not hospital:
            print(f"[Scheduler] 병원 없음: {hospital_id}")
            return

        print(f"[Scheduler] 병원 확인: {hospital.name}, naver_place_id={hospital.naver_place_id}")
        reviews = await scraper_service.scrape_all(hospital)
        print(f"[Scheduler] 스크래퍼 수집 결과: {len(reviews)}건")

        new_count = 0
        for i, r in enumerate(reviews):
            if r.platform_review_id:
                exists = db.query(Review).filter(
                    Review.platform == r.platform,
                    Review.platform_review_id == r.platform_review_id,
                ).first()
                if exists:
                    continue

            db_review = Review(
                hospital_id=r.hospital_id,
                platform=r.platform,
                platform_review_id=r.platform_review_id,
                review_text=r.review_text,
                rating=r.rating,
                visitor_name=r.visitor_name,
                visited_date=r.visited_date,
            )
            db.add(db_review)
            new_count += 1

            # 50건마다 중간 커밋 (중단 시 손실 최소화)
            if new_count % 50 == 0:
                db.commit()
                print(f"[Scheduler] 중간 저장: {new_count}건")

        db.commit()
        print(f"[Scheduler] {hospital.name}: 신규 리뷰 {new_count}건 저장 완료")

    except Exception as e:
        db.rollback()
        print(f"[Scheduler] 에러 발생 ({hospital_id}): {e}")
        print(traceback.format_exc())
    finally:
        db.close()


def schedule_hospital(hospital: Hospital):
    """병원별 크롤링 주기를 스케줄러에 등록"""
    job_id = f"collect_{hospital.hospital_id}"

    # 기존 job 있으면 제거 후 재등록
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    scheduler.add_job(
        collect_reviews_for_hospital,
        trigger=IntervalTrigger(hours=hospital.crawl_interval_hours),
        id=job_id,
        args=[hospital.hospital_id],
        replace_existing=True,
        max_instances=1,
    )
    print(f"[Scheduler] 등록: {hospital.name} (매 {hospital.crawl_interval_hours}시간)")


def init_scheduler():
    """앱 시작 시 DB의 모든 활성 병원 스케줄 등록"""
    db: Session = SessionLocal()
    try:
        hospitals = db.query(Hospital).filter(Hospital.is_active == True).all()
        for hospital in hospitals:
            schedule_hospital(hospital)
        print(f"[Scheduler] 초기화 완료: {len(hospitals)}개 병원 등록")
    finally:
        db.close()

    scheduler.start()
    print("[Scheduler] APScheduler 시작")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("[Scheduler] APScheduler 종료")
