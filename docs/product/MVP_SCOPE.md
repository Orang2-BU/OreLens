# OreLens — MVP Scope

## 1. Goal

The MVP must prove that Sectors mining and company data can be transformed into useful, explainable commodity intelligence for IDX mining companies.

The priority is an end-to-end working workflow, not maximum feature count.

---

## 2. Supported Commodities

Included:
- Coal
- Gold
- Nickel
- Copper

Excluded from MVP:
- Bauxite
- Silver
- Cobalt
- other partial-coverage commodities

---

## 3. Core Question

> **How exposed is an IDX mining company to a selected commodity, how resilient is the company, and what evidence explains the result?**

---

## 4. Must-Have Features

### Commodity Selection
Users can select Coal, Gold, Nickel, or Copper.

### Commodity Overview
Must show:
- commodity price context,
- historical trend,
- production,
- reserves/resources,
- production concentration,
- trade/import/export context,
- key demand context,
- selected macro context.

### Company Universe
For each commodity:
- company,
- ticker,
- exposure,
- resilience,
- fundamental summary,
- data confidence.

### Exposure Analysis
Candidate MVP inputs:
- commodity revenue share where available,
- production dependency,
- sales dependency,
- geographic concentration,
- operational concentration,
- historical commodity beta where history is sufficient.

### Resilience Analysis
Candidate MVP inputs:
- reserve coverage,
- production stability,
- site diversification,
- sales diversification,
- profitability,
- leverage,
- license context.

### Fundamental Profile
Must include:
- revenue growth,
- net-income growth,
- ROE,
- DER,
- PE,
- PB.

### Evidence View
Each material output should show:
- metric,
- source,
- period,
- observed value,
- transformation,
- interpretation,
- confidence.

### Scenario Analysis
Must support structured shocks such as:
- commodity price shock,
- supply shock,
- demand shock where supported,
- selected macro shock.

Outputs:
- relative sensitivity,
- vulnerability,
- resilience,
- major drivers,
- evidence.

No unsupported stock-price prediction.

---

## 5. MVP Screens

1. Home / Commodity Selector
2. Commodity Overview
3. Company Comparison
4. Company Detail
5. Scenario Simulator

---

## 6. Data Sources

### Sectors — Core
- commodity price,
- production,
- reserves/resources,
- trade,
- mining companies,
- company operations,
- sales,
- sites,
- licenses,
- company financials,
- listed-company fundamentals.

### External — Enrichment
**World Bank:** GDP and broad macro.
**FRED:** USD, yields, real rates, inflation.
**UN Comtrade:** imports/exports and trade-demand proxies.
**EIA:** coal and energy context.
**IEA:** EV/battery/energy-transition context where feasible.

---

## 7. Analytical Methods Allowed

Included:
- YoY growth,
- HHI concentration,
- percentile normalization,
- Z-score where useful,
- reserve coverage,
- correlation screening,
- basic multivariate regression,
- rolling regression if history supports it,
- historical commodity beta.

Conditional:
- regime comparison,
- PCA,
- VAR/VECM,
- dynamic weights.

Only use conditional methods if data history and validation are sufficient.

Excluded:
- deep learning,
- black-box prediction,
- neural forecasting,
- unsupported scoring.

---

## 8. Data-Quality Rules

- missing is never equal to zero,
- original unit is retained,
- normalized unit is explicit,
- source and timestamp are retained,
- confidence is attached,
- peer comparisons are commodity-aware.

---

## 9. Out of Scope

- automated trading,
- broker integration,
- buy/sell signals,
- target prices,
- portfolio management,
- social feed,
- mobile app,
- complex auth,
- payments/subscriptions,
- generalized AI chatbot,
- all-commodity coverage.

---

## 10. MVP Acceptance Criteria

The MVP passes if:
- all four commodities can be selected,
- at least one analyzable company exists per commodity,
- exposure works,
- resilience works,
- fundamentals work,
- evidence is visible,
- scenario engine runs,
- outputs are deterministic,
- missing data is transparent,
- Sectors is clearly core,
- demo runs without manual intervention.

---

## 11. Deferred Features

Possible Phase 2:
- geopolitical event engine,
- dynamic regime models,
- central-bank gold-flow analysis,
- copper inventory intelligence,
- stainless-steel production model,
- battery chemistry model,
- grid-investment model,
- alerts,
- portfolio analysis,
- natural-language research assistant.
