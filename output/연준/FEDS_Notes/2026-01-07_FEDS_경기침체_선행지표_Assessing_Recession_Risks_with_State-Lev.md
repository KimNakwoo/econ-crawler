# FEDS Notes - Assessing Recession Risks with State-Level Data

> 날짜: 2026-01-07
> 저자: Hie Joo Ahn, Yunjong Eo, and Lucas Moyon
> 주제: 경기침체/선행지표
> 출처: https://www.federalreserve.gov/econres/notes/feds-notes/assessing-recession-risks-with-state-level-data-20260107.html

## 📌 초록 (원문)
This note evaluates recession risks at the national and state levels using a state-of-the-art Bayesian Markov-switching model that distinguishes between full-recovery recessions (U-shaped recessions) and those that generate lasting damage, or hysteresis (L-shaped recessions). While states exhibit considerable heterogeneity in their business-cycle experiences, most saw some degree of hysteresis in the past recessions that occurred prior to the COVID pandemic. By contrast, the model classifies the pandemic-induced recession as a full-recovery episode with a low likelihood of hysteresis, reflecting the rapid rebound from the sharp downturn. The model suggests that the risk of a national recession has been low of late, though the state-level data reveal pockets of risk.

## 📋 한국어 번역
안희주 2, 어윤종 3, 루카스 모욘

이 노트는 완전 회복 경기 침체(U자형 경기 침체)와 지속적인 손상 또는 히스테리시스(L자형 경기 침체)를 생성하는 경기 침체를 구별하는 최첨단 베이지안 마르코프 전환 모델을 사용하여 국가 및 주 차원에서 경기 침체 위험을 평가합니다. 주정부는 경기주기 경험에서 상당한 이질성을 보였지만, 대부분은 코로나19 대유행 이전에 발생한 경기 침체에서 어느 정도 히스테리시스를 경험했습니다. 대조적으로, 이 모델은 팬데믹으로 인한 경기 침체를 급격한 경기 침체에서 빠른 반등을 반영하여 히스테리시스 가능성이 낮은 완전 회복 에피소드로 분류합니다. 이 모델은 국가 차원의 데이터가 위험을 드러내고 있지만 최근 국가 경기 침체의 위험이 낮다는 것을 시사합니다.

미국 경제는 지난 5년 동안 큰 순환 변동을 겪었습니다. 2020년에 코로나19 팬데믹으로 인해 경제 활동이 갑자기 중단되었지만 재정 부양책, 확장 통화 정책, 백신 출시가 결합되어 빠른 회복을 뒷받침했습니다(예: Fleming et al., 2020; Milstein and Wessel, 2024; Romer, 2021). 그러나 경제에 지속적인 피해가 있었습니까? 이제 우리는 또 다른 경기 침체의 위험에 처해 있습니까?

Ahn과 Eo(2025)의 최근 연구는 이러한 질문에 답하는 데 도움이 될 수 있습니다. 4 Ahn과 Eo는 국가 및 주 차원의 비농업 급여 고용 데이터를 사용하여 최첨단 베이지안 마르코프 전환 모델을 추정하여 전체 및 지역 수준 모두에서 이력 현상 위험을 조사합니다. 이 모델은 경기 순환을 확장, U자형 경기 침체, L자형 경기 침체의 세 단계 중 하나로 분류하고 각 시점에 대해 미국의 각 주가 이러한 단계 중 하나에 있을 확률을 추정합니다. 5 이를 통해 이 모델은 지역 노동 시장의 장기적 구조적 변화를 반영하는 전체 및 주 차원 고용 성장의 장기적인 변화를 설명하는 동시에 팬데믹과 그에 따른 회복 기간 동안 나타난 전례 없는 데이터 변동을 적절하게 조정합니다. 6

그림 1은 우리가 측정하는 세 가지 경기 순환 단계의 양식화된 예를 보여줍니다. 고용 증가율이 장기 비율 이상일 때 경제는 팽창 상태에 있고, 고용 증가율이 지속적으로 마이너스일 때 경기 침체 상태에 있습니다. 불황은 두 가지 회복 패턴으로 더욱 구분됩니다. U자형 경기 침체에서 고용은 결국 경기 침체가 없었다면 따랐을 경로(파란색 점선)로 돌아갑니다. 이와 대조적으로, L자형 불황은 고용 수준을 영구적으로 낮추고, 이후의 경기 확장은 고용을 경기 침체 이전의 궤적(파란색 실선)으로 회복시키지 못합니다. 이러한 L자형 회복을 히스테리시스(hysteresis)라고 하며, 경기 침체 충격이 경제 활동에 영구적이거나 장기간 영향을 미치는 현상입니다. 기업이 고용과 생산 능력을 급격히 감소시켜 경제의 생산 잠재력에 지속적으로 부정적인 영향을 미치는 경우 부정적인 수요 충격으로 인해 히스테리시스가 발생할 수 있습니다(직업별 인적 자본을 파괴하고 노동 시장에 대한 근로자의 애착을 약화시킴으로써 부분적으로 - Blanchard, 2018 참조).

참고: X축은 경기주기 정점 이후의 기간을 나타냅니다. 검은색 점선은 경기 침체가 발생하지 않았을 경우의 가상 생산량 수준을 나타냅니다. 음영 처리된 부분은 경제가 침체된 기간을 나타냅니다. 경기 침체 이전 기간은 확장 단계에 해당합니다.

본 노트에서는 1960년 1분기부터 2025년 4분기까지의 데이터를 사용하여 안과 어(2025)의 추정치를 확장하고, 최근 몇 년간 코로나19 경기 침체로 인한 히스테리시스 위험과 국가 및 지역 경기 침체 확률을 모두 평가합니다. 7

