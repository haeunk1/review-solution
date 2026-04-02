from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.store import Store
from app.models.review import Review, Platform
from app.services.scraper_service import scraper_service
import traceback

scheduler = AsyncIOScheduler()


async def collect_reviews_for_store(store_id: str):
    """특정 업장의 모든 플랫폼 리뷰를 수집하고 DB에 저장"""
    db: Session = SessionLocal()
    try:
        store = db.query(Store).filter(
            Store.store_id == store_id,
            Store.is_active == True,
        ).first()

        if not store:
            print(f"[Scheduler] 업장 없음: {store_id}")
            return

        print(f"[Scheduler] 업장 확인: {store.name}, naver_place_id={store.naver_place_id}")
        reviews = await scraper_service.scrape_all(store)
        print(f"[Scheduler] 스크래퍼 수집 결과: {len(reviews)}건")

        STOP_AFTER = 5
        new_count = 0
        consecutive_exists = 0

        for r in reviews:
            if r.platform_review_id:
                exists = db.query(Review).filter(
                    Review.platform == r.platform,
                    Review.platform_review_id == r.platform_review_id,
                ).first()
                if exists:
                    consecutive_exists += 1
                    if consecutive_exists >= STOP_AFTER:
                        print(f"[Scheduler] {store.name}: 기존 리뷰 {STOP_AFTER}개 연속 감지, 수집 중단")
                        break
                    continue
                else:
                    consecutive_exists = 0

            db_review = Review(
                store_id=r.hospital_id,
                platform=r.platform,
                platform_review_id=r.platform_review_id,
                review_text=r.review_text,
                rating=r.rating,
                visitor_name=r.visitor_name,
                visited_date=r.visited_date,
            )
            db.add(db_review)
            new_count += 1

            if new_count % 50 == 0:
                db.commit()

        db.commit()
        print(f"[Scheduler] {store.name}: 신규 리뷰 {new_count}건 저장 완료")

    except Exception as e:
        db.rollback()
        print(f"[Scheduler] 에러 발생 ({store_id}): {e}")
        print(traceback.format_exc())
    finally:
        db.close()


def schedule_store(store: Store):
    """업장별 크롤링 주기를 스케줄러에 등록"""
    job_id = f"collect_{store.store_id}"

    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    scheduler.add_job(
        collect_reviews_for_store,
        trigger=IntervalTrigger(hours=store.crawl_interval_hours),
        id=job_id,
        args=[store.store_id],
        replace_existing=True,
        max_instances=1,
    )


def init_scheduler():
    """앱 시작 시 DB의 모든 활성 업장 스케줄 등록"""
    db: Session = SessionLocal()
    try:
        stores = db.query(Store).filter(Store.is_active == True).all()
        for store in stores:
            schedule_store(store)
    finally:
        db.close()

    scheduler.start()


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("[Scheduler] APScheduler 종료")
