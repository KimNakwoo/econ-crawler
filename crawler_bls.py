# ============================================================
# crawler_bls.py - BLS CPI / PPI / NFP 크롤러
#
# 전략:
#   1차) BLS HTML(cpi.nr0.htm 등) 직접 스크래핑 → Table A 원본 그대로 추출
#   2차) 차단(403) 시 BLS Public Data API 폴백 → 동일 양식으로 재구성
#
# 출력 양식 (Obsidian 결과물과 동일):
#   # CPI 발표 · YYYY-MM-DD
#   > 출처: BLS (URL)
#   ## 📋 Table A
#   (멀티컬럼 SA MoM% × 7개월 + NSA 12M%, 들여쓰기)
#   ## 📝 상세 해설
#   (섹션별 한국어 해설 - HTML 번역 또는 Gemini 생성)
# ============================================================

import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from config import REQUEST_TIMEOUT, REQUEST_DELAY
from utils import save_markdown, get_headers, translate_paragraph_by_paragraph

CPI_URL = "https://www.bls.gov/news.release/cpi.nr0.htm"
PPI_URL = "https://www.bls.gov/news.release/ppi.nr0.htm"
NFP_URL = "https://www.bls.gov/news.release/empsit.nr0.htm"
BLS_API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

MONTH_KO = {
    "M01":"1월","M02":"2월","M03":"3월","M04":"4월",
    "M05":"5월","M06":"6월","M07":"7월","M08":"8월",
    "M09":"9월","M10":"10월","M11":"11월","M12":"12월",
}

# CSS class → 전각공백 들여쓰기
INDENT_CSS = {
    "indent0": "",   "indent1": "　",   "indent2": "　　",
    "indent3": "　　　", "indent4": "　　　　",
}

# ─── BLS API 관련 ─────────────────────────────────────────────

# CPI Table A 시리즈 (API 폴백용)
CPI_TABLE_A = [
    ("All items",                              "CUSR0000SA0",    "CUUR0000SA0"),
    ("　Food",                                 "CUSR0000SAF",    "CUUR0000SAF"),
    ("　　Food at home",                       "CUSR0000SAF1",   "CUUR0000SAF1"),
    ("　　Food away from home",                "CUSR0000SEFV",   "CUUR0000SEFV"),
    ("　Energy",                               "CUSR0000SA0E",   "CUUR0000SA0E"),
    ("　　Energy commodities",                 "CUSR0000SACL2",  "CUUR0000SACL2"),
    ("　　　Gasoline (all types)",             "CUSR0000SETB01", "CUUR0000SETB01"),
    ("　　　Fuel oil",                         "CUSR0000SETB02", "CUUR0000SETB02"),
    ("　　Energy services",                    "CUSR0000SASS",   "CUUR0000SASS"),
    ("　　　Electricity",                      "CUSR0000SEHE",   "CUUR0000SEHE"),
    ("　　　Utility (piped) gas service",      "CUSR0000SEHF01", "CUUR0000SEHF01"),
    ("All items less food and energy",         "CUSR0000SA0L1E", "CUUR0000SA0L1E"),
    ("　Commodities less food and energy",     "CUSR0000SACL1E", "CUUR0000SACL1E"),
    ("　　New vehicles",                       "CUSR0000SETA01", "CUUR0000SETA01"),
    ("　　Used cars and trucks",               "CUSR0000SETA02", "CUUR0000SETA02"),
    ("　　Apparel",                            "CUSR0000SAA",    "CUUR0000SAA"),
    ("　　Medical care commodities",           "CUSR0000SAM1",   "CUUR0000SAM1"),
    ("　Services less energy services",        "CUSR0000SASLE",  "CUUR0000SASLE"),
    ("　　Shelter",                            "CUSR0000SAH1",   "CUUR0000SAH1"),
    ("　　Transportation services",            "CUSR0000SAS4",   "CUUR0000SAS4"),
    ("　　Medical care services",              "CUSR0000SAM2",   "CUUR0000SAM2"),
]

