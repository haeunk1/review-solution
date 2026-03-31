from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import hashlib
import logging
import httpx
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)


def _stable_id(platform: str, *parts: str) -> str:
    """리뷰 내용 기반 안정적 ID 생성 (인덱스 변동 무관)"""
    key = "|".join(parts)
    return f"{platform}_{hashlib.md5(key.encode()).hexdigest()[:16]}"


@dataclass
class ReviewData:
    hospital_id: str
    platform: str  # "naver" | "google" | "gangnamunni"
    platform_review_id: Optional[str]
    review_text: str
    rating: Optional[str] = None
    visitor_name: Optional[str] = "익명"
    visited_date: Optional[str] = None


class BaseScraper(ABC):
    """모든 플랫폼 스크래퍼의 공통 인터페이스"""

    @abstractmethod
    async def scrape(self, place_id: str, hospital_id: str, max_pages: int = 3) -> List[ReviewData]:
        pass

    async def _launch_browser(self, playwright):
        return await playwright.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

    async def _new_context(self, browser):
        return await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )


class NaverScraper(BaseScraper):
    """네이버 플레이스 리뷰 스크래퍼"""

    PLATFORM = "naver"
    BASE_URL = "https://pcmap.place.naver.com/hospital/{place_id}/review/visitor"

    async def scrape(self, place_id: str, hospital_id: str, max_reviews: int = 30) -> List[ReviewData]:
        results: List[ReviewData] = []

        async with async_playwright() as p:
            browser = await self._launch_browser(p)
            context = await self._new_context(browser)
            page = await context.new_page()

            url = self.BASE_URL.format(place_id=place_id)
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(3000)

                # '펼쳐서 더보기' 버튼 클릭으로 max_reviews개 이상 로드
                while True:
                    current = len(await page.query_selector_all('li.place_apply_pui'))
                    if current >= max_reviews:
                        break
                    more_btn = page.locator('span.TeItc').first
                    if await more_btn.count() > 0 and await more_btn.is_visible():
                        await more_btn.click()
                        await page.wait_for_timeout(2000)
                        new_count = len(await page.query_selector_all('li.place_apply_pui'))
                        if new_count <= current:
                            break
                    else:
                        break

                review_elements = await page.query_selector_all('li.place_apply_pui')

                for element in review_elements:
                    text_el = await element.query_selector('div.pui__vn15t2')
                    review_text = await text_el.inner_text() if text_el else ""

                    name_el = await element.query_selector('span.pui__NMi-Dp')
                    visitor_name = await name_el.inner_text() if name_el else "익명"

                    date_el = await element.query_selector('span.pui__gfuUIT span.pui__blind:last-child')
                    visited_date = await date_el.inner_text() if date_el else ""

                    text = review_text.replace("\n", " ").strip()
                    if text:
                        results.append(ReviewData(
                            hospital_id=hospital_id,
                            platform=self.PLATFORM,
                            platform_review_id=_stable_id(
                                self.PLATFORM, visitor_name.strip(), visited_date.strip(), text[:40]
                            ),
                            review_text=text,
                            rating=None,  # 네이버는 키워드 리뷰 위주
                            visitor_name=visitor_name.strip(),
                            visited_date=visited_date.strip(),
                        ))

            except Exception as e:
                print(f"[NaverScraper] 크롤링 에러: {e}")
            finally:
                await browser.close()

        return results


