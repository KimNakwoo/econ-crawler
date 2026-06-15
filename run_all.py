# ============================================================
# run_all.py - 경제지표 크롤러 메인 실행 파일
# 오늘 발표 지표를 자동 감지하여 해당 크롤러만 실행
# + 연준 의장 연설 / FEDS Notes / FOMC 의사록은 매일 체크 (새벽 5시 전용)
# ============================================================

import os
from datetime import datetime
from config import OUTPUT_FOLDERS, IS_GITHUB

# ────────────────────────────────────────────────────────────
# 실행 트리거 판단
#
# - 새벽 5시(KST) 전용 크론('0 20 * * 0-4'): 매일 체크
#   (FOMC의사록/연준연설/FEDS_Notes) 전담. today_flags 기반 지표
#   (CPI/PPI/NFP/FOMC/베이지북)는 다른 크론에서 처리하므로 스킵
#   → 같은 날 중복 실행/중복 번역 방지.
# - 그 외 크론(21:31/22:31/03:31/04:31): today_flags 기반 지표만 처리,
#   매일 체크는 스킵.
# - workflow_dispatch(수동 실행) / 로컬 실행: 둘 다 처리(테스트 편의).
# ────────────────────────────────────────────────────────────
DAILY_CHECK_CRON = "0 20 * * 0-4"
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
            print("[INFO] 수동 실행 모드로 전환 (모든 지표 OFF)")
            today_flags = {"cpi": False, "ppi": False, "nfp": False, "fomc": False, "beige": False}
            calendar = []

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
                run_fomc_statement()
                run_fomc_presser()
                results.append(("FOMC", "✅ 완료"))
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
