# ============================================================
# crawler_fomc.py - FOMC 크롤러
# 대상:
#   - 성명서(Statement)
#   - 기자회견(Press Conference) 전문
#   - 의사록(Minutes) ← 신규: 회의 약 3주 후 공개
# ============================================================

import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from config import OUTPUT_FOLDERS, FED_URL_PATTERNS, FED_RSS, REQUEST_TIMEOUT, REQUEST_DELAY
from utils import (
    save_markdown,
    translate_paragraph_by_paragraph,
    md_header,
    md_meta,
    get_headers,
)


def fetch_page(url: str) -> BeautifulSoup:
    time.sleep(REQUEST_DELAY)
    resp = requests.get(url, headers=get_headers(), timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "lxml")


def extract_fed_article(soup: BeautifulSoup) -> str:
    """Federal Reserve 페이지에서 본문 텍스트 추출"""
    content_div = (
        soup.find("div", id="content")
        or soup.find("div", class_="col-xs-12")
        or soup.find("article")
        or soup.find("main")
    )

    paragraphs = content_div.find_all("p") if content_div else soup.find_all("p")

    lines = []
    for p in paragraphs:
        text = p.get_text(separator=" ").strip()
        if text and len(text) > 20:
            lines.append(text)

    return "\n\n".join(lines)


def extract_presser(soup: BeautifulSoup) -> list:
    """
    기자회견 스크립트에서 발언자별 블록 추출
    반환: [{"speaker": "CHAIR POWELL", "text": "..."}, ...]
    """
    content_div = (
        soup.find("div", id="content")
        or soup.find("div", class_="col-xs-12")
        or soup.find("main")
    )

    paragraphs = content_div.find_all("p") if content_div else soup.find_all("p")

    exchanges = []
    current_speaker = "UNKNOWN"
    current_lines = []

    for p in paragraphs:
        text = p.get_text(separator=" ").strip()
        if not text or len(text) < 5:
            continue

        speaker_pattern = re.match(r"^([A-Z][A-Z\s\.]{2,40})\.\s*$", text)

        if speaker_pattern:
            if current_lines:
                exchanges.append({
                    "speaker": current_speaker,
                    "text": "\n\n".join(current_lines),
                })
                current_lines = []
            current_speaker = speaker_pattern.group(1).strip()
        else:
            current_lines.append(text)

    if current_lines:
        exchanges.append({
            "speaker": current_speaker,
            "text": "\n\n".join(current_lines),
        })

    return exchanges


# ─── FOMC 의사록 URL 탐색 ─────────────────────────────────────

def find_latest_minutes_url() -> tuple:
    """
    FOMC 캘린더 페이지에서 가장 최근 의사록(Minutes) URL 탐색
    반환: (url, meeting_date_str) or (None, None)
    """
    try:
        resp = requests.get(FED_RSS["fomc_cal"], headers=get_headers(), timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        # "Minutes" 링크 탐색 - 가장 먼저 나오는 것이 최신
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "fomcminutes" in href:
                url = href if href.startswith("http") else "https://www.federalreserve.gov" + href
                # 날짜 추출 (예: fomcminutes20260507.htm → 2026-05-07)
                m = re.search(r"fomcminutes(\d{8})", href)
                if m:
                    d = m.group(1)
                    date_str = f"{d[:4]}-{d[4:6]}-{d[6:]}"
                    return url, date_str

    except Exception as e:
        print(f"[FOMC 의사록] 캘린더 조회 실패: {e}")

    return None, None


def _minutes_processed_path() -> str:
    folder = OUTPUT_FOLDERS["minutes"]
    import os
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, ".processed.txt")


def is_minutes_processed(date_str: str) -> bool:
    path = _minutes_processed_path()
    import os
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        return date_str in f.read()


def mark_minutes_processed(date_str: str):
    path = _minutes_processed_path()
    with open(path, "a", encoding="utf-8") as f:
        f.write(date_str + "\n")


# ─── FOMC 성명서 크롤링 ──────────────────────────────────────

def run_fomc_statement():
    """FOMC 성명서 크롤링 → 원문 + 번역 저장"""
    date_str = datetime.now().strftime("%Y%m%d")
    url = FED_URL_PATTERNS["fomc_statement"].format(date=date_str)

    print(f"  [FOMC 성명서] 크롤링 시작: {url}")
    display_date = datetime.now().strftime("%Y-%m-%d")

    try:
        soup = fetch_page(url)
        body_en = extract_fed_article(soup)

        if not body_en:
            print("  [FOMC 성명서] 본문을 가져오지 못했습니다.")
            return

        print(f"  [FOMC 성명서] 본문 {len(body_en)}자 → 번역 시작")
        body_ko = translate_paragraph_by_paragraph(body_en)

        md = md_header(f"FOMC 성명서 - {display_date}", 1)
        md += f"\n> 출처: {url}\n\n"
        md += md_header("📋 한국어 번역", 2)
        md += body_ko + "\n\n"
        md += md_header("📄 영문 원본", 2)
        md += body_en + "\n\n"
        md += md_meta(url, "FOMC")

        save_markdown("fomc_statement", "FOMC_성명서", md, display_date)
        print("  [FOMC 성명서] 완료")

    except Exception as e:
        print(f"  [FOMC 성명서] 오류: {e}")
        raise


# ─── FOMC 기자회견 크롤링 ─────────────────────────────────────

