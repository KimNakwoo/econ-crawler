# FEDS Notes - Investor Composition of Money Market Funds and Its Implications for Flow Dynamics

> 날짜: 2026-05-08
> 저자: Yi Li, Nick Panetta, and Weston Watts
> 주제: 금융여건
> 출처: https://www.federalreserve.gov/econres/notes/feds-notes/investor-composition-of-money-market-funds-and-its-implications-for-flow-dynamics-20260508.html

## 📌 초록 (원문)
Money market funds (MMFs) play a critical role in supplying short-term funding to corporations, banks, and governments. While existing research has made substantial progress in understanding MMF portfolio choices and investor flows, little is known about the composition of MMFs' institutional investors.

## 📋 한국어 번역
MMF(머니마켓펀드)는 기업, 은행, 정부에 단기 자금을 공급하는 데 중요한 역할을 합니다. 기존 연구는 MMF 포트폴리오 선택과 투자자 흐름을 이해하는 데 상당한 진전을 이루었지만 MMF의 기관 투자자 구성에 대해서는 알려진 바가 거의 없습니다. 본 FEDS Note에서는 새로 이용 가능한 데이터를 사용하여 MMF의 투자자 구성에 대한 개요를 제공하고 이것이 펀드의 포트폴리오 특성 및 흐름 역학과 어떻게 관련되는지 조사합니다. 우리는 은행이 지배적인 투자자일 때 MMF가 더 변동성이 큰 흐름을 경험하고 대규모 유출 가능성이 더 높은 경향이 있음을 발견했습니다. 이러한 패턴에 따라 은행을 주요 투자자로 하는 MMF는 더 유동적이고 위험도가 낮은 포트폴리오를 보유합니다. 비록 우리의 방법론이 인과관계를 규명하려고 시도하지는 않지만, 그 결과는 MMF가 투자자 행동에 대응하고 포트폴리오 위험을 통합적인 방식으로 관리한다는 것을 시사합니다.

MMF는 매달 증권거래위원회(SEC) 양식 N-MFP를 제출해야 합니다. 1 2024년 6월부터 SEC는 기관 프라임 MMF에게 유형별 투자자 구성 내역을 공개하도록 요구했습니다. 각 펀드의 주식 클래스에 대해 보고되는 투자자 유형에 대한 새로운 데이터는 세분화된 보안 수준 보유 및 유동성 지표를 포함하여 수년 동안 수집된 Form N-MFP 데이터를 보완합니다. 이러한 데이터를 결합하면 투자자 구성을 펀드의 포트폴리오 노출, 위험 프로필 및 유동성 관리와 연결할 수 있습니다. 또한, 우리는 일일 흐름 정보를 사용하여 투자자 흐름 역학의 측정값을 구성하며, 이를 통해 투자자 구성이 흐름 행동에 잠재적인 영향을 미치는지 여부를 조사할 수 있습니다.

우리의 샘플은 2024년 6월부터 2025년 8월까지입니다. 우리는 총 펀드 수준이 아닌 주식 클래스 수준에서 분석을 수행합니다. 왜냐하면 다양한 주식 클래스는 종종 서로 다른 투자자 세그먼트를 대상으로 하고 실질적으로 다른 흐름 역학을 나타낼 수 있기 때문입니다. 우리는 공개적으로 제공되고 샘플 기간 동안 N-MFP 보고서를 일관되게 제출하는 기관 프라임 MMF에 중점을 둡니다. 2024년 10월 SEC 개혁 시행 이전에 청산, 전환 또는 다른 펀드와 합병된 펀드는 일관된 패널 유지를 위해 제외됩니다. 2 최종 샘플에는 8개 기관 프라임 펀드의 32개 주식 클래스가 포함됩니다. 3