PPI_TABLE = [
    ("Final demand",                           "WPSFD4",         "WPSFD4"),
    ("　Final demand goods",                   "WPSFD49116",     "WPSFD49116"),
    ("　　Foods",                              "WPSFD4111",      "WPSFD4111"),
    ("　　Energy",                             "WPSFD4112",      "WPSFD4112"),
    ("　　Goods less foods and energy",        "WPSFD4113",      "WPSFD4113"),
    ("　Final demand services",                "WPSFD4131",      "WPSFD4131"),
    ("　　Trade services",                     "WPSFD41311",     "WPSFD41311"),
    ("　　Transportation and warehousing",     "WPSFD41312",     "WPSFD41312"),
    ("　　Services less trade/transport",      "WPSFD41313",     "WPSFD41313"),
    ("Final demand less foods, energy, trade", "WPSFD4111TT",    "WPSFD4111TT"),
]

NFP_TABLE = [
    ("Total nonfarm",                          "CES0000000001",  "CES0000000001"),
    ("　Total private",                        "CES0500000001",  "CES0500000001"),
    ("　　Goods-producing",                    "CES0600000001",  "CES0600000001"),
    ("　　　Mining and logging",               "CES1000000001",  "CES1000000001"),
    ("　　　Construction",                     "CES2000000001",  "CES2000000001"),
    ("　　　Manufacturing",                    "CES3000000001",  "CES3000000001"),
    ("　　Private service-providing",          "CES0800000001",  "CES0800000001"),
    ("　　　Trade, transport, utilities",      "CES4000000001",  "CES4000000001"),
    ("　　　Information",                      "CES5000000001",  "CES5000000001"),
    ("　　　Financial activities",             "CES5500000001",  "CES5500000001"),
    ("　　　Prof. and business services",      "CES6000000001",  "CES6000000001"),
    ("　　　Education and health services",    "CES6500000001",  "CES6500000001"),
    ("　　　Leisure and hospitality",          "CES7000000001",  "CES7000000001"),
    ("　Government",                           "CES9000000001",  "CES9000000001"),
    ("Unemployment rate (%)",                  "LNS14000000",    "LNS14000000"),
    ("Avg hourly earnings ($)",                "CES0500000003",  "CES0500000003"),
]


# ─── 1차: BLS HTML 스크래핑 ───────────────────────────────────

def _try_fetch_html(url: str):
    """BLS 보도자료 HTML 요청. 차단 시 None 반환."""
    try:
        time.sleep(REQUEST_DELAY)
        resp = requests.get(url, headers=get_headers(), timeout=REQUEST_TIMEOUT)
        if resp.status_code in (403, 429, 503):
            print(f"  [BLS HTML] 차단 ({resp.status_code}) → API 폴백")
            return None
        resp.raise_for_status()
        print(f"  [BLS HTML] 수신 성공 ({len(resp.content)//1024} KB)")
        return BeautifulSoup(resp.text, "lxml")
    except Exception as e:
        print(f"  [BLS HTML] 실패: {e} → API 폴백")
        return None


def _detect_indent(cell) -> str:
    """
    <td> 셀의 들여쓰기 레벨을 CSS 클래스 또는 &nbsp; 개수로 감지.
    반환: 전각공백 문자열
    """
    classes = " ".join(cell.get("class", []))
    for css, spaces in INDENT_CSS.items():
        if css in classes:
            return spaces

    # &nbsp; 또는 일반 공백 카운트
    raw_html = str(cell)
    nbsp_count = raw_html.count("&nbsp;") + raw_html.count(" ")
    if nbsp_count >= 6:
        return "　　　"
    elif nbsp_count >= 4:
        return "　　"
    elif nbsp_count >= 2:
        return "　"

    # 텍스트 앞 공백
    raw_text = cell.get_text()
    leading = len(raw_text) - len(raw_text.lstrip("  "))
    if leading >= 6:
        return "　　　"
    elif leading >= 4:
        return "　　"
    elif leading >= 2:
        return "　"
    return ""


