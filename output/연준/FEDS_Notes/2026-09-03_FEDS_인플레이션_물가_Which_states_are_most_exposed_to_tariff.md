# FEDS Notes - 관세 인상에 가장 많이 노출된 주들은 어디일까요?
소비 채널에 기반한 새로운 측정 방식 / Which states are most exposed to tariff increases? A new measure based on the consumption channel

> 날짜: 2026-09-03
> 저자: Nick Heyman,Colin J. Hottman, and Ryan Monarch
> 주제: 인플레이션/물가
> 출처: https://www.federalreserve.gov/econres/notes/feds-notes/which-states-are-most-exposed-to-tariff-increases-a-new-measure-based-on-the-consumption-channel-20260903.html

## 📌 초록
본 보고서는 주(state)들이 직접 소비자재 수입품을 소비하는 측면에서 겪는 이질적인 노출을 분석하며, 이는 관세와 같은 무역 비용 증가에 주(state)들이 노출되는 중요한 경로이다. Hottman과 Monarch (2020) 및 Hottman과 Monarch (2026)가 미국 소득 십분위와 다른 인구통계학적 집단을 위해 유사한 측정치를 구축하는 데 사용했던 방법론을 기반으로, 우리는 최근 연도 데이터를 사용하여 새로운 주(state) 수준 측정치를 구축한다.

## 📋 한국어 번역
닉 헤이먼, 콜린 J. 핫맨, 라이언 모나크 1

이 보고서는 주들이 직접 소비자 상품 수입 소비 측면에서 이질적인 노출을 보이는 것을 조사하며, 이는 관세와 같은 무역 비용 증가에 주들이 노출되는 중요한 경로입니다. 핫맨과 모나크(2020) 및 핫맨과 모나크(2026)가 미국 소득 10분위 및 기타 인구통계학적 그룹에 대한 유사한 측정치를 구성하기 위해 사용한 방법론을 바탕으로, 우리는 최근 연도 데이터를 사용하여 새로운 주 수준 측정치를 구성합니다. 우리는 주들 간의 노출에 큰 차이가 있음을 발견하고, 이러한 차이의 일부 원인을 문서화한 다음, 이들이 암시하는 관세의 대략적인 영향을 논의하며 마무리합니다.

우리는 소비 측면에서 다양한 미국 주들의 직접 소비자 상품 수입 노출에 대한 새로운 측정치를 구성합니다. 이를 위해, 먼저 2023년 소비자 지출 조사(CES)를 사용하여 31개 미국 주(미국 인구의 86%를 포함)의 대표 가구를 대상으로 소비자 제품 범주에 대한 평균 연간 지출을 생성합니다. 2 둘째, 우리는 또한 미국 인구조사국(U.S. Census Bureau)의 2023년 주 수준 수입 데이터를 사용합니다. 수입 데이터 내에서 소비자 상품을 필터링하기 위해, 우리는 유엔 통계국(United Nations Statistics Division)에서 제공하는 광범위 경제 범주 분류(BEC)와 일치시키고 소비재로 지정되지 않은 HS 코드를 제외합니다. 우리는 LLM 기반 텍스트 설명 일치(Furman et al 2017의 일치에서 시작하는 Claude Sonnet 4 사용)를 사용하여 수입 데이터의 개별 제품 범주(HS 코드 기준)를 CES 제품 범주와 일치시킵니다. 이 두 가지 데이터셋을 사용하여 각 주에 대해 총 소비자 지출 중 직접 수입된 소비자 상품에 대한 지출의 비율을 생성할 수 있습니다. 이를 통해 수입 소비에서 주들 간의 차이를 비교할 수 있으며, 이는 그림 1에 요약되어 있습니다.

참고: 연한 회색으로 표시된 주는 우리 표본에 포함되지 않습니다.

직접 소비자 상품 수입이 소비에서 차지하는 비중은 어느 정도일까요? 이 비중은 주마다 크게 다릅니다. 수입 소비 비중이 가장 높은 곳은 캘리포니아(13.8%)와 뉴저지(12.7%)이며, 가장 낮은 곳은 네브래스카(2.6%)와 미주리(2.6%)입니다. 31개 주의 단순 평균은 5.6%이고, 인구 가중 평균은 7.1%입니다. 이 수치들은 전국적인 수입 소비에 대한 이전 추정치(약 10%에 근접, 예: Hottman and Monarch (2020) 또는 Borusyak and Jaravel (2021) 참조)와 유사하지만 더 작습니다. 그러나 이전 연구는 주로 비례성 가정에 의존하여, 전국 수준의 수입 침투율을 범주 수준의 소비 차이와 결합하여 가구 간의 이질적인 수입 노출을 추정했습니다. 여기서는 주 수준 수입 데이터를 사용함으로써 이러한 비례성 가정을 완화하며, 수입 데이터와 소비 데이터 모두 주마다 직접적으로 다릅니다. 동시에, 우리는 이제 도매 가격으로 효과적으로 측정된 수입 가치와 소매 가격으로 측정된 소비 가치를 비교하고 있기 때문에, 주 수준에서 계산한 소비의 수입 비중이 가구 소득 수준에서 유사한 측정치에 대한 이전 추정치보다 평균적으로 낮다는 것은 놀라운 일이 아닙니다. 3