N-MFP 양식에는 각 주식 클래스의 투자자를 12개 범주로 분류하기 위한 자금이 필요합니다. 4 우리는 이들을 딜러(브로커/딜러), 은행(예금 기관), 회사(비금융 회사), 기타(나머지 모든 유형)의 네 그룹으로 통합합니다. 그림 1에서 볼 수 있듯이, 표본 기간 동안 딜러와 은행은 각각 기관 프라임 MMF 투자의 약 30%를 차지하고 회사와 기타는 각각 약 20%를 차지합니다.

참고: "은행" = 예금 기관; "딜러" = 브로커/딜러; "회사" = 비금융 회사; "기타"에는 등록된 투자 회사, 보험 회사, 지방 자치 단체, 비영리 단체, 연금 기금, 민간 기금, 국부 기금 및 N-MFP 양식에 보고된 "기타 투자자"가 포함됩니다. 범례는 위에서 아래로 계열을 식별합니다.

그런 다음 각 주식 클래스의 주요 투자자 유형을 나타내기 위해 4개의 더미 변수(Dealer, Bank, Firm 및 Other)를 정의합니다. 특히, $$Dealer_{i,t}$$는 딜러가 $$t$$ 월에 $$i$$ 주식 클래스에 대한 투자의 50% 이상을 제공하는 경우 1이고, 그렇지 않은 경우 0입니다. 다른 지표도 유사하게 정의됩니다. 구조적으로, 최대 하나의 주요 투자자 지표는 특정 달의 특정 주식 클래스에 대해 1과 같을 수 있습니다.

표 1은 주식 클래스-월 패널을 기반으로 이러한 주요 투자자 지표에 대한 요약 통계를 보고합니다. 주식 클래스 전체에 걸쳐 딜러가 주요 투자자일 확률은 23%, 은행이 주요 투자자일 확률은 26%, 비금융회사가 주요 투자자일 확률은 11%입니다. 19%의 주식 클래스에서는 단일 투자자 유형이 전체 투자의 절반 이상을 차지하지 않습니다.

다음으로 투자자 유형이 주요 펀드 특성과 어떤 관련이 있는지 살펴보겠습니다. 다양한 유형의 투자자는 유동성과 위험 감수에 대해 뚜렷한 선호를 가질 수 있습니다. 이러한 선호도는 MMF 전체에 대한 투자자의 배분 결정뿐만 아니라 펀드 매니저가 특정 투자자 기반을 유치하고 대응하기 위해 펀드 특성을 조정하는 방법에도 영향을 미칠 수 있습니다. 인과관계를 규명하기보다는 투자자 구성과 규모, 유동성 상태, 위험 프로필 등 펀드 특성 간의 연관성을 조사합니다.

구체적으로, 우리는 주간 유동 자산(WLA)과 가중 평균 만기(WAM)를 사용하여 펀드의 포트폴리오 유동성을 파악하고(만기가 길면 유동성이 낮다는 것을 나타냄) 총수익률의 횡단면 백분위수 순위와 위험 자산 비율을 사용하여 위험 감수를 대리합니다. 5 표 2는 주식 클래스-월 수준에서 이러한 펀드 특성에 대한 요약 통계를 제공합니다.

투자자 기반과 펀드 포트폴리오 선택 사이의 관계에 대한 간단한 설명을 제공하기 위해 샘플 기간 동안 MMF 주식 클래스를 주요 투자자 유형에 따라 그룹으로 분류하고 각 그룹의 평균 유동성 수준과 위험 측정값을 표시합니다.

그림 2는 다른 기관 프라임 MMF에 비해 은행 투자자가 지배하는 펀드가 더 높은 수준의 주간 유동 자산을 보유하고 평균적으로 더 짧은 가중 평균 만기를 유지한다는 것을 보여줍니다. 유사한 방법론을 기반으로 한 그림 3은 은행 투자자가 지배하는 펀드가 다른 펀드에 비해 평균 총 수익률이 낮고 위험 자산을 적게 보유하고 있음을 보여줍니다.