def _html_table_to_md(table_elem) -> str | None:
    """
    BLS HTML <table> → 마크다운 테이블 변환.
    멀티행 헤더를 단일 헤더 행으로 평탄화.
    """
    all_rows = table_elem.find_all("tr")
    if len(all_rows) < 3:
        return None

    # ── 헤더 처리 ──────────────────────────────────────────────
    # BLS 표는 보통 2~3행 헤더: 1행=섹션명, 2행=월명/구분
    # 마지막 헤더 행(월별 컬럼)만 사용
    thead = table_elem.find("thead")
    if thead:
        header_rows = thead.find_all("tr")
        data_rows   = table_elem.find("tbody").find_all("tr") if table_elem.find("tbody") else []
    else:
        # thead/tbody 없는 경우 첫 행을 헤더로
        header_rows = all_rows[:2]
        data_rows   = all_rows[2:]

    # colspan 처리를 감안해 헤더 재구성
    # 1열(항목명)은 고정, 나머지는 마지막 헤더 행 값
    col_labels = ["항목"]
    if header_rows:
        last_hdr = header_rows[-1]
        for th in last_hdr.find_all(["th", "td"]):
            text = th.get_text(strip=True)
            if text:
                col_labels.append(text)

    # ── 데이터 행 처리 ─────────────────────────────────────────
    md_rows = []
    for tr in data_rows:
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue

        # 첫 셀: 들여쓰기 + 항목명
        indent    = _detect_indent(cells[0])
        item_name = cells[0].get_text(strip=True)
        if not item_name:
            continue

        values = []
        for c in cells[1:]:
            v = c.get_text(strip=True)
            values.append(v if v else "-")

        md_rows.append([f"{indent}{item_name}"] + values)

    if not md_rows:
        return None

    # ── 마크다운 테이블 빌드 ───────────────────────────────────
    max_cols = max(len(r) for r in md_rows)
    hdr = col_labels + ["-"] * (max_cols - len(col_labels))
    hdr = hdr[:max_cols]

    lines = [
        "| " + " | ".join(hdr) + " |",
        "| " + " | ".join(["---"] * max_cols) + " |",
    ]
    for row in md_rows:
        padded = row + ["-"] * (max_cols - len(row))
        lines.append("| " + " | ".join(padded[:max_cols]) + " |")

    return "\n".join(lines) + "\n"


def _find_table_by_keyword(soup, keyword: str):
    """caption 또는 인접 제목에서 keyword 가 포함된 <table> 반환."""
    for table in soup.find_all("table"):
        caption = table.find("caption")
        if caption and keyword.lower() in caption.get_text().lower():
            return table

    for heading in soup.find_all(["h2", "h3", "h4", "p", "div"]):
        if keyword.lower() in heading.get_text().lower():
            nxt = heading.find_next_sibling("table") or heading.find_next("table")
            if nxt:
                return nxt
    return None


def _extract_narrative(soup, section_keywords: list) -> dict:
    """
    BLS HTML에서 섹션별 서술 텍스트 추출.
    section_keywords: [("Food", "식품 (Food)"), ...]
    반환: {"식품 (Food)": "영문 텍스트...", ...}
    """
    paras = soup.find_all("p")
    sections = {}
    current_key = None
    current_lines = []

    for p in paras:
        text = p.get_text(strip=True)
        if not text or len(text) < 20:
            continue

        matched_key = None
        for en_kw, ko_label in section_keywords:
            # 문단 시작이 섹션 키워드인 경우 (예: "Food" 또는 "Food\n")
            if re.match(rf"^{re.escape(en_kw)}\b", text, re.I):
                matched_key = ko_label
                break

        if matched_key:
            if current_key and current_lines:
                sections[current_key] = "\n\n".join(current_lines)
            current_key  = matched_key
            current_lines = [text]  # 헤더 문단 포함
        elif current_key:
            # 다음 표/섹션 시작 신호면 종료
            if re.match(r"^Table\s+[A-Z0-9]", text, re.I):
                sections[current_key] = "\n\n".join(current_lines)
                current_key   = None
                current_lines = []
            else:
                current_lines.append(text)

    if current_key and current_lines:
        sections[current_key] = "\n\n".join(current_lines)

    return sections