수입 소비 측면에서 주들 간에 상당한 이질성이 있음을 보여준 후, 다음으로 이러한 변동의 잠재적 원인으로 다음을 고려합니다: A) 측정 문제; B) 규모 및 중간 소득과 같은 주 수준 변수의 차이; C) 각 주의 수입 바구니에 있는 제품 구성의 차이; D) 주 수입에서 다양한 원산지 국가에 대한 노출의 차이. 우리는 이들 각각을 차례로 탐구합니다.

A. 측정 문제
주별 수입 비중의 큰 변동 중 일부를 설명할 수 있는 두 가지 잠재적 측정 문제 원인이 있습니다. 하나는 소비자 지출 조사(Consumer Expenditure Survey)에 있고 다른 하나는 인구조사국(Census)의 주 수준 수입 데이터에 있습니다.

소비자 지출 조사는 전국 대표성을 갖도록 설계되었을 뿐이며, 주 수준 추정치는 잠재적으로 높은 분산을 가질 수 있습니다. 우리는 이를 여러 가지 방법으로 해결하려고 시도했습니다. 첫째, CES에서 300가구 이상이 응답한 주만 포함했습니다(포함된 31개 주 중 80%는 500가구 이상을 가짐). 우리는 또한 각 주 내의 CES 지출을 2023년 BEA의 주별 PCE 데이터에 있는 PCE 총합과 일치시키도록 조정했습니다(다시 말해, CES 데이터는 총 주 소비자 지출이 아닌 특정 제품 범주의 상대적 중요성을 얻는 데만 사용됩니다). 마지막으로, 직접 소비자 수입을 식별할 때, 포함된 주의 3분의 2 미만에서 나타나는 UCC 코드는 모두 제외했습니다(522개 코드 중 119개 코드가 제외됨). 따라서 수입 비중의 차이는 주로 일부 주가 다른 주가 소비하지 않는다고 보고하는 제품 범주를 소비하기 때문에 발생하는 것은 아닙니다.

인구조사국 주 수준 수입 데이터는 전자 통관 신고서의 미국 목적지 주 코드에 기반하며, 이는 수입된 상품이 최종적으로 전달될 미국 주를 의미합니다(항구는 아님). 이 데이터는 문헌에서, 예를 들어 Rodríguez-Clare et al. (2025)의 최근 연구에서 사용됩니다. 그러나 특정 경우에 이 목적지 주는 유통 지점을 반영할 수 있으며, 여기서 선적물은 나중에 다른 주로 추가 분배될 수 있습니다. 우리는 소수의 제품 코드(37개 UCC 코드)에서 주별 소비 수입 비중의 차이가 믿기 어려울 정도로 크다는 것을 발견했습니다. 그러한 경우, 제품별 주 수입 비중은 해당 제품의 전국 수입 비중으로 대체되었습니다. 따라서 우리가 보고하는 총 주 수준 수입 비중의 차이는 잘못된 측정으로 인해 발생했을 가능성이 있는 제품 수준의 극단적인 차이를 반영하지 않습니다. 우리가 이를 해결하려고 시도했음에도 불구하고, 캘리포니아와 뉴저지가 그림 1에서 그렇게 두드러지는 이유는 이 두 주가 미국에서 가장 큰 두 항구를 가지고 있으며, 궁극적으로 다른 주로 이동하는 일부 선적물이 처음에는 이 두 주의 유통 지점으로 전달될 수 있기 때문일 가능성이 남아 있습니다.

