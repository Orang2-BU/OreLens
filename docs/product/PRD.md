# OreLens — Product Requirements Document (PRD)

## 1. Product Overview

**Product Name:** OreLens
**Hackathon Track:** Market Intelligence
**Primary Market:** Indonesia Stock Exchange (IDX) mining companies
**Commodity Scope:** Coal, Gold, Nickel, Copper
**Core Data Provider:** Sectors API
**External Enrichment:** World Bank, FRED, UN Comtrade, EIA, IEA, and other official/public sources where required.

OreLens is a commodity-intelligence platform that helps users understand:

1. how a commodity environment is changing,
2. how exposed a mining company is to that commodity,
3. how resilient the company is to changes in that environment,
4. how healthy the company’s fundamentals are,
5. what evidence supports the analysis.

OreLens is an information and research-support product. It does **not** provide buy/sell recommendations, target prices, automated trading, or guaranteed forecasts.

---

## 2. Problem Statement

Mining-company analysis is fragmented. An investor may need to separately examine:

- commodity prices,
- production and reserves,
- trade flows,
- consumer-country demand,
- mining operations,
- sales destinations,
- licenses,
- company financials,
- valuation,
- currency and macro variables,
- structural-demand trends.

OreLens aims to answer:

> **How exposed is a company to a commodity, how resilient is it to changing commodity conditions, and why?**

---

## 3. Target Users

### Primary
Retail investors and independent analysts who already understand basic stock analysis but want more structured commodity-specific intelligence.

### Secondary
- equity-research students,
- junior analysts,
- commodity researchers,
- financial-content researchers.

---

## 4. Product Principles

1. **Sectors-first** — Sectors remains the core mining and company-data provider.
2. **Explainable by default** — every analytical output should be traceable to evidence.
3. **Exposure is not quality** — high exposure is not inherently positive or negative.
4. **Resilience is separate from exposure** — a company can be highly exposed and highly resilient.
5. **No arbitrary scoring without validation** — weighting must be informed by research and historical testing.
6. **Missing data is not zero** — missing metrics reduce confidence rather than being silently imputed.
7. **No unsupported prediction** — stock-price or revenue forecasts require a defensible model.

---

## 5. Core Analytical Architecture

### 5.1 Commodity Intelligence Engine
Evaluates:

- Physical Supply
- Physical Demand
- Structural Demand
- Macro Sensitivity
- Event / Policy Context

### 5.2 Company Intelligence Engine
Evaluates:

- Commodity Exposure
- Resilience
- Fundamental Profile
- Historical Commodity Sensitivity
- Evidence

Final OreLens intelligence combines commodity context with company-specific exposure and resilience.

---

## 6. Supported Commodities

The MVP supports:

- Coal
- Gold
- Nickel
- Copper

Other commodities are out of scope for the hackathon MVP.

---

## 7. Commodity-Specific Driver Framework

### Coal
**Supply:** Indonesia/global production, export availability, reserves, disruptions.
**Demand:** China/India imports, electricity demand, coal consumption.
**Structural/Substitution:** natural-gas prices, renewable generation, energy transition.
**Macro:** USD, China/India economic activity.

### Gold
**Supply:** mine production, reserves.
**Demand:** central-bank purchases, investment demand, jewelry demand where available.
**Macro:** real rates, Treasury yields, USD, inflation.
**Risk:** geopolitical context.

### Nickel
**Supply:** Indonesia/global production, reserves, concentration, quota/policy context.
**Physical Demand:** stainless steel, China imports, industrial activity.
**Structural Demand:** EV sales, battery demand, battery chemistry.
**Macro:** USD, China economy.

### Copper
**Supply:** mine production, reserves, concentration, inventory where available, disruptions.
**Physical Demand:** China imports, industrial production, manufacturing.
**Structural Demand:** grid investment, electrification, EV deployment, renewable capacity.
**Macro:** USD, China/global growth.

---

## 8. Company Analysis Model

### 8.1 Exposure
Answers:

> **How dependent is the company on the selected commodity?**

Candidate metrics:
- commodity revenue share,
- production dependency,
- sales dependency,
- geographic sales concentration,
- operational concentration,
- historical commodity beta.

### 8.2 Resilience
Answers:

> **How capable is the company of absorbing or adapting to commodity shocks?**

