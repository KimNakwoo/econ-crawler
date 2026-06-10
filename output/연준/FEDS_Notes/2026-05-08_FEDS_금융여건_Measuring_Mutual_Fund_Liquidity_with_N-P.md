# FEDS Notes - Measuring Mutual Fund Liquidity with N-PORT

> 날짜: 2026-05-08
> 저자: Erik Larsson, Ty Kawamura, andChaehee Shin
> 주제: 금융여건
> 출처: https://www.federalreserve.gov/econres/notes/feds-notes/measuring-mutual-fund-liquidity-with-n-port-20260508.html

## 📌 초록 (원문)
Open-end mutual funds play a critical role in financial markets and remain major holders of key securities including corporate, Treasury, and municipal bonds. Past stress episodes have exposed the fragility of liquidity provision by corporate bond mutual funds, which can experience large investor outflows that must be met on demand despite holding relatively illiquid assets.

## 📋 한국어 번역
에릭 라르손(Erik Larsson), 타이 카와무라(Ty Kawamura), 신채희 1

개방형 뮤추얼 펀드는 금융 시장에서 중요한 역할을 하며 회사채, 국채, 지방채를 포함한 주요 증권의 주요 보유자로 남아 있습니다. 과거의 스트레스 에피소드는 상대적으로 비유동적인 자산을 보유하고 있음에도 불구하고 수요에 따라 충족되어야 하는 대규모 투자자 유출을 경험할 수 있는 회사채 뮤추얼 펀드의 유동성 공급의 취약성을 노출시켰습니다. 자금은 상환을 충족하기 위해 현금 및 기타 단기 수단을 적극적으로 관리하므로 이러한 유동성 완충 장치는 잠재적인 충격에 대한 첫 번째 방어선 역할을 합니다. 완충 장치는 주요 증권의 가격을 하락시킬 수 있는 불매출을 예방하는 데도 도움이 되므로 이러한 완충 장치의 규모와 구성을 모니터링하는 것은 금융 안정성에 대한 잠재적인 취약성을 이해하는 데 중요합니다. 2

유동성 완충 장치의 중요한 역할에도 불구하고, 회사채 뮤추얼 펀드에서 사용하는 모든 범위의 현금 및 기타 단기 유동 자산을 체계적으로 포착하는 데 사용할 수 있는 쉽게 이용 가능한 포괄적인 유동성 완충 장치는 없습니다. 이 노트에서 우리는 (장기) 회사채 뮤추얼 펀드의 단기 유동 자산 비율(SLAR)을 정의하기 위해 이전 양식을 중단하고 보다 세부적인 보유 자산 분류를 제공한 이후 도입된 증권 거래 위원회(SEC)의 비교적 새로운 양식 N-PORT를 사용합니다. N-PORT 양식은 풍부한 정보를 제공하지만 펀드 유형, 개별 보유 자산의 유동성 분류 등 주요 요소가 공개되지 않아 뮤추얼 펀드 유동성을 측정하기가 어렵습니다. 우리는 이러한 한계를 유연하게 해결하는 새로운 데이터 기반 방법론을 개발합니다. 우리는 N-PORT가 회사채 뮤추얼 펀드의 유동성 포지션과 프로필을 측정하는 데 유용한 도구라는 것을 발견했습니다. 회사채 뮤추얼 펀드는 유동성을 위해 비은행 머니마켓 상품에 크게 의존하고 있으며, 유동성 완충 장치는 스트레스 이후 하락과 그에 따른 재구축의 반복적인 패턴을 따릅니다.

우리의 분석은 등록된 투자 관리 회사가 제출하는 월별 규제 보고서인 SEC Form N-PORT를 기반으로 합니다. 이는 2016년에 시작된 보고 현대화 노력의 결과인 N-CSR, N-CSRS 및 N-Q 형식의 후속입니다. N-PORT의 단계별 규제 준수 기간은 2019년 3분기에 시작되어 전체 파일러를 포함하는 첫 번째 보고 분기인 2020년 2분기에 완료되었습니다. 우리의 목적을 위해 우리는 합리적으로 광범위한 적용 범위를 갖춘 1분기인 2019년 4분기부터 데이터를 사용합니다. 이를 통해 코로나19 팬데믹 충격의 전후 역학을 포착할 수도 있습니다. 데이터는 SEC 웹사이트에서 연구자 친화적인 형식으로 제공됩니다. 3

N-PORT 서류에는 자금 규모, 성과, 보유 자산 및 금융 안정성과 관련된 기타 활동과 관련된 자세한 정보가 포함되어 있지만 일부 양식 항목의 기밀성으로 인해 자금 유동성을 정량화하는 것은 연구자의 창의성에 맡겨져 있습니다. 즉, 항목 C.7은 서류 제출자에게 개인 보유 자산을 네 가지 유동성 분류 중 하나로 분류하도록 요청하지만 이 정보는 대중에게 공개되지 않습니다. 마찬가지로, 펀드는 공정 가치 수준 계층 구조(항목 C.8)를 사용하여 보유 자산을 분류하도록 요청 받지만 이 개념은 데이터가 제공하는 다른 기능과 비교하여 유동성에 대한 프록시가 너무 거칠습니다.