그림 2는 국가 수준의 급여 고용 증가율(패널 A)과 실질 GDP 증가율(패널 B)을 사용하여 추정된 U자형 및 L자형 경기 침체 확률을 보여줍니다. 8 경기 침체 확률은 NBER 경기 침체 날짜와 밀접하게 일치합니다. 또한, 급여 고용을 사용하면 L자형 경기 침체 가능성이 더 높아지며, 이는 히스테리시스 효과가 총생산보다 노동 시장에서 더 크다는 것을 의미합니다. 9 대표적인 사례가 대불황이다. 고용 기준 추정치는 이 기간을 L자형 불황으로 분류하지만, GDP 기준 추정치는 회복이 장기화되는 U자형 불황으로 분류한다. 10

참고: 이 수치는 비농업 부문 고용 증가율(패널 A)과 실질 GDP 성장률(패널 B)을 사용하여 추정한 국가 차원의 L자형 및 U자형 경기 침체 가능성을 표시합니다. 2025년 4분기의 경우 비농업 부문 고용 증가율은 10월과 11월의 평균으로 계산됩니다. 이 글을 쓰는 시점에는 12월 데이터를 사용할 수 없기 때문입니다. 파란색 점선은 U자형 경기침체 확률을 나타내고, 빨간색 실선은 L자형 경기침체 확률을 나타냅니다. y축은 확률을 나타내고 x축은 날짜를 나타냅니다. 음영 처리된 막대는 전미경제연구소(National Bureau of Economic Research)가 날짜별로 기록한 미국 경기 침체를 나타냅니다. 1960년 4월~1961년 2월, 1969년 12월~1970년 11월, 1973년 11월~1975년 3월, 1980년 1월~1980년 7월, 1981년 7월~1982년 11월, 1990년 7월~1991년 3월, 3월 2001년~2001년 11월, 2007년 12월~2009년 6월, 2020년 2월~2020년 4월.

주정부 수준의 급여 고용 데이터는 전국 집계에서는 분명하지 않은 지역적 비즈니스 주기의 풍부한 이질성을 드러냅니다. 그림 3은 두 가지 유형의 경기 침체(패널 A의 U자형, 패널 B의 L자형)에 대한 경기 침체 확률의 히트맵을 보여줍니다. 모든 주에서 일반적으로 비슷한 시기에 경기 침체를 경험했지만(주 전체에 걸쳐, 경기 침체 확률의 상승은 NBER 경기 침체와 일치함), 이러한 경기 침체의 규모는 주마다 상당히 달랐습니다. 일부 주에서는 다른 지역에서는 관찰되지 않는 특이한 침체를 ​​경험하기도 했습니다. 예를 들어, 루이지애나는 2005년 허리케인 카트리나 이후 U자형 및 L자형 경기 침체에 직면했고, 노스다코타는 2015년 셰일 오일 생산의 호황과 그에 따른 파산으로 인해 L자형 경기 침체를 겪었습니다.

참고: 수치는 주 차원의 비농업 급여 고용 데이터를 사용하여 추정한 L자형 경기 침체(패널 A)와 U자형 경기 침체(패널 B)를 경험할 확률을 보여줍니다. 이 글을 쓰는 시점을 기준으로 주정부 비농업 부문 고용 증가는 8월까지 가능합니다. 2025년 3분기에는 7월과 8월의 평균을 사용합니다. 상태는 y축에 표시되고 x축은 달력 시간입니다. 각 히트맵의 색상이 어두울수록 경기침체 확률이 높음을 나타냅니다.

1990년대 이후에는 주 전체에서 U자형 경기 침체가 덜 일반적이었으며(그림 3의 패널 B), 이 기간 동안 L자형 회복이 경기 침체의 지배적인 특징이 되었다는 점은 주목할 만합니다. 이 패턴은 지역 노동 시장의 광범위한 실업 회복과 다양한 수준의 히스테리시스를 반영합니다.

팬데믹 경기 침체와 회복(2020년 이후)에 초점을 맞춘 이 모델은 경기 침체를 전체적으로는 물론 주 전체에 걸쳐 U자형으로 분류하며, 이는 이후의 빠른 반등과 일치합니다(그림 2 및 3). 그럼에도 불구하고 뉴욕, 뉴저지 등 일부 주에서는 L자형 경기 침체 가능성이 다소 높아 지속적인 피해를 시사하고 있습니다. 11

최근 몇 년간(2023~2025년) 미국 경제가 침체에 빠질 가능성은 여전히 ​​낮았고, 주 차원의 경기 침체 확률은 0~10%에 이릅니다. 대부분의 주의 확률은 0에 가깝지만 매사추세츠와 로드 아일랜드는 U자형 경기 침체 확률이 10%에 가까워 낮지만 무시할 수는 없습니다. 이러한 패턴과 일치하게, 연준의 2025년 8월 베이지 북의 증거는 뉴잉글랜드 경제가 국가 경제보다 악화되고 있음을 나타내며, 2025년 11월 베이지 북은 수요 약화로 인해 해당 지역의 고용 수준이 소폭 하락했음을 나타냅니다(대규모 정리해고는 없음). 12 따라서 미국 경제가 경기 침체에 진입할 가능성은 거의 없지만 주정부 수준의 데이터는 위험을 지적합니다. 13

베이지안 마르코프 전환 모델은 역사를 해석하는 데 효과적이지만 경기 침체를 사전에 예측하는 것은 여전히 ​​어려운 과제로 남아 있으며 경제학자들 사이에서 지속적인 연구 주제입니다. 14

