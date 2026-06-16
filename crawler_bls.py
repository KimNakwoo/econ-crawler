# ============================================================
# crawler_bls.py - BLS 공식 사이트 크롤러 (CPI / PPI / NFP)
# ============================================================

import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from config import URLS, REQUEST_TIMEOUT, REQUEST_DELAY
from utils import save_markdown, translate_paragraph_by_paragraph, get_headers

CPI_URL     = "https://www.bls.gov/news.release/cpi.nr0.htm"
CPI_PDF_URL = "https://www.bls.gov/news.release/pdf/cpi.pdf"

DETAIL_TABLES = {
    "ppi": [
        ("요약",              "https://www.bls.gov/news.release/ppi.nr0.htm"),
        ("최종수요 (Table 1)", "https://www.bls.gov/news.release/ppi.t01.htm"),
        ("중간수요 (Table 2)", "https://www.bls.gov/news.release/ppi.t02.htm"),
    ],
    "nfp": [
        ("요약",                 "https://www.bls.gov/news.release/empsit.nr0.htm"),
        ("고용 현황 (Table A)",   "https://www.bls.gov/news.release/empsit.t01.htm"),
        ("업종별 고용 (Table B)", "https://www.bls.gov/news.release/empsit.t17.htm"),
    ],
}

PDF_URLS = {
    "ppi": "https://www.bls.gov/news.release/pdf/ppi.pdf",
    "nfp": "https://www.bls.gov/news.release/pdf/empsit.pdf",
}

MONTH_MAP = {
    "Jan":"1월","Feb":"2월","Mar":"3월","Apr":"4월",
    "May":"5월","Jun":"6월","Jul":"7월","Aug":"8월",
    "Sep":"9월","Oct":"10월","Nov":"11월","Dec":"12월",
}

INDENT_LEVELS = {
    "All items":0,"Food":0,"Food at home":1,
    "Cereals and bakery products":2,"Meats, poultry, fish, and eggs":2,
    "Dairy and related products":2,"Fruits and vegetables":2,
    "Nonalcoholic beverages and beverage materials":2,"Other food at home":2,
    "Food away from home":1,"Energy":0,"Energy commodities":1,
    "Fuel oil":2,"Motor fuel":2,"Gasoline (all types)":3,
    "Energy services":1,"Electricity":2,"Utility (piped) gas service":2,
    "All items less food and energy":0,
    "Commodities less food and energy commodities":1,
    "Apparel":2,"New vehicles":2,"Used cars and trucks":2,
    "Medical care commodities":2,"Alcoholic beverages":2,
    "Tobacco and smoking products":2,"Services less energy services":1,
    "Shelter":2,"Rent of primary residence":3,
    "Owners' equivalent rent of residences":3,"Medical care services":2,
    "Physicians' services":3,"Hospital services":3,
    "Transportation services":2,"Motor vehicle maintenance and repair":3,
    "Motor vehicle insurance":3,"Airline fares":3,
    "Final demand":0,"Final demand goods":1,"Final demand foods":2,
    "Final demand energy":2,"Final demand goods less foods and energy":2,
    "Final demand services":1,"Final demand trade services":2,
    "Final demand transportation and warehousing services":2,
    "Final demand services less trade, transportation, and warehousing":2,
    "Final demand less foods, energy, and trade services":0,
    "Total nonfarm":0,"Total private":1,"Goods-producing":2,
    "Mining and logging":3,"Construction":3,"Manufacturing":3,
    "Durable goods":4,"Nondurable goods":4,"Private service-providing":2,
    "Trade, transportation, and utilities":3,"Information":3,
    "Financial activities":3,"Professional and business services":3,
    "Education and health services":3,"Leisure and hospitality":3,
    "Other services":3,"Government":1,"Federal":2,"State and local":2,
    "Unemployment rate":0,"Average hourly earnings":0,
}

INDENT_UNIT = "　"

# Cloudflare 봇 차단 페이지 감지 키워드
_BOT_SIGNALS = [
    "bot activity", "automated", "error code:", "ray id",
    "please enable cookies", "checking your browser",
    "cloudflare", "just a moment",
]


# ─── 봇 감지 체크 ────────────────────────────────────────────

def _is_bot_page(soup: BeautifulSoup) -> bool:
    text = soup.get_text().lower()
    return any(sig in text for sig in _BOT_SIGNALS)


# ─── PDF 폴백 파서 ────────────────────────────────────────────

