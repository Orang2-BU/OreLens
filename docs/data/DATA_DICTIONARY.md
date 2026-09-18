# OreLens — Data Dictionary v0.1

## 1. Purpose

This document defines candidate metrics used by OreLens.

No analytical weight is final until:
1. data availability is confirmed,
2. units/frequency are validated,
3. missingness is measured,
4. historical behavior is tested,
5. methodology is backtested.

Supported commodities:
- Coal
- Gold
- Nickel
- Copper

---

## 2. Confidence Levels

- **High** — direct structured data from a reliable source
- **Medium** — derived from complete structured data
- **Low** — proxy or partial coverage
- **Unavailable** — insufficient data

Missing values must never be silently converted to zero.

---

## 3. Commodity Intelligence Categories

1. Physical Supply
2. Physical Demand
3. Structural Demand
4. Macro Sensitivity
5. Event / Policy Context

---

## 4. Common Commodity Metrics

| Metric | Category | Source | Frequency | Transformation | Expected Use | Priority |
|---|---|---|---|---|---|---|
| Commodity Price | Market | Sectors | Available interval | return / rolling return | Reference variable | Core |
| Global Production | Supply | Sectors | Annual | YoY | Supply growth | Core |
| Production Share | Supply | Sectors | Annual | % / HHI | Supply concentration | Core |
| Global Reserves | Supply | Sectors | Annual | share / HHI | Long-run supply structure | Core |
| Export Value | Trade | Sectors | Annual | YoY | Trade/supply proxy | Core |
| Import Value | Demand | Sectors | Annual | YoY | Demand proxy | Core |
| Trade Concentration | Demand | Derived | Annual | HHI | Market dependency | Core |
| Indonesia Production | Supply | Sectors | Annual | YoY | Indonesia contribution | Core |
| Export Destination | Demand | Sectors | Annual | share / HHI | Destination dependency | Core |
| USD Strength | Macro | FRED | Daily/Monthly | return/change | USD sensitivity | Core |
| Global GDP Growth | Macro | World Bank/IMF | Annual | YoY | Broad demand | Support |
| China GDP Growth | Macro/Demand | World Bank | Annual | YoY | Industrial demand proxy | Core for Coal/Nickel/Copper |
| China Industrial Activity | Demand | OECD/external | Monthly | YoY/Z-score | Industrial demand proxy | Core for Nickel/Copper |
| Geopolitical Event Signal | Event | GDELT/external | Daily | count/Z-score | Context | Optional |

---

## 5. Coal Metrics

### Supply

| Metric | Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|
| Indonesia Coal Production | Sectors | Annual | YoY | Higher supply may pressure price | Core |
| Global Coal Production | Sectors | Annual | YoY | Global supply condition | Core |
| Indonesia Production Share | Sectors | Annual | % | Indonesia relevance | Core |
| Coal Reserve Share | Sectors | Annual | %/HHI | Supply concentration | Core |
| Coal Export Value | Sectors | Annual | YoY | Export availability | Core |
| Production Concentration | Derived | Annual | HHI | Disruption sensitivity | Core |

### Demand

| Metric | Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|
| China Coal Imports | UN Comtrade | Monthly/Annual | YoY | Stronger demand | Core |
| India Coal Imports | UN Comtrade | Monthly/Annual | YoY | Stronger demand | Core |
| China GDP | World Bank | Annual | YoY | Macro demand | Core |
| India GDP | World Bank | Annual | YoY | Macro demand | Support |
| Electricity Demand | EIA/external | Monthly/Annual | YoY | Power-demand support | Core |
| Coal Consumption | EIA/external | Monthly/Annual | YoY | Direct demand proxy | Core |

### Structural / Substitution

| Metric | Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|
| Natural Gas Price | EIA/FRED | Daily/Monthly | return | Higher gas may support coal substitution | Core |
| Renewable Generation | EIA/external | Monthly/Annual | YoY/share | Potential coal displacement | Support |
| Energy Transition Trend | IEA | Annual | trend | Structural context | Optional |

---

## 6. Gold Metrics

### Supply

| Metric | Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|
| Global Gold Production | Sectors | Annual | YoY | Mine supply | Core |
| Indonesia Gold Production | Sectors | Annual | YoY | Local supply | Core |
| Global Gold Reserves | Sectors | Annual | share/HHI | Long-term supply | Core |
| Production Concentration | Derived | Annual | HHI | Disruption sensitivity | Core |