대신 우리는 풍부한 개인 보유 데이터 세트를 활용하여 뮤추얼 펀드 유동성에 대해 누락된 정보를 추론하고 보유 자산별로 펀드 유형을 식별합니다. 구체적으로 보유 데이터에는 자산 유형(항목 C.4.a), 발행자 유형(C.4.b) 및 주소(C.5.a), 채무 증권 만기일(C.9.a) 및 달러 가치(C.2.c)에 대한 세부 정보가 포함됩니다. 우리는 이 정보를 사용하여 단기 유동 자산(SLA)을 다음의 총 달러 금액으로 정의합니다.

비교를 위해 각 펀드의 SLA를 순자산으로 나누어 SLAR(단기유동자산비율)을 구합니다.

마지막으로 N-PORT 데이터를 등록된 투자운용사에 대한 인구 조사와 유사한 정보를 포함하는 연례 보고서인 N-CEN과 결합하여 표 1의 기준을 사용하여 장기 국내 회사채 뮤추얼 펀드 샘플을 구성합니다.

표 2는 2019년 4분기부터 2025년 3분기까지의 기간을 다루고 369개의 고유 펀드를 포함하는 최종 샘플의 선택된 특성을 보여줍니다. 2025년 3분기 기준으로 이들 펀드의 총 순자산은 약 4,510억 달러에 달합니다.

업계 최고의 데이터 엔지니어링 소프트웨어 dbt(데이터 구축 도구)로 선별된 우리의 데이터는 최소한 세 가지 방식으로 뮤추얼 펀드 연구 장치에 기여합니다.

이 섹션에서는 위에 설명된 방법론을 사용하여 결과를 제시하고 논의합니다.

그림 1은 우리 표본의 모든 회사채 뮤추얼 펀드에 대한 유동자산 분포의 시계열을 보여줍니다. 시간 전반에 걸쳐 평균적으로 회사채 뮤추얼 펀드의 평균(중앙값) SLAR은 4.7%(3.4%)입니다. 이는 투자자 환매 비용을 줄이기 위해 유동성 완충 장치를 보유하기 위해 상당한 유동성 전환을 수행하는 펀드의 인센티브와 일치합니다. 그 규모는 현재 중단된 데이터 세트를 기반으로 한 문헌의 이전 연구 결과와도 일치합니다. 7 우리 지표의 주요 차이점은 앞서 설명한 대로 단기 유동 자산을 현금 및 현금 등가물, 국채, 환매조건부채권, STIV로 세밀하게 분해할 수 있다는 것입니다. 이러한 상품은 유동성 완충 장치 역할을 하지만, 유동성은 기초 시장 상황에 따라 달라질 수 있으며, 펀드 유동성을 투자자 환매뿐만 아니라 잠재적으로 해당 시장 상황과 연결합니다.

참고: SLAR은 총 순자산 대비 단기 유동 자산의 비율로 정의됩니다. 샘플의 총 자산이 2020년 2분기에 관찰된 수준의 약 90%에 도달하는 2019년 4분기에 샘플을 시작합니다.

출처: SEC 양식 N-PORT 및 직원 계산.

펀드는 사분위수 범위(25~75번째 백분위수) 약 1.5~7.2%(짙은 빨간색 영역)에서 볼 수 있듯이 SLAR에서 상당한 단면적 이질성을 가지고 있습니다. 비유동성 자산을 보유하고 있는 일부 펀드는 특정 기간(15~85번째 백분위수, 연한 빨간색 영역)에 SLAR이 10%에 달합니다. 게다가 분포는 오른쪽으로 치우쳐 있습니다. 평균(검은 점선)은 중앙값(검은 실선)보다 약 5% 정도 높습니다.

그림 2는 이제 자산 가중 집계 SLAR과 그 구성으로 전환되며, 이는 집계 산업에 대해 더 많은 정보를 제공할 수 있습니다. 몇 가지 관찰이 주목할 만합니다. 첫째, 채권펀드의 유동성 전환은 현금보유보다는 STIV, repo 등 비은행 단기금융시장상품에 크게 의존한다. 이러한 자산은 정상적인 조건에서 유동성을 유지하면서 자금에 추가 수익을 제공합니다. STIV는 샘플의 대부분 기간에서 유동성 보유액의 절반 이상, 즉 총 순자산의 3.2%를 차지합니다. STIV는 뮤추얼 펀드가 마진에서 유동성을 가장 자주 조정하는 도구인 것으로 보입니다. Repo는 총 자산의 1.5%로 SLAR에서 두 번째로 큰 범주를 구성합니다. 현금은 시간이 지남에 따라 총 순자산의 평균 약 0.4%를 차지하며 다음 순위를 차지합니다. 기금은 또한 단기 재무부 채권을 보유하지만 이는 SLAR의 작은 구성 요소일 뿐입니다.