이전 연구에 따르면 초기 실업수당 청구, 해고, 수익률 곡선의 기울기, 신용 스프레드 등의 측정값은 향후 경기 침체에 대한 신호를 전달합니다(예: Berge, 2015). 15 그림 4에 표시된 이러한 측정값은 일반적으로 가까운 미래에 경기 침체 위험이 높아지는 것을 나타내지 않습니다. 초기 청구 및 해고 지표는 여전히 낮으며(패널 A), 수익률 곡선의 양의 기울기(국채 스프레드)와 낮은 신용 스프레드에 반영된 금융 시장 측정값은 경기 침체 위험이 역사적 기준에 비해 낮다는 것을 시사합니다(패널 B). 16 마찬가지로 Sahm 규칙, Michaillat와 Saez(2025)가 제안한 규칙, 클리블랜드 연준의 정서 기반 모델, 샌프란시스코 연준의 노동 시장 스트레스 지표 등 경험적 또는 모델 기반 지표는 모두 임박한 경기 침체 가능성이 낮다는 신호입니다. 17

참고: 패널 A에서는 초기 UI 청구가 4주 이동 평균으로 보고됩니다. 대유행 시대 관측으로 인해 최근 변동이 무시되는 것을 방지하기 위해 y축은 250에서 잘립니다. 패널 B에서 국채 스프레드는 10년물과 3개월물 국채 수익률의 차이로 정의됩니다. 신용 스프레드는 BBB 회사채 수익률과 10년 만기 국채 수익률의 차이입니다. 2020년 2월부터 4월까지의 음영 영역은 NBER 경기 침체를 나타냅니다. 단위는 백분율 포인트입니다.

출처: 저자 계산; ICE Data Indices LLC, 허가를 받아 사용됨 연방준비은행 이사회; 미국 노동통계국; 미국 노동부.

전반적으로 거시경제 데이터와 다양한 경기 침체 예측 방법은 국가 경기 침체 위험이 여전히 낮다는 것을 나타냅니다. 그러나 일부 지역의 경기 침체 위험과 미국 경제의 현재 순환 상황을 둘러싼 불확실성을 고려할 때 경제의 여러 부분에 걸쳐 경제 상황을 면밀히 모니터링하는 것이 여전히 중요합니다.

Abraham, Katharine G., John Haltiwanger, Kristin Sandusky 및 James R. Spletzer(2013). "가구 데이터와 시설 데이터 간의 고용 차이 탐색."  노동경제학논문, vol. 31(4월), S129–S172.

안희주, 어윤종(2025). "히스테리시스 및 하향 명목 임금 경직성의 역할: 미국의 증거", 금융 및 경제 토론 시리즈 2025-062, 연방 준비 제도 이사회, 워싱턴 D.C.

안톨린-디아즈, 후안, 파올로 수리코(2025). "정부 지출의 장기적 효과", American Economic Review, vol. 115(7월), 2376~2413페이지.

바우어, 로렌, 크리스틴 E. 브로드디, 웬디 에델버그, 지미 오도넬(2020). "COVID-19와 미국 경제에 관한 10가지 사실."  해밀턴 프로젝트, 브루킹스 연구소, 워싱턴 DC.

버지, 트래비스 J. (2015). "선행 지표를 이용한 경기 침체 예측: 경기 순환에 따른 모델 평균화 및 선택."  예측 저널, vol. 34, pp. 455–471, https://doi.org/10.1002/for.2345.

Berge, Travis J., Damjan Pfajfar(출시 예정). “경기 순환의 형태: 미국의 시각.”  옥스포드 경제 및 통계 게시판.

뷰리, 트루먼 F. (1999). 경기 침체 중에 임금이 떨어지지 않는 이유. 매사추세츠주 케임브리지: 하버드 대학교 출판부.

블랜차드, 올리비에(2018). "자연율 가설을 기각해야 하는가?" Journal of Economic Perspectives, American Economic Association, vol. 32(1), pp. 97–120, 겨울.

연방준비제도 이사회(2025a).  The Beige Book, 2025년 8월. 워싱턴 D.C.: 이사회.

연방준비제도 이사회(2025b).  The Beige Book, 2025년 11월. 워싱턴 D.C.: 이사회.

Cerra, Valerie, Antonio Fatas, Sweta C. Saxena(2023). "히스테리시스와 경기순환," 경제문헌학회지, vol. 61(3월), pp. 181–225.

듀프라즈, 스테판 듀프라즈, 에미 나카무라, 존 스테인슨(2025). "경기 순환의 따내기 모델", Journal of Monetary Economics, vol. 152 (6월).

어윤종, 제임스 몰리(2022). "대공황 이후 미국 경제가 정체된 이유는 무엇입니까?"  경제 및 통계 검토, 104(3월), pp. 246–258.

어윤종, 제임스 몰리(2023). "전문 예측가들의 설문조사가 불황의 형태를 실시간으로 예측하는 데 도움이 됩니까?" CAMA 작업 보고서 2023년 5월 24일(5월), http://dx.doi.org/10.2139/ssrn.4451874.

플레밍, 마이클, 아사니 사르카르, 피터 반 태슬(2020). "COVID-19 전염병과 연준의 대응", 뉴욕 연방준비은행, 리버티 스트리트 이코노믹스(Liberty Street Economics), 4월.

프랜시스, 네빌, 로라 E. 잭슨, 마이클 T. 오양(2018). “경기대응정책과 경기침체 후 회복 속도.”  화폐, 신용 및 은행 업무 저널, vol. 50(4월), 675~704페이지.