B. 주 수준의 규모 및 소득 변동
우리는 인구조사국(Census Bureau)과 BEA의 주별 가구 중간 소득, 주 GDP, 주 인구 데이터를 사용하여 이를 수입 제품에 대한 우리의 추정 지출과 비교합니다. 수입 지출과 주 수준 실질 GDP(0.65) 및 주 수준 인구(0.65) 모두 사이에 강한 양의 상관관계가 있습니다. 따라서 더 큰 주(총 경제 생산량 또는 인구 측면에서)는 다른 주보다 직접 수입된 소비자 상품에서 오는 소비 비중이 더 높으며, 이는 중력형 관계에서 예상되는 바와 같습니다(미국 지역 수출의 중력 관계 증거는 Boehm et al. (2026) 참조). 하지만 주별 명목 가구 중간 소득에 대한 수입 지출을 회귀하면 경제적으로 작고 통계적으로 0과 구별할 수 없는 계수가 나오는데, 이는 이전 연구에서 발견된 소득 대비 평평한 수입 비중과 일치합니다(Hottman and Monarch (2020), Borusyak and Jaravel (2021)).

C. 주별 수입 제품 구성의 차이
각 주는 다른 비율로 제품을 소비하며, 이는 주의 수입 노출 차이를 설명할 수 있습니다. CES 범주를 사용하여 수입 지출을 9가지 광범위한 범주로 나눕니다: 가구 및 내구 가전제품, 자동차 및 부품, 레크리에이션 용품 및 차량, 기타 내구재, 의류 및 신발, 식음료 구매, 휘발유 및 기타 에너지 상품, 그리고 기타 비내구재. 변동을 체계적으로 조사하기 위해 Hottman et al. (2016)과 같은 회귀 기반 분산 분해를 사용하여 주별 수입 비중의 분산을 우리의 제품 분류가 그 분산에 기여한 정도로 할당했으며, 그 결과는 표 1에 나와 있습니다. 예를 들어, 휴대폰과 같은 품목을 포함하는 포괄적인 범주인 "기타 내구재"에 대한 수입 지출의 차이가 주 수준 수입 비중 분산의 약 24%를 설명하는 반면, "식음료"와 "가구 및 가전제품"은 각각 약 14%를 설명합니다. 따라서 종합적으로 이 세 가지 범주의 차이만으로 주별 소비 수입 비중 분산의 50% 이상을 설명합니다.

D. 주별 원산지 국가 노출 차이

미국 주들은 수입 바구니에서 다른 원산지 국가에 차등적으로 노출됩니다. 예를 들어, 일리노이주의 수입품 중 거의 29%가 중국에서 오는 반면, 매사추세츠주의 수입품 중 약 9%만이 중국에서 오는 것으로 추정됩니다. 우리는 다시 한번 분산 분해를 실시했으며, 이번에는 주요 무역 파트너 및 국가 그룹으로 나누었으며, 그 결과는 표 2에 보고되어 있습니다. 우리는 중국으로부터의 수입 지출 차이가 주 수입 비중 분산의 약 24%를 설명하고, EU는 약 19%, 멕시코는 약 15%를 설명한다는 것을 발견했습니다. 종합적으로, 이 세 국가에 대한 수입 지출의 차이는 주별 수입 비중 분산의 거의 60%를 설명합니다. 흥미롭게도, 캐나다로부터의 수입 지출 차이는 변동의 약 2%만을 설명합니다.

참고: 반올림으로 인해 합계가 정확히 1이 되지 않습니다.

마지막으로, 우리의 계산에서 암시되는 주별 관세 부과에 대한 대략적인 추정치를 제시합니다. 최근 관세 인상이 모든 미국 수입품에 일률적으로 적용된 것은 아니지만, 직접적인 주 수준 노출의 잠재적 차이를 설명하기 위해 최근 관세 조치를 모든 미국 최종재 수입에 대한 균일한 10%포인트 관세 인상으로 근사합니다. 4 이 연습에서는 설명 목적으로 이 균일 관세가 소비자 가격에 완전히 전가된다고 가정합니다. 이러한 단순화된 가정과 소비 점유율로서의 주 수준 수입 데이터를 고려할 때, 관세에 가장 큰 영향을 받는 주를 식별하는 것은 간단합니다: 수입 점유율이 가장 높은 주들입니다.

그림 1에서 볼 수 있듯이, 모든 제품에 대한 균일한 관세 인상이 적용될 경우, 캘리포니아, 뉴저지, 텍사스, 펜실베이니아의 가구들이 가장 큰 영향을 받을 것이며, 네브래스카, 미주리, 코네티컷, 콜로라도의 가구들은 가장 적은 영향을 받을 것입니다. 정량적으로, 우리의 단순화된 가정은 캘리포니아는 약 1.4%의 생활비 증가를, 펜실베이니아는 약 0.8%의 생활비 증가를 경험할 것이며, 네브래스카는 약 0.3%의 생활비 증가만을 경험할 것임을 암시합니다. 따라서 우리는 균일한 미국 관세 인상에 대한 직접적인 생활비 노출 측면에서 미국 주들 간에 큰 차이가 있음을 발견합니다. 물론, 우리의 이전 분산 분해는 비균일적이고 부문 및 국가별 관세 또한 주들 간에 상당한 효과 차이를 초래할 것으로 예상됨을 암시합니다.