def _fetch_pdf_text(pdf_url: str) -> str:
    """BLS PDF에서 텍스트 추출 (HTML 차단 시 폴백)"""
    try:
        import pdfplumber, io
        resp = requests.get(pdf_url, headers=get_headers(), timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        with pdfplumber.open(io.BytesIO(resp.content)) as pdf:
            pages = []
            for page in pdf.pages[:15]:   # 첫 15페이지
                t = page.extract_text()
                if t:
                    pages.append(t)
        text = "\n\n".join(pages)
        print(f"  [BLS PDF] {len(text)}자 추출 완료")
        return text
    except Exception as e:
        print(f"  [BLS PDF] 실패: {e}")
        return ""


# ─── HTML fetch (Playwright stealth → requests 폴백) ──────────

def fetch(url: str) -> BeautifulSoup:
    """
    1단계: Playwright + stealth (Cloudflare 우회)
    2단계: 봇 차단 페이지 감지 → 예외 발생
    3단계: requests 폴백 (403이면 호출부에서 PDF로 재시도)
    """
    time.sleep(REQUEST_DELAY)

    # ── Playwright 시도 ──────────────────────────────────────
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled",
                      "--no-sandbox", "--disable-dev-shm-usage"],
            )
            ctx = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                ),
                locale="en-US",
                timezone_id="America/New_York",
                viewport={"width": 1280, "height": 800},
            )
            page = ctx.new_page()
            page.add_init_script(
                "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
            )
            # playwright-stealth 적용 (설치된 경우)
            try:
                from playwright_stealth import stealth_sync
                stealth_sync(page)
                print("  [BLS] playwright-stealth 적용됨")
            except ImportError:
                pass
            page.goto(url, wait_until="networkidle", timeout=60000)
            html = page.content()
            title = page.title()
            browser.close()

        soup = BeautifulSoup(html, "lxml")
        pre_cnt = len(soup.find_all("pre"))
        tbl_cnt = len(soup.find_all("table"))
        print(f"  [BLS] 제목: {title} | pre:{pre_cnt} table:{tbl_cnt}")

        if _is_bot_page(soup):
            raise Exception("Cloudflare 봇 차단 페이지 감지 — HTML 수집 불가")

        return soup

    except Exception as pw_err:
        print(f"  [BLS] Playwright 실패: {pw_err}")

    # ── requests 폴백 ─────────────────────────────────────────
    print("  [BLS] requests 시도...")
    resp = requests.get(url, headers=get_headers(), timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "lxml")
    if _is_bot_page(soup):
        raise Exception("requests도 봇 차단 — HTML 수집 불가")
    return soup


# ─── 공통 유틸 ────────────────────────────────────────────────

def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def shorten_header(h: str) -> str:
    h = h.strip()
    if re.search(r"(expenditure|category|item|commodity|industry|series)", h, re.I):
        return "항목"
    mo = ""
    m = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\.?\s*\d{4}", h)
    if m:
        mo = " " + MONTH_MAP.get(m.group(1), m.group(1))
    if re.search(r"unadjusted.{0,15}12.mo", h, re.I):   return f"비조정 12M%{mo}"
    if re.search(r"unadjusted.{0,15}1.mo",  h, re.I):   return f"비조정 1M%{mo}"
    if re.search(r"seasonally.{0,15}12.mo", h, re.I):   return f"계절조정 12M%{mo}"
    if re.search(r"(seasonally|seas).{0,15}1.mo", h, re.I): return f"계절조정 1M%{mo}"
    if re.search(r"un-?\s*adjusted.{0,10}12", h, re.I): return f"비조정 12M%{mo}"
    if re.search(r"change.{0,10}month", h, re.I):        return f"월간%{mo}"
    if re.search(r"change.{0,10}year|12.mo", h, re.I):   return f"연간%{mo}"
    if re.search(r"level|number|thousand", h, re.I):     return f"수치{mo}"
    return h


def apply_indent(item_name: str) -> str:
    cn = re.sub(r"\s*\d+\s*$", "", item_name).strip()
    cn = re.sub(r"\s*\([^)]*\)\s*$", "", cn).strip()
    return INDENT_UNIT * INDENT_LEVELS.get(cn, 0) + item_name


def apply_indent_to_rows(rows: list) -> list:
    return [[apply_indent(row[0])] + row[1:] for row in rows if row]


def fmt_table(headers: list, rows: list) -> str:
    if not headers or not rows:
        return "_데이터 없음_\n"
    short_h = [shorten_header(h) for h in headers]
    n = len(short_h)
    rows = [r[:n] + [""] * (n - len(r)) for r in rows]
    lines = (
        ["| " + " | ".join(short_h) + " |",
         "| " + " | ".join(["---"] * n) + " |"]
        + ["| " + " | ".join(r) + " |" for r in rows]
    )
    return "\n".join(lines) + "\n"


def parse_table(table_el) -> tuple:
    headers, rows = [], []
    for tr in table_el.find_all("tr"):
        ths = tr.find_all("th")
        tds = tr.find_all("td")
        if ths and not tds:
            row = [clean(x.get_text()) for x in ths]
            if any(row): headers = row
        elif tds:
            row = [clean(x.get_text()) for x in tds]
            if any(row): rows.append(row)
    return headers, rows