### Demand / Macro

| Metric | Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|
| Real Interest Rate | FRED | Daily/Monthly | level/change | Higher real rates often pressure gold | Core |
| US Treasury Yield | FRED | Daily | change | Opportunity-cost context | Core |
| USD Strength | FRED | Daily/Monthly | return | Stronger USD often pressures gold | Core |
| US Inflation | FRED | Monthly | YoY | Inflation regime | Core |
| Central Bank Gold Demand | WGC/IMF/ECB | Monthly/Quarterly | net purchases | Demand support | Support |
| Investment Demand | WGC/external | Monthly | flows | Financial demand | Optional |
| Geopolitical Risk | GDELT/external | Daily/Monthly | Z-score | Safe-haven context | Optional |

---

## 7. Nickel Metrics

### Supply

| Metric | Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|
| Indonesia Nickel Production | Sectors | Annual | YoY | Higher supply may pressure price | Core |
| Global Nickel Production | Sectors | Annual | YoY | Global supply | Core |
| Indonesia Production Share | Sectors | Annual | % | Indonesia supply power | Core |
| Nickel Reserves | Sectors | Annual | share/HHI | Long-run supply | Core |
| Nickel Export Value | Sectors | Annual | YoY | Trade proxy | Core |
| Production Concentration | Derived | Annual | HHI | Supply concentration | Core |

### Physical Demand

| Metric | Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|
| China Nickel Imports | UN Comtrade | Monthly/Annual | YoY | Demand support | Core |
| China Industrial Activity | OECD/external | Monthly | YoY/Z-score | Industrial demand | Core |
| China GDP | World Bank | Annual | YoY | Macro demand | Core |
| Stainless Steel Demand Proxy | External | Monthly/Annual | YoY | Major industrial demand | High-priority gap |

### Structural Demand

| Metric | Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|
| EV Battery Demand | IEA | Annual | YoY | Structural nickel demand | Core |
| EV Sales | IEA | Annual | YoY | Battery-demand proxy | Core |
| Battery Chemistry Share | IEA/external | Annual | share | Nickel-bearing chemistry relevance | Support |

---

## 8. Copper Metrics

### Supply

| Metric | Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|
| Global Copper Production | Sectors | Annual | YoY | Supply trend | Core |
| Indonesia Copper Production | Sectors | Annual | YoY | Local supply | Core |
| Copper Reserves | Sectors | Annual | share | Long-run capacity | Core |
| Production Concentration | Derived | Annual | HHI | Disruption sensitivity | Core |
| Copper Export Value | Sectors | Annual | YoY | Trade proxy | Core |
| Copper Inventory | External | Daily/Weekly | change/days supply | Market balance | High-priority gap |

### Demand

| Metric | Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|
| China Copper Imports | UN Comtrade | Monthly/Annual | YoY | Demand proxy | Core |
| China Industrial Activity | OECD/external | Monthly | YoY | Industrial demand | Core |
| China GDP | World Bank | Annual | YoY | Macro demand | Core |
| Global Manufacturing Activity | OECD/external | Monthly | index/change | Industrial cycle | Support |

### Structural Demand

| Metric | Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|
| Grid Investment | IEA/external | Annual | YoY | Structural demand | Support |
| EV Deployment | IEA | Annual | YoY | Electrification demand | Support |
| Renewable Capacity | IEA/external | Annual | YoY | Structural demand | Optional |

---

## 9. Company Identity and Operations

| Metric | Source | Frequency | Transformation | Role |
|---|---|---|---|---|
| Commodity Type | Sectors | Static/update | categorical | Universe |
| Production Volume | Sectors | Annual | YoY | Exposure/operations |
| Sales Volume | Sectors | Annual | YoY | Exposure |
| Production Growth | Derived | Annual | YoY | Operational health |
| Sales Growth | Derived | Annual | YoY | Operational health |
| Resources | Sectors | Annual | normalized | Resilience |
| Reserves | Sectors | Annual | normalized | Resilience |
| Reserve Coverage | Derived | Annual | reserves/production | Resilience |
| Mining Site Count | Sectors | Update-based | count | Diversification |
| Site Production Concentration | Derived | Annual | HHI | Operational concentration |
| License Status | Sectors | Update-based | categorical | Operational context |
| License Expiry | Sectors | Update-based | years remaining | Operational context |

---

## 10. Company Exposure Metrics