# ─── HTML 기반 CPI 빌드 ───────────────────────────────────────

def _build_from_html_cpi(soup, date_str: str) -> str:
    """BLS HTML에서 CPI 마크다운 생성"""
    print("  [CPI] HTML에서 Table A 추출")

    md  = f"# CPI 발표 · {date_str}\n\n"
    md += f"> 출처: BLS ({CPI_URL})\n\n"

    # Table A
    table_elem = _find_table_by_keyword(soup, "Table A")
    if table_elem:
        table_md = _html_table_to_md(table_elem)
        if table_md:
            md += "## 📋 Table A\n\n" + table_md + "\n"
            print("  [CPI] Table A 추출 완료")
        else:
            print("  [CPI] Table A 파싱 실패 - 섹션 생략")
    else:
        print("  [CPI] Table A를 찾지 못함")

    # 서술 텍스트 추출 및 번역
    section_kws = [
        ("Food",                           "### 식품 (Food)"),
        ("Energy",                         "### 에너지 (Energy)"),
        ("All items less food and energy", "### 식품 및 에너지 제외 (All items less food and energy)"),
    ]
    narratives = _extract_narrative(soup, section_kws)

    if narratives:
        md += "## 📝 상세 해설\n\n"
        for header, en_text in narratives.items():
            print(f"  [CPI] 번역 중: {header}")
            ko_text = translate_paragraph_by_paragraph(en_text)
            md += f"{header}\n\n{ko_text}\n\n"
    else:
        # 서술 텍스트 없으면 Gemini로 생성
        md += "## 📝 상세 해설\n\n"
        md += _gemini_from_html(soup, "cpi") + "\n"

    md += f"\n---\n*수집: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 출처: BLS*\n"
    return md


def _build_from_html_ppi(soup, date_str: str) -> str:
    """BLS HTML에서 PPI 마크다운 생성"""
    print("  [PPI] HTML에서 표 추출")

    md  = f"# PPI 발표 · {date_str}\n\n"
    md += f"> 출처: BLS ({PPI_URL})\n\n"

    # PPI는 Table 1 (Final demand) 기준
    table_elem = (
        _find_table_by_keyword(soup, "Table 1")
        or _find_table_by_keyword(soup, "Final demand")
    )
    if table_elem:
        table_md = _html_table_to_md(table_elem)
        if table_md:
            md += "## 📋 Table 1. Final Demand\n\n" + table_md + "\n"

    section_kws = [
        ("Final demand goods",    "### 최종수요 상품 (Final demand goods)"),
        ("Final demand services", "### 최종수요 서비스 (Final demand services)"),
        ("Final demand",          "### 최종수요 (Final demand)"),
    ]
    narratives = _extract_narrative(soup, section_kws)

    md += "## 📝 상세 해설\n\n"
    if narratives:
        for header, en_text in narratives.items():
            ko_text = translate_paragraph_by_paragraph(en_text)
            md += f"{header}\n\n{ko_text}\n\n"
    else:
        md += _gemini_from_html(soup, "ppi") + "\n"

    md += f"\n---\n*수집: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 출처: BLS*\n"
    return md


