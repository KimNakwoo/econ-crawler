# ============================================================
# crawler_fomc.py - FOMC 크롤러
# 대상: 성명서(Statement) + 기자회견(Press Conference) 전문
# 영문 원본 + 한국어 번역 동시 저장
# ============================================================

import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from config import URLS, REQUEST_TIMEOUT, REQUEST_DELAY
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
    """
    Federal Reserve 페이지에서 본문 텍스트 추출
    """
    # Fed 페이지 본문은 주로 div#content 또는 div.col-xs-12 안에 있음
    content_div = (
        soup.find("div", id="content")
        or soup.find("div", class_="col-xs-12")
        or soup.find("article")
        or soup.find("main")
    )

    if not content_div:
        # fallback: 모든 p 태그
        paragraphs = soup.find_all("p")
    else:
        paragraphs = content_div.find_all("p")

    lines = []
    for p in paragraphs:
        text = p.get_text(separator=" ").strip()
        # 너무 짧거나 네비게이션 텍스트 제거
        if text and len(text) > 20:
            lines.append(text)

    return "\n\n".join(lines)


def extract_presser(soup: BeautifulSoup) -> list:
    """
    기자회견 스크립트 추출
    반환: [{"speaker": "CHAIR POWELL", "text": "..."}, ...]
    """
    content_div = (
        soup.find("div", id="content")
        or soup.find("div", class_="col-xs-12")
        or soup.find("main")
    )

    if not content_div:
        paragraphs = soup.find_all("p")
    else:
        paragraphs = content_div.find_all("p")

    exchanges = []
    current_speaker = "UNKNOWN"
    current_lines = []

    for p in paragraphs:
        text = p.get_text(separator=" ").strip()
        if not text or len(text) < 5:
            continue

        # 발언자 감지 (예: "CHAIR POWELL.", "REPORTER.", "MS. LOGAN.")
        is_speaker = (
            text.isupper()
            or text.endswith(".")
            and len(text) < 60
            and text == text.upper()
        )

        # 더 정확한 발언자 패턴
        import re
        speaker_pattern = re.match(r"^([A-Z][A-Z\s\.]{2,40})\.\s*$", text)

        if speaker_pattern:
            # 이전 발언자 저장
            if current_lines:
                exchanges.append({
                    "speaker": current_speaker,
                    "text": "\n\n".join(current_lines),
                })
                current_lines = []
            current_speaker = speaker_pattern.group(1).strip()
        else:
            current_lines.append(text)

    # 마지막 발언자 저장
    if current_lines:
        exchanges.append({
            "speaker": current_speaker,
            "text": "\n\n".join(current_lines),
        })

    return exchanges


# ------------------------------------------------------------
# FOMC 성명서 크롤링
# ------------------------------------------------------------

def run_fomc_statement():
    """FOMC 성명서 크롤링 → 원문 + 번역 저장"""
    url = URLS.get("fomc_statement")
    if not url:
        print("  [FOMC 성명서] URL이 config.py에 설정되지 않았습니다.")
        return

    print(f"  [FOMC 성명서] 크롤링 시작: {url}")
    date_str = datetime.now().strftime("%Y-%m-%d")

    try:
        soup = fetch_page(url)
        body_en = extract_fed_article(soup)

        if not body_en:
            print("  [FOMC 성명서] 본문을 가져오지 못했습니다.")
            return

        print(f"  [FOMC 성명서] 본문 추출 완료 ({len(body_en)}자) → 번역 시작...")
        body_ko = translate_paragraph_by_paragraph(body_en)

        # 마크다운 구성
        md = md_header(f"FOMC 성명서 - {date_str}", 1)
        md += f"\n> 출처: {url}\n\n"

        md += md_header("📋 한국어 번역", 2)
        md += body_ko + "\n\n"

        md += md_header("📄 영문 원본", 2)
        md += body_en + "\n\n"

        md += md_meta(url, "FOMC")

        save_markdown("fomc", "FOMC_성명서", md, date_str)
        print(f"  [FOMC 성명서] 완료")

    except Exception as e:
        print(f"  [FOMC 성명서] 오류: {e}")
        raise


# ------------------------------------------------------------
# FOMC 기자회견 크롤링
# ------------------------------------------------------------

def run_fomc_presser():
    """FOMC 기자회견 전문 크롤링 → 발언자별 정리 + 번역"""
    url = URLS.get("fomc_presser")
    if not url:
        print("  [FOMC 기자회견] URL이 config.py에 설정되지 않았습니다.")
        return

    print(f"  [FOMC 기자회견] 크롤링 시작: {url}")
    date_str = datetime.now().strftime("%Y-%m-%d")

    try:
        soup = fetch_page(url)
        exchanges = extract_presser(soup)

        if not exchanges:
            # fallback: 단순 전체 텍스트
            body_en = extract_fed_article(soup)
            if not body_en:
                print("  [FOMC 기자회견] 본문을 가져오지 못했습니다.")
                return
            exchanges = [{"speaker": "전체", "text": body_en}]

        print(f"  [FOMC 기자회견] {len(exchanges)}개 발언 블록 추출 → 번역 시작...")

        # 마크다운 구성
        md = md_header(f"FOMC 기자회견 전문 - {date_str}", 1)
        md += f"\n> 출처: {url}\n\n"
        md += "> **구성**: 발언자별 한국어 번역 + 영문 원본\n\n"

        for i, exchange in enumerate(exchanges, 1):
            speaker = exchange["speaker"]
            text_en = exchange["text"]

            # 번역
            print(f"  [FOMC 기자회견] 번역 중 ({i}/{len(exchanges)}): {speaker[:30]}...")
            text_ko = translate_paragraph_by_paragraph(text_en)

            md += f"---\n\n"
            md += md_header(f"🎙️ {speaker}", 3)
            md += f"**[번역]**\n\n{text_ko}\n\n"
            md += f"**[원문]**\n\n{text_en}\n\n"

        md += md_meta(url, "FOMC")

        save_markdown("fomc", "FOMC_기자회견", md, date_str)
        print(f"  [FOMC 기자회견] 완료")

    except Exception as e:
        print(f"  [FOMC 기자회견] 오류: {e}")
        raise


# ------------------------------------------------------------
# 통합 실행
# ------------------------------------------------------------

def run_fomc():
    """성명서 + 기자회견 모두 실행"""
    run_fomc_statement()
    run_fomc_presser()


if __name__ == "__main__":
    run_fomc()
