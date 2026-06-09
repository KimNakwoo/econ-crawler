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
from datetime import datetime, timedelta, date
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


# ─── 공휴일 판별 ──────────────────────────────────────────────

def is_korean_holiday(d: date) -> bool:
    """한국 공휴일 여부 (holidays 패키지 사용)"""
    try:
        import holidays as holidays_pkg
        kr = holidays_pkg.country_holidays("KR", years=d.year)
        return d in kr
    except ImportError:
        print("[공휴일] holidays 패키지 없음 - 공휴일 판별 불가")
        return False


# ─── BLS 발표 일정 크롤링 ─────────────────────────────────────

def fetch_bls_schedule(year: int) -> list:
    """
    BLS 연간 발표 일정 페이지에서 CPI / PPI / NFP 날짜 수집
    반환: [{"indicator": "cpi", "date": date(2026,6,11), "time": "오후 9:30"}, ...]
    """
    url = "https://www.bls.gov/schedule/news_release/current_year.asp"
    try:
        resp = requests.get(url, timeout=15,
                            headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception as e:
        print(f"[BLS 일정] 수집 실패: {e}")
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
        if len(cells) < 2:
            continue
        title = cells[0].get_text(strip=True)
        date_text = cells[1].get_text(strip=True) if len(cells) > 1 else ""

        indicator = None
        for keyword, ind in keyword_map.items():
            if keyword in title:
                indicator = ind
                break
        if not indicator:
            continue

        # 날짜 파싱 (예: "Wednesday, June 11, 2026")
        try:
            dt = datetime.strptime(
                re.sub(r"^\w+,\s*", "", date_text.strip()), "%B %d, %Y"
            ).date()
            results.append({
                "indicator": indicator,
                "date": dt,
                "time": "오후 9:30",
            })
        except Exception:
            continue

    return results


def fetch_fed_schedule() -> list:
    """Fed 사이트에서 FOMC 일정 수집"""
    results = []
    try:
        url = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
        resp = requests.get(url, timeout=15,
                            headers={"User-Agent": "Mozilla/5.0"})
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
                    if dt >= date.today():
                        results.append({
                            "indicator": "fomc",
                            "date": dt,
                            "time": "새벽 3:00",
                        })
                except Exception:
                    pass
    except Exception as e:
        print(f"[Fed FOMC 일정] 수집 실패: {e}")

    return results


def get_all_schedule() -> list:
    """BLS + Fed 전체 일정 병합"""
    year = datetime.now().year
    schedule = fetch_bls_schedule(year) + fetch_fed_schedule()
    schedule.sort(key=lambda x: x["date"])
    return schedule


# ─── 필터 함수 ───────────────────────────────────────────────

def this_week_schedule(schedule: list) -> list:
    """
    이번 주 월~금 일정.
    일요일에 호출하면 내일(월요일)부터 시작하는 주를 기준으로 함.
    """
    today = date.today()
    if today.weekday() == 6:  # 일요일
        monday = today + timedelta(days=1)
    else:
        monday = today - timedelta(days=today.weekday())
    friday = monday + timedelta(days=4)
    return [s for s in schedule if monday <= s["date"] <= friday]


def next_week_schedule(schedule: list) -> list:
    """다음 주 월~금 일정 (금요일 오후 알림용)"""
    today = date.today()
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    monday = today + timedelta(days=days_until_monday)
    friday = monday + timedelta(days=4)
    return [s for s in schedule if monday <= s["date"] <= friday]


def today_schedule(schedule: list) -> list:
    """오늘 발표 일정"""
    today = date.today()
    return [s for s in schedule if s["date"] == today]


def next_month_schedule(schedule: list) -> list:
    """다음 달 일정"""
    today = date.today()
    if today.month == 12:
        nm_year, nm_month = today.year + 1, 1
    else:
        nm_year, nm_month = today.year, today.month + 1
    return [s for s in schedule
            if s["date"].year == nm_year and s["date"].month == nm_month]


def is_last_day_of_month() -> bool:
    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    return today.day == last_day


# ─── 메시지 포맷 ─────────────────────────────────────────────

def fmt_date(d: date) -> str:
    return f"{d.month:02d}/{d.day:02d}({DAY_KO[d.weekday()]})"


def fmt_weekly(schedule: list, label: str = "이번 주", monday: date = None) -> str:
    """주간 일정 메시지 포맷"""
    if monday is None:
        today = date.today()
        if today.weekday() == 6:
            monday = today + timedelta(days=1)
        else:
            monday = today - timedelta(days=today.weekday())

    if not schedule:
        return f"📅 <b>{label} 발표 예정 지표</b>\n\n{label} 발표 없음"

    lines = [f"📅 <b>{label} 발표 예정 지표</b>\n"]
    for i in range(5):  # 월~금
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
    """오늘 발표 일정 메시지 (발표 없는 날도 항상 전송)"""
    today = date.today()
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
    today = date.today()
    if today.month == 12:
        nm_year, nm_month = today.year + 1, 1
    else:
        nm_year, nm_month = today.year, today.month + 1

    # 주차별 그룹핑 (1일~7일=1주차, 8일~14일=2주차, ...)
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

    today = date.today()

    if mode == "weekly":
        # 금요일 오후 3:30 → 다음 주 예고
        # 일요일 오전 9시  → 이번 주 예고
        if today.weekday() == 4:  # 금요일
            days_until_monday = 3  # 금→월 = 3일
            next_monday = today + timedelta(days=days_until_monday)
            week = next_week_schedule(schedule)
            msg = fmt_weekly(week, label="다음 주", monday=next_monday)
        else:  # 일요일
            next_monday = today + timedelta(days=1)
            week = this_week_schedule(schedule)
            msg = fmt_weekly(week, label="다음 주", monday=next_monday)
        send_telegram(msg)

    elif mode == "daily":
        # 매일 오전 8시: 항상 오늘 발표 일정 전송
        today_events = today_schedule(schedule)
        msg = fmt_daily(today_events)
        send_telegram(msg)

        # 말일이면 다음 달 예고 전송
        # 단, 오늘이 공휴일이면 9시(daily_late)에 전송하므로 여기서는 스킵
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
        # 매일 오전 9시: 말일 + 공휴일인 경우에만 다음 달 예고 전송
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