def _build_from_html_nfp(soup, date_str: str) -> str:
    """BLS HTML에서 NFP 마크다운 생성"""
    print("  [NFP] HTML에서 표 추출")

    md  = f"# 비농업고용(NFP) 발표 · {date_str}\n\n"
    md += f"> 출처: BLS ({NFP_URL})\n\n"

    table_elem = (
        _find_table_by_keyword(soup, "Table A")
        or _find_table_by_keyword(soup, "nonfarm")
    )
    if table_elem:
        table_md = _html_table_to_md(table_elem)
        if table_md:
            md += "## 📋 Table A\n\n" + table_md + "\n"

    section_kws = [
        ("Total nonfarm employment",   "### 비농업고용 (Total nonfarm)"),
        ("Unemployment",               "### 실업률 (Unemployment)"),
        ("Average hourly earnings",    "### 시간당 평균임금 (Average hourly earnings)"),
    ]
    narratives = _extract_narrative(soup, section_kws)

    md += "## 📝 상세 해설\n\n"
    if narratives:
        for header, en_text in narratives.items():
            ko_text = translate_paragraph_by_paragraph(en_text)
            md += f"{header}\n\n{ko_text}\n\n"
    else:
        md += _gemini_from_html(soup, "nfp") + "\n"

    md += f"\n---\n*수집: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 출처: BLS*\n"
    return md


def _gemini_from_html(soup, indicator: str) -> str:
    """HTML 텍스트 일부를 Gemini로 요약·번역 (서술 텍스트 미탐지 시 폴백)"""
    try:
        import os
        from google import genai as _genai
        key = os.environ.get("GEMINI_API_KEY", "")
        if not key:
            return "_Gemini API 키 없음_\n"
        client = _genai.Client(api_key=key)

        full_text = soup.get_text(separator="\n", strip=True)
        excerpt   = full_text[:4000]

        label_map = {"cpi": "CPI", "ppi": "PPI", "nfp": "비농업고용(NFP)"}
        prompt = (
            f"다음은 미국 BLS {label_map.get(indicator, indicator.upper())} 보도자료 텍스트입니다.\n"
            "주요 내용을 한국어로 섹션별(식품/에너지/근원 또는 해당 지표의 주요 항목)로 요약해주세요.\n"
            f"BLS 공식 보도자료 문체로, 수치를 구체적으로 언급하면서 작성하세요.\n\n{excerpt}"
        )
        resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return resp.text.strip() + "\n"
    except Exception as e:
        print(f"  [Gemini] 실패: {e}")
        return "_해설 생성 실패_\n"


# ─── 2차: BLS API 폴백 ────────────────────────────────────────

