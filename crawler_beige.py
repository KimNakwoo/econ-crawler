# ============================================================
# crawler_beige.py - 베이지북(Beige Book) 크롤러
# Federal Reserve 공식 사이트에서 전문 수집 + 한국어 번역
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


def extract_beige_sections(soup: BeautifulSoup) -> list:
    """
    베이지북 섹션별 추출
    반환: [{"title": "Overview", "text": "..."}, {"title": "Boston", "text": "..."}, ...]
    """
    sections = []

    content = (
        soup.find("div", id="content")
        or soup.find("div", class_="col-xs-12")
        or soup.find("main")
        or soup
    )

    # 섹션 헤더 찾기 (h2, h3, h4)
    current_title = "개요"
    current_paragraphs = []

    for element in content.find_all(["h2", "h3", "h4", "p"]):
        tag = element.name

        if tag in ["h2", "h3", "h4"]:
            # 이전 섹션 저장
            if current_paragraphs:
                sections.append({
                    "title": current_title,
                    "text": "\n\n".join(current_paragraphs),
                })
                current_paragraphs = []
            current_title = element.get_text(separator=" ").strip()

        elif tag == "p":
            text = element.get_text(separator=" ").strip()
            if text and len(text) > 20:
                current_paragraphs.append(text)

    # 마지막 섹션 저장
    if current_paragraphs:
        sections.append({
            "title": current_title,
            "text": "\n\n".join(current_paragraphs),
        })

    # 섹션이 없으면 전체 p 태그로 fallback
    if not sections:
        all_text = "\n\n".join(
            p.get_text(separator=" ").strip()
            for p in content.find_all("p")
            if len(p.get_text(separator=" ").strip()) > 20
        )
        if all_text:
            sections = [{"title": "전문", "text": all_text}]

    return sections


def run_beige():
    """베이지북 전문 크롤링 → 섹션별 원문 + 번역 저장"""
    url = URLS.get("beige")
    if not url:
        print("  [베이지북] URL이 config.py에 설정되지 않았습니다.")
        return

    print(f"  [베이지북] 크롤링 시작: {url}")
    date_str = datetime.now().strftime("%Y-%m-%d")

    try:
        soup = fetch_page(url)
        sections = extract_beige_sections(soup)

        if not sections:
            print("  [베이지북] 본문을 가져오지 못했습니다.")
            return

        print(f"  [베이지북] {len(sections)}개 섹션 추출 완료 → 번역 시작...")

        # 마크다운 구성
        md = md_header(f"베이지북(Beige Book) - {date_str}", 1)
        md += f"\n> 출처: {url}\n\n"
        md += "> **구성**: 섹션별 한국어 번역 + 영문 원본 (지역별 경제 현황 포함)\n\n"

        # 목차
        md += md_header("목차", 2)
        for i, sec in enumerate(sections, 1):
            md += f"{i}. {sec['title']}\n"
        md += "\n"

        # 섹션별 번역 + 원문
        for i, section in enumerate(sections, 1):
            title = section["title"]
            text_en = section["text"]

            print(f"  [베이지북] 번역 중 ({i}/{len(sections)}): {title[:40]}...")
            text_ko = translate_paragraph_by_paragraph(text_en)

            md += f"---\n\n"
            md += md_header(f"{i}. {title}", 2)

            md += md_header("🇰🇷 한국어 번역", 3)
            md += text_ko + "\n\n"

            md += md_header("🇺🇸 영문 원본", 3)
            md += text_en + "\n\n"

        md += md_meta(url, "베이지북")

        save_markdown("beige", "베이지북", md, date_str)
        print(f"  [베이지북] 완료")

    except Exception as e:
        print(f"  [베이지북] 오류: {e}")
        raise


if __name__ == "__main__":
    run_beige()