참고: 범례는 아래에서 위로 정렬됩니다. SLAR은 총 순자산 대비 단기 유동 자산(SLA)의 비율로 정의됩니다. 이 그림에서는 샘플에 포함된 모든 회사채 뮤추얼 펀드의 분자(SLA)와 분모(총 순자산)에 대한 집계 값을 사용하여 SLAR을 계산합니다. 샘플의 총 자산이 2020년 2분기에 관찰된 수준의 약 90%에 도달하는 2019년 4분기에 샘플을 시작합니다.

출처: SEC 양식 N-PORT 및 직원 계산.

둘째, 스트레스 이후 SLAR의 하락과 이에 따른 재구축은 채권펀드의 유동성 관리에서 반복되는 패턴으로 보입니다. 예를 들어, 2020년 1분기에 코로나19가 발생한 후 가중 평균 SLAR은 6.5%에서 4.9%로 떨어졌는데, 이는 대규모 투자자 환매를 충족한 결과일 가능성이 높습니다. 그러나 이후 분기 동안 채권 뮤추얼 펀드는 2020년 남은 기간 동안의 강력한 투자자 유입에 힘입어 유동성 포지션을 재구축했고, SLAR은 2021년 초 총 자산의 5.8%로 정점에 이르렀습니다. SLAR이 다시 하락하여 2022년 중반에 최저치를 기록한 후(통화 정책 긴축과 관련된 막대한 투자자 유출로 인해) 이후 반등하여 2021년 말까지 다시 한번 비슷한 높은 수준인 5.5%로 상승했습니다. 2022. 가장 최근에는 일부 채권 뮤추얼 펀드가 시장 변동성 에피소드 이후 대규모 환매를 경험한 2025년 4월 이후 평균 비율이 2025년 2분기 5.1%에서 2025년 3분기 4.3%로 0.8%포인트 감소했습니다. 이러한 관찰은 SLAR이 스트레스 상황과 진화하는 시장 상황에 대응하여 유동 자산의 역동적인 관리를 반영하여 시간이 지남에 따라 크게 변동한다는 점을 강조합니다.

이 관계를 공식화하기 위해 탐색적 최소 제곱(OLS) 회귀 분석을 수행합니다. Table 3은 회귀 분석에 사용된 변수의 요약 통계를 보여준다. 우리는 SLAR과 잠재적으로 상관관계가 있는 두 가지 추가 펀드 수준 특성을 통합합니다. "레벨 3 자산(%)"은 제한된 시장 활동과 공시 가격 또는 관찰 가능한 시장 기반 평가 벤치마크의 부재를 반영하여 공정 가치 계층 구조 하에서 관찰할 수 없는 중요한 입력을 사용하여 공정 가치를 측정하는 자산의 펀드 포트폴리오 지분을 나타냅니다. "가중 평균 만기(WAM)"는 보유 금액을 가중치로 사용하여 펀드가 보유하는 자산의 평균 만기를 취하며 연도 단위로 표시됩니다. 두 변수 모두 포트폴리오 비유동성과 이자율 위험에 대한 프록시 역할을 할 수 있으며, 이는 예방 목적을 위해 더 큰 유동성 완충 장치가 필요할 수 있습니다.

참고: "순 흐름"은 이번 분기에 펀드의 순 흐름을 백분율로 나타낸 것입니다. "레벨 3 자산"은 퍼센트 단위입니다. "WAM"은 가중 평균 성숙도(년)를 나타냅니다. SLAR은 총 순자산 대비 단기 유동 자산(SLA)의 비율로 정의됩니다. 모든 변수는 펀드 분기 분포의 상위 및 하위 2.5%에서 윈저화됩니다.

출처: SEC 양식 N-PORT 및 직원 계산.