| Metric | Source | Frequency | Transformation | Role | Priority |
|---|---|---|---|---|---|
| Commodity Revenue Share | Sectors segment data | Annual | % | Exposure | Core if available |
| Production Dependency | Sectors | Annual | % | Exposure | Core |
| Sales Dependency | Sectors | Annual | % | Exposure | Core |
| Geographic Sales Concentration | Sectors | Annual | HHI | Exposure/resilience | Core |
| Top Destination Share | Sectors | Annual | % | Exposure | Core |
| Operational Concentration | Derived | Annual | HHI | Exposure | Core |
| Commodity Beta | Sectors stock + commodity price | Monthly | regression beta | Historical sensitivity | Support |

Fallback:
- missing revenue share ≠ zero,
- use production/sales evidence,
- reduce confidence.

---

## 11. Fundamental Profile

| Metric | Category | Source | Frequency | Transformation | Priority |
|---|---|---|---|---|---|
| Revenue | Growth | Sectors | Quarterly/Annual | YoY | Core |
| Revenue Growth | Growth | Derived | Quarterly/Annual | YoY | Core |
| Net Income | Growth | Sectors | Quarterly/Annual | YoY | Core |
| Net Income Growth | Growth | Derived | Quarterly/Annual | YoY | Core |
| ROE | Profitability | Sectors | Quarterly/Annual | peer percentile | Core |
| ROA | Profitability | Sectors | Quarterly/Annual | peer percentile | Support |
| Net Margin | Profitability | Sectors/Derived | Quarterly/Annual | % | Core |
| DER | Leverage | Sectors | Quarterly/Annual | peer percentile | Core |
| Debt/Assets | Leverage | Sectors | Quarterly/Annual | % | Support |
| PE | Valuation | Sectors | Current/periodic | peer percentile | Core |
| PB | Valuation | Sectors | Current/periodic | peer percentile | Core |
| Market Cap | Market | Sectors | Daily/current | log/percentile | Support |

---

## 12. Resilience Metrics

| Metric | Calculation | Why It Matters | Priority |
|---|---|---|---|
| Reserve Coverage | reserves / annual production | Production sustainability | Core |
| Production Stability | volatility of production growth | Operational consistency | Core |
| Site Diversification | site HHI / count | Reduces single-site dependency | Core |
| Sales Diversification | destination HHI | Reduces market dependency | Core |
| Revenue Growth | YoY revenue | Business momentum | Core |
| Profitability | ROE/net margin | Shock absorption | Core |
| Leverage | DER | Debt vulnerability | Core |
| License Context | status/expiry | Operational continuity | Core |
| Commodity Diversification | commodity shares | Reduces single-commodity dependency | Support |
| Liquidity/Cash | cash/debt | Downturn buffer | Support |

---

## 13. Derived Metric Definitions

### HHI
`HHI = Σ share_i²`

Use for:
- country supply concentration,
- site concentration,
- sales-destination concentration,
- trade concentration.

### Reserve Coverage
`Reserve Coverage = Company Reserves / Annual Production`

Comparative indicator only; not literal mine life.

### YoY Growth
`YoY = (Current - Previous) / Previous`

### Historical Commodity Beta
`Company Return_t = α + β × Commodity Return_t + ε`

Beta describes historical sensitivity, not future certainty.

---

## 14. Normalization

Preferred methods:
- YoY growth,
- rolling returns,
- Z-score,
- peer percentile,
- HHI,
- log transform,
- standardized beta.

Peer groups should be commodity-specific where possible.

---

## 15. Open Gaps

| Metric | Commodity | Candidate Source | Status |
|---|---|---|---|
| Stainless Steel Production | Nickel | external industry source | unresolved |
| Copper Inventory | Copper | exchange/market source | unresolved |
| Central Bank Gold Purchases | Gold | WGC/IMF | validate |
| Detailed Coal Demand | Coal | EIA/Comtrade | validate |
| Battery Chemistry Share | Nickel | IEA | validate |
| Grid Investment | Copper | IEA/external | validate |
| Geopolitical Risk | All | GDELT/external | optional |

---

## 16. Quant Research Pipeline

```text
Data Collection
→ Frequency Alignment
→ Missing-Data Audit
→ Transformation
→ Correlation Screening
→ Multivariate Regression
→ Rolling Regression
→ Regime Comparison
→ Backtest
→ Driver Importance
```

Weights are not locked before this pipeline is validated.