참고: "은행"은 은행이 주식 클래스 투자의 50% 이상을 차지하는 경우 주요 투자자 유형으로 정의됩니다. 다른 주요 투자자 유형도 유사하게 정의됩니다. "없음"은 단일 투자자 유형이 전체 투자의 절반 이상을 차지하지 않음을 나타냅니다.

참고: "은행"은 은행이 주식 클래스 투자의 50% 이상을 차지하는 경우 주요 투자자 유형으로 정의됩니다. 다른 주요 투자자 유형도 유사하게 정의됩니다. "없음"은 단일 투자자 유형이 전체 투자의 절반 이상을 차지하지 않음을 나타냅니다.

다음으로, 이러한 관계를 체계적으로 수량화하고 일반적인 시간 효과 및 기타 혼란 요인을 설명하기 위해 주요 투자자 지표에 대한 펀드 특성에 대한 동시 패널 회귀 분석을 실행합니다.

$$$$ {펀드\ 특성}_{i,t}=\alpha+\beta_{딜러}\times 딜러_{i,t}+\beta_{은행}\times Bank_{i,t}+\beta_{회사}\times 회사_{i,t}+\beta_{기타}\times Other_{i,t}+\gamma\times{HHI}_{i,t}+\mu_t+\epsilon_{i,t}. $$$$

주요 투자자 지표 외에도, 우리는 Herfindahl-Hirschman Index(HHI)에 의해 대체되는 특정 주식 클래스에 대한 투자자 유형의 집중도를 통제합니다. 우리는 투자자 구성 척도(예: $$\beta$$)에 대한 계수가 인과관계보다는 연관성으로 해석되어야 한다는 점을 강조합니다. 이 계수는 다양한 투자자 프로필을 가진 주식 클래스에 따라 펀드 특성이 어떻게 다른지 설명합니다. 또한 모든 펀드에 영향을 미치는 일반적인 시계열 충격을 흡수하기 위해 연월 고정 효과($$\mu_t$$)를 제어합니다. 표준 오류는 단면 의존성과 계열 상관 관계를 설명하기 위해 주식 클래스 및 월 수준에서 양방향으로 클러스터링됩니다.

그림 2와 3의 결과와 일관되게, 표 3의 회귀 결과는 은행이 주요 투자자인 펀드가 보다 보수적인 포트폴리오 포지션을 유지한다는 것을 보여줍니다. 즉, 더 짧은 포트폴리오 만기를 유지하고(즉, 더 높은 유동성) 총수익률은 더 낮습니다(즉, 더 낮은 위험). 이와 대조적으로 딜러나 비금융회사가 주로 보유하는 펀드는 장기 포트폴리오를 보유합니다. 6

이러한 조사 결과는 펀드의 투자자 기반과 포트폴리오 선택 사이에 중요한 연관성이 있음을 지적합니다. 특히, 은행을 주요 투자자로 하는 펀드가 보다 보수적인 포트폴리오를 보유하는 경향은 왜 그러한 차이가 발생하는지에 대한 의문을 제기합니다. 다음 섹션의 분석에 따르면 이러한 패턴은 은행 투자자의 흐름 역학과 일치하는 것으로 보입니다.

다음으로 투자자 기반과 흐름 역학 간의 관계를 조사합니다. 직관적으로 투자자 흐름은 투자자 자신에 의해 주도되며 다양한 유형의 투자자는 다양한 철수 패턴을 나타낼 수 있습니다. 구체적으로, 우리는 특정 투자자 기반 특성을 지닌 펀드가 다음 달에 더 큰 흐름 변동성을 경험하는지 또는 대규모 유출 가능성이 더 높은지를 테스트합니다.

이러한 관계를 평가하기 위해 현재 투자자 기반을 바탕으로 다음 달 흐름 결과를 회귀 분석합니다.

