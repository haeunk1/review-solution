import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

class ScraperService:
    async def get_naver_reviews(self, hospital_id: str, max_pages: int = 3):
        results = []
        
        async with async_playwright() as p:
            # 1. 브라우저 실행 (headless=True면 창이 안 뜸, 테스트 시 False 권장)
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            # 2. 네이버 플레이스 리뷰 탭 직행 URL
            url = f"https://pcmap.place.naver.com/hospital/{hospital_id}/review/visitor"
            await page.goto(url, wait_until="networkidle")

            try:
                # 3. '더보기' 버튼 클릭 (원하는 페이지만큼)
                for _ in range(max_pages):
                    more_button = page.locator('a.f_S_P') # 네이버 더보기 버튼 클래스 (변경될 수 있음)
                    if await more_button.is_visible():
                        await more_button.click()
                        await page.wait_for_timeout(1000) # 로딩 대기
                    else:
                        break

                # 4. 리뷰 리스트 아이템 추출
                # 네이버 리뷰 아이템의 공통 클래스 셀렉터
                review_elements = await page.query_selector_all('li.p_S_f') 

                for element in review_elements:
                    # 리뷰 텍스트 (내용이 길면 '더보기'가 또 있을 수 있음)
                    text_element = await element.query_selector('.z_p_x')
                    review_text = await text_element.inner_text() if text_element else ""

                    # 방문자명
                    name_element = await element.query_selector('.P_Y_u')
                    visitor_name = await name_element.inner_text() if name_element else "익명"

                    # 방문 날짜 및 별점 등 (네이버 구조에 따라 상세 선택 필요)
                    # 보통 '...번째 방문' 같은 텍스트 포함
                    date_element = await element.query_selector('.X_x_x') # 예시 클래스
                    visited_date = await date_element.inner_text() if date_element else ""

                    if review_text: # 내용이 있는 경우만 수집
                        results.append({
                            "hospital_id": hospital_id,
                            "review_text": review_text.replace("\n", " "),
                            "visitor_name": visitor_name,
                            "visited_date": visited_date,
                            "rating": "5" # 네이버는 현재 별점 대신 키워드 리뷰 위주
                        })

            except Exception as e:
                print(f"⚠️ 크롤링 중 에러 발생: {e}")
            finally:
                await browser.close()
                
        return results

scraper_service = ScraperService()