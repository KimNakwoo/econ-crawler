# ============================================================
# crawler_bls.py - BLS 공개 API 기반 CPI / PPI / NFP 크롤러
#
# BLS.gov HTML/PDF는 GitHub Actions IP를 차단하므로
# BLS 공개 데이터 API(api.bls.gov)를 사용합니다.
# 인증 없이 일 500건 요청 가능. 인증 추가 시 3,000건.
# ============================================================
import json
import re
import time
import requests
from datetime import datetime
from config import REQUEST_TIMEOUT, REQUEST_DELAY
from utils import save_markdown, translate_paragraph_by_paragraph, get_headers
BLS_API_V2 = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
# ─── 시리즈 정의 ──────────────────────────────────────────────
CPI_SERIES = {
    "CPI 전체 (미계절조정)":             "CUUR0000SA0",
    "CPI 근원 (미계절조정)":             "CUUR0000SA0L1E",
    "CPI 전체 (계절조정)":               "CUSR0000SA0",
    "CPI 근원 (계절조정)":               "CUSR0000SA0L1E",
    "식품":                              "CUUR0000SAF",
    "에너지":                            "CUUR0000SA0E",
    "주거":                              "CUUR0000SAH1",
    "교통":                              "CUUR0000SAT",
    "의료":                              "CUUR0000SAM",
}
PPI_SERIES = {
    "PPI 최종수요":                      "WPSFD4",
    "최종수요 상품":                     "WPSFD49116",
    "최종수요 서비스":                   "WPSFD4131",
    "최종수요 (식품·에너지 제외)":       "WPSFD4111",
}
NFP_SERIES = {
    "비농업고용 총계 (천명)":            "CES0000000001",
    "민간부문 고용 (천명)":              "CES0500000001",
    "실업률 (%)":                        "LNS14000000",
    "경제활동참가율 (%)":                "LNS11300000",
    "시간당 임금 ($)":                   "CES0500000003",
    "주당 평균 근무시간":                "CES0500000002",
}
MONTH_KO = {
    "M01":"1월","M02":"2월","M03":"3월","M04":"4월",
    "M05":"5월","M06":"6월","M07":"7월","M08":"8월",
    "M09":"9월","M10":"10월","M11":"11월","M12":"12월",
}
# ─── BLS API 요청 ─────────────────────────────────────────────
def _fetch_bls_api(series_ids: list, start_year: int = None, end_year: int = None) -> dict:
    """
    BLS API v2에서 시리즈 데이터 일괄 요청
    반환: {series_id: [{"year":..,"period":..,"value":..}, ...]}
    """
    now = datetime.now()
    if not end_year:
        end_year = now.year
    if not start_year:
        start_year = now.year - 1   # 전년도부터 조회 (YoY 계산용)
    payload = {
        "seriesid":  series_ids,
        "startyear": str(start_year),
        "endyear":   str(end_year),
    }
    time.sleep(REQUEST_DELAY)
    resp = requests.post(
        BLS_API_V2,
        json=payload,
        headers={"Content-Type": "application/json", **get_headers()},
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "REQUEST_SUCCEEDED":
        raise Exception(f"BLS API 오류: {data.get('message', data.get('status'))}")
    result = {}
    for series in data.get("Results", {}).get("series", []):
        sid = series["seriesID"]
        result[sid] = sorted(
            series.get("data", []),
            key=lambda x: (x["year"], x["period"]),
        )
    return result
# ─── 계산 유틸 ────────────────────────────────────────────────
def _get_value(records: list, year: str, period: str) -> float | None:
    for r in records:
        if r["year"] == year and r["period"] == period:
            try:
                return float(r["value"])
            except (ValueError, KeyError):
                return None
    return None
def _latest(records: list) -> dict | None:
    """가장 최신 레코드 반환 (연간 제외, M01-M12만)"""
    monthly = [r for r in records if r["period"].startswith("M") and r["period"] != "M13"]
    return monthly[-1] if monthly else None
def _prev_month_period(year: str, period: str) -> tuple:
    m = int(period[1:])
    y = int(year)
    if m == 1:
        return str(y - 1), "M12"
    return str(y), f"M{m-1:02d}"
def _same_month_last_year(year: str, period: str) -> tuple:
    return str(int(year) - 1), period
def _pct_change(new: float | None, old: float | None) -> str:
    if new is None or old is None or old == 0:
        return "N/A"
    return f"{(new - old) / old * 100:+.2f}%"
def _fmt_val(val: float | None, decimals: int = 3) -> str:
    if val is None:
        return "N/A"
    return f"{val:.{decimals}f}"
# ─── 마크다운 테이블 생성 ──────────────────────────────────────
def _build_table(label: str, series_map: dict, api_data: dict) -> str:
    rows = []
    latest_period_label = ""
    for name, sid in series_map.items():
        records = api_data.get(sid, [])
        if not records:
            rows.append([name, "N/A", "N/A", "N/A"])
            continue
        latest = _latest(records)
        if not latest:
            rows.append([name, "N/A", "N/A", "N/A"])
            continue
        y, p = latest["year"], latest["period"]
        if not latest_period_label:
            latest_period_label = f"{y}년 {MONTH_KO.get(p, p)}"
        val = _get_value(records, y, p)
        py, pp = _prev_month_period(y, p)
        val_prev = _get_value(records, py, pp)
        yy, yp = _same_month_last_year(y, p)
        val_yoy = _get_value(records, yy, yp)
        # NFP 고용은 절대값(천명) + 전월차, 지수류는 % 변화
        if "천명" in name:
            chg_mom = f"{val - val_prev:+.0f}천명" if val and val_prev else "N/A"
            chg_yoy = f"{val - val_yoy:+.0f}천명" if val and val_yoy else "N/A"
            val_str = f"{val:,.0f}천명" if val else "N/A"
        elif "%" in name or "시간당" in name or "근무시간" in name:
            chg_mom = _pct_change(val, val_prev) if not ("%" in name) else (f"{val - val_prev:+.1f}%p" if val and val_prev else "N/A")
            chg_yoy = f"{val - val_yoy:+.2f}" if val and val_yoy else "N/A"
            val_str = _fmt_val(val, 1)
        else:
            chg_mom = _pct_change(val, val_prev)
            chg_yoy = _pct_change(val, val_yoy)
            val_str = _fmt_val(val, 3)
        rows.append([name, val_str, chg_mom, chg_yoy])
    if not rows:
        return "_데이터 없음_\n"
    period_hdr = latest_period_label or "최신"
    header = ["항목", f"수치 ({period_hdr})", "전월비", "전년동월비"]
    lines = (
        ["| " + " | ".join(header) + " |",
         "| " + " | ".join(["---"] * len(header)) + " |"]
        + ["| " + " | ".join(r) + " |" for r in rows]
    )
    return "\n".join(lines) + "\n"
# ─── Gemini 해설 생성 ──────────────────────────────────────────
def _gemini_analysis(indicator: str, table_md: str, forecast: dict) -> str:
    """
    BLS 데이터 테이블을 바탕으로 Gemini가 한국어 해설 생성
    """
    try:
        from google import genai
        import os
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            return "_Gemini API 키 없음 - 해설 생략_\n"
        client = genai.Client(api_key=api_key)
        forecast_text = ""
        if forecast:
            lines = [f"- {k}: {v}" for k, v in forecast.items()]
            forecast_text = "\n".join(lines)
        prompt = f"""당신은 전문 경제 애널리스트입니다.
아래 {indicator} 데이터를 바탕으로 한국어로 간결하고 전문적인 해설을 작성하세요.
{f'예측치 정보:{chr(10)}{forecast_text}{chr(10)}' if forecast_text else ''}
데이터 테이블:
{table_md}
작성 지침:
- 핵심 수치(전월비, 전년비) 중심으로 서술
- 시장 함의(연준 정책 방향) 1~2문장 포함
- 총 200~300자 이내
- 특수 기호나 마크다운 없이 평문으로 작성"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text.strip() + "\n"
    except Exception as e:
        print(f"  [Gemini 해설] 실패: {e}")
        return "_해설 생성 실패_\n"
# ─── 공개 실행 함수 ───────────────────────────────────────────
def run_cpi(forecast: dict = None):
    print("  [CPI] BLS API 크롤링 시작")
    date_str = datetime.now().strftime("%Y-%m-%d")
    forecast = forecast or {}
    series_ids = list(CPI_SERIES.values())
    api_data = _fetch_bls_api(series_ids)
    print(f"  [CPI] API 데이터 수신: {len(api_data)}개 시리즈")
    table_md = _build_table("CPI", CPI_SERIES, api_data)
    md  = f"# CPI 발표 · {date_str}\n\n"
    md += f"> 출처: BLS Public Data API (api.bls.gov)\n\n"
    if forecast:
        md += "## 📊 예측치 vs 실제치\n\n"
        rows = []
        for name, val in forecast.items():
            parts    = [p.strip() for p in val.split("|")]
            actual   = parts[0].replace("실제:", "").strip() if parts       else "-"
            fcast    = parts[1].replace("예측:", "").strip() if len(parts)>1 else "-"
            previous = parts[2].replace("이전:", "").strip() if len(parts)>2 else "-"
            rows.append([name, actual, fcast, previous])
        hdr = ["항목", "실제치", "예측치", "이전치"]
        md += "| " + " | ".join(hdr) + " |\n"
        md += "| " + " | ".join(["---"] * len(hdr)) + " |\n"
        for r in rows:
            md += "| " + " | ".join(r) + " |\n"
        md += "\n"
    md += "## 📋 CPI 주요 항목\n\n"
    md += table_md + "\n"
    md += "## 📝 해설\n\n"
    md += _gemini_analysis("CPI (소비자물가지수)", table_md, forecast)
    md += f"\n---\n*수집: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 출처: BLS API*\n"
    save_markdown("cpi", "CPI", md, date_str)
    print("  [CPI] 완료")
def run_ppi(forecast: dict = None):
    print("  [PPI] BLS API 크롤링 시작")
    date_str = datetime.now().strftime("%Y-%m-%d")
    forecast = forecast or {}
    series_ids = list(PPI_SERIES.values())
    api_data = _fetch_bls_api(series_ids)
    print(f"  [PPI] API 데이터 수신: {len(api_data)}개 시리즈")
    table_md = _build_table("PPI", PPI_SERIES, api_data)
    md  = f"# PPI 발표 · {date_str}\n\n"
    md += f"> 출처: BLS Public Data API (api.bls.gov)\n\n"
    if forecast:
        md += "## 📊 예측치 vs 실제치\n\n"
        rows = []
        for name, val in forecast.items():
            parts    = [p.strip() for p in val.split("|")]
            actual   = parts[0].replace("실제:", "").strip() if parts       else "-"
            fcast    = parts[1].replace("예측:", "").strip() if len(parts)>1 else "-"
            previous = parts[2].replace("이전:", "").strip() if len(parts)>2 else "-"
            rows.append([name, actual, fcast, previous])
        hdr = ["항목", "실제치", "예측치", "이전치"]
        md += "| " + " | ".join(hdr) + " |\n"
        md += "| " + " | ".join(["---"] * len(hdr)) + " |\n"
        for r in rows:
            md += "| " + " | ".join(r) + " |\n"
        md += "\n"
    md += "## 📋 PPI 주요 항목\n\n"
    md += table_md + "\n"
    md += "## 📝 해설\n\n"
    md += _gemini_analysis("PPI (생산자물가지수)", table_md, forecast)
    md += f"\n---\n*수집: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 출처: BLS API*\n"
    save_markdown("ppi", "PPI", md, date_str)
    print("  [PPI] 완료")
def run_nfp(forecast: dict = None):
    print("  [NFP] BLS API 크롤링 시작")
    date_str = datetime.now().strftime("%Y-%m-%d")
    forecast = forecast or {}
    series_ids = list(NFP_SERIES.values())
    api_data = _fetch_bls_api(series_ids)
    print(f"  [NFP] API 데이터 수신: {len(api_data)}개 시리즈")
    table_md = _build_table("NFP", NFP_SERIES, api_data)
    md  = f"# 비농업고용(NFP) 발표 · {date_str}\n\n"
    md += f"> 출처: BLS Public Data API (api.bls.gov)\n\n"
    if forecast:
        md += "## 📊 예측치 vs 실제치\n\n"
        rows = []
        for name, val in forecast.items():
            parts    = [p.strip() for p in val.split("|")]
            actual   = parts[0].replace("실제:", "").strip() if parts       else "-"
            fcast    = parts[1].replace("예측:", "").strip() if len(parts)>1 else "-"
            previous = parts[2].replace("이전:", "").strip() if len(parts)>2 else "-"
            rows.append([name, actual, fcast, previous])
        hdr = ["항목", "실제치", "예측치", "이전치"]
        md += "| " + " | ".join(hdr) + " |\n"
        md += "| " + " | ".join(["---"] * len(hdr)) + " |\n"
        for r in rows:
            md += "| " + " | ".join(r) + " |\n"
        md += "\n"
    md += "## 📋 고용 주요 항목\n\n"
    md += table_md + "\n"
    md += "## 📝 해설\n\n"
    md += _gemini_analysis("NFP (비농업고용)", table_md, forecast)
    md += f"\n---\n*수집: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 출처: BLS API*\n"
    save_markdown("nfp", "NFP", md, date_str)
    print("  [NFP] 완료")