# ─── CPI 파싱 ────────────────────────────────────────────────

def extract_cpi_sections(soup: BeautifulSoup) -> dict:
    intro_text = ""
    table_headers, table_rows = [], []
    body_parts = []
    state = "before_table"

    for el in soup.find_all(["pre", "table"]):
        if state == "done":
            break
        if el.name == "pre":
            raw = el.get_text()
            if state == "before_table":
                m = re.search(r"CONSUMER PRICE INDEX", raw, re.I)
                if m:
                    intro_text = raw[m.start():].strip()
            else:
                if "Contact Information" in raw:
                    body_parts.append(raw[:raw.find("Contact Information")].strip())
                    state = "done"
                else:
                    body_parts.append(raw.strip())
        elif el.name == "table" and state == "before_table":
            table_headers, table_rows = parse_table(el)
            state = "after_table"

    if intro_text or table_headers:
        print("  [BLS] 구형 HTML 파싱 성공")
        return {"intro_text": intro_text, "table_headers": table_headers,
                "table_rows": table_rows, "body_text": "\n\n".join(body_parts)}

    # 신형 HTML 폴백
    print("  [BLS] 신형 HTML 파싱 시도")
    content = (soup.find("article") or soup.find("main")
               or soup.find("div", id=re.compile(r"content|main", re.I))
               or soup.body)
    paras = []
    if content:
        tables = content.find_all("table")
        if tables:
            table_headers, table_rows = parse_table(tables[0])
        paras = [clean(p.get_text()) for p in content.find_all("p") if len(clean(p.get_text())) > 40]

    return {"intro_text": "\n\n".join(paras[:5]),
            "table_headers": table_headers, "table_rows": table_rows,
            "body_text": "\n\n".join(paras[5:])}


def build_markdown_cpi(date_str: str, forecast: dict) -> str:
    md  = f"# CPI 발표 · {date_str}\n\n"
    md += f"> 출처: BLS ({CPI_URL})\n\n"

    if forecast:
        md += "## 📊 예측치 vs 실제치\n\n"
        rows = []
        for name, val in forecast.items():
            parts  = [p.strip() for p in val.split("|")]
            actual   = parts[0].replace("실제:", "").strip() if parts     else "-"
            fcast    = parts[1].replace("예측:", "").strip() if len(parts)>1 else "-"
            previous = parts[2].replace("이전:", "").strip() if len(parts)>2 else "-"
            rows.append([name, actual, fcast, previous])
        md += fmt_table(["항목", "실제치", "예측치", "이전치"], rows)
        md += "\n"

    # ── HTML 시도 ────────────────────────────────────────────
    html_ok = False
    try:
        soup = fetch(CPI_URL)
        sec  = extract_cpi_sections(soup)
        if sec["intro_text"]:
            print("  [CPI] 헤드라인 번역 중...")
            md += "## 📰 헤드라인 요약\n\n"
            md += translate_paragraph_by_paragraph(sec["intro_text"]) + "\n\n"
        md += "## 📋 Table A\n\n"
        if sec["table_headers"] and sec["table_rows"]:
            md += fmt_table(sec["table_headers"], apply_indent_to_rows(sec["table_rows"]))
        else:
            md += "_테이블 파싱 실패_\n"
        md += "\n"
        if sec["body_text"]:
            print("  [CPI] 본문 번역 중...")
            md += "## 📝 상세 해설\n\n"
            md += translate_paragraph_by_paragraph(sec["body_text"]) + "\n\n"
        html_ok = True
    except Exception as e:
        print(f"  [CPI] HTML 실패: {e}")

    # ── PDF 폴백 ─────────────────────────────────────────────
    if not html_ok:
        print("  [CPI] PDF 폴백 시도...")
        pdf_text = _fetch_pdf_text(CPI_PDF_URL)
        if pdf_text:
            md += "## 📰 본문 (PDF 원문 번역)\n\n"
            md += translate_paragraph_by_paragraph(pdf_text[:8000]) + "\n\n"
        else:
            md += "_HTML 및 PDF 수집 모두 실패 (BLS 접근 차단)_\n\n"

    md += f"\n---\n*수집: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 출처: BLS*\n"
    return md


# ─── PPI / NFP ────────────────────────────────────────────────

def extract_main_table(soup: BeautifulSoup) -> tuple:
    best_h, best_r, mx = [], [], 0
    for table in soup.find_all("table"):
        h, rows = parse_table(table)
        if len(rows) > mx and h:
            mx = len(rows); best_h, best_r = h, rows
    return best_h, best_r