$$$$ Flow\ Outcome_{i,t+1}=\alpha+\beta_{Dealer}\times Dealer_{i,t}+\beta_{Bank}\times Bank_{i,t}+\beta_{Firm}\times Firm_{i,t}+\beta_{Other}\times Other_{i,t} \\ +\gamma\times{HHI}_{i,t}+\mu_t+\epsilon_{i,t}, $$$$

여기서 $$Flow\ Outcome$$은 (i) $$t + 1$$ 월 동안 $$i$$ 주식 클래스의 일일 흐름 비율의 표준 편차 또는 (ii) $$t + 1$$ 월에서 해당 주식 클래스가 최소 5%의 일일 순 유출을 경험한 일수의 비율입니다. 모든 회귀에는 연월 고정 효과가 포함되며 표준 오류는 주식 클래스와 월 수준 모두에서 양방향 클러스터링됩니다.

표 4는 은행이 주요 투자자일 때 MMF가 더 변동성이 큰 흐름을 경험하는 경향이 있으며 다음 달에 대규모 유출에 직면할 가능성이 더 높다는 것을 보여줍니다. 7 이러한 조사 결과는 은행을 주요 투자자로 둔 MMF가 보다 보수적이고 유동적인 포트폴리오 포지션을 유지한다는 당사의 이전 결과와 일치합니다. 종합적으로, 우리의 결과는 MMF가 은행의 상대적으로 변동성이 큰 자금 흐름과 대규모 인출 경향에 대응하여 추가적인 예방 조치를 취할 수 있음을 시사합니다. 이러한 흐름 패턴은 은행의 MMF 투자 동기와 이러한 투자 관리에 대한 은행의 동기를 반영할 수 있으며, 이는 이 문서의 범위를 벗어나는 문제입니다.

새로운 데이터를 사용하여 우리는 기관 프라임 MMF의 투자자 구성이 포트폴리오 결정 및 흐름 역학과 유의미한 연관이 있음을 발견했습니다. 우리가 찾은 관계는 MMF가 투자자 행동에 반응하고 포트폴리오 위험을 통합된 방식으로 관리한다는 것을 나타냅니다.

우리의 분석은 MMF 사이에 중대한 스트레스가 없었던 15개월 기간을 기반으로 하며 시장 긴장 기간 동안 투자자 구성의 예측 역할은 여전히 ​​불확실하지만, 결과는 투자자 구성이 MMF 흐름 역학에 대한 유익한 지표임을 시사합니다. 이러한 패턴은 스트레스 상황 동안 대규모 상환 가능성에 영향을 미칠 수 있으므로 MMF 실행 위험 평가 시 고려해야 할 사항이 있습니다.

1. 단일 MMF는 다양한 투자자 그룹을 대상으로 다양한 주식 클래스를 제공하는 경우가 많습니다. 이들 클래스는 동일한 기본 포트폴리오를 갖고 있지만 일반적으로 수수료 구조와 투자자 자격이 다릅니다.  텍스트로 돌아가기

2. SEC는 2020년 3월 프라임 MMF 운영에 이어 2023년 7월 업계를 위한 개혁안을 채택했습니다. 개혁은 2024년 10월부터 전면적으로 시행되었습니다.

3. 피더 펀드와 머니마켓 ETF는 최종 표본에서 제외됩니다.  텍스트로 돌아가기

4. 12가지 유형은 브로커/딜러, 예금기관, 비금융회사, 등록투자회사, 보험회사, 지방자치단체, 비영리단체, 연기금, 사모펀드, 국부펀드 및 기타 투자자입니다.  텍스트로 돌아가기

5. 주간 유동 자산은 미국 정부의 현금, 직접 및 특정 간접 부채, 영업일 기준 5일 이내에 만기되는 유가 증권 및 영업일 기준 5일 이내에 만기되는 미수금 잔액을 의미합니다. 위험자산 비중은 기업어음, 예금증서, 정기예금으로 구성된 펀드자산의 비율입니다.  텍스트로 돌아가기