표 4는 기존 문헌의 결과와 광범위하게 일치하는 결과를 보여줍니다. 동시 순 흐름은 SLAR과 양의 상관관계가 있지만, 이 평균 효과의 경제적 크기는 미미합니다(분기별 순 흐름의 1% 포인트 증가는 SLAR의 약 5bp 증가와 관련됨). 더 중요한 것은 SLAR이 지난 분기의 극심한 흐름과 높은 상관관계가 있는 것으로 보인다는 것입니다. "최근 높은 유출" 및 "최근 높은 유입"은 각각 펀드의 후행 순 흐름이 자체 흐름 분포의 하위 10%에 속하는지 아니면 상위 10%에 속하는지 여부를 나타냅니다. 열 (1)은 기본 사양을 제공하지만 열 (2)-(4)의 선호 사양은 SLAR 변동의 상당 부분을 흡수하는 시간 및/또는 자금 고정 효과를 도입합니다. 포인트 추정치는 이러한 고정 효과 사양에 따라 다소 다르지만 질적 패턴은 일관되게 유지됩니다. 이전 분기에 비정상적으로 큰 유출을 경험한 펀드는 이후에 낮은 유동성 버퍼를 보유하는 반면, 대규모 유입을 경험한 펀드는 더 높은 버퍼를 보유합니다. 예를 들어, 시간 고정 효과가 있는 열 (2)에서 지난 분기의 극단적인 유출은 0.26% 포인트 낮은 SLAR과 연관되어 있으며 이는 스트레스 유출에 따른 유동성 완충액의 활성 감소와 일치합니다. 자금 및 시간 고정 효과가 모두 포함된 열 (4)에서 이전 분기의 극심한 유입은 0.26% 포인트 높은 SLAR과 관련이 있습니다.

참고: SLAR은 총 순자산 대비 단기 유동 자산(SLA) 비율로 정의됩니다. 여기서는 백분율로 표시됩니다. "순 흐름"은 이번 분기에 펀드의 순 흐름을 백분율로 나타낸 것입니다. "최근 높은 유출"과 "최근 높은 유입"은 각각 지난 분기의 펀드 순 흐름이 펀드 순 흐름 분포의 하위 10% 또는 상위 10%에 속하는 경우 1인 표시 변수입니다. "레벨 3 자산"은 백분율로 표시되며 "1{레벨 3 자산>0}"은 펀드가 엄격히 양수인 레벨 3 자산을 보유하는 경우 1이 되는 표시 변수입니다. "가중 평균 성숙도(WAM)"는 연도 단위로 표시됩니다. 표준 오류는 열 (1)과 (3)의 펀드 시간 수준과 열 (2)와 (4)의 펀드 수준에서 괄호 안에 표시됩니다. 유의성 수준은 *** p<0.01, ** p<0.05, * p<0.1로 표시됩니다.

출처: SEC 양식 N-PORT 및 직원 계산.

펀드의 특성도 중요합니다. 레벨 3 자산의 비중이 높은 펀드는 더 큰 유동성 완충 장치를 보유합니다. 열 (2)에서 레벨 3 자산의 긍정적인 지분을 보유한 펀드는 SLAR의 0.59% 포인트 증가와 관련되어 비유동성 펀드에 대한 사전 유동성 관리의 역할을 강조합니다. 펀드 고정 효과가 도입되면 열 (3)-(4)에서 계수는 통계적으로 유의하지 않게 됩니다. 이는 시간이 지남에 따라 포트폴리오 할당이 펀드 내에서 매우 안정적인 경향이 있다는 사실을 반영하는 것 같습니다. 성숙도와의 관계는 더욱 미묘합니다. WAM이 길어질수록 대부분의 사양에서 SLAR이 낮아지고, 이는 장기 자산을 보유하는 펀드가 금리 위험에 더 많이 노출됨에도 불구하고 단기 유동성 요구가 낮아지고 신용 위험이 낮아질 수 있음을 시사합니다.

이 노트에서는 N-PORT에 대한 데이터 기반의 유연한 접근 방식을 사용하는 것이 주요 정보를 사용할 수 없거나 데이터에서 불완전하게 관찰되는 환경에서 뮤추얼 펀드 유동성을 측정하기 위한 강력한 도구가 될 수 있음을 보여줍니다. 우리의 분석에 따르면 회사채 뮤추얼 펀드는 유동성 완충 장치로 다양한 단기 유동 자산, 특히 STIV와 repo를 많이 사용하는 것으로 나타났습니다. 이는 펀드 유동성이 투자자 환매뿐 아니라 이러한 비은행 단기 금융시장 상품 시장 상황에 의해서도 형성된다는 것을 암시할 수 있습니다. 이러한 유동성 포지션은 시간이 지남에 따라 크게 변동하며, 스트레스 후 감소와 후속 재건의 체계적인 패턴을 나타냅니다. 마지막으로, 우리가 선별한 데이터와 SLA(R) 지표는 다양한 자금 샘플에 대한 유동성 모니터링 활동으로 쉽게 확장 가능합니다.

Anadu, Kenechukwu 및 Fang Cai(2019). "미국 은행 대출 및 고수익 뮤추얼 펀드의 유동성 전환 위험", FEDS 노트. 워싱턴: 연방준비제도 이사회, 2019년 8월 9일.

Chernenko, Sergey, Aditya Sunderam(2016). " 자산 관리의 유동성 변화: 뮤추얼 펀드의 현금 보유에서 얻은 증거(PDF) ." 국립 경제 연구국 조사 보고서 22391.

