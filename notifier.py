# ============================================================
# notifier.py - 경제지표 일정 알림 (텔레그램)
#
# 실행 모드 (GitHub Actions에서 환경변수로 구분):
#   NOTIFY_MODE=weekly      → 주간 예고
#                             일요일 오전 9시 = 이번 주(월~금) 일정
#                             금요일 오후 3:30 = 다음 주(월~금) 일정
#   NOTIFY_MODE=daily       → 평일 오전 8시: 오늘 발표 예정 (항상 전송)
#                             + 말일이고 공휴일 아니면 다음 달 일정도 전송
#   NOTIFY_MODE=daily_late  → 평일 오전 9시: 말일 + 공휴일인 경우에만 다음 달 예고
# ============================================================
import os
import re
import requests
from datetime import datetime, timedelta, date, timezone
import calendar

# ── 텔레그램 설정
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ── 지표 표시 이름
INDICATOR_LABELS = {
    "cpi":   "CPI (소비자물가지수)",
    "ppi":   "PPI (생산자물가지수)",
    "nfp":   "NFP (비농업고용)",
    "fomc":  "FOMC 금리결정",
    "beige": "베이지북",
}

# ── 요일 한국어
DAY_KO = ["월", "화", "수", "목", "금", "토", "일"]

# ── 월 한국어
MONTH_KO = {
    1:"1월", 2:"2월", 3:"3월", 4:"4월", 5:"5월", 6:"6월",
    7:"7월", 8:"8월", 9:"9월", 10:"10월", 11:"11월", 12:"12월"
}

# ── KST 기준 오늘 날짜 (GitHub Actions는 UTC 기준이므로 반드시 KST로 변환)
KST = timezone(timedelta(hours=9))

def today_kst() -> date:
    """KST(한국시간) 기준 오늘 날짜 반환"""
    return datetime.now(KST).date()


# ─── 공휴일 판별 ──────────────────────────────────────────────
def is_korean_holiday(d: date) -> bool:
    try:
        import holidays as holidays_pkg
        kr = holidays_pkg.country_holidays("KR", years=d.year)
        return d in kr
    except ImportError:
        print("[공휴일] holidays 패키지 없음 - 공휴일 판별 불가")
        return False


# ─── BLS 발표 일정 크롤링 ─────────────────────────────────────
def fetch_bls_schedule(year: int) -> list:
    # 두 URL 순서대로 시도 (BLS가 서버 환경에서 403 차단하는 경우 대비)
    urls = [
        "https://www.bls.gov/schedule/news_release/releaseCalendar.htm",
        "https://www.bls.gov/schedule/news_release/current_year.asp",
    ]
    # 실제 브라우저처럼 보이는 헤더
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    resp = None
    for url in urls:
        try:
            session = requests.Session()
            session.headers.update(headers)
            resp = session.get(url, timeout=15)
            resp.raise_for_status()
            print(f"[BLS 일정] 수집 성공: {url}")
            break
        except Exception as e:
            print(f"[BLS 일정] 실패 ({url}): {e}")
            resp = None
    if resp is None:
        print("[BLS 일정] 모든 URL 실패 - BLS 일정 없이 진행")
        return []

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text, "lxml")

    results = []
    keyword_map = {
        "Consumer Price Index": "cpi",
        "Producer Price Index": "ppi",
        "Employment Situation":  "nfp",
    }

    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        date_text  = cells[0].get_text(strip=True)
        time_text  = cells[1].get_text(strip=True)
        title      = cells[2].get_text(strip=True)

        indicator = None
        for keyword, ind in keyword_map.items():
            if keyword in title:
                indicator = ind
                break
        if not indicator:
            continue

        try:
            dt = datetime.strptime(
                re.sub(r"^\w+,\s*", "", date_text.strip()), "%B %d, %Y"
            ).date()
        except Exception:
            continue

        def _is_edt(d):
            mar = d.replace(month=3, day=1)
            second_sun_mar = mar + timedelta(days=(6 - mar.weekday()) % 7 + 7)
            nov = d.replace(month=11, day=1)
            first_sun_nov = nov + timedelta(days=(6 - nov.weekday()) % 7)
            return second_sun_mar <= d < first_sun_nov

        if "08:30" in time_text:
            kst_time = "오후 9:30" if _is_edt(dt) else "오후 10:30"
        elif "10:00" in time_text:
            kst_time = "오후 11:00" if _is_edt(dt) else "자정 12:00"
        else:
            kst_time = "오후 9:30"

        results.append({"indicator": indicator, "date": dt, "time": kst_time})

    return results