후쿠이, 마사오, 에미 나카무라, 존 스테인슨(2023). "여성, 자산 효과 및 느린 회복", 미국 경제 저널: 거시경제학, vol. 15(1월), pp. 269-313.

Furlanetto, Francesco, Antoine Lepetit, Ørjan Robstad, Juan Rubio-Ramírez 및 Pål Ulvedal(2025). “히스테리시스 효과 추정.”  미국 경제 저널: 거시경제학, vol. 17(1월), pp. 35–70.

가르시가, 크리스티안, 제임스 미첼(2025). " 지역 경제 심리를 활용하여 미국 경기 침체를 실시간으로 예측합니다."  경제논평, 2025-13호. 클리블랜드: 클리블랜드 연방준비은행, 11월.

Garimella, Rohit, Òscar Jordà, Sanjay R. Singh(2025). " 노동 시장 스트레스 추적 ."  FRBSF 경제 서신, 2025-19. 샌프란시스코: 샌프란시스코 연방준비은행, 8월.

홀, 닉, 오스본 잭슨(2025). "2025년 11월 18일까지의 뉴잉글랜드 경제 상황."  뉴잉글랜드 경제 상황.  보스턴: 보스턴 연방준비은행, 11월.

해밀턴, 제임스 D. (1989). “비정상 시계열 및 경기 순환에 대한 경제적 분석에 대한 새로운 접근 방식.”  Econometrica, 57(3월), pp. 357–384.

해밀턴, 제임스 D., 마이클 T. 오양(2012). “지역 불황의 확산.”  경제 및 통계 검토, vol. 94(11월), 935~947페이지.

Hammond, Bill, McCall Zeutzius(2025). "뉴욕 인구는 코로나19로부터 회복하기 위해 애쓰고 있습니다." 엠파이어 공공 정책 센터(Empire Center for Public Policy).

렌자, 미셸, 조르지오 E. 프리미세리(2022). "2020년 3월 이후 벡터 자기회귀를 추정하는 방법."  응용계량학 저널, vol. 37(3월), 688~699페이지.

Michaillat, Pascal, Emmanuel Saez(2025). "불황이 시작됐나요?"  옥스포드 경제 및 통계 게시판, vol. 87(12월), pp. 1047–1058, https://doi.org/10.1111/obes.12685.

밀스타인, 에릭, 데이비드 웨셀(2024). "연준은 코로나19 위기에 어떻게 대응했나요?"  브루킹스 연구소, 1월.

로머, 크리스티나 D. (2021). "팬데믹에 대한 재정 정책 대응." 경제 활동에 관한 브루킹스 보고서, 봄, pp. 89-110.

1. 면책 조항: FEDS Notes는 이사회 직원이 자신의 견해를 제공하고 경제 및 금융 분야의 다양한 주제에 대한 분석을 제시하는 기사입니다. 이 기사는 FEDS 작업 보고서 및 IFDP 보고서보다 짧고 기술 지향적이지 않습니다. Stephanie Aaronson, Gianni Amisano, Travis Berge, Andrew Figura, Glenn Follette, Norm Morin 및 Jeremy Rudd의 유용한 의견과 제안에 감사드립니다. 이 메모의 모든 오류는 우리 자신의 것입니다.  텍스트로 돌아가기

2. 안과 모욘: Federal Reserve Board of Governors, 20th Street and Constitution Avenue NW, Washington, DC 20551, U.S.A. 텍스트로 돌아가기

3. 어: 고려대학교 경제학과, 서울 02841, 대한민국.  텍스트로 돌아가기

4. 최근 연구에서는 경기 침체 회복의 히스테리시스와 차이가 점점 더 강조되고 있습니다(예: Cerra et al., 2023; Fukui et al., 2023; Furlanetto et al., 2025; Antolín-Díaz and Surico, 2025; Dupraz et al., 2025). Ahn and Eo(2025)는 관련 문헌에 대한 종합적인 검토를 제공합니다.  텍스트로 돌아가기

5. Eo와 Morley(2022)는 총 GDP 성장을 사용하여 최대 가능성을 통해 추정된 세 가지 경기 순환 상태를 갖춘 통계 모델을 개발합니다. 우리의 분석은 주 수준 데이터를 사용하고, 비농업 급여 고용을 사용하여 국가 주기를 식별하고, 베이지안 추정 접근 방식을 사용함으로써 Eo와 Morley(2022)의 프레임워크를 확장합니다.  텍스트로 돌아가기

6. 통계모형 및 추정에 대한 자세한 내용은 안·어(2025)의 3절을 참고한다. 팬데믹으로 인한 경제 활동의 전례 없는 변동은 역사적 비즈니스 주기 단계에 대한 평가를 근본적으로 변경하는 방식으로 모델의 모수 추정에 영향을 미칩니다. 이는 Lenza 및 Priiceri(2022) 및 Eo 및 Morley(2023)를 비롯한 다른 저자가 지적한 문제입니다. 이러한 연구에 따라 우리는 대유행이 시작될 때(2020년 2분기) 활성화되고 그에 따른 실제 활동의 큰 변동의 영향을 줄이는 할인 기능을 통합합니다. 이 조정은 이후 기간에 점차적으로 단계적으로 폐지됩니다.  텍스트로 돌아가기

7. 2025년 4분기에는 10월과 11월의 전국 급여 고용 평균 성장률을 사용합니다. 주 차원의 비농업 부문 고용 증가는 8월까지 가능합니다. 2025년 3분기에는 7월과 8월의 평균을 사용합니다.  텍스트로 돌아가기