Chernenko, Sergey 및 Viet-Dung Doan(2024). "흐름 유발 거래: 지방채 뮤추얼 펀드의 일일 거래에서 얻은 증거." SSRN 4684397에서 이용 가능합니다.

Jiang, Hao, Dan Li, Ashley Wang(2021). " 회사채 뮤추얼 펀드를 통한 역동적인 유동성 관리 ." 금융 및 정량 분석 ​​저널 56(5): 1622-1652.

1. 여기에 표현된 견해는 엄밀히 말하면 저자의 견해이며 반드시 연방준비제도이사회나 연방준비제도의 견해를 대변하는 것은 아닙니다.  텍스트로 돌아가기

2. 현행 SEC 규정 22e-4에 따라 개방형 펀드는 보유 자산을 4가지 유동성 범주로 분류하고 "고유동성 투자 최소 기준"(HLIM)을 설정해야 합니다. 그러나 이 요구 사항은 주로 유동성이 높은 자산을 보유하지 않는 펀드에만 적용되며, 펀드는 일정한 최소 금액 없이 유연하게 자체 HLIM을 설정할 수도 있습니다. 2022년에 SEC는 요건을 모든 펀드로 확대하고 HLIM에 대해 순자산의 최소 10%에 대한 엄격한 기준을 설정하는 개정안을 제안했습니다. 그러나 이 층은 2024년 최종 규칙에서는 채택되지 않았습니다.  텍스트로 돌아가기

3. https://www.sec.gov/data-research/sec-markets-data/form-n-port-data-sets.  텍스트로 돌아가기

4. 모든 증권 유형에 대해 데이터는 남은 성숙도만 보고하므로 원래 성숙도 대신 남은 성숙도를 사용합니다. 이러한 방식으로 샘플에는 원래 만기가 길었지만 남은 만기가 짧아 일반적으로 유동성이 높은 증권이 포함됩니다.  텍스트로 돌아가기

5. STIV는 본질적으로 단기 유동 자산이고 데이터의 대부분의 STIV 관찰에는 만기 날짜가 포함되어 있지 않기 때문에 STIV에 대한 90일 만기 제한을 완화합니다.  텍스트로 돌아가기

6. 55% 컷오프는 순자산 대비 부채 보유 분포에 대한 탐색적 데이터 분석을 통해 알 수 있으며, 이는 다양한 펀드 전략으로 인해 다양합니다. 우리는 55% 기준점 이상의 펀드가 국내 회사채 펀드의 실제 모집단을 대표한다고 평가합니다.  텍스트로 돌아가기

7. Jiang, Li, and Wang(2021)은 2002~2014년 반기별 N-SAR 신고(중단)를 사용하여 회사채 펀드가 보유한 평균 현금이 총 자산의 약 5%인 것으로 확인했습니다. Chernenko와 Sunderam(2016)도 동일한(중단된) 데이터를 사용하여 2004~2012년 회사채 펀드의 현금 및 현금 등가물 보유 중앙값이 5.3%임을 확인했습니다. Anadu 및 Cai(2019)는 2007~2019년에 특정 은행 대출 및 고수익 뮤추얼 펀드의 평균 현금 및 현금 등가물 보유 비율이 더 높다는 사실을 발견했습니다.  텍스트로 돌아가기

라르손, 에릭, 타이 카와무라, 신채희(2026). "N-PORT를 통한 뮤추얼 펀드 유동성 측정", FEDS Notes. 워싱턴: 연방준비제도 이사회, 2026년 5월 8일, https://doi.org/10.17016/2380-7172.4037.

면책 조항: FEDS Notes는 이사회 직원이 자신의 견해를 제공하고 경제 및 금융 분야의 다양한 주제에 대한 분석을 제공하는 기사입니다. 이 기사는 FEDS 작업 보고서 및 IFDP 보고서보다 짧고 기술 지향적이지 않습니다.

## 📄 영문 원본
Erik Larsson, Ty Kawamura, and  Chaehee Shin 1

Open-end mutual funds play a critical role in financial markets and remain major holders of key securities including corporate, Treasury, and municipal bonds. Past stress episodes have exposed the fragility of liquidity provision by corporate bond mutual funds, which can experience large investor outflows that must be met on demand despite holding relatively illiquid assets. Funds actively manage cash and other short-term instruments to meet redemptions, making these liquidity buffers serve as the first line of defense against potential shocks. Because the buffers also help prevent fire sales that could depress prices of key securities, monitoring the size and composition of these buffers is central to understanding potential vulnerabilities to financial stability. 2