def fetch_fed_schedule() -> list:
    results = []
    try:
        url = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "lxml")

        for div in soup.find_all(["div", "p", "td"]):
            text = div.get_text()
            m = re.search(r"(\w+ \d+(?:-\d+)?),?\s*(\d{4})", text)
            if m:
                try:
                    raw = m.group(0)
                    raw_clean = re.sub(r"\d+-(\d+)", r"\1", raw)
                    dt = datetime.strptime(raw_clean.strip(), "%B %d, %Y").date()
                    if dt >= today_kst():
                        results.append({"indicator": "fomc", "date": dt, "time": "새벽 3:00"})
                except Exception:
                    pass
    except Exception as e:
        print(f"[Fed FOMC 일정] 수집 실패: {e}")
    return results


def get_all_schedule() -> list:
    year = today_kst().year
    schedule = fetch_bls_schedule(year) + fetch_fed_schedule()
    schedule.sort(key=lambda x: x["date"])
    return schedule


# ─── 필터 함수 ───────────────────────────────────────────────
def this_week_schedule(schedule: list) -> list:
    today = today_kst()
    if today.weekday() == 6:
        monday = today + timedelta(days=1)
    else:
        monday = today - timedelta(days=today.weekday())
    friday = monday + timedelta(days=4)
    return [s for s in schedule if monday <= s["date"] <= friday]


def next_week_schedule(schedule: list) -> list:
    today = today_kst()
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    monday = today + timedelta(days=days_until_monday)
    friday = monday + timedelta(days=4)
    return [s for s in schedule if monday <= s["date"] <= friday]


def today_schedule(schedule: list) -> list:
    today = today_kst()
    return [s for s in schedule if s["date"] == today]


def next_month_schedule(schedule: list) -> list:
    today = today_kst()
    if today.month == 12:
        nm_year, nm_month = today.year + 1, 1
    else:
        nm_year, nm_month = today.year, today.month + 1
    return [s for s in schedule
            if s["date"].year == nm_year and s["date"].month == nm_month]


def is_last_day_of_month() -> bool:
    today = today_kst()
    last_day = calendar.monthrange(today.year, today.month)[1]
    return today.day == last_day


# ─── 메시지 포맷 ─────────────────────────────────────────────
def fmt_date(d: date) -> str:
    return f"{d.month:02d}/{d.day:02d}({DAY_KO[d.weekday()]})"


def fmt_weekly(schedule: list, label: str = "이번 주", monday: date = None) -> str:
    if monday is None:
        today = today_kst()
        if today.weekday() == 6:
            monday = today + timedelta(days=1)
        else:
            monday = today - timedelta(days=today.weekday())
    if not schedule:
        return f"📅 <b>{label} 발표 예정 지표</b>\n\n{label} 발표 없음"
    lines = [f"📅 <b>{label} 발표 예정 지표</b>\n"]
    for i in range(5):
        day = monday + timedelta(days=i)
        day_events = [s for s in schedule if s["date"] == day]
        label_day = fmt_date(day)
        if day_events:
            for e in day_events:
                lines.append(f"  {label_day}  📊 {INDICATOR_LABELS.get(e['indicator'], e['indicator'])}  {e['time']}")
        else:
            lines.append(f"  {label_day}  -")
    return "\n".join(lines)