6. 표에는 보고되지 않았지만 주요 투자자 지표를 연속 투자자 지분으로 대체할 때 유사한 패턴을 관찰합니다.  텍스트로 돌아가기

7. 두 가지 견고성 검사(표시되지 않음)를 수행합니다. (i) 다음 달 대신 다음 분기에 대한 흐름 결과를 계산하고 (ii) 주요 투자자 지표를 지속적인 투자자 지분 측정으로 대체합니다. 두 접근 방식 모두 일관된 결과를 낳습니다.  텍스트로 돌아가기

Li, Yi, Nick Panetta, Weston Watts(2026). "머니 마켓 펀드의 투자자 구성 및 흐름 역학에 대한 영향", FEDS Notes. 워싱턴: 연방준비제도 이사회, 2026년 5월 8일, https://doi.org/10.17016/2380-7172.3973.

면책 조항: FEDS Notes는 이사회 직원이 자신의 견해를 제공하고 경제 및 금융 분야의 다양한 주제에 대한 분석을 제공하는 기사입니다. 이 기사는 FEDS 작업 보고서 및 IFDP 보고서보다 짧고 기술 지향적이지 않습니다.

## 📄 영문 원본
Money market funds (MMFs) play a critical role in supplying short-term funding to corporations, banks, and governments. While existing research has made substantial progress in understanding MMF portfolio choices and investor flows, little is known about the composition of MMFs' institutional investors. In this FEDS Note, we use newly available data to provide an overview of MMFs' investor composition and examine how it relates to funds' portfolio characteristics and flow dynamics. We find that when banks are the dominant investors, MMFs tend to experience more volatile flows and a higher likelihood of large outflows. Consistent with this pattern, MMFs with banks as principal investors hold more liquid and lower-risk portfolios. Although our methodology does not attempt to establish causality, the results suggest that MMFs respond to investor behavior and manage portfolio risk in an integrated manner.

MMFs must file Securities and Exchange Commission (SEC) Form N-MFP each month. 1  Beginning in June 2024, the SEC required institutional prime MMFs to disclose a breakdown of their investor composition by type. The new data on investor types, which is reported for each of a fund's share classes, complements Form N-MFP data that have been collected for many years, including granular security-level holdings and liquidity metrics. In combination, these data allow us to link investor composition to a fund's portfolio exposures, risk profiles, and liquidity management. In addition, we use daily flow information to construct measures of investor flow dynamics, which enables us to examine whether investor composition has a potential influence on flow behavior.

Our sample spans June 2024 through August 2025. We conduct the analysis at the share-class level rather than the aggregate fund level, since different share classes often target distinct investor segments and may exhibit materially different flow dynamics. We focus on institutional prime MMFs that are publicly offered and that consistently file N-MFP reports throughout the sample period. Funds that were liquidated, converted, or merged with another fund prior to the implementation of SEC reforms in October 2024 are excluded to maintain a consistent panel. 2  The final sample includes 32 share classes from 8 institutional prime funds. 3

Form N-MFP requires funds to classify investors in each share class into 12 categories. 4  We consolidate these into four groups: Dealer (broker/dealers), Bank (depository institutions), Firm (nonfinancial firms), and Other (all remaining types). As shown in Figure 1, over our sample period, Dealer and Bank each account for roughly 30% of investments in institutional prime MMFs, while Firm and Other each contribute about 20%.

Note: "Bank" = depository institutions; "Dealer" = broker/dealers; "Firm" = nonfinancial firms; "Other" includes registered investment companies, insurance companies, municipalities, nonprofits, pension funds, private funds, sovereign funds, and "other investors" as reported in Form N-MFP. The legend identifies series in order from top to bottom.

We then define four dummy variables ( Dealer ,  Bank ,  Firm , and  Other ) to indicate the principal-investor type for each share class. Specifically, $$Dealer_{i,t}$$ equals 1 if dealers provide more than 50% of the investments in share class $$i$$ in month $$t$$, and 0 otherwise. The other indicators are defined analogously. By construction, at most one principal-investor indicator can equal 1 for a given share class in a given month.