Despite the important role of liquidity buffers, there is no readily available, comprehensive metric of liquidity buffers that can be used to systematically capture the full range of cash and other short-term liquid assets used by corporate bond mutual funds. In this note, we use the Securities and Exchange Commission's (SEC) relatively new Form N-PORT—introduced following the discontinuation of prior forms and providing more granular classifications of holdings—to define Short-Term Liquid Assets Ratio (SLAR) of (long-term) corporate bond mutual funds. While Form N-PORT offers rich information, key elements including the fund type and liquidity classification of individual holdings are not publicly disclosed and make it challenging to measure mutual fund liquidity. We develop a new data-informed methodology that flexibly resolves these limitations. We find that N-PORT is a valuable tool for measuring liquidity positions and profiles of corporate bond mutual funds. Corporate bond mutual funds rely heavily on nonbank money market instruments for liquidity, and liquidity buffers follow a recurring pattern of post-stress drawdowns and subsequent rebuilding.

Our analysis is based on SEC Form N-PORT, a monthly regulatory report filed by registered investment management companies. It is the successor of forms N-CSR, N-CSRS, and N-Q that resulted from reporting modernization efforts that began in 2016. A phased regulatory compliance period for N-PORT began in 2019 Q3 and finished in 2020 Q2, the first reporting quarter containing the full universe of filers. For our purposes, we use the data beginning in 2019 Q4, the first quarter with reasonably broad coverage, which also allows us to capture the before-and-after dynamics of the COVID-19 pandemic shock. The data are available in researcher-friendly format on the SEC website. 3

While N-PORT filings contain detailed information related to fund size, performance, holdings, and other activities relevant to financial stability, quantifying fund liquidity is left to the creativity of researchers due to the confidentiality of some form items. Namely, Item C.7 asks filers to categorize their individual holdings into one of four liquidity classifications, but this information is not disclosed to the public. Similarly, funds are asked to classify their holdings using the Fair Value Level Hierarchy (Item C.8), but this concept is too coarse of a proxy for liquidity relative to what other features of the data offer.

We instead draw on the rich set of individual holdings data to infer the missing information on mutual fund liquidity and identify fund types by their asset holdings. Specifically, the holdings data contain details about the asset type (Item C.4.a), issuer type (C.4.b) and domicile (C.5.a), maturity date for debt securities (C.9.a), and dollar value (C.2.c). We use this information to define  Short-Term Liquid Assets  (SLA) as the total dollar amount of:

For comparison purposes, we divide the SLA for each fund by its net assets to arrive at the  Short-Term Liquid Assets Ratio  (SLAR).

Finally, we augment the N-PORT data by joining it with N-CEN, an annual report that contains census-like information about registered investment management companies, to construct our sample of long-term, domestic corporate bond mutual funds using the criteria in Table 1.

Table 2 shows selected characteristics of the final sample, which covers the time period of 2019 Q4-2025 Q3 and contains 369 unique funds. As of 2025 Q3, these funds account for about $451 billion in total net assets altogether.

Our data, curated with the industry-leading data engineering software  dbt  (data build tool), contributes to the mutual fund research apparatus in at least three ways:

This section presents and discusses the findings using the methodology described above.

Figure 1 shows the time series of the distribution of liquid assets for all corporate bond mutual funds in our sample. On average across time, an average (median) corporate bond mutual fund has a SLAR of 4.7% (3.4%). This is consistent with the incentives of funds undertaking significant liquidity transformation to hold liquidity buffers to reduce the costs of meeting investor redemptions. The magnitude is also in line with previous findings from the literature based on datasets that are now discontinued. 7  The key distinction of our metric is that it allows for the granular decomposition of short-term liquid assets into cash and cash equivalents, Treasury Bills, repos, and STIVs as described earlier. These instruments serve as liquidity buffers, though their liquidity may vary with conditions in underlying markets, linking fund liquidity not only to investor redemptions but also potentially to those market conditions.

Note: SLAR is defined as short-term liquid assets as a percentage of total net assets. We begin the sample in 2019 Q4, when total assets in our sample reach roughly 90% of the level observed in 2020 Q2, the first quarter with full coverage.

Source: SEC form N-PORT and staff calculations.

Funds have significant cross-sectional heterogeneity in SLAR, as can be seen from the interquartile range (25-75th percentile) of about 1.5-7.2% (dark red region). Some funds, likely the ones with illiquid holdings, have SLAR as high as 10% in some periods (15-85th percentile, light red region). Furthermore, the distribution is right-skewed; the average (dashed black line) hovers around 5%, above the median (solid black line).

Figure 2 now turns to the asset-weighted aggregated SLAR and its composition, which may be more informative about the aggregate industry. Several observations are noteworthy. First, liquidity transformation of bond funds significantly relies on nonbank money market instruments such as STIVs and repos, rather than cash holdings alone. These assets offer funds additional yields while remaining liquid under normal conditions. STIVs amount to more than half of liquidity holdings, or 3.2% of total net assets, in most periods in our sample. STIVs appear to be the instrument through which mutual funds most often adjust their liquidity at the margin. Repo constitutes the second-largest category of SLAR, at 1.5% of total assets. Cash ranks next, with an average share of around 0.4% of total net assets over time. Funds also hold short-term Treasury bills but these account for only a minor component of SLAR.

