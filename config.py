import os

# ============================================================
# config.py - 환경 설정
# GitHub Actions 실행 시 자동으로 클라우드 경로로 전환됩니다
# ============================================================

# 실행 환경 감지
IS_GITHUB = bool(os.environ.get("GITHUB_ACTIONS"))

if IS_GITHUB:
    # GitHub Actions: 스크립트 위치 기준 output/ 폴더
    BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
else:
    # 로컬 PC: Obsidian 경로 직접 지정
    BASE_PATH = r"C:\Users\user\Desktop\ALL\obsidian\경제지표"

_FED = os.path.join(BASE_PATH, "연준")  # 연준 관련 자료 상위 폴더

OUTPUT_FOLDERS = {
    # ── 경제지표 ─────────────────────────────────────────────
    "cpi":            os.path.join(BASE_PATH, "CPI"),
    "ppi":            os.path.join(BASE_PATH, "PPI"),
    "nfp":            os.path.join(BASE_PATH, "비농업고용"),
    "beige":          os.path.join(BASE_PATH, "베이지북"),
    # ── 연준 하위 항목 ────────────────────────────────────────
    "fomc_statement": os.path.join(_FED, "성명서"),
    "fomc_presser":   os.path.join(_FED, "기자회견"),
    "minutes":        os.path.join(_FED, "의사록"),
    "speech":         os.path.join(_FED, "의장연설"),
    "feds_notes":     os.path.join(_FED, "FEDS_Notes"),
}

# ── BLS 공식 URL (고정)
URLS = {
    "cpi":  "https://www.bls.gov/news.release/cpi.nr0.htm",
    "ppi":  "https://www.bls.gov/news.release/ppi.nr0.htm",
    "nfp":  "https://www.bls.gov/news.release/empsit.nr0.htm",
}

# ── Fed URL 패턴 (날짜 기반 자동 생성)
FED_URL_PATTERNS = {
    "fomc_statement": "https://www.federalreserve.gov/newsevents/pressreleases/monetary{date}a.htm",
    "fomc_presser":   "https://www.federalreserve.gov/monetarypolicy/fomcpresconf{date}.htm",
    "fomc_minutes":   "https://www.federalreserve.gov/monetarypolicy/fomcminutes{date}.htm",
    "beige":          "https://www.federalreserve.gov/monetarypolicy/beigebook{yearmonth}.htm",
}

# ── Fed RSS / 목록 URL
FED_RSS = {
    "speeches":   "https://www.federalreserve.gov/feeds/speeches.xml",
    "feds_notes": "https://www.federalreserve.gov/econres/notes/feds-notes/default.htm",
    "fomc_cal":   "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm",
    "board_bios": "https://www.federalreserve.gov/aboutthefed/bios/board/default.htm",
}

# ── 번역 설정
TRANSLATE_ENGINE = "google"   # 무료, API 키 불필요
DEEPL_API_KEY    = ""

# ── 요청 설정
REQUEST_DELAY   = 2
REQUEST_TIMEOUT = 30

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