Table 1 reports the summary statistics for these principal-investor indicators based on the share class–month panel. Across share classes, there is a 23% probability that dealers are the principal investor, a 26% probability that banks are the principal investor, and an 11% probability that nonfinancial firms are the principal investor. For 19% of share classes, no single investor type accounts for more than half of total investments.

We next examine how investor types relate to key fund characteristics. Different types of investors may have distinct preferences for liquidity and risk-taking. These preferences may influence investors' allocation decisions across MMFs as well as how fund managers adjust fund characteristics to attract and respond to specific investor bases. Rather than attempting to establish causality, we examine the associations between investor composition and fund characteristics, including size, liquidity condition, and risk profiles.

Specifically, we use weekly liquid assets (WLA) and weighted-average maturity (WAM) to capture funds' portfolio liquidity (with longer maturity indicating lower liquidity), and the cross-sectional percentile ranking of gross yield and the share of risky assets to proxy for risk-taking. 5  Table 2 provides summary statistics for these fund characteristics at the share class-month level.

To provide a simple illustration of the relationship between investor base and fund portfolio choices, we sort MMF share classes over the sample period into groups based on their principal-investor type and plot the average levels of liquidity and risk measures for each group.

Figure 2 shows that, relative to other institutional prime MMFs, funds dominated by bank investors hold higher levels of weekly liquid assets and maintain shorter weighted average maturities on average. Based on a similar methodology, Figure 3 shows that funds dominated by bank investors earn lower average gross yields and hold fewer risky assets relative to their peers.

Note: "Bank" is defined as the principal-investor type if banks account for more than 50% of a share class's investments; other principal-investor types are defined analogously. "None" indicates that no single investor type accounts for more than half of total investments.

Note: "Bank" is defined as the principal-investor type if banks account for more than 50% of a share class's investments; other principal-investor types are defined analogously. "None" indicates that no single investor type accounts for more than half of total investments.

Next, to systematically quantify these relationships and account for common time effects and other confounding factors, we run contemporaneous panel regressions of fund characteristics on principal-investor indicators:

$$$$ {Fund\ Charateristics}_{i,t}=\alpha+\beta_{Dealer}\times Dealer_{i,t}+\beta_{Bank}\times Bank_{i,t}+\beta_{Firm}\times Firm_{i,t}+\beta_{Other}\times Other_{i,t}+\gamma\times{HHI}_{i,t}+\mu_t+\epsilon_{i,t}. $$$$

In addition to the principal-investor indicators, we control for the concentrations of investor types for a given share class, proxied by the Herfindahl-Hirschman Index (HHI). We emphasize that the coefficients on investor composition measures (i.e., $$\beta$$) should be interpreted as associative rather than causal: they describe how fund characteristics vary across share classes with different investor profiles. We also control for year-month fixed effects ($$\mu_t$$) to absorb common time-series shocks that influence all funds. Standard errors are two-way clustered at the share-class and month levels to account for cross-sectional dependence and serial correlation.

Consistent with the findings in Figure 2 and 3, regression results in Table 3 show that funds in which banks are the principal investors maintain more conservative portfolio positions: they keep shorter portfolio maturities (i.e., higher liquidity) and generate lower gross yields (i.e., lower risk). In contrast, funds predominantly held by dealers or nonfinancial firms hold longer-duration portfolios. 6

These findings point to a significant association between a fund's investor base and its portfolio choices. In particular, the tendency for funds with banks as their primary investors to hold more conservative portfolios raises the question of why such differences arise. Our analysis in the next section suggests that these patterns appear to be consistent with the flow dynamics of bank investors.

We next examine the relationships between investor base and flow dynamics. Intuitively, investor flows are driven by the investors themselves, and different types of investors may exhibit different withdrawal patterns. Specifically, we test whether funds with certain investor base characteristics experience greater flow volatility or a higher probability of large outflows in the subsequent month.

