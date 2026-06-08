# ============================================================
# crawler_investing.py - Investing.com 경제 캘린더 크롤러
# 예측치(컨센서스), 실제치, 이전치 수집
# + 오늘 발표 지표 자동 감지
# ============================================================

import time
import requests
from datetime import datetime, date
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

CALENDAR_URL = "https://www.investing.com/economic-calendar/"

# investing.com 표기 → 내부 지표 키 매핑
INDICATOR_MAP = {
    "cpi": [
        "CPI",
        "Core CPI",
        "Consumer Price Index",
    ],
    "ppi": [
        "PPI",
        "Core PPI",
        "Producer Price Index",
    ],
    "nfp": [
        "Nonfarm Payrolls",
        "Non-Farm Payrolls",
        "NFP",
        "Unemployment Rate",
        "Average Hourly Earnings",
    ],
    "fomc": [
        "Fed Interest Rate Decision",
        "FOMC",
        "Federal Funds Rate",
        "FOMC Statement",
        "Fed Rate Decision",
    ],
    "beige": [
        "Beige Book",
        "Fed Beige Book",
    ],
}

# FOMC/베이지북 URL 자동 생성 패턴 (Fed 공식 사이트)
FED_URL_PATTERNS = {
    "fomc_statement": "https://www.federalreserve.gov/newsevents/pressreleases/monetary{date}a.htm",
    "fomc_presser":   "https://www.federalreserve.gov/monetarypolicy/fomcpresconf{date}.htm",
    "beige":          "https://www.federalreserve.gov/monetarypolicy/beigebook{yearmonth}.htm",
}


# ------------------------------------------------------------
# Fed URL 자동 생성 및 검증
# ------------------------------------------------------------

def try_build_fed_url(pattern_key: str, target_date: date = None) -> str:
    """
    오늘 날짜로 Fed URL을 자동 생성하고 실제 존재하는지 확인
    존재하면 URL 반환, 없으면 빈 문자열 반환
    """
    if target_date is None:
        target_date = date.today()

    pattern = FED_URL_PATTERNS.get(pattern_key, "")
    if not pattern:
        return ""

    url = pattern.format(
        date=target_date.strftime("%Y%m%d"),
        yearmonth=target_date.strftime("%Y%m"),
    )

    try:
        resp = requests.head(url, timeout=10, allow_redirects=True)
        if resp.status_code == 200:
            print(f"  [URL 자동감지] {pattern_key}: {url}")
            return url
        else:
            print(f"  [URL 자동감지] {pattern_key} 페이지 없음 (status {resp.status_code}): {url}")
            return ""
    except Exception as e:
        print(f"  [URL 자동감지] {pattern_key} 확인 실패: {e}")
        return ""


# ------------------------------------------------------------
# 캘린더 크롤링
# ------------------------------------------------------------

def fetch_calendar() -> list:
    """
    investing.com 경제 캘린더에서 오늘 미국 지표 수집
    반환: [{"name": "CPI", "actual": "0.3%", "forecast": "0.3%", "previous": "0.4%", "time": "08:30"}, ...]
    """
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="en-US",
        )
        page = context.new_page()

        try:
            print(f"  [Investing] 캘린더 페이지 로딩 중...")
            page.goto(CALENDAR_URL, wait_until="networkidle", timeout=30000)
            time.sleep(3)

            # 쿠키 배너 닫기
            try:
                page.click("button#onetrust-accept-btn-handler", timeout=3000)
                time.sleep(1)
            except PlaywrightTimeout:
                pass

            # 오늘 탭 클릭
            try:
                page.click("a#timeFrame_today", timeout=5000)
                time.sleep(2)
            except PlaywrightTimeout:
                pass

            rows = page.query_selector_all("tr.js-event-item")
            print(f"  [Investing] 총 {len(rows)}개 이벤트 발견")

            for row in rows:
                try:
                    # 미국 지표만
                    flag = row.query_selector("td.flagCur span")
                    if flag:
                        country = flag.get_attribute("title") or ""
                        if "United States" not in country:
                            continue

                    name_el = row.query_selector("td.event a")
                    if not name_el:
                        continue
                    name = name_el.inner_text().strip()

                    time_el = row.query_selector("td.time")
                    release_time = time_el.inner_text().strip() if time_el else ""

                    actual_el = row.query_selector("td.act")
                    actual = actual_el.inner_text().strip() if actual_el else ""

                    forecast_el = row.query_selector("td.fore")
                    forecast = forecast_el.inner_text().strip() if forecast_el else ""

                    prev_el = row.query_selector("td.prev")
                    previous = prev_el.inner_text().strip() if prev_el else ""

                    importance_els = row.query_selector_all("td.sentiment i.grayFullBullishIcon")
                    importance = len(importance_els)

                    results.append({
                        "name": name,
                        "time": release_time,
                        "actual": actual if actual else "미발표",
                        "forecast": forecast if forecast else "-",
                        "previous": previous if previous else "-",
                        "importance": "★" * importance,
                    })

                except Exception:
                    continue

        except Exception as e:
            print(f"  [Investing] 크롤링 오류: {e}")

        finally:
            browser.close()

    return results