Note: Legend ordered from bottom to top. SLAR is defined as short-term liquid assets (SLA) as a percentage of total net assets. In this figure, we compute SLAR using aggregate values for both the numerator (SLA) and the denominator (total net assets) across all corporate bond mutual funds in our sample. We begin the sample in 2019 Q4, when total assets in our sample reach roughly 90% of the level observed in 2020 Q2, the first quarter with full coverage.

Source: SEC form N-PORT and staff calculations.

Second, the post-stress decline in SLAR followed by subsequent rebuilding appears to be a recurring pattern in liquidity management by bond funds. For instance, after the Covid-19 outbreak in 2020 Q1, the weighted-average SLAR fell from 6.5% to 4.9%, likely an outcome of meeting heavy investor redemptions. Over the subsequent quarters, however, bond mutual funds rebuilt their liquidity positions, supported by strong investor inflows in the remainder of 2020, and SLAR peaked at 5.8% of total assets in early 2021. After the SLAR declined again, reaching its lowest in mid-2022—likely following heavy investor outflows associated with monetary policy tightening—it subsequently rebounded, rising to a similarly high level of 5.5% once again by the end of 2022. Most recently, after April 2025 when some bond mutual funds experienced large redemptions after market volatility episodes, the average ratio declined by 0.8 percentage points, from 5.1% in 2025 Q2 to 4.3% in 2025 Q3. These observations highlight that SLAR fluctuates substantially over time, reflecting the dynamic management of liquid assets in response to stress episodes and evolving market conditions.

To formalize this relationship, we conduct an exploratory ordinary least squares (OLS) regression analysis. Table 3 shows the summary statistics of variables used for the regression. We incorporate two additional fund-level characteristics potentially correlated with SLAR. "Level 3 assets (%)" indicate the fund's portfolio share of assets whose fair values are measured using significant unobservable inputs under the fair value hierarchy, reflecting limited market activity and the absence of quoted prices or observable market-based valuation benchmarks. "Weighted Average Maturity (WAM)" takes the average maturity of the assets held by the fund, using holding amounts as weights, and is shown in years. Both variables might serve as proxies for portfolio illiquidity and interest rate risk, which may necessitate a larger liquidity buffer for precautionary purposes.

Note: "Net flow" is fund's net flow this quarter, in percent. "Level 3 Assets" is in percent. "WAM" refers to weighted average maturity, in years. SLAR is defined as short-term liquid assets (SLA) as a percentage of total net assets. All variables are winsorized at the top and bottom 2.5% of fund-quarter distribution.

Source: SEC form N-PORT and staff calculations.

Table 4 shows the results that broadly align with findings in existing literature. Contemporaneous net flows are positively associated with SLAR, although the economic magnitude of this average effect is modest (a one-percentage-point increase in quarterly net flows is associated with around 5 basis point increase in SLAR). More importantly, SLAR seems to be highly correlated with extreme flows in the last quarter. "Recent High Outflow" and "Recent High Inflow" each indicate whether the fund's lagged net flow fell in the bottom or top 10% of its own flow distribution. While Column (1) provides a baseline specification, the preferred specifications in Columns (2)-(4) introduce time and/or fund fixed effects, which absorb a substantial share of the variation in SLAR. Although the point estimates vary somewhat across these fixed effects specifications, the qualitative pattern remains consistent: funds that experienced unusually large outflows in the previous quarter hold lower liquidity buffers subsequently, whereas those that experienced large inflows hold higher buffers. For instance, in Column (2) with time fixed effects, extreme outflows in the last quarter are associated with SLAR lower by 0.26 percentage points, consistent with active drawdowns of liquidity buffers following stress outflows. In Column (4), which includes both fund and time fixed effects, extreme inflows in the previous quarter are associated with 0.26 percentage points higher SLAR.

Note: SLAR is defined as short-term liquid assets (SLA) as a percentage of total net assets; here it is shown in percent. "Net flow" is fund's net flow this quarter, in percent. "Recent High Outflow" and "Recent High Inflow" are each indicator variables that are 1 if the fund's net flow in the last quarter belong to either bottom or top 10% of the fund's net flow distribution. "Level 3 Assets" is in percent and "1{Level 3 Assets>0}" is an indicator variable that is 1 if the fund has a strictly positive Level 3 assets. "Weighted Average Maturity (WAM)" is shown in years. Standard errors are clustered at the fund-time-level in Columns (1) and (3), and at the fund-level in Columns (2) and (4), reported in parentheses. Significance levels are denoted by: *** p<0.01, ** p<0.05, * p<0.1.