8. 그림 2는 전체 표본 기간의 정보를 통합한 평활화된 확률 추정치를 보고합니다. 우리의 목표는 모델의 실시간 성능보다는 과거 비즈니스 주기 단계를 평가하는 것이기 때문입니다.  텍스트로 돌아가기

9. 역사적으로 고용은 불황 회복 기간 동안 실질 GDP와는 다른 역동성을 보였으며, 이는 히스테리시스를 평가할 때 생산량과 노동 시장 데이터를 모두 고려하는 것이 중요함을 강조합니다.  텍스트로 돌아가기

10. 이 평가에 따라 인구 대비 고용 비율은 2019년까지 경기 침체 이전 수준으로 회복되지 않았습니다. 텍스트로 돌아가기

11. 실제로 2020년 4월 뉴욕과 뉴저지는 다른 주보다 코로나 관련 사망자가 더 많았습니다(Bauer et al., 2020). 모델 추정치와 일치하게, 뉴욕주의 인구는 2020년보다 2024년에도 낮은 수준을 유지했습니다(Hammond and Zeutzius, 2025). 또한 뉴욕과 뉴저지 모두 전국 평균에 비해 팬데믹 이후 평균보다 낮은 GDP 성장률을 보여줍니다.  텍스트로 돌아가기

12. 2025년 8월 베이지 북의 1, 2페이지와 2025년 11월 베이지 북의 2페이지를 참조하세요. 뉴잉글랜드의 노동 시장 약화에 대한 추가 증거는 Hall and Jackson(2025)에서 나옵니다. Hall and Jackson(2025)은 이들 주에서 실업 보험에 대한 초기 및 지속적인 청구가 국가 추세를 앞지른다고 지적합니다.  텍스트로 돌아가기

13. 올해 이민으로 인한 노동 공급 감소로 인해 급여 증가율이 둔화되었지만 모델에서는 이러한 감소 속도를 경기 침체의 징후로 간주하지 않습니다.  텍스트로 돌아가기

14. 예를 들어 Hamilton(1989), Hamilton 및 Owyang(2012), Francis et al. (2018), Eo 및 Morley(2022), Berge 및 Pfajfar(출시 예정).  텍스트로 돌아가기

