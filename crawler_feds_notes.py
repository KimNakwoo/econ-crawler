# ============================================================
# crawler_feds_notes.py - FEDS Notes 크롤러
#
# 대상 주제 (제목 + 초록 키워드 매칭):
#   - 인플레이션/물가
#   - 노동시장
#   - 금융여건
#   - 경기침체 선행지표
#
# 동작 방식:
#   1. FEDS Notes 목록 페이지 크롤링
#   2. 관심 주제 키워드 필터링
#   3. 미처리 노트만 번역·저장 (처리 이력: .processed.txt)
#
# 저장 경로: OUTPUT_FOLDERS["feds_notes"]
# ============================================================

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from config import OUTPUT_FOLDERS, REQUEST_TIMEOUT, REQUEST_DELAY, FED_RSS
from utils import (
    save_markdown,
    translate_paragraph_by_paragraph,
    md_header,
    md_meta,
    get_headers,
)

FED_BASE = "https://www.federalreserve.gov"

# ─── 주제별 키워드 ────────────────────────────────────────────
TOPIC_KEYWORDS: dict = {
    "인플레이션_물가": [
        "inflation", "price index", "cpi", "pce", "tariff", "disinflation",
        "retail price", "consumer price", "cost-push", "supply chain price",
    ],
    "노동시장": [
        "labor market", "labor supply", "labor demand", "employment",
        "wage", "unemployment", "job", "worker", "payroll", "hiring",
        "participation rate",
    ],
    "금융여건": [
        "financial condition", "credit", "bank lending", "lending standard",
        "liquidity", "yield", "financial stability", "balance sheet",
        "treasury rate", "funding", "credit spread", "bank resilience",
    ],
    "경기침체_선행지표": [
        "recession", "yield curve", "leading indicator", "gdp growth",
        "slowdown", "uncertainty", "downside risk", "contraction",
        "business cycle", "economic outlook", "growth forecast",
    ],
}


def matches_topic(title: str, abstract: str) -> tuple:
    """
    제목 + 초록에서 관심 주제 키워드 매칭
    반환: (매칭여부, 매칭된 주제 이름)
    """
    text = (title + " " + abstract).lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw.lower() in text for kw in keywords):
            return True, topic
    return False, ""


# ─── 목록 페이지 파싱 ─────────────────────────────────────────

def fetch_notes_listing() -> list:
    """
    FEDS Notes 목록 페이지 파싱
    반환: [{"title": ..., "url": ..., "date": "YYYY-MM-DD", "abstract": ..., "authors": ...}, ...]
    """
    resp = requests.get(FED_RSS["feds_notes"], headers=get_headers(), timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    notes = []

    # 각 노트 블록 탐색: h5 태그가 제목+링크를 포함
    for h5 in soup.find_all("h5"):
        link = h5.find("a", href=True)
        if not link:
            continue

        title = link.get_text(strip=True)
        href  = link["href"]
        if not href.startswith("http"):
            href = FED_BASE + href

        # 날짜: h5 위 또는 같은 div에서 탐색
        date_str = ""
        parent = h5.find_parent()
        if parent:
            # "March 05, 2026" 패턴 탐색
            text = parent.get_text()
            m = re.search(r"(\w+ \d{1,2}, \d{4})", text)
            if m:
                try:
                    dt = datetime.strptime(m.group(1), "%B %d, %Y")
                    date_str = dt.strftime("%Y-%m-%d")
                except Exception:
                    pass

        # URL에서도 날짜 추출 가능 (예: ...-20260305.html)
        if not date_str:
            m = re.search(r"(\d{8})", href)
            if m:
                d = m.group(1)
                date_str = f"{d[:4]}-{d[4:6]}-{d[6:]}"

        # 초록: h5 다음 p 태그
        abstract = ""
        next_p = h5.find_next_sibling("p")
        if next_p:
            abstract = next_p.get_text(strip=True)
        else:
            # 부모 컨테이너에서 탐색
            if parent:
                p_tags = parent.find_all("p")
                if p_tags:
                    abstract = p_tags[0].get_text(strip=True)

        # 저자
        authors = ""
        if parent:
            # 저자는 보통 h5 바로 다음, p 앞에 위치
            for tag in h5.find_next_siblings():
                if tag.name in ["h5", "h4", "h3"]:
                    break
                t = tag.get_text(strip=True)
                # 저자 패턴: 이름들, 쉼표/and로 구분, 짧은 텍스트
                if t and len(t) < 200 and t != abstract[:50]:
                    if re.search(r"\band\b|,", t) or len(t.split()) <= 6:
                        authors = t
                        break

        notes.append({
            "title":    title,
            "url":      href,
            "date":     date_str,
            "abstract": abstract,
            "authors":  authors,
        })

    return notes


# ─── 개별 노트 본문 크롤링 ────────────────────────────────────

def fetch_note_content(url: str) -> tuple:
    """
    노트 HTML 페이지에서 본문 + 이미지 URL 추출
    반환: (body_text, [image_url, ...])
    """
    time.sleep(REQUEST_DELAY)
    resp = requests.get(url, headers=get_headers(), timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "lxml")

    content_div = (
        soup.find("div", id="content")
        or soup.find("div", class_=re.compile(r"col-xs|article|note"))
        or soup.find("article")
        or soup.find("main")
    )

    target = content_div or soup

    # 이미지 URL 수집 (아이콘/로고 제외)
    image_urls = []
    seen = set()
    for img in target.find_all("img"):
        src = img.get("src", "").strip()
        if not src:
            continue
        skip_words = ["icon", "logo", "banner", "button", "arrow", "bullet",
                      "spacer", "pixel", "bls_emblem", "flag", "dot-gov"]
        if any(w in src.lower() for w in skip_words):
            continue
        if src.startswith("//"):
            src = "https:" + src
        elif not src.startswith("http"):
            src = FED_BASE + src
        if src not in seen:
            seen.add(src)
            image_urls.append(src)

    if content_div:
        paragraphs = content_div.find_all("p")
    else:
        paragraphs = soup.find_all("p")

    lines = []
    for p in paragraphs:
        text = p.get_text(separator=" ").strip()
        # 짧은 네비게이션/저작권 텍스트 제외
        if text and len(text) > 40:
            lines.append(text)

    return "\n\n".join(lines), image_urls


# ─── 처리 완료 URL 관리 ──────────────────────────────────────

def _processed_path() -> str:
    folder = OUTPUT_FOLDERS["feds_notes"]
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, ".processed.txt")