Boehm, Christoph E., Aaron Flaaen, Nitya Pandalai-Nayar, and Jan Schlupp, "The local-area incidence of exporting", _Journal of International Economics_, 2026, Vol. 161.

Borusyak, Kirill, and Xavier Jaravel, "The Distributional Effects of Trade: Theory and Evidence from the United States", NBER Working Paper 28957, 2021.

Furman, Jason, Katheryn N. Russ, and Jay Shambaugh, "U.S. Tariffs are an Arbitrary and Regressive Tax", VoxEU.org, 2017.

Hottman, Colin J., and Ryan Monarch, "A matter of taste: Estimating import price inflation across U.S. income groups", _Journal of International Economics_, 2020, Vol. 127.

Hottman, Colin J., and Ryan Monarch, "Oh, Give me a Home (Trade Share): Differential Import Price Inflation and Gains from Trade Across U.S. Households", Working Paper, 2026.

Hottman, Colin J., Stephen J. Redding, and David E. Weinstein, "Quantifying the Sources of Firm Heterogeneity", _Quarterly Journal of Economics_, 2016, Vol. 131, No. 3.

Minton, Robbie, and Mariano Somale, "Detecting Tariff Effects on Consumer Prices in Real Time", FEDS Notes, Washington: Board of Governors of the Federal Reserve System, 2025.

Rodríguez-Clare, Andrés, Mauricio Ulate and Jose P. Vasquez, "The 2025 Trade War: Dynamic Impacts Across U.S. States and the Global Economy", NBER Working Paper 33792, 2025.

1. 닉 헤이먼 및 콜린 J. 핫맨: 연방준비제도 이사회 (이메일: [email protected] 및 [email protected] ). 라이언 모나크: 시라큐스 대학교 (이메일: [email protected] ). 표현된 견해는 전적으로 저자의 책임이며, 연방준비제도 이사회 또는 연방준비제도와 관련된 다른 어떤 개인의 견해를 반영하는 것으로 해석되어서는 안 됩니다. 텍스트로 돌아가기

2. 이 작업을 시작할 당시, 소비자 지출 조사에서 2023년이 이용 가능한 최신 연도였습니다. 2.A 섹션에서 논의한 바와 같이, 데이터 가용성을 고려하여 31개 미국 주에 중점을 둡니다. 텍스트로 돌아가기

3. PCE 브리지 테이블을 사용하여 수입 가치에 소매 마진을 추가하고 그에 따라 수입 비중을 늘릴 수 있었지만, Minton and Somale (2025)에서 논의된 마진 관련 전가 가정과 일치시키기 위해 그렇게 하지 않기로 결정했습니다. 텍스트로 돌아가기

4. 단순화를 위해 이 분석은 하위 최종 소비자 상품에 통합되는 상위 중간 투입재에 대한 관세를 통한 간접 노출을 무시합니다. 이러한 간접 수입을 포함하지 않기 때문에, 우리의 수입 비중은 소비에서 총 수입 비중의 하한선입니다. 그리고 다른 모든 것이 동일하다면, 간접 수입에 대한 관세를 포함하면 우리가 논의하는 생활비 효과가 증가할 것입니다. 텍스트로 돌아가기

Heyman, Nick, Colin J. Hottman, and Ryan Monarch (2026). "Which states are most exposed to tariff increases? A new measure based on the consumption channel," FEDS Notes. Washington: Board of Governors of the Federal Reserve System, September 03, 2026, https://doi.org/10.17016/2380-7172.4157.

면책 조항: FEDS Notes는 이사회 직원들이 경제 및 금융의 다양한 주제에 대한 자신의 견해를 제시하고 분석하는 기사입니다. 이 기사들은 FEDS Working Papers 및 IFDP 논문보다 짧고 기술적인 내용이 덜합니다.

## 🖼️ 그림 및 차트
**Figure 1**

![Figure 1](https://www.federalreserve.gov/econres/notes/feds-notes/figure1-4157.png)

> [원본 링크](https://www.federalreserve.gov/econres/notes/feds-notes/figure1-4157.png)


---
*출처: https://www.federalreserve.gov/econres/notes/feds-notes/which-states-are-most-exposed-to-tariff-increases-a-new-measure-based-on-the-consumption-channel-20260903.html | 수집: 2026-09-03 18:12 | 지표: FEDS_NOTES*