15. 뉴욕 연방준비은행(https://www.newyorkfed.org/research/capital_markets/ycfaq#/overview)의 연구를 통해 추가적인 경험적 증거가 발견되었습니다.  텍스트로 돌아가기

16. 3개월물과 10년물 국채 수익률 사이의 스프레드로 측정되는 수익률 곡선의 기울기는 2023년과 2024년에 마이너스였지만 이 기간 동안 경기 침체는 구체화되지 않았습니다.  텍스트로 돌아가기

17. Sahm Rule 경기 침체 지표는 세인트루이스 연방준비은행의 FRED 데이터베이스(https://fred.stlouisfed.org/series/SAHMREALTIME, 2025년 12월 11일 다운로드)에서 검색한 실시간 측정값 [SAHMREALTIME]입니다.  텍스트로 돌아가기

안희주, 어윤종, 루카스 모욘(2026). "국가 수준 데이터로 경기 침체 위험 평가", FEDS Notes. 워싱턴: 연방준비제도 이사회, 2026년 1월 7일, https://doi.org/10.17016/2380-7172.3992.

면책 조항: FEDS Notes는 이사회 직원이 자신의 견해를 제공하고 경제 및 금융 분야의 다양한 주제에 대한 분석을 제공하는 기사입니다. 이 기사는 FEDS 작업 보고서 및 IFDP 보고서보다 짧고 기술 지향적이지 않습니다.

## 📄 영문 원본
Hie Joo Ahn 2 , Yunjong Eo 3 , and Lucas Moyon

This note evaluates recession risks at the national and state levels using a state-of-the-art Bayesian Markov-switching model that distinguishes between full-recovery recessions (U-shaped recessions) and those that generate lasting damage, or hysteresis (L-shaped recessions). While states exhibit considerable heterogeneity in their business-cycle experiences, most saw some degree of hysteresis in the past recessions that occurred prior to the COVID pandemic. By contrast, the model classifies the pandemic-induced recession as a full-recovery episode with a low likelihood of hysteresis, reflecting the rapid rebound from the sharp downturn. The model suggests that the risk of a national recession has been low of late, though the state-level data reveal pockets of risk.

The U.S. economy has seen large cyclical swings over the past five years. In 2020, the COVID-19 pandemic brought economic activity to an abrupt halt, but a combination of fiscal stimulus, expansionary monetary policy, and the vaccine rollout supported a swift recovery (e.g., Fleming et al., 2020; Milstein and Wessel, 2024; Romer, 2021). But was there lasting damage to the economy? Are we now at risk of another recession?

Recent research by Ahn and Eo (2025) can help answer these questions. 4  Ahn and Eo examine hysteresis risks at both the aggregate and regional levels by estimating a state-of-the-art Bayesian Markov-switching model using national- and state-level nonfarm payroll employment data. The model classifies the business cycle into one of three phases—expansion, U‑shaped recession, and L-shaped recession—and estimates, for each point in time, the probability that each U.S. state is in one of these phases. 5  In doing so, the model accounts for secular changes in aggregate and state-level employment growth that reflect long-run structural shifts in regional labor markets, while also appropriately adjusting for the unprecedented swings in the data seen during the pandemic and subsequent recovery. 6

Figure 1 gives a stylized example of the three business-cycle phases we measure. The economy is in expansion when employment growth is at or above its long-run rate, and in recession when employment growth is negative for a sustained period. Recessions are further distinguished by two recovery patterns. In a U-shaped recession, employment eventually returns to the path it would have followed absent the recession (dashed blue line). In contrast, an L-shaped recession permanently lowers the level of employment, and the subsequent expansion does not restore employment to its pre-recession trajectory (solid blue line). This L-shaped recovery is referred to as  hysteresis , a phenomenon in which recessionary shocks have permanent or long-lasting effects on economic activity. Hysteresis can occur following a negative demand shock if firms sharply reduce employment and productive capacity, in turn generating persistent adverse effects on the economy's productive potential (partly by destroying job-specific human capital and weakening workers' attachment to the labor market—see Blanchard, 2018).

Note: The X-axis denotes periods after a business cycle peak. The black dotted line indicates the hypothetical output level if a recession had not occurred; the shaded area represents periods in which the economy is in a recession. The periods prior to the recession correspond to expansionary phases.

In this note, we extend Ahn and Eo (2025)'s estimates using data from 1960:Q1 to 2025:Q4 and assess both the risk of hysteresis stemming from the COVID-19 recession and national and regional recession probabilities in recent years. 7

Figure 2 displays the probabilities of U-shaped and L-shaped recessions estimated using national-level payroll employment growth (Panel A) and real GDP growth (Panel B). 8  The recession probabilities closely align with the NBER recession dates. In addition, using payroll employment yields higher probabilities of L-shaped recessions, suggesting that hysteresis effects are stronger in the labor market than in aggregate output. 9  A prominent example is the Great Recession: The employment-based estimate classifies this period as an L‑shaped recession, but the GDP-based estimate classifies it as a U-shaped recession with a prolonged recovery. 10

Note: The figures display the probabilities of L-shaped and U-shaped recessions at the national level, estimated using nonfarm payroll employment growth (Panel A) and real GDP growth (Panel B). For 2025:Q4, nonfarm payroll employment growth is computed as the average of October and November, as December data are unavailable at the time of writing. The blue dashed lines represent the probability of a U-shaped recession, while the red solid lines represent the probability of an L-shaped recession. The y‑axis indicates the probability, and the x-axis indicates the date. The shaded bars indicate U.S. recessions as dated by the National Bureau of Economic Research: April 1960–February 1961, December 1969–November 1970, November 1973–March 1975, January 1980–July 1980, July 1981–November 1982, July 1990–March 1991, March 2001–November 2001, December 2007–June 2009, and February 2020–April 2020.

State-level payroll employment data reveal rich heterogeneity in regional business cycles that is not apparent in national aggregates. Figure 3 presents heatmaps of recession probabilities for the two types of recessions (U-shaped in Panel A and L-shaped in Panel B). Although all the states generally experienced economic downturns at similar times—across states, the elevated recession probabilities line up with NBER recessions—the magnitudes of these recessions varied considerably across states. Some states also experienced idiosyncratic downturns not observed in other areas. For example, Louisiana faced a recession with both U-shaped and L‑shaped characteristics in 2005 after Hurricane Katrina, and North Dakota underwent an L‑shaped recession in 2015 following the boom and subsequent bust in shale oil production.

Note: The figures show the probability that states experience L-shaped recessions (Panel A) and U-shaped recessions (Panel B), estimated using state-level nonfarm payroll employment data. As of the time of writing, state-level nonfarm payroll employment growth is available through August; for 2025:Q3, we use the average of July and August. States are shown on the y-axis, and the x-axis is calendar time. Darker colors in each heat map indicate higher recession probabilities.

It is notable that, across states, U-shaped recessions became less common after the 1990s (Panel B of Figure 3), making L-shaped recoveries the dominant feature of recessions during this period. This pattern reflects pervasive jobless recoveries and varying degrees of hysteresis in regional labor markets.

Focusing on the pandemic recession and recovery (2020‑onward), the model classifies the recession as U-shaped in the aggregate as well as across states, consistent with the swift rebound that followed (Figures 2 and 3). Nonetheless, some states—such as New York and New Jersey—exhibit somewhat elevated probabilities of an L-shaped recession, suggesting lasting damage. 11

In recent years (2023–2025), the likelihood that the U.S. economy is in a recession has remained low, with state-level recession probabilities ranging from zero to 10 percent. While most states' probabilities are close to zero, Massachusetts and Rhode Island exhibit U-shaped recession probabilities near 10 percent, which are low but not negligible. Consistent with this pattern, evidence from the Federal Reserve's August 2025 Beige Book indicates that the New England economy is faring worse than the national economy, and the November 2025 Beige Book indicates that the level of employment in that region had edged lower due to weakened demand (but without major layoffs). 12  Thus, while the U.S. economy is unlikely to have entered a recession, the state-level data point to pockets of risk. 13

Although the Bayesian Markov-switching model is effective for interpreting history, predicting a recession in advance still remains as a challenging task and is an ongoing research topic among economists. 14

According to previous research, measures such as initial unemployment claims, layoffs, the slope of yield curve, and the credit spread carry signals about future recessions (e.g., Berge, 2015). 15  These measures, as shown in Figure 4, generally do not indicate an elevated risk of economic recession in the near future: Initial claims and layoff indicators remain low (Panel A), and financial market measures—reflected in the positive slope of the yield curve (the treasury spread) and low credit spreads—suggest that recession risks are low by historical standards (Panel B). 16  Similarly, heuristic or model-based indicators—including the Sahm Rule, the rule proposed by Michaillat and Saez (2025), the Cleveland Fed's sentiment-based model, and the San Francisco Fed's Labor Market Stress Indicator—all signal a low probability of an imminent recession. 17

Note: In panel A, initial UI claims are reported as a 4-week moving average. The y-axis is truncated at 250 to prevent pandemic-era observations from muting recent variation. In panel B, The Treasury spread is defined as the difference between the 10-year and 3-month Treasury yields. The credit spread is the difference between yields on BBB corporate bonds and 10-year Treasuries. Shaded areas spanning February – April 2020 denote the NBER recession. Units are in percentage points.

Source: Authors' calculation; ICE Data Indices LLC, used with permission; Federal Reserve Board of Governors; U.S. Bureau of Labor Statistics; U.S. Department of Labor.

Overall, macroeconomic data and a range of recession-prediction methods indicate that the risk of a national recession remains low. However, given pockets of recession risk in some regions and uncertainty surrounding the U.S. economy's current cyclical position, it remains important to closely monitor economic conditions across different parts of the economy.

Abraham, Katharine G., John Haltiwanger, Kristin Sandusky, and James R. Spletzer (2013). "Exploring Differences in Employment between Household and Establishment Data."  Journal of Labor Economics , vol. 31 (April), S129–S172.

Ahn, Hie Joo and Yunjong Eo (2025). "Hysteresis and the Role of Downward Nominal Wage Rigidity: Evidence from U.S. States,"  Finance and Economics Discussion Series  2025-062, Board of Governors of the Federal Reserve System, Washington, D.C.

Antolin-Diaz, Juan and Paolo Surico (2025). "The Long-Run Effects of Government Spending,"  American Economic Review , vol. 115 (July), pp. 2376–2413.

Bauer, Lauren, Kristen E. Broady, Wendy Edelberg, and Jimmy O'Donnell (2020). "Ten Facts about COVID-19 and the U.S. Economy."  The Hamilton Project,   Brookings Institution , Washington, DC.

Berge, Travis J. (2015). "Predicting Recessions with Leading Indicators: Model Averaging and Selection over the Business Cycle."  Journal of Forecasting , vol. 34, pp. 455–471, https://doi.org/10.1002/for.2345.

Berge, Travis J., and Damjan Pfajfar (forthcoming). "The Shape of the Business Cycle: The View from U.S. States."  Oxford Bulletin of Economics and Statistics .

Bewley, Truman F. (1999). Why Wages Don't Fall During a Recession. Cambridge, MA: Harvard University Press.

Blanchard, Olivier (2018). "Should We Reject the Natural Rate Hypothesis?,"  Journal of Economic Perspectives , American Economic Association, vol. 32(1), pp. 97–120, Winter.

Board of Governors of the Federal Reserve System (2025a).  The Beige Book , August 2025. Washington, D.C.: Board of Governors.

Board of Governors of the Federal Reserve System (2025b).  The Beige Book , November 2025. Washington, D.C.: Board of Governors.

Cerra, Valerie, Antonio Fatas, and Sweta C. Saxena (2023). "Hysteresis and Business Cycles,"  Journal of Economic Literature , vol. 61 (March), pp. 181–225.

Dupraz, Stéphane Dupraz, Emi Nakamura, and Jón Steinsson (2025). "A plucking model of business cycles,"  Journal of Monetary  Economics, vol. 152 (June).

Eo, Yunjong, and James Morley (2022). "Why Has the U.S. Economy Stagnated since the Great Recession?"  Review of Economics and Statistics , 104 (March), pp. 246–258.

Eo, Yunjong, and James Morley (2023). "Does the Survey of Professional Forecasters Help Predict the Shape of Recessions in Real Time?" CAMA Working Paper 24/2023 (May), http://dx.doi.org/10.2139/ssrn.4451874.

Fleming, Michael, Asani Sarkar, and Peter Van Tassel (2020). "The COVID-19 pandemic and the Fed's response," Federal Reserve Bank of New York, Liberty Street Economics, April.

Francis, Neville, Laura E. Jackson, and Michael T. Owyang (2018). "Countercyclical Policy and the Speed of Recovery after Recessions."  Journal of Money, Credit and Banking , vol. 50 (April), pp. 675–704.

Fukui, Masao, Emi Nakamura, and Jón Steinsson (2023). "Women, Wealth Effects, and Slow Recoveries,"  American Economic Journal: Macroeconomics , vol. 15 (January), pp. 269-313.

Furlanetto, Francesco, Antoine Lepetit, Ørjan Robstad, Juan Rubio-Ramírez, and Pål Ulvedal (2025). "Estimating Hysteresis Effects."  American Economic Journal: Macroeconomics , vol. 17 (January), pp. 35–70.

Garciga, Christian, and James Mitchell (2025). " Forecasting U.S. Recessions in Real Time Using Regional Economic Sentiment ."  Economic Commentary , No. 2025-13. Cleveland: Federal Reserve Bank of Cleveland, November.

Garimella, Rohit, Òscar Jordà, and Sanjay R. Singh (2025). " Tracking Labor Market Stress ."  FRBSF Economic Letter , 2025-19. San Francisco: Federal Reserve Bank of San Francisco, August.

Hall, Nick, and Osborne Jackson (2025). " New England Economic Conditions through November 18, 2025 ."  New England Economic Conditions.  Boston: Federal Reserve Bank of Boston, November.

Hamilton, James D. (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle."  Econometrica , 57 (March), pp. 357–384.

Hamilton, James D., and Michael T. Owyang (2012). "The Propagation of Regional Recessions."  Review of Economics and Statistics , vol. 94 (November), pp. 935–947.

Hammond, Bill, and McCall Zeutzius (2025). " New York's population is struggling to recover from COVID-19 ," Empire Center for Public Policy.

Lenza, Michele, and Giorgio E. Primiceri (2022). "How to Estimate a Vector Autoregression after March 2020."  Journal of Applied Econometrics , vol. 37 (March), pp. 688–699.

Michaillat, Pascal, and Emmanuel Saez (2025). "Has the Recession Started?"  Oxford Bulletin of Economics and Statistics , vol. 87 (December), pp. 1047–1058, https://doi.org/10.1111/obes.12685.

Milstein, Eric, and David Wessel (2024). "What did the Fed do in response to the COVID-19 crisis?"  Brookings Institution , January.

Romer, Christina D. (2021). "The fiscal policy response to the pandemic . "  Brookings Papers on Economic Activity , Spring, pp. 89–110.

1. Disclaimer: FEDS Notes are articles in which Board staff offer their own views and present analysis on a range of topics in economics and finance. These articles are shorter and less technically oriented than FEDS Working Papers and IFDP papers. We gratefully acknowledge useful comments and suggestions from Stephanie Aaronson, Gianni Amisano, Travis Berge, Andrew Figura, Glenn Follette, Norm Morin and Jeremy Rudd. All errors in this note are our own.  Return to text

2. Ahn and Moyon: Federal Reserve Board of Governors, 20th Street and Constitution Avenue NW, Washington, DC 20551, U.S.A.  Return to text

3. Eo: Department of Economics, Korea University, Seoul 02841, South Korea.  Return to text

4. Recent research has increasingly emphasized hysteresis and differences in recession recoveries (e.g., Cerra et al., 2023; Fukui et al., 2023; Furlanetto et al., 2025; Antolín-Díaz and Surico, 2025; Dupraz et al., 2025). Ahn and Eo (2025) provide a comprehensive review of the related literature.  Return to text

5. Eo and Morley (2022) develop a statistical model with three business-cycle states, estimated via maximum likelihood using aggregate GDP growth. Our analysis extends the framework of Eo and Morley (2022) by using state-level data, by using nonfarm payroll employment to help identify the national cycle, and by employing a Bayesian estimation approach.  Return to text

6. See Section 3 of Ahn and Eo (2025) for details on the statistical model and its estimation. The unprecedented swing in economic activity caused by the pandemic influences the model's parameter estimates in ways that fundamentally change its assessment of historical business-cycle phases—an issue noted by other authors, including Lenza and Primiceri (2022) and Eo and Morley (2023). Following these studies, we incorporate a discount function that activates at the onset of the pandemic (2020:Q2) and reduces the influence of the large swings in real activity that follow; this adjustment is then gradually phased out in subsequent periods.  Return to text

7. For 2025:Q4, we use the average growth rate of national payroll employment in October and November. State-level nonfarm payroll employment growth is available through August; for 2025:Q3, we use the average of July and August.  Return to text

8. Figure 2 reports the smoothed probability estimates, which incorporate information from the entire sample period, as our goal is to assess historical business-cycle phases rather than the real-time performance of the model.  Return to text

9. Historically, employment exhibits dynamics during recession recoveries that differ from those of real GDP, underscoring the importance of considering both output and labor-market data when assessing hysteresis.  Return to text

10. Consistent with this assessment, the employment-to-population ratio did not return to its pre-recession level until 2019.  Return to text

11. Indeed, New York and New Jersey experienced more Covid-related deaths than other states in April 2020 (Bauer et al., 2020). Consistent with the model estimates, New York state's population remained lower in 2024 than in 2020 (Hammond and Zeutzius, 2025). In addition, both New York and New Jersey show lower-than-average post-pandemic GDP growth relative to the national average.  Return to text

12. See pages 1 and 2 of the August 2025 Beige Book and page 2 of the November 2025 Beige Book. Additional evidence for labor market weakness in New England comes from Hall and Jackson (2025), who note that initial and continued claims for unemployment insurance in these states outpace national trends.  Return to text

13. A reduced labor supply from immigration this year contributed to the slower payroll growth, but the model does not view this reduced pace as indicative of an economic downturn.  Return to text

14. See, for example, Hamilton (1989), Hamilton and Owyang (2012), Francis et al. (2018), Eo and Morley (2022), Berge and Pfajfar (forthcoming).  Return to text

15. Additional empirical evidence has been found by research at the Federal Reserve Bank of New York ( https://www.newyorkfed.org/research/capital_markets/ycfaq#/overview ).  Return to text

16. The slope of the yield curve, measured by the spread between 3-month and 10-year Treasury yields, was negative in 2023 and 2024 but a recession did not materialize during these years.  Return to text

17. The Sahm Rule recession indicator, is a real-time measure [SAHMREALTIME] that was retrieved from the Federal Reserve Bank of St. Louis's FRED database ( https://fred.stlouisfed.org/series/SAHMREALTIME , downloaded December 11, 2025).  Return to text

Ahn, Hie Joo, Yunjong Eo, and Lucas Moyon (2026). "Assessing Recession Risks with State-Level Data," FEDS Notes. Washington: Board of Governors of the Federal Reserve System, January 7, 2026, https://doi.org/10.17016/2380-7172.3992.

Disclaimer:  FEDS Notes are articles in which Board staff offer their own views and present analysis on a range of topics in economics and finance. These articles are shorter and less technically oriented than FEDS Working Papers and IFDP papers.


---
*출처: https://www.federalreserve.gov/econres/notes/feds-notes/assessing-recession-risks-with-state-level-data-20260107.html | 수집: 2026-06-10 01:45 | 지표: FEDS_NOTES*