Source: SEC form N-PORT and staff calculations.

Fund characteristics also matter. Funds with a higher share of Level 3 assets hold larger liquidity buffers. In Column (2), funds that have positive shares of Level 3 assets are associated with a 0.59 percentage point increase in SLAR, highlighting the role of precautionary liquidity management for illiquid funds. The coefficient becomes statistically insignificant in Columns (3)-(4) once fund fixed effects are introduced, which likely reflects the fact that portfolio allocations tend to be highly stable within funds over time. The relationship with maturity is more nuanced. Longer WAM is associated with lower SLAR in most specifications, suggesting that funds holding longer-dated assets may face lower short-term liquidity needs and lower credit risk, despite greater exposure to interest rate risk.

In this note, we show that using a data-informed, flexible approach on N-PORT can be a powerful tool for measuring mutual fund liquidity, in settings where key information is unavailable or incompletely observed in the data. Our analysis reveals that corporate bond mutual funds heavily use a range of short-term liquid assets as liquidity buffers, in particular, STIVs and repos. It might imply that fund liquidity is shaped not only by investor redemptions but also by conditions in markets for these nonbank money market instruments. These liquidity positions fluctuate significantly over time, exhibiting a systematic pattern of post-stress decline followed by subsequent rebuilding. Finally, our curated data and SLA(R) metrics are easily scalable to liquidity monitoring exercises for different samples of funds.

Anadu, Kenechukwu, and Fang Cai (2019). " Liquidity Transformation Risks in U.S. Bank Loan and High-Yield Mutual Funds ," FEDS Notes. Washington: Board of Governors of the Federal Reserve System, August 9, 2019.

Chernenko, Sergey, and Aditya Sunderam (2016). " Liquidity Transformation in Asset Management: Evidence from the Cash Holdings of Mutual Funds (PDF) ." National Bureau of Economic Research Working Paper 22391.

Chernenko, Sergey, and Viet-Dung Doan (2024). "Flow-induced trading: Evidence from the daily trading of municipal bond mutual funds." Available at SSRN 4684397.

Jiang, Hao, Dan Li, and Ashley Wang (2021). " Dynamic Liquidity Management by Corporate Bond Mutual Funds ." Journal of Financial and Quantitative Analysis 56 (5): 1622-1652.

1. The views expressed here are strictly those of the authors and do not necessarily represent the views of the Federal Reserve Board or the Federal Reserve System.  Return to text

2. Under the current SEC Rule 22e-4, open-end funds must classify their holdings into four liquidity categories and set a "highly liquid investment minimum" (HLIM). However, this requirement only applies to funds that do not primarily hold highly liquid assets, and the funds can also flexibly set their own HLIM, without any uniform minimum. In 2022, the SEC proposed amendments that would have extended the requirement to all funds and set a hard floor of at least 10% of net assets for HLIM; however, this floor was not adopted in the 2024 final rule.  Return to text

3.  https://www.sec.gov/data-research/sec-markets-data/form-n-port-data-sets .  Return to text

4. For all security types, we rely on remaining maturity instead of original maturity since the data only reports remaining maturity. In this way, the sample includes securities that may have had longer original maturities but now have short remaining maturities, which are typically highly liquid.  Return to text

5. We relax the 90-day maturity restriction for STIVs since they are short-term liquid assets by nature and most STIV observations in the data do not contain a maturity date.  Return to text

6. The 55% cutoff is informed by our exploratory data analysis of the distribution of debt holdings relative to net assets, which is multimodal due to differing fund strategies. We assess that funds at or above the 55% threshold are representative of the true population of domestic corporate bond funds.  Return to text

7. Jiang, Li, and Wang (2021) find the average cash held by corporate bond funds to be around 5% of total assets using semi-annual N-SAR filings (discontinued) for 2002-2014. Chernenko and Sunderam (2016) also use the same (discontinued) data and find a median cash and cash equivalent holding of 5.3% for corporate bond funds for 2004-2012. Anadu and Cai (2019) find higher ratios of average cash and cash equivalent holdings for selected bank loan and high-yield mutual funds for 2007-2019.  Return to text

Larsson, Erik, Ty Kawamura, and Chaehee Shin (2026). "Measuring Mutual Fund Liquidity with N-PORT," FEDS Notes. Washington: Board of Governors of the Federal Reserve System, May 08, 2026, https://doi.org/10.17016/2380-7172.4037.

Disclaimer:  FEDS Notes are articles in which Board staff offer their own views and present analysis on a range of topics in economics and finance. These articles are shorter and less technically oriented than FEDS Working Papers and IFDP papers.


---
*출처: https://www.federalreserve.gov/econres/notes/feds-notes/measuring-mutual-fund-liquidity-with-n-port-20260508.html | 수집: 2026-06-10 01:16 | 지표: FEDS_NOTES*