def load_processed() -> set:
    path = _processed_path()
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def mark_processed(url: str):
    path = _processed_path()
    with open(path, "a", encoding="utf-8") as f:
        f.write(url + "\n")


# ─── 메인 실행 함수 ──────────────────────────────────────────

def run_feds_notes():
    """FEDS Notes 크롤링 - 관심 주제 + 새 노트만 처리"""
    print("[FEDS Notes] 시작")

    notes = fetch_notes_listing()
    processed = load_processed()
    print(f"[FEDS Notes] 목록 {len(notes)}건 수집")

    new_count = 0
    for note in notes:
        if note["url"] in processed:
            continue

        matched, topic = matches_topic(note["title"], note["abstract"])
        if not matched:
            mark_processed(note["url"])  # 관심 없는 노트도 처리 완료로 표시
            continue

        print(f"[FEDS Notes] 새 노트 ({topic}): {note['title'][:60]}")

        try:
            body_en, image_urls = fetch_note_content(note["url"])

            if not body_en:
                print("[FEDS Notes] 본문 없음 - 스킵")
                mark_processed(note["url"])
                continue

            print(f"[FEDS Notes] 본문 {len(body_en)}자 → 번역 시작")

            # 제목 번역 (한국어 / English 병기)
            title_ko = translate_paragraph_by_paragraph(note["title"])
            title_en = note["title"]

            # 초록 번역
            abstract_ko = translate_paragraph_by_paragraph(note["abstract"]) if note["abstract"] else ""

            # 본문 번역
            body_ko = translate_paragraph_by_paragraph(body_en)

            date_str = note["date"] or datetime.now().strftime("%Y-%m-%d")

            # 마크다운 구성
            md = md_header(f"FEDS Notes - {title_ko} / {title_en}", 1)
            md += f"\n> 날짜: {date_str}\n"
            if note["authors"]:
                md += f"> 저자: {note['authors']}\n"
            md += f"> 주제: {topic.replace('_', '/')}\n"
            md += f"> 출처: {note['url']}\n\n"

            # 초록 (번역본)
            if abstract_ko:
                md += md_header("📌 초록", 2)
                md += abstract_ko + "\n\n"

            # 본문 번역
            md += md_header("📋 한국어 번역", 2)
            md += body_ko + "\n\n"

            # 이미지 (figures/charts)
            if image_urls:
                md += md_header("🖼️ 그림 및 차트", 2)
                for i, img_url in enumerate(image_urls, 1):
                    md += f"**Figure {i}**\n\n"
                    md += f"![Figure {i}]({img_url})\n\n"
                    md += f"> [원본 링크]({img_url})\n\n"

            md += md_meta(note["url"], "FEDS_Notes")

            # 파일명: 날짜_주제_제목축약
            slug = re.sub(r"[^\w\s-]", "", note["title"])[:40].strip().replace(" ", "_")
            filename = f"FEDS_{topic}_{slug}"
            save_markdown("feds_notes", filename, md, date_str)
            mark_processed(note["url"])
            new_count += 1
            print(f"[FEDS Notes] 저장 완료: {date_str}")

        except Exception as e:
            print(f"[FEDS Notes] 오류: {e}")
            continue

    if new_count == 0:
        print("[FEDS Notes] 새 노트 없음")
        return False
    else:
        print(f"[FEDS Notes] {new_count}건 완료")
        return True


if __name__ == "__main__":
    run_feds_notes()