To evaluate these relationships, we regress next month's flow outcomes on current investor base:

$$$$ Flow\ Outcome_{i,t+1}=\alpha+\beta_{Dealer}\times Dealer_{i,t}+\beta_{Bank}\times Bank_{i,t}+\beta_{Firm}\times Firm_{i,t}+\beta_{Other}\times Other_{i,t} \\ +\gamma\times{HHI}_{i,t}+\mu_t+\epsilon_{i,t}, $$$$

where $$Flow\ Outcome$$ is either (i) the standard deviation of share class $$i$$'s daily percentage flows during month $$t + 1$$ or (ii) the percentage of days in month $$t + 1$$ in which the share class experiences daily net outflows of at least 5%. All regressions include year–month fixed effects, and standard errors are two-way clustered at both the share-class and month levels.

Table 4 shows that when banks are the principal investors, MMFs tend to experience more volatile flows and are more likely to face large outflows in the subsequent month. 7  These findings are consistent with our earlier result that MMFs with banks as principal investors maintain more conservative and liquid portfolio positions. Together, our results suggest that MMFs may take additional precautions in response to banks' relatively more volatile flows and greater propensity for large-scale withdrawals. Such flow patterns may reflect banks' motives for investing in MMFs and their management of these investments, issues that are beyond the scope of this note.

Using novel data, we find that the investor composition of institutional prime MMFs is significantly associated with their portfolio decisions and flow dynamics. The relationships we find indicate that MMFs respond to investor behavior and manage portfolio risk in an integrated manner.

While our analysis is based on a 15-month period in which there was no material stress among MMFs, and the predictive role of investor composition during periods of market strain remains uncertain, the results suggest that investor composition is an informative indicator of MMF flow dynamics. These patterns may have implications for the likelihood of large redemptions during stress episodes and therefore warrant consideration in assessments of MMF run risk.

1. A single MMF often offers multiple share classes targeted to different investor groups; while these classes have the same underlying portfolio, they usually differ in fee structures and investor eligibility.  Return to text

2. Following the runs on prime MMFs in March 2020, the SEC adopted reforms for the industry in July 2023. The reforms were fully implemented starting in October 2024.  Return to text

3. Feeder funds and money market ETFs are excluded from the final sample.  Return to text

4. The 12 types are: broker/dealers, depository institutions, nonfinancial firms, registered investment companies, insurance companies, municipalities, nonprofit organizations, pension funds, private funds, sovereign funds, and other investors.  Return to text

5. Weekly liquid assets are cash, direct and certain indirect debt of the U.S. Government, securities that mature within five business days, and receivable balances due within five business days. Risky asset share is the percentage of fund assets comprised of commercial paper, certificates of deposit, and time deposits.  Return to text

6. Although not reported in the table, we observe similar patterns when replacing the principal-investor indicators with continuous investor shares.  Return to text

7. We conduct two robustness checks (not shown): (i) computing flow outcomes over the subsequent quarter instead of the next month, and (ii) replacing principal-investor indicators with continuous investor-share measures. Both approaches yield consistent results.  Return to text

Li, Yi, Nick Panetta, and Weston Watts (2026). "Investor Composition of Money Market Funds and Its Implications for Flow Dynamics," FEDS Notes. Washington: Board of Governors of the Federal Reserve System, May 08, 2026, https://doi.org/10.17016/2380-7172.3973.

Disclaimer:  FEDS Notes are articles in which Board staff offer their own views and present analysis on a range of topics in economics and finance. These articles are shorter and less technically oriented than FEDS Working Papers and IFDP papers.


---
*출처: https://www.federalreserve.gov/econres/notes/feds-notes/investor-composition-of-money-market-funds-and-its-implications-for-flow-dynamics-20260508.html | 수집: 2026-06-10 01:17 | 지표: FEDS_NOTES*