def run_fomc_presser():
    """FOMC 기자회견 전문 크롤링 → 발언자별 정리 + 번역"""
    date_str = datetime.now().strftime("%Y%m%d")
    url = FED_URL_PATTERNS["fomc_presser"].format(date=date_str)

    print(f"  [FOMC 기자회견] 크롤링 시작: {url}")
    display_date = datetime.now().strftime("%Y-%m-%d")

    try:
        soup = fetch_page(url)
        exchanges = extract_presser(soup)

        if not exchanges:
            body_en = extract_fed_article(soup)
            if not body_en:
                print("  [FOMC 기자회견] 본문을 가져오지 못했습니다.")
                return
            exchanges = [{"speaker": "전체", "text": body_en}]

        print(f"  [FOMC 기자회견] {len(exchanges)}개 발언 블록 → 번역 시작")

        md = md_header(f"FOMC 기자회견 전문 - {display_date}", 1)
        md += f"\n> 출처: {url}\n\n"
        md += "> **구성**: 발언자별 한국어 번역 + 영문 원본\n\n"

        for i, exchange in enumerate(exchanges, 1):
            speaker = exchange["speaker"]
            text_en = exchange["text"]
            print(f"  [FOMC 기자회견] 번역 중 ({i}/{len(exchanges)}): {speaker[:30]}...")
            text_ko = translate_paragraph_by_paragraph(text_en)

            md += "---\n\n"
            md += md_header(f"🎙️ {speaker}", 3)
            md += f"**[번역]**\n\n{text_ko}\n\n"
            md += f"**[원문]**\n\n{text_en}\n\n"

        md += md_meta(url, "FOMC")

        save_markdown("fomc_presser", "FOMC_기자회견", md, display_date)
        print("  [FOMC 기자회견] 완료")

    except Exception as e:
        print(f"  [FOMC 기자회견] 오류: {e}")
        raise


# ─── FOMC 의사록 크롤링 (신규) ───────────────────────────────

def run_minutes():
    """
    FOMC 의사록 크롤링 → 원문 + 번역 저장
    - FOMC 캘린더에서 최신 의사록 URL 자동 탐색
    - 이미 처리한 의사록은 스킵
    - 회의 약 3주 후 공개되므로 매일 체크
    """
    print("[FOMC 의사록] 시작")

    url, date_str = find_latest_minutes_url()
    if not url:
        print("[FOMC 의사록] 최신 의사록 URL을 찾을 수 없음")
        return False

    print(f"[FOMC 의사록] 최신 의사록: {date_str} → {url}")

    if is_minutes_processed(date_str):
        print(f"[FOMC 의사록] 이미 처리됨 ({date_str}) - 스킵")
        return False

    try:
        soup = fetch_page(url)
        body_en = extract_fed_article(soup)

        if not body_en or len(body_en) < 500:
            print("[FOMC 의사록] 본문이 너무 짧거나 없음 (아직 미공개일 수 있음)")
            return

        print(f"[FOMC 의사록] 본문 {len(body_en)}자 → 섹션 분할 후 번역")

        # 의사록은 길이가 매우 길므로 섹션별로 분할하여 번역
        # 주요 섹션 헤더 패턴 (Fed 의사록 표준 구조)
        section_patterns = [
            r"Staff Review of the Economic Situation",
            r"Staff Review of the Financial Situation",
            r"Staff Economic Outlook",
            r"Participants['’] Views",
            r"Committee Policy Action",
            r"Developments in Financial Markets",
        ]

        sections = _split_minutes_sections(body_en, section_patterns)
        print(f"[FOMC 의사록] {len(sections)}개 섹션 분할 완료")

        md = md_header(f"FOMC 의사록 - {date_str}", 1)
        md += f"\n> 회의일: {date_str}\n"
        md += f"> 출처: {url}\n\n"
        md += "> **핵심 섹션만 번역합니다** (전체 번역은 분량 관계로 섹션 요약)\n\n"

        for sec_title, sec_body in sections:
            print(f"[FOMC 의사록] 번역 중: {sec_title[:50]}")
            sec_ko = translate_paragraph_by_paragraph(sec_body)

            md += md_header(f"📌 {sec_title}", 2)
            md += md_header("한국어 번역", 3)
            md += sec_ko + "\n\n"
            md += md_header("영문 원본", 3)
            md += sec_body + "\n\n"

        md += md_meta(url, "FOMC의사록")

        save_markdown("minutes", "FOMC_의사록", md, date_str)
        mark_minutes_processed(date_str)
        print(f"[FOMC 의사록] 완료: {date_str}")
        return True

    except Exception as e:
        print(f"[FOMC 의사록] 오류: {e}")
        raise


def _split_minutes_sections(body: str, patterns: list) -> list:
    """
    의사록 본문을 섹션별로 분할
    반환: [(섹션제목, 섹션본문), ...]
    섹션 미탐지 시 전체를 하나의 섹션으로 반환
    """
    # 줄 단위로 분할 후 헤더 탐색
    lines = body.split("\n\n")
    sections = []
    current_title = "전문"
    current_lines = []

    for line in lines:
        matched_section = None
        for pat in patterns:
            if re.search(pat, line, re.IGNORECASE):
                matched_section = line.strip()[:80]
                break

        if matched_section:
            if current_lines:
                sections.append((current_title, "\n\n".join(current_lines)))
            current_title = matched_section
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_title, "\n\n".join(current_lines)))

    # 섹션이 없으면 전체를 3등분
    if len(sections) <= 1 and body:
        chunk_size = len(body) // 3
        sections = [
            ("전반부",  body[:chunk_size]),
            ("중반부",  body[chunk_size:2*chunk_size]),
            ("후반부",  body[2*chunk_size:]),
        ]

    return sections


# ─── 통합 실행 ───────────────────────────────────────────────

def run_fomc():
    """성명서 + 기자회견 실행 (FOMC 당일)"""
    run_fomc_statement()
    run_fomc_presser()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "minutes":
        run_minutes()
    else:
        run_fomc()