def extract_section_texts(soup: BeautifulSoup) -> list:
    sections = []
    current_title, current_paras = None, []
    found_first = False
    for el in soup.find_all(["pre", "table", "h2", "h3", "h4", "p"]):
        tag = el.name
        if tag in ("pre", "table"):
            found_first = True
            if tag == "table" and current_title and current_paras:
                sections.append({"title": current_title, "text": "\n\n".join(current_paras)})
                current_paras = []
            continue
        if not found_first:
            continue
        if tag in ("h2", "h3", "h4"):
            if current_title and current_paras:
                sections.append({"title": current_title, "text": "\n\n".join(current_paras)})
                current_paras = []
            current_title = clean(el.get_text())
        elif tag == "p":
            t = clean(el.get_text())
            if len(t) > 60 and not t.startswith("NOTE:") and not t.startswith("Footnote") and current_title:
                current_paras.append(t)
    if current_title and current_paras:
        sections.append({"title": current_title, "text": "\n\n".join(current_paras)})
    if not sections:
        paras = [clean(p.get_text()) for p in soup.find_all("p") if len(clean(p.get_text())) > 60]
        if paras:
            sections = [{"title": "본문", "text": "\n\n".join(paras)}]
    return sections


def build_markdown_bls(indicator: str, date_str: str, forecast: dict) -> str:
    label_map = {"ppi": "PPI", "nfp": "비농업고용(NFP)"}
    label = label_map.get(indicator, indicator.upper())

    md  = f"# {label} 발표 · {date_str}\n\n"
    md += f"> 출처: BLS (https://www.bls.gov)\n\n"

    if forecast:
        md += "## 📊 예측치 vs 실제치\n\n"
        rows = []
        for name, val in forecast.items():
            parts    = [p.strip() for p in val.split("|")]
            actual   = parts[0].replace("실제:", "").strip() if parts       else "-"
            fcast    = parts[1].replace("예측:", "").strip() if len(parts)>1 else "-"
            previous = parts[2].replace("이전:", "").strip() if len(parts)>2 else "-"
            rows.append([name, actual, fcast, previous])
        md += fmt_table(["항목", "실제치", "예측치", "이전치"], rows)
        md += "\n"

    html_ok = False
    for table_label, url in DETAIL_TABLES.get(indicator, []):
        md += f"### {table_label}\n\n"
        try:
            s = fetch(url)
            if url == DETAIL_TABLES[indicator][0][1]:
                sections = extract_section_texts(s)
                headers, rows = extract_main_table(s)
                if headers and rows:
                    md += fmt_table(headers, apply_indent_to_rows(rows))
                if sections:
                    md += "\n## 📝 표 해설\n\n"
                    for i, sec in enumerate(sections, 1):
                        print(f"  [{label}] 번역 중 ({i}/{len(sections)}): {sec['title'][:30]}...")
                        md += f"### {sec['title']}\n\n"
                        md += translate_paragraph_by_paragraph(sec["text"]) + "\n\n"
                html_ok = True
            else:
                headers, rows = extract_main_table(s)
                if headers and rows:
                    md += fmt_table(headers, apply_indent_to_rows(rows))
                else:
                    md += "_테이블 파싱 실패_\n"
        except Exception as e:
            print(f"  [{label}] HTML 실패: {e}")
            md += f"_수집 실패: {e}_\n"
        md += "\n"

    # ── PDF 폴백 ─────────────────────────────────────────────
    if not html_ok and indicator in PDF_URLS:
        print(f"  [{label}] PDF 폴백 시도...")
        pdf_text = _fetch_pdf_text(PDF_URLS[indicator])
        if pdf_text:
            md += "## 📰 본문 (PDF 원문 번역)\n\n"
            md += translate_paragraph_by_paragraph(pdf_text[:8000]) + "\n\n"
        else:
            md += "_HTML 및 PDF 수집 모두 실패 (BLS 접근 차단)_\n\n"

    md += f"\n---\n*수집: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 출처: BLS*\n"
    return md


# ─── 공개 실행 함수 ───────────────────────────────────────────

def run_cpi(forecast: dict = None):
    print("  [CPI] 크롤링 시작")
    date_str = datetime.now().strftime("%Y-%m-%d")
    md = build_markdown_cpi(date_str, forecast or {})
    save_markdown("cpi", "CPI", md, date_str)
    print("  [CPI] 완료")


def run_ppi(forecast: dict = None):
    print("  [PPI] 크롤링 시작")
    date_str = datetime.now().strftime("%Y-%m-%d")
    md = build_markdown_bls("ppi", date_str, forecast or {})
    save_markdown("ppi", "PPI", md, date_str)
    print("  [PPI] 완료")


def run_nfp(forecast: dict = None):
    print("  [NFP] 크롤링 시작")
    date_str = datetime.now().strftime("%Y-%m-%d")
    md = build_markdown_bls("nfp", date_str, forecast or {})
    save_markdown("nfp", "NFP", md, date_str)
    print("  [NFP] 완료")
