# ============================================================
# crawler_fed_speech.py - 연준 의장 연설 크롤러
#
# 동작 방식:
#   1. Fed 연설 RSS에서 최신 목록 수집
#   2. 현재 의장(Chair) 성씨를 Fed 홈페이지에서 동적 조회
#   3. 의장 연설만 필터링
#   4. 아직 저장되지 않은 새 연설만 번역·저장
#
# 저장 경로: OUTPUT_FOLDERS["speech"]
# ============================================================

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from config import OUTPUT_FOLDERS, REQUEST_TIMEOUT, REQUEST_DELAY, FED_RSS, HEADERS
from utils import (
    save_markdown,
    translate_paragraph_by_paragraph,
    md_header,
    md_meta,
    get_headers,
)

FED_BASE = "https://www.federalreserve.gov"


# ─── 의장 성씨 동적 조회 ──────────────────────────────────────

def get_chair_lastname() -> str:
    """
    Fed Board of Governors 페이지에서 현재 의장(Chair) 성씨 조회.
    bio 링크 URL 패턴 (/aboutthefed/bios/board/LASTNAME.htm) 기반으로 추출.
    Vice Chair는 제외. 실패 시 빈 문자열 반환.
    """
    try:
        resp = requests.get(FED_RSS["board_bios"], headers=get_headers(), timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        # bio 링크 패턴: /aboutthefed/bios/board/LASTNAME.htm
        bio_pattern = re.compile(r"/aboutthefed/bios/board/(\w+)\.htm", re.I)

        for a in soup.find_all("a", href=bio_pattern):
            m = bio_pattern.search(a["href"])
            if not m:
                continue
            lastname_candidate = m.group(1).lower()
            if lastname_candidate in ("default", "board", "index"):
                continue

            # 해당 링크 주변 텍스트에서 "Chair" 확인 (Vice Chair 제외)
            parent = a.find_parent()
            if not parent:
                continue
            parent_text = parent.get_text(" ", strip=True)

            # 부모가 너무 넓으면 조부모까지 확인
            if len(parent_text) > 500:
                parent = a.find_parent(["div", "li", "tr", "section"])
                if parent:
                    parent_text = parent.get_text(" ", strip=True)

            if re.search(r'\bChair\b', parent_text, re.I) and "Vice" not in parent_text:
                print(f"[연설] 현재 의장 성씨 조회: {lastname_candidate}")
                return lastname_candidate

    except Exception as e:
        print(f"[연설] 의장 조회 실패: {e}")

    return ""


# ─── RSS 파싱 ──────────────────────────────────────────────

def fetch_speech_rss() -> list:
    """
    연설 RSS 파싱
    반환: [{"title": "...", "url": "...", "date": "YYYY-MM-DD", "lastname": "..."}, ...]
    """
    resp = requests.get(FED_RSS["speeches"], headers=get_headers(), timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "xml")

    speeches = []
    for item in soup.find_all("item"):
        title_text = item.find("title")
        link_text  = item.find("link")
        pub_text   = item.find("pubDate")

        if not title_text or not link_text:
            continue

        title = title_text.get_text(strip=True)
        url   = link_text.get_text(strip=True)

        # 성씨는 제목 첫 번째 단어 (예: "Powell, ..." → "powell")
        lastname = title.split(",")[0].strip().lower()

        # 날짜 파싱
        date_str = ""
        if pub_text:
            try:
                pub = pub_text.get_text(strip=True)
                # "Thu, 28 May 2026 00:00:00 GMT"
                dt = datetime.strptime(pub[:16].strip(), "%a, %d %b %Y")
                date_str = dt.strftime("%Y-%m-%d")
            except Exception:
                # URL에서 날짜 추출 (예: powell20260528a.htm)
                m = re.search(r"(\d{8})", url)
                if m:
                    d = m.group(1)
                    date_str = f"{d[:4]}-{d[4:6]}-{d[6:]}"

        speeches.append({
            "title":    title,
            "url":      url,
            "date":     date_str,
            "lastname": lastname,
        })

    return speeches


# ─── 개별 연설 크롤링 ─────────────────────────────────────────

def fetch_speech_content(url: str) -> tuple:
    """
    연설 HTML 페이지에서 화자 정보, 본문, 이미지 추출
    반환: (speaker_info, body_text, image_urls)
    """
    time.sleep(REQUEST_DELAY)
    resp = requests.get(url, headers=get_headers(), timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "lxml")

    # 화자 정보 (이름 + 직함)
    speaker_info = ""
    for tag in soup.find_all(["p", "div", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if re.search(r"Chair|Governor|President", text) and len(text) < 200:
            speaker_info = text
            break

    # 본문 추출
    content_div = (
        soup.find("div", id="content")
        or soup.find("div", class_=re.compile(r"col-xs|article|speech"))
        or soup.find("article")
        or soup.find("main")
    )

    target = content_div or soup

    # 이미지 URL 수집
    image_urls = []
    seen = set()
    skip_words = ["icon", "logo", "banner", "button", "arrow", "bullet",
                  "spacer", "pixel", "bls_emblem", "flag", "dot-gov"]
    for img in target.find_all("img"):
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

    if content_div:
        paragraphs = content_div.find_all("p")
    else:
        paragraphs = soup.find_all("p")

    lines = []
    for p in paragraphs:
        text = p.get_text(separator=" ").strip()
        if text and len(text) > 30:
            lines.append(text)

    body = "\n\n".join(lines)
    return speaker_info, body, image_urls


# ─── 처리 완료 URL 관리 ──────────────────────────────────────

def _processed_path() -> str:
    folder = OUTPUT_FOLDERS["speech"]
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

def run_speech():
    """의장 연설 크롤링 - 새 연설만 처리"""
    print("[연설] 시작")

    chair_lastname = get_chair_lastname()
    if chair_lastname:
        print(f"[연설] 의장 성씨: {chair_lastname}")
    else:
        print("[연설] 의장 성씨 조회 실패 - RSS 첫 번째 발화자 기준으로 진행")

    speeches = fetch_speech_rss()
    processed = load_processed()

    if chair_lastname:
        # 의장 성씨로 필터
        chair_speeches = [s for s in speeches if s["lastname"] == chair_lastname]
    else:
        # 폴백: RSS에서 가장 많이 등장한 성씨 = 현재 의장으로 추정
        from collections import Counter
        name_counts = Counter(s["lastname"] for s in speeches if s["lastname"])
        if name_counts:
            chair_lastname = name_counts.most_common(1)[0][0]
            print(f"[연설] 폴백: RSS 최다 발화자 '{chair_lastname}' 를 의장으로 추정")
            chair_speeches = [s for s in speeches if s["lastname"] == chair_lastname]
        else:
            print("[연설] 발화자 없음 - 종료")
            return False

    print(f"[연설] 의장 연설 {len(chair_speeches)}건 발견")

    new_count = 0
    for speech in chair_speeches:
        if speech["url"] in processed:
            continue

        print(f"[연설] 새 연설 처리: {speech['title'][:60]}")

        try:
            speaker_info, body_en, image_urls = fetch_speech_content(speech["url"])

            if not body_en:
                print(f"[연설] 본문 없음 - 스킵")
                mark_processed(speech["url"])
                continue

            print(f"[연설] 본문 {len(body_en)}자 → 번역 시작")

            # 제목 (성씨 제거 → 연설 제목만)
            speech_title_en = speech["title"].split(",", 1)[-1].strip() if "," in speech["title"] else speech["title"]
            speech_title_ko = translate_paragraph_by_paragraph(speech_title_en)
            date_str = speech["date"] or datetime.now().strftime("%Y-%m-%d")

            body_ko = translate_paragraph_by_paragraph(body_en)

            # 마크다운 구성
            md = md_header(f"연준 의장 연설 - {speech_title_ko} / {speech_title_en}", 1)
            md += f"\n> 날짜: {date_str}\n"
            if speaker_info:
                md += f"> 화자: {speaker_info}\n"
            md += f"> 출처: {speech['url']}\n\n"

            md += md_header("📋 한국어 번역", 2)
            md += body_ko + "\n\n"

            # 이미지
            if image_urls:
                md += md_header("🖼️ 그림 및 차트", 2)
                for i, img_url in enumerate(image_urls, 1):
                    md += f"**Figure {i}**\n\n"
                    md += f"![Figure {i}]({img_url})\n\n"
                    md += f"> [원본 링크]({img_url})\n\n"

            md += md_meta(speech["url"], "연준의장연설")

            save_markdown("speech", "연설", md, date_str)
            mark_processed(speech["url"])
            new_count += 1
            print(f"[연설] 저장 완료: {date_str}")

        except Exception as e:
            print(f"[연설] 오류: {e}")
            continue

    if new_count == 0:
        print("[연설] 새 연설 없음")
        return False
    else:
        print(f"[연설] {new_count}건 완료")
        return True


if __name__ == "__main__":
    run_speech()
