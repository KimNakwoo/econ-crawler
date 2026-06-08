# ============================================================
# utils.py - 공통 유틸리티
# ============================================================

import os
import time
import textwrap
from datetime import datetime
from deep_translator import GoogleTranslator
from config import OUTPUT_FOLDERS, TARGET_LANGUAGE, REQUEST_DELAY


# ------------------------------------------------------------
# 번역
# ------------------------------------------------------------

def translate_text(text: str, chunk_size: int = 4500) -> str:
    """
    긴 텍스트를 청크로 나눠 번역 (Google 무료 API 한계: 5000자)
    """
    if not text or not text.strip():
        return ""

    text = text.strip()
    chunks = textwrap.wrap(text, chunk_size, break_long_words=False, break_on_hyphens=False)
    translated_chunks = []

    translator = GoogleTranslator(source="en", target=TARGET_LANGUAGE)

    for i, chunk in enumerate(chunks):
        try:
            result = translator.translate(chunk)
            translated_chunks.append(result)
            if i < len(chunks) - 1:
                time.sleep(0.5)  # API 과부하 방지
        except Exception as e:
            print(f"  [번역 오류] 청크 {i+1}: {e}")
            translated_chunks.append(chunk)  # 실패 시 원문 유지

    return "\n\n".join(translated_chunks)


def translate_paragraph_by_paragraph(text: str) -> str:
    """
    문단 단위로 번역 (FOMC/베이지북용 - 문맥 보존)
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    translated = []

    translator = GoogleTranslator(source="en", target=TARGET_LANGUAGE)

    for i, para in enumerate(paragraphs):
        try:
            if len(para) > 4500:
                # 너무 긴 문단은 청크 분할
                result = translate_text(para)
            else:
                result = translator.translate(para)
            translated.append(result)
            time.sleep(0.3)
        except Exception as e:
            print(f"  [번역 오류] 문단 {i+1}: {e}")
            translated.append(para)

    return "\n\n".join(translated)


# ------------------------------------------------------------
# 파일 저장
# ------------------------------------------------------------

def save_markdown(indicator: str, title: str, content: str, date: str = None) -> str:
    """
    Obsidian 볼트에 마크다운 파일 저장
    반환값: 저장된 파일 경로
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    folder = OUTPUT_FOLDERS.get(indicator)
    if not folder:
        raise ValueError(f"알 수 없는 지표: {indicator}")

    os.makedirs(folder, exist_ok=True)

    filename = f"{date}_{title}.md"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  → 저장 완료: {filepath}")
    return filepath


# ------------------------------------------------------------
# 마크다운 포맷 헬퍼
# ------------------------------------------------------------

def md_header(text: str, level: int = 1) -> str:
    return f"{'#' * level} {text}\n"


def md_table(headers: list, rows: list) -> str:
    """
    헤더와 행 리스트로 마크다운 표 생성
    예) headers=["항목","전월비","전년비"], rows=[["식품","0.3%","2.1%"], ...]
    """
    col_widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
                  for i, h in enumerate(headers)]

    def fmt_row(cells):
        return "| " + " | ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(cells)) + " |"

    separator = "| " + " | ".join("-" * w for w in col_widths) + " |"

    lines = [fmt_row(headers), separator] + [fmt_row(row) for row in rows]
    return "\n".join(lines) + "\n"


def md_meta(source_url: str, indicator: str) -> str:
    """문서 하단 메타 정보"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"\n---\n*출처: {source_url} | 수집: {now} | 지표: {indicator.upper()}*\n"


# ------------------------------------------------------------
# 공통 요청 헤더
# ------------------------------------------------------------

def get_headers() -> dict:
    from config import HEADERS
    return HEADERS