Candidate metrics:
- reserve coverage,
- production stability,
- site diversification,
- sales diversification,
- profitability,
- leverage,
- license context,
- liquidity where available.

### 8.3 Fundamental Profile
Dimensions:
- Growth
- Profitability
- Leverage
- Valuation
- Balance-sheet strength

Candidate metrics:
- revenue growth,
- net-income growth,
- ROE,
- ROA,
- net margin,
- DER,
- debt/assets,
- PE,
- PB.

---

## 9. Main User Journey

### Flow A — Select Commodity
User selects Coal, Gold, Nickel, or Copper.

### Flow B — Understand Commodity Environment
OreLens shows price context, production, reserves, trade, demand proxies, macro context, and driver profile.

### Flow C — Compare Companies
OreLens lists related IDX mining companies with:
- Exposure
- Resilience
- Fundamental Profile
- Data Confidence

### Flow D — Investigate a Company
Company detail includes:
- operations,
- exposure breakdown,
- resilience breakdown,
- fundamentals,
- sales destinations,
- reserves,
- historical commodity sensitivity,
- evidence.

### Flow E — Run a Scenario
Examples:
- Nickel price -20%
- Copper demand -10%
- Coal supply +10%
- Gold real yield +100 bps

OreLens returns relative sensitivity and explanatory evidence, not target prices.

---

## 10. Product Screens

### Home
- commodity selector,
- coverage summary,
- short value proposition.

### Commodity Overview
- price trend,
- supply indicators,
- demand indicators,
- reserves,
- trade,
- macro context,
- driver profile.

### Company Comparison
- ticker,
- company,
- exposure,
- resilience,
- fundamentals,
- confidence.

### Company Detail
- company overview,
- exposure,
- resilience,
- fundamentals,
- operational metrics,
- evidence.

### Scenario Simulator
- commodity,
- shock type,
- shock magnitude,
- company sensitivity,
- resilience,
- evidence.

---

## 11. Data Sources

### Core — Sectors
Used for:
- commodity prices,
- production,
- resources/reserves,
- trade,
- export destinations,
- mining companies,
- company production,
- sales volume,
- company reserves,
- mining sites,
- licenses,
- sales destinations,
- company financials,
- listed-company fundamentals.

### External Enrichment
**World Bank:** GDP and broad macro.
**FRED:** USD, yields, real rates, inflation.
**UN Comtrade:** commodity import/export demand proxies.
**EIA:** coal and energy context.
**IEA:** EV, battery, and energy-transition context.
**GDELT / similar:** optional event and geopolitical context.

---

## 12. Technical Direction

### Frontend
- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query
- ECharts or Recharts

### Backend
- Django
- Django REST Framework
- PostgreSQL

### Analytics
- Python
- Polars
- DuckDB
- Parquet
- NumPy
- SciPy
- statsmodels
- scikit-learn

### Testing
- pytest
- pytest-django
- Vitest
- Playwright

---

## 13. Team Ownership

### Product Research + Quant/Scenario
Owns metric definitions, literature review, quant methodology, normalization, exposure/resilience logic, scenarios, backtesting, and analytical validation.

### Backend + Data
Owns Sectors/external API integrations, ingestion, validation, storage, Django API, and data contracts.

### Frontend + UI/UX
Owns interfaces, visualizations, comparison, evidence UI, and scenario UX.

### Integration + QA + Deployment
Owns end-to-end integration, CI, deployment, integration testing, and demo stability.

---

## 14. Non-Goals

The MVP does not include:
- automated trading,
- broker execution,
- investment recommendations,
- target prices,
- portfolio management,
- social features,
- mobile apps,
- subscriptions,
- full AI chatbot,
- unsupported forecasting.

---

## 15. Success Criteria

OreLens MVP succeeds if:

1. all four commodities are selectable,
2. commodity intelligence loads,
3. companies can be compared,
4. exposure is explainable,
5. resilience is explainable,
6. fundamentals are visible,
7. scenario analysis works,
8. evidence is traceable,
9. missing data is handled transparently,
10. Sectors remains core,
11. the full workflow works in the final demo.

---

## 16. Definition of Done

```text
Commodity
→ Commodity Intelligence
→ Company Comparison
→ Company Detail
→ Exposure
→ Resilience
→ Fundamentals
→ Evidence
→ Scenario Analysis
```