def fmt_daily(schedule: list) -> str:
    today = today_kst()
    date_str = f"{today.year}-{today.month:02d}-{today.day:02d}({DAY_KO[today.weekday()]})"
    lines = [f"⏰ {date_str}"]
    if not schedule:
        lines.append("경제지표 발표 없음")
    else:
        for e in schedule:
            lines.append(f"📊 {INDICATOR_LABELS.get(e['indicator'], e['indicator'])}  {e['time']}")
    return "\n".join(lines)


def fmt_next_month(schedule: list) -> str:
    if not schedule:
        return ""
    today = today_kst()
    if today.month == 12:
        nm_year, nm_month = today.year + 1, 1
    else:
        nm_year, nm_month = today.year, today.month + 1
    last_day = calendar.monthrange(nm_year, nm_month)[1]
    max_week = (last_day - 1) // 7 + 1
    weeks: dict = {}
    for e in schedule:
        w = (e["date"].day - 1) // 7 + 1
        weeks.setdefault(w, []).append(e)
    lines = [f"📆 <b>{MONTH_KO[nm_month]} 발표 일정 예고</b>"]
    for w in range(1, max_week + 1):
        lines.append(f"\n{w}주차")
        if w in weeks:
            for e in sorted(weeks[w], key=lambda x: x["date"]):
                lines.append(f"  {fmt_date(e['date'])}  📊 {INDICATOR_LABELS.get(e['indicator'], e['indicator'])}  {e['time']}")
        else:
            lines.append("없음")
    return "\n".join(lines)


# ─── 텔레그램 전송 ────────────────────────────────────────────
def send_telegram(message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[텔레그램] 토큰/채팅ID 미설정 - 콘솔 출력만 함")
        print(message)
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    resp = requests.post(url, data={
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       message,
        "parse_mode": "HTML",
    })
    if resp.status_code == 200:
        print("[텔레그램] 전송 완료")
    else:
        print(f"[텔레그램] 전송 실패: {resp.text}")


# ─── 메인 ────────────────────────────────────────────────────
def main():
    mode = os.environ.get("NOTIFY_MODE", "daily")
    print(f"[알림] 모드: {mode}")

    schedule = get_all_schedule()
    print(f"[알림] 수집된 일정: {len(schedule)}건")

    today = today_kst()
    print(f"[알림] KST 오늘 날짜: {today}")

    if mode == "weekly":
        if today.weekday() == 4:  # 금요일
            next_monday = today + timedelta(days=3)
            week = next_week_schedule(schedule)
            msg = fmt_weekly(week, label="다음 주", monday=next_monday)
        else:  # 일요일
            next_monday = today + timedelta(days=1)
            week = this_week_schedule(schedule)
            msg = fmt_weekly(week, label="이번 주", monday=next_monday)
        send_telegram(msg)

    elif mode == "daily":
        today_events = today_schedule(schedule)
        msg = fmt_daily(today_events)
        send_telegram(msg)

        if is_last_day_of_month():
            if is_korean_holiday(today):
                print("[알림] 말일이지만 공휴일 - 다음 달 예고는 오전 9시(daily_late)에 전송")
            else:
                nm = next_month_schedule(schedule)
                if nm:
                    print("[알림] 말일 평일 - 다음 달 예고 전송")
                    send_telegram(fmt_next_month(nm))
                else:
                    print("[알림] 다음 달 일정 없음")

    elif mode == "daily_late":
        if is_last_day_of_month() and is_korean_holiday(today):
            nm = next_month_schedule(schedule)
            if nm:
                print("[알림] 말일 공휴일 - 다음 달 예고 전송 (9시)")
                send_telegram(fmt_next_month(nm))
            else:
                print("[알림] 다음 달 일정 없음")
        else:
            print("[알림] daily_late: 말일 공휴일 아님 - 스킵")


if __name__ == "__main__":
    main()