def _fetch_bls_api(series_ids: list, start_year: int, end_year: int) -> dict:
    """BLS API v2 → {series_id: [records]}"""
    all_data = {}
    for i in range(0, len(series_ids), 25):
        chunk = series_ids[i:i + 25]
        payload = {"seriesid": chunk, "startyear": str(start_year), "endyear": str(end_year)}
        time.sleep(REQUEST_DELAY)
        try:
            resp = requests.post(
                BLS_API,
                json=payload,
                headers={"Content-Type": "application/json", **get_headers()},
                timeout=REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") != "REQUEST_SUCCEEDED":
                print(f"  [BLS API] 경고: {data.get('message')}")
                continue
            for series in data.get("Results", {}).get("series", []):
                sid     = series["seriesID"]
                records = sorted(
                    [r for r in series.get("data", [])
                     if r["period"].startswith("M") and r["period"] != "M13"],
                    key=lambda x: (x["year"], x["period"]),
                )
                all_data[sid] = records
        except Exception as e:
            print(f"  [BLS API] 청크 오류: {e}")
    return all_data


def _get_val(records, year, period):
    for r in records:
        if r["year"] == year and r["period"] == period:
            try:
                return float(r["value"])
            except (ValueError, KeyError):
                return None
    return None


def _prev_period(year, period):
    m, y = int(period[1:]), int(year)
    return (str(y - 1), "M12") if m == 1 else (str(y), f"M{m-1:02d}")


def _pct(new, old, decimals=1):
    if new is None or old is None or old == 0:
        return "-"
    return f"{(new - old) / old * 100:.{decimals}f}"


def _build_api_table(table_def: list, api_data: dict, indicator: str) -> tuple:
    """API 데이터로 멀티컬럼 테이블 생성. 반환: (markdown, summary_dict)"""
    base_recs = api_data.get(table_def[0][1], [])
    if not base_recs:
        return "_데이터 없음_\n", {}

    latest     = base_recs[-1]
    ly, lp     = latest["year"], latest["period"]

    # 최근 7개월
    months = []
    y, p = ly, lp
    for _ in range(7):
        months.insert(0, (y, p))
        y, p = _prev_period(y, p)

    col_headers = ["항목"]
    for my, mp in months:
        col_headers.append(f"SA 1M% {MONTH_KO.get(mp, mp)}")
    col_headers.append(f"NSA 12M% {MONTH_KO.get(lp, lp)}")

    rows    = []
    summary = {}

    for label, sa_sid, nsa_sid in table_def:
        sa_recs  = api_data.get(sa_sid, [])
        nsa_recs = api_data.get(nsa_sid, [])
        row = [label]

        mom_vals = []
        for my, mp in months:
            py, pp = _prev_period(my, mp)
            curr = _get_val(sa_recs, my, mp)
            prev = _get_val(sa_recs, py, pp)
            v    = _pct(curr, prev)
            row.append(v)
            mom_vals.append(v)

        # 12M NSA
        py_y, py_p = str(int(ly) - 1), lp
        curr_nsa   = _get_val(nsa_recs, ly, lp)
        prev_nsa   = _get_val(nsa_recs, py_y, py_p)
        yoy        = _pct(curr_nsa, prev_nsa)
        row.append(yoy)
        rows.append(row)

        clean = label.replace("　", "").strip()
        if mom_vals[-1] != "-" or yoy != "-":
            summary[clean] = {"mom": mom_vals[-1], "yoy": yoy}

    lines = [
        "| " + " | ".join(col_headers) + " |",
        "| " + " | ".join(["---"] * len(col_headers)) + " |",
    ] + ["| " + " | ".join(r) + " |" for r in rows]

    return "\n".join(lines) + "\n", summary


def _gemini_detail_from_api(indicator: str, summary: dict, date_label: str) -> str:
    """API 데이터 기반 Gemini 섹션별 해설 (HTML 차단 시 폴백)"""
    try:
        import os
        from google import genai as _genai
        key = os.environ.get("GEMINI_API_KEY", "")
        if not key:
            return "_Gemini API 키 없음_\n"
        client = _genai.Client(api_key=key)

        data_lines = "\n".join(
            f"- {k}: 전월비 {v['mom']}%, 전년비 {v['yoy']}%"
            for k, v in summary.items()
        )

        sections_spec = {
            "cpi": (
                "### 식품 (Food)\n[식품 항목 해설]\n\n"
                "### 에너지 (Energy)\n[에너지 항목 해설]\n\n"
                "### 식품 및 에너지 제외 (All items less food and energy)\n[근원물가 해설]"
            ),
            "ppi": (
                "### 최종수요 (Final demand)\n[전체 해설]\n\n"
                "### 최종수요 상품 (Final demand goods)\n[상품 해설]\n\n"
                "### 최종수요 서비스 (Final demand services)\n[서비스 해설]"
            ),
            "nfp": (
                "### 비농업고용 (Total nonfarm)\n[고용 해설]\n\n"
                "### 민간부문 (Total private)\n[업종별 해설]\n\n"
                "### 실업률 및 임금\n[실업률·임금 해설]"
            ),
        }.get(indicator, "")

        prompt = (
            f"미국 BLS {indicator.upper()} {date_label} 데이터:\n{data_lines}\n\n"
            "위 데이터를 바탕으로 BLS 공식 보도자료 문체의 한국어 섹션별 해설을 작성하세요.\n"
            "수치를 구체적으로 언급하고 각 섹션 200~300자 분량으로 작성하세요.\n\n"
            f"출력 형식:\n{sections_spec}"
        )
        resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return resp.text.strip() + "\n"
    except Exception as e:
        print(f"  [Gemini] 실패: {e}")
        return "_해설 생성 실패_\n"


def _build_from_api(indicator: str, source_url: str, date_str: str,
                    table_def: list, api_data: dict) -> str:
    """API 데이터로 Obsidian 양식 마크다운 생성 (HTML 차단 시 폴백)"""
    label_map = {"cpi": "CPI", "ppi": "PPI", "nfp": "비농업고용(NFP)"}
    label     = label_map.get(indicator, indicator.upper())
    title_map = {"cpi": "Table A", "ppi": "Final Demand Table", "nfp": "Employment Table"}

    base_recs    = api_data.get(table_def[0][1], [])
    latest_month = ""
    if base_recs:
        lt = base_recs[-1]
        latest_month = f"{lt['year']}년 {MONTH_KO.get(lt['period'], '')}"

    table_md, summary = _build_api_table(table_def, api_data, indicator)

    md  = f"# {label} 발표 · {date_str}\n\n"
    md += f"> 출처: BLS ({source_url})\n\n"
    md += f"## 📋 {title_map.get(indicator, 'Table')}\n\n"
    md += table_md + "\n"
    md += "## 📝 상세 해설\n\n"
    md += _gemini_detail_from_api(indicator, summary, latest_month)
    md += f"\n---\n*수집: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 출처: BLS*\n"
    return md


# ─── 공개 실행 함수 ───────────────────────────────────────────

def run_cpi(forecast: dict = None):
    print("  [CPI] 시작")
    date_str = datetime.now().strftime("%Y-%m-%d")

    # 1차: HTML 스크래핑
    soup = _try_fetch_html(CPI_URL)
    if soup:
        md = _build_from_html_cpi(soup, date_str)
    else:
        # 2차: API 폴백
        print("  [CPI] BLS API 폴백")
        now = datetime.now()
        all_ids  = list({row[1] for row in CPI_TABLE_A} | {row[2] for row in CPI_TABLE_A})
        api_data = _fetch_bls_api(all_ids, now.year - 1, now.year)
        print(f"  [CPI] API 시리즈 수신: {len(api_data)}개")
        md = _build_from_api("cpi", CPI_URL, date_str, CPI_TABLE_A, api_data)

    save_markdown("cpi", "CPI", md, date_str)
    print("  [CPI] 완료")


def run_ppi(forecast: dict = None):
    print("  [PPI] 시작")
    date_str = datetime.now().strftime("%Y-%m-%d")

    soup = _try_fetch_html(PPI_URL)
    if soup:
        md = _build_from_html_ppi(soup, date_str)
    else:
        print("  [PPI] BLS API 폴백")
        now = datetime.now()
        all_ids  = list({row[1] for row in PPI_TABLE} | {row[2] for row in PPI_TABLE})
        api_data = _fetch_bls_api(all_ids, now.year - 1, now.year)
        md = _build_from_api("ppi", PPI_URL, date_str, PPI_TABLE, api_data)

    save_markdown("ppi", "PPI", md, date_str)
    print("  [PPI] 완료")


def run_nfp(forecast: dict = None):
    print("  [NFP] 시작")
    date_str = datetime.now().strftime("%Y-%m-%d")

    soup = _try_fetch_html(NFP_URL)
    if soup:
        md = _build_from_html_nfp(soup, date_str)
    else:
        print("  [NFP] BLS API 폴백")
        now = datetime.now()
        all_ids  = list({row[1] for row in NFP_TABLE} | {row[2] for row in NFP_TABLE})
        api_data = _fetch_bls_api(all_ids, now.year - 1, now.year)
        md = _build_from_api("nfp", NFP_URL, date_str, NFP_TABLE, api_data)

    save_markdown("nfp", "NFP", md, date_str)
    print("  [NFP] 완료")
