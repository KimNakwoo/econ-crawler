# ============================================================
# crawler_beige.py - 베이지북(Beige Book) 크롤러
# Federal Reserve 공식 사이트에서 전문 수집 + 한국어 번역
# ============================================================

import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config import FED_URL_PATTERNS, REQUEST_TIMEOUT, REQUEST_DELAY
from utils import (
    save_markdown,
    translate_paragraph_by_paragraph,
    md_header,
    md_meta,
    get_headers,
)

FED_BASE = "https://www.federalreserve.gov"


def find_latest_beige_url() -> str:
    """
    최근 6개월 이내 가장 최신 베이지북 URL 탐색
    베이지북은 연 8회 발행 (주로 1, 3, 4, 6, 7, 9, 10, 11월)
    """
    pattern = FED_URL_PATTERNS["beige"]
    today = datetime.now()

    # 오늘 포함 최근 6개월을 역순으로 시도
    for i in range(6):
        dt = today.replace(day=1) - timedelta(days=i * 28)
        yearmonth = dt.strftime("%Y%m")
        url = pattern.format(yearmonth=yearmonth)
        try:
            resp = requests.head(url, headers=get_headers(), timeout=10)
            if resp.status_code == 200:
                print(f"  [베이지북] URL 확인: {url}")
                return url
        except Exception:
            continue

    return ""


def fetch_page(url: str) -> BeautifulSoup:
    time.sleep(REQUEST_DELAY)
    resp = requests.get(url, headers=get_headers(), timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "lxml")


def extract_beige_sections(soup: BeautifulSoup) -> tuple:
    """
    베이지북 섹션별 추출 + 이미지 URL 수집
    반환: ([{"title": ..., "text": ...}, ...], [image_url, ...])
    """
    content = (
        soup.find("div", id="content")
        or soup.find("div", class_="col-xs-12")
        or soup.find("main")
        or soup
    )

    # 이미지 수집
    image_urls = []
    seen = set()
    skip_words = ["icon", "logo", "banner", "button", "arrow", "bullet",
                  "spacer", "pixel", "flag", "dot-gov"]
    for img in content.find_all("img"):
        src = img.get("src", "").strip()
        if not src or any(w in src.lower() for w in skip_words):
            continue
        if src.startswith("//"):
            src = "https:" + src
        elif not src.startswith("http"):
            src = FED_BASE + src
        if src not in seen:
            seen.add(src)
            image_urls.append(src)

    # 섹션 추출
    sections = []
    current_title = "개요"
    current_paragraphs = []

    for element in content.find_all(["h2", "h3", "h4", "p"]):
        tag = element.name
        if tag in ["h2", "h3", "h4"]:
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

    if current_paragraphs:
        sections.append({
            "title": current_title,
            "text": "\n\n".join(current_paragraphs),
        })

    if not sections:
        all_text = "\n\n".join(
            p.get_text(separator=" ").strip()
            for p in content.find_all("p")
            if len(p.get_text(separator=" ").strip()) > 20
        )
        if all_text:
            sections = [{"title": "전문", "text": all_text}]

    return sections, image_urls


def run_beige():
    """베이지북 전문 크롤링 → 섹션별 번역 저장"""
    url = find_latest_beige_url()
    if not url:
        print("  [베이지북] 최신 URL을 찾을 수 없습니다.")
        return

    print(f"  [베이지북] 크롤링 시작: {url}")
    date_str = datetime.now().strftime("%Y-%m-%d")

    try:
        soup = fetch_page(url)
        sections, image_urls = extract_beige_sections(soup)

        if not sections:
            print("  [베이지북] 본문을 가져오지 못했습니다.")
            return

        print(f"  [베이지북] {len(sections)}개 섹션 추출 완료 → 번역 시작...")

        # 마크다운 구성
        md = md_header(f"베이지북 / Beige Book - {date_str}", 1)
        md += f"\n> 출처: {url}\n\n"

        # 목차
        md += md_header("목차", 2)
        for i, sec in enumerate(sections, 1):
            md += f"{i}. {sec['title']}\n"
        md += "\n"

        # 섹션별 번역
        for i, section in enumerate(sections, 1):
            title = section["title"]
            text_en = section["text"]
            print(f"  [베이지북] 번역 중 ({i}/{len(sections)}): {title[:40]}...")
            text_ko = translate_paragraph_by_paragraph(text_en)

            md += "---\n\n"
            md += md_header(f"{i}. {title}", 2)
            md += text_ko + "\n\n"

        # 이미지
        if image_urls:
            md += md_header("🖼️ 그림 및 차트", 2)
            for i, img_url in enumerate(image_urls, 1):
                md += f"![Figure {i}]({img_url})\n\n"
                md += f"> [원본 링크]({img_url})\n\n"

        md += md_meta(url, "베이지북")

        save_markdown("beige", "베이지북", md, date_str)
        print("  [베이지북] 완료")

    except Exception as e:
        print(f"  [베이지북] 오류: {e}")
        raise


if __name__ == "__main__":
    run_beige()
