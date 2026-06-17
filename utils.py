# ============================================================
# utils.py - 공통 유틸리티
# ============================================================
import os
import time
import textwrap
from datetime import datetime
from config import OUTPUT_FOLDERS, TARGET_LANGUAGE, REQUEST_DELAY
# ------------------------------------------------------------
# 번역 (Gemini API → 실패 시 Google Translate 폴백)
# ------------------------------------------------------------
# Gemini 무료 티어: 분당 15회 제한 → 호출 간 최소 간격(초) 확보
_GEMINI_MIN_INTERVAL = 4.5
_last_gemini_call_at = [0.0]
def _translate_with_gemini(text: str) -> str:
    """
    Gemini API로 문서 전체를 한 번에 번역.
    GEMINI_API_KEY 환경변수 필요.
    분당 호출 제한(429) 방지를 위해 호출 간격을 두고,
    429 발생 시 한 번 대기 후 재시도한다.
    """
    from google import genai
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 미설정")
    client = genai.Client(api_key=api_key)
    prompt = (
        "Translate the following English text to Korean.\n"
        "- Preserve all paragraph breaks (blank lines between paragraphs)\n"
        "- Preserve markdown formatting (**, ##, >, etc.)\n"
        "- Return only the translated text, no explanations\n\n"
        f"{text}"
    )
    # ── 호출 간격 확보 (분당 15회 제한 대응) ──────────────────
    elapsed = time.time() - _last_gemini_call_at[0]
    if elapsed < _GEMINI_MIN_INTERVAL:
        time.sleep(_GEMINI_MIN_INTERVAL - elapsed)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
    except Exception as e:
        if "429" in str(e):
            print("  [번역] Gemini 429 - 30초 대기 후 1회 재시도")
            time.sleep(30)
            _last_gemini_call_at[0] = time.time()
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
        else:
            raise
    finally:
        _last_gemini_call_at[0] = time.time()
    return response.text.strip()
def _translate_with_google(text: str) -> str:
    """Google Translate 무료 API (폴백용)"""
    from deep_translator import GoogleTranslator
    chunks = textwrap.wrap(text, 4500, break_long_words=False, break_on_hyphens=False)
    translator = GoogleTranslator(source="en", target=TARGET_LANGUAGE)
    results = []
    for i, chunk in enumerate(chunks):
        try:
            results.append(translator.translate(chunk))
            if i < len(chunks) - 1:
                time.sleep(0.5)
        except Exception as e:
            print(f"  [Google번역 오류] 청크 {i+1}: {e}")
            results.append(chunk)
    return "\n\n".join(results)
def translate_text(text: str, chunk_size: int = 4500) -> str:
    """
    텍스트 번역.
    Gemini API 키가 있으면 Gemini 사용, 없으면 Google Translate 폴백.
    """
    if not text or not text.strip():
        return ""
    text = text.strip()
    if os.environ.get("GEMINI_API_KEY"):
        try:
            print("  [번역] Gemini API 사용")
            return _translate_with_gemini(text)
        except Exception as e:
            print(f"  [번역] Gemini 실패, Google로 폴백: {e}")
    return _translate_with_google(text)
def translate_paragraph_by_paragraph(text: str) -> str:
    """
    문서 번역 (크롤러 전용 인터페이스).
    Gemini: 문서 전체를 한 번에 번역 (빠름)
    폴백: 문단 단위 순차 번역
    """
    if not text or not text.strip():
        return ""
    text = text.strip()
    if os.environ.get("GEMINI_API_KEY"):
        try:
            return _translate_with_gemini(text)
        except Exception as e:
            print(f"  [번역] Gemini 실패, Google로 폴백: {e}")
    # Google Translate 폴백 - 문단 단위
    from deep_translator import GoogleTranslator
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    translator = GoogleTranslator(source="en", target=TARGET_LANGUAGE)
    translated = []
    for i, para in enumerate(paragraphs):
        try:
            if len(para) > 4500:
                result = _translate_with_google(para)
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