class GooglePlacesClient(BaseScraper):
    """Google Places API를 이용한 구글 리뷰 수집 클라이언트

    참고: Places API는 장소당 최대 5개의 리뷰만 반환합니다 (구글 정책).
    사용 전 Google Cloud Console에서 Places API를 활성화하고
    .env의 GOOGLE_MAPS_API_KEY를 설정해야 합니다.
    """

    PLATFORM = "google"
    PLACES_DETAIL_URL = "https://maps.googleapis.com/maps/api/place/details/json"

    async def scrape(self, place_id: str, hospital_id: str, **kwargs) -> List[ReviewData]:
        from app.core.config import settings

        if not settings.GOOGLE_MAPS_API_KEY:
            logger.warning(
                "[GooglePlaces] GOOGLE_MAPS_API_KEY가 설정되지 않았습니다. "
                ".env 파일에 GOOGLE_MAPS_API_KEY를 추가하세요."
            )
            return []

        params = {
            "place_id": place_id,
            "fields": "reviews",
            "language": "ko",
            "key": settings.GOOGLE_MAPS_API_KEY,
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(self.PLACES_DETAIL_URL, params=params)
                response.raise_for_status()
                data = response.json()
        except Exception as e:
            logger.error(f"[GooglePlaces] API 요청 실패: {e}")
            return []

        status = data.get("status")
        if status != "OK":
            logger.error(f"[GooglePlaces] API 오류 상태: {status} — {data.get('error_message', '')}")
            return []

        raw_reviews = data.get("result", {}).get("reviews", [])
        results: List[ReviewData] = []

        for review in raw_reviews:
            review_text: str = review.get("text", "").replace("\n", " ").strip()
            if not review_text:
                continue

            visitor_name: str = review.get("author_name", "익명")
            rating: Optional[str] = str(review.get("rating")) if review.get("rating") is not None else None

            # unix timestamp → YYYY-MM-DD
            timestamp: Optional[int] = review.get("time")
            visited_date: str = (
                datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d") if timestamp else ""
            )

            platform_review_id = _stable_id(self.PLATFORM, visitor_name, visited_date, review_text[:40])

            results.append(ReviewData(
                hospital_id=hospital_id,
                platform=self.PLATFORM,
                platform_review_id=platform_review_id,
                review_text=review_text,
                rating=rating,
                visitor_name=visitor_name,
                visited_date=visited_date,
            ))

        return results


class GangnamUnniScraper(BaseScraper):
    """강남언니 리뷰 스크래퍼"""

    PLATFORM = "gangnamunni"
    BASE_URL = "https://gangnamunni.com/hospitals/{place_id}/reviews"

    async def scrape(self, place_id: str, hospital_id: str, max_pages: int = 3) -> List[ReviewData]:
        results: List[ReviewData] = []

        async with async_playwright() as p:
            browser = await self._launch_browser(p)
            context = await self._new_context(browser)
            page = await context.new_page()

            url = self.BASE_URL.format(place_id=place_id)
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(2000)

                # 더보기 버튼 반복 클릭
                for _ in range(max_pages):
                    more_btn = page.locator('button:has-text("더보기")')
                    if await more_btn.count() > 0 and await more_btn.first.is_visible():
                        await more_btn.first.click()
                        await page.wait_for_timeout(1500)
                    else:
                        break

                review_elements = await page.query_selector_all('li[class*="review"]')

                for idx, element in enumerate(review_elements):
                    text_el = await element.query_selector('p[class*="content"], div[class*="content"]')
                    review_text = await text_el.inner_text() if text_el else ""

                    name_el = await element.query_selector('span[class*="nickname"], span[class*="name"]')
                    visitor_name = await name_el.inner_text() if name_el else "익명"

                    rating_el = await element.query_selector('span[class*="rating"], div[class*="star"]')
                    rating = await rating_el.inner_text() if rating_el else None

                    date_el = await element.query_selector('span[class*="date"], time')
                    visited_date = await date_el.inner_text() if date_el else ""

                    text = review_text.replace("\n", " ").strip()
                    name = visitor_name.strip()
                    date = visited_date.strip()
                    if text:
                        results.append(ReviewData(
                            hospital_id=hospital_id,
                            platform=self.PLATFORM,
                            platform_review_id=_stable_id(self.PLATFORM, name, date, text[:40]),
                            review_text=text,
                            rating=rating,
                            visitor_name=name,
                            visited_date=date,
                        ))

            except Exception as e:
                print(f"[GangnamUnniScraper] 크롤링 에러: {e}")
            finally:
                await browser.close()

        return results


class ScraperService:
    """플랫폼별 스크래퍼를 통합 관리하는 서비스"""

    _scrapers = {
        "naver": NaverScraper(),
        "google": GooglePlacesClient(),
        "gangnamunni": GangnamUnniScraper(),
    }

    async def scrape_platform(
        self,
        platform: str,
        place_id: str,
        hospital_id: str,
        max_reviews: int = 100,
    ) -> List[ReviewData]:
        scraper = self._scrapers.get(platform)
        if not scraper:
            raise ValueError(f"지원하지 않는 플랫폼: {platform}")
        return await scraper.scrape(place_id, hospital_id, max_reviews)

    async def scrape_all(self, hospital) -> List[ReviewData]:
        """병원의 모든 플랫폼 리뷰를 수집"""
        results: List[ReviewData] = []
        platform_map = {
            "naver": hospital.naver_place_id,
            "google": hospital.google_place_id,
            "gangnamunni": hospital.gangnamunni_id,
        }
        for platform, place_id in platform_map.items():
            if place_id:
                reviews = await self.scrape_platform(platform, place_id, hospital.hospital_id)
                results.extend(reviews)
        return results


scraper_service = ScraperService()
