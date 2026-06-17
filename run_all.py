# ============================================================
# run_all.py - 경제지표 크롤러 메인 실행 파일
# 오늘 발표 지표를 자동 감지하여 해당 크롤러만 실행
# + 연준 의장 연설 / FEDS Notes / FOMC 의사록은 매일 체크 (새벽 5시 전용)
# ============================================================

import os
from datetime import datetime, date, timezone, timedelta
from config import OUTPUT_FOLDERS, IS_GITHUB

# ────────────────────────────────────────────────────────────
# 실행 트리거 판단
#
# - 자정(KST) 전용 크론('0 15 * * 0-4'): 매일 체크
#   (FOMC의사록/연준연설/FEDS_Notes) 전담. today_flags 기반 지표
#   (CPI/PPI/NFP/FOMC/베이지북)는 다른 크론에서 처리하므로 스킵
#   → 같은 날 중복 실행/중복 번역 방지.
# - 그 외 크론(21:31/22:31/03:31/04:31): today_flags 기반 지표만 처리,
#   매일 체크는 스킵.
# - workflow_dispatch(수동 실행) / 로컬 실행: 둘 다 처리(테스트 편의).
# ────────────────────────────────────────────────────────────
DAILY_CHECK_CRON = "0 15 * * 0-4"

# ────────────────────────────────────────────────────────────
# 하드코딩 발표 일정 (Investing.com 차단 시 폴백용)
# BLS_SCHEDULE / FOMC_SCHEDULE (notifier.py)과 동기화 필요
# ────────────────────────────────────────────────────────────
_KST = timezone(timedelta(hours=9))

_HARDCODED_SCHEDULE: dict = {
    "cpi": [
        (2026,  1, 15), (2026,  2, 12), (2026,  3, 12), (2026,  4, 10),
        (2026,  5, 13), (2026,  6, 10), (2026,  7, 14), (2026,  8, 12),
        (2026,  9, 11), (2026, 10, 14), (2026, 11, 12), (2026, 12, 10),
    ],
    "ppi": [
        (2026,  1, 16), (2026,  2, 13), (2026,  3, 13), (2026,  4, 11),
        (2026,  5, 14), (2026,  6, 11), (2026,  7, 15), (2026,  8, 13),
        (2026,  9, 15), (2026, 10, 16), (2026, 11, 13), (2026, 12, 11),
    ],
    "nfp": [
        (2026,  1,  9), (2026,  2,  6), (2026,  3,  6), (2026,  4,  3),
        (2026,  5,  1), (2026,  6,  5), (2026,  7,  3), (2026,  8,  7),
        (2026,  9,  4), (2026, 10,  2), (2026, 11,  6), (2026, 12,  4),
    ],
    "fomc": [
        (2026,  1, 28), (2026,  3, 18), (2026,  4, 29), (2026,  6, 17),
        (2026,  7, 29), (2026,  9, 16), (2026, 10, 28), (2026, 12,  9),
    ],
}

def _today_kst() -> date:
    return datetime.now(_KST).date()

def _get_today_flags_from_schedule() -> dict:
    """Investing.com 실패 시 하드코딩 날짜로 today_flags 결정"""
    today = _today_kst()
    flags = {"cpi": False, "ppi": False, "nfp": False, "fomc": False, "beige": False}
    for indicator, dates in _HARDCODED_SCHEDULE.items():
        for y, m, d in dates:
            if date(y, m, d) == today:
                flags[indicator] = True
                break
    return flags
_cron_schedule = os.environ.get("CRON_SCHEDULE", "")
_event_name = os.environ.get("GITHUB_EVENT_NAME", "")

IS_DAILY_CHECK_RUN = (_cron_schedule == DAILY_CHECK_CRON)

RUN_SCHEDULED_INDICATORS = (
    not IS_GITHUB
    or not IS_DAILY_CHECK_RUN
    or _event_name == "workflow_dispatch"
)
RUN_DAILY_CHECK = (
    not IS_GITHUB
    or IS_DAILY_CHECK_RUN
    or _event_name == "workflow_dispatch"
)


def ensure_folders():
    """출력 폴더가 없으면 생성"""
    for path in OUTPUT_FOLDERS.values():
        os.makedirs(path, exist_ok=True)