# ------------------------------------------------------------
# 오늘 발표 지표 자동 감지 (핵심 기능)
# ------------------------------------------------------------

def detect_today_indicators(calendar_data: list) -> dict:
    """
    캘린더 데이터를 분석해서 오늘 발표되는 지표를 자동 감지
    반환: {
        "cpi": True/False,
        "ppi": True/False,
        "nfp": True/False,
        "fomc": True/False,
        "beige": True/False,
        "fomc_statement_url": "...",
        "fomc_presser_url": "...",
        "beige_url": "...",
    }
    """
    detected = {key: False for key in INDICATOR_MAP.keys()}
    detected["fomc_statement_url"] = ""
    detected["fomc_presser_url"] = ""
    detected["beige_url"] = ""

    # 캘린더에서 지표 감지
    for item in calendar_data:
        name = item["name"].lower()
        for indicator_key, keywords in INDICATOR_MAP.items():
            if any(kw.lower() in name for kw in keywords):
                detected[indicator_key] = True
                print(f"  [자동감지] {indicator_key.upper()} 발표 확인: {item['name']} ({item['time']})")

    # FOMC/베이지북 감지 시 URL 자동 생성
    if detected["fomc"]:
        detected["fomc_statement_url"] = try_build_fed_url("fomc_statement")
        detected["fomc_presser_url"]   = try_build_fed_url("fomc_presser")

    if detected["beige"]:
        detected["beige_url"] = try_build_fed_url("beige")

    return detected


# ------------------------------------------------------------
# 예측치 추출 헬퍼
# ------------------------------------------------------------

def get_forecast_for(indicator: str, calendar_data: list) -> dict:
    """지표명으로 예측치 딕셔너리 반환"""
    keywords = INDICATOR_MAP.get(indicator.lower(), [indicator])
    matched = {}

    for item in calendar_data:
        if any(kw.lower() in item["name"].lower() for kw in keywords):
            matched[item["name"]] = (
                f"실제: {item['actual']} | 예측: {item['forecast']} | 이전: {item['previous']}"
            )

    return matched


def format_calendar_markdown(calendar_data: list) -> str:
    """캘린더 데이터를 마크다운 표로 변환"""
    if not calendar_data:
        return "_데이터 없음_\n"

    from utils import md_table
    headers = ["시간", "지표명", "실제치", "예측치", "이전치", "중요도"]
    rows = [
        [item["time"], item["name"], item["actual"],
         item["forecast"], item["previous"], item["importance"]]
        for item in calendar_data
    ]
    return md_table(headers, rows)


if __name__ == "__main__":
    print("Investing.com 캘린더 크롤링 테스트")
    data = fetch_calendar()
    print(f"\n수집된 지표 수: {len(data)}")
    detected = detect_today_indicators(data)
    print(f"\n오늘 발표 지표: {detected}")