def save_run_log(results: list):
    """
    실행 결과를 output/.last_run.txt에 저장
    GitHub Actions에서 텔레그램 알림 메시지 생성에 활용
    """
    if not IS_GITHUB:
        return
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", ".last_run.txt")
    kst_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    lines = [f"TIME={kst_time} UTC"]
    for indicator, status in results:
        lines.append(f"{indicator}={status}")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    ensure_folders()
    results = []  # [(지표명, 상태), ...]

    # ────────────────────────────────────────────────────────────
    # 오늘 발표 지표 (today_flags 기반) - 새벽 5시 전용 크론에서는 스킵
    # ────────────────────────────────────────────────────────────
    if RUN_SCHEDULED_INDICATORS:
        # ── Investing.com에서 오늘 발표 지표 자동 감지 ──────────────
        try:
            from crawler_investing import fetch_calendar, detect_today_indicators, get_forecast_for
            print("[INFO] Investing.com 캘린더 확인 중...")
            calendar = fetch_calendar()
            today_flags = detect_today_indicators(calendar)
            print(f"[INFO] 오늘 발표 지표: { {k: v for k, v in today_flags.items() if v} }")
        except Exception as e:
            print(f"[WARNING] Investing.com 감지 실패: {e}")
            print("[INFO] 하드코딩 일정으로 폴백 (BLS_SCHEDULE / FOMC_SCHEDULE 기준)")
            today_flags = _get_today_flags_from_schedule()
            active = {k: v for k, v in today_flags.items() if v}
            print(f"[INFO] 하드코딩 기반 오늘 지표: {active if active else '없음'}")
            calendar = []

        # ── 강제 실행 지표 (workflow_dispatch 수동 입력) ─────────────
        _force = os.environ.get("FORCE_INDICATORS", "").strip()
        if _force:
            print(f"[INFO] 강제 실행 지표 지정: {_force}")
            for _ind in _force.split(","):
                _ind = _ind.strip().lower()
                if _ind in today_flags:
                    today_flags[_ind] = True
                    print(f"[INFO] {_ind.upper()} 강제 실행 ON")

        # ── CPI ─────────────────────────────────────────────────────
        if today_flags.get("cpi"):
            try:
                from crawler_bls import run_cpi
                forecast = get_forecast_for("cpi", calendar) if calendar else {}
                run_cpi(forecast)
                results.append(("CPI", "✅ 완료"))
            except Exception as e:
                print(f"[ERROR] CPI 실패: {e}")
                results.append(("CPI", "❌ 실패"))

        # ── PPI ─────────────────────────────────────────────────────
        if today_flags.get("ppi"):
            try:
                from crawler_bls import run_ppi
                forecast = get_forecast_for("ppi", calendar) if calendar else {}
                run_ppi(forecast)
                results.append(("PPI", "✅ 완료"))
            except Exception as e:
                print(f"[ERROR] PPI 실패: {e}")
                results.append(("PPI", "❌ 실패"))

        # ── NFP ─────────────────────────────────────────────────────
        if today_flags.get("nfp"):
            try:
                from crawler_bls import run_nfp
                forecast = get_forecast_for("nfp", calendar) if calendar else {}
                run_nfp(forecast)
                results.append(("비농업고용(NFP)", "✅ 완료"))
            except Exception as e:
                print(f"[ERROR] NFP 실패: {e}")
                results.append(("비농업고용(NFP)", "❌ 실패"))

        # ── FOMC ─────────────────────────────────────────────────────
        if today_flags.get("fomc"):
            try:
                from crawler_fomc import run_fomc_statement, run_fomc_presser
                ok_stmt   = run_fomc_statement()
                ok_presser = run_fomc_presser()
                if ok_stmt or ok_presser:
                    results.append(("FOMC", "✅ 완료"))
                else:
                    results.append(("FOMC", "⏳ 미발표 (재시도 필요)"))
            except Exception as e:
                print(f"[ERROR] FOMC 실패: {e}")
                results.append(("FOMC", "❌ 실패"))

        # ── 베이지북 ─────────────────────────────────────────────────
        if today_flags.get("beige"):
            try:
                from crawler_beige import run_beige
                run_beige()
                results.append(("베이지북", "✅ 완료"))
            except Exception as e:
                print(f"[ERROR] 베이지북 실패: {e}")
                results.append(("베이지북", "❌ 실패"))
    else:
        print("[INFO] 새벽 5시 매일체크 전용 실행 - 발표일 기반 지표(CPI/PPI/NFP/FOMC/베이지북)는 스킵")

    # ────────────────────────────────────────────────────────────
    # 매일 체크 항목 (발표일과 무관, 새벽 5시 크론 또는 수동 실행에서만)
    # ────────────────────────────────────────────────────────────
    if RUN_DAILY_CHECK:
        # ── FOMC 의사록 (회의 약 3주 후 공개, 매일 체크) ────────────
        try:
            from crawler_fomc import run_minutes
            found = run_minutes()
            if found:
                results.append(("FOMC의사록", "✅ 완료"))
        except Exception as e:
            print(f"[ERROR] FOMC 의사록 실패: {e}")
            results.append(("FOMC의사록", "❌ 실패"))

        # ── 연준 의장 연설 (매일 체크) ───────────────────────────────
        try:
            from crawler_fed_speech import run_speech
            found = run_speech()
            if found:
                results.append(("연준의장연설", "✅ 완료"))
        except Exception as e:
            print(f"[ERROR] 연설 크롤링 실패: {e}")
            results.append(("연준의장연설", "❌ 실패"))

        # ── FEDS Notes (매일 체크) ───────────────────────────────────
        try:
            from crawler_feds_notes import run_feds_notes
            found = run_feds_notes()
            if found:
                results.append((f"FEDS_Notes", "✅ 완료"))
        except Exception as e:
            print(f"[ERROR] FEDS Notes 실패: {e}")
            results.append(("FEDS_Notes", "❌ 실패"))
    else:
        print("[INFO] 매일체크(의사록/연설/FEDS_Notes)는 새벽 5시 전용 - 이번 실행에서는 스킵")

    # ── 실행 결과 요약 ───────────────────────────────────────────
    if results:
        print("\n" + "="*40)
        print("실행 결과:")
        for name, status in results:
            print(f"  {name}: {status}")
        print("="*40)
        save_run_log(results)
    else:
        print("[INFO] 오늘 발표 지표 없음 / 새 연구자료 없음. 종료.")

if __name__ == "__main__":
    main()
