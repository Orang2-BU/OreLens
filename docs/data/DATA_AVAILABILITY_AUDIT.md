# OreLens — Data Availability Audit v0.1

## 1. Purpose

This document verifies that the metrics defined in `DATA_DICTIONARY.md` can actually be obtained and used.

The audit should be filled from **real API responses**, not documentation assumptions.

It determines:
- availability,
- endpoint,
- historical depth,
- frequency,
- unit,
- missingness,
- freshness,
- API cost,
- rate limit,
- licensing,
- analytical usability.

No production scoring should be finalized before this audit is substantially complete.

---

## 2. Status Legend

- ✅ Confirmed
- 🟡 Needs live validation
- 🔁 Fallback/proxy required
- ❌ Unavailable
- ⏳ Pending

---

## 3. Required Audit Fields

| Field | Description |
|---|---|
| metric_id | Internal unique identifier |
| metric_name | Human-readable name |
| source | Provider |
| endpoint | API endpoint |
| commodity | Coal/Gold/Nickel/Copper/All |
| geography | Global/country/company |
| unit | Original unit |
| normalized_unit | Internal unit |
| frequency | Daily/Monthly/Quarterly/Annual |
| earliest_date | Earliest usable observation |
| latest_date | Latest usable observation |
| observation_count | Total rows |
| missing_count | Missing rows |
| missing_rate | Missing percentage |
| last_updated | Freshness |
| api_cost | Credits/requests |
| rate_limit | Provider limit |
| license | Usage terms |
| confidence | High/Medium/Low |
| analytics_ready | Yes/No |
| notes | Special issues |

---

## 4. Sectors Audit — Commodity Layer

### 4.1 Commodity Price History

| Commodity | Status | Earliest | Latest | Frequency | Unit | Request Window | Missing Rate | API Cost | Ready |
|---|---|---|---|---|---|---|---|---|---|
| Coal | 🟡 | TBD | TBD | TBD | TBD | Validate | TBD | TBD | No |
| Gold | 🟡 | TBD | TBD | TBD | TBD | Validate | TBD | TBD | No |
| Nickel | 🟡 | TBD | TBD | TBD | TBD | Validate | TBD | TBD | No |
| Copper | 🟡 | TBD | TBD | TBD | TBD | Validate | TBD | TBD | No |

Tasks:
- fetch real sample,
- confirm date format,
- confirm price unit/currency,
- test historical batching,
- estimate credit cost,
- measure continuity.

### 4.2 Global Production

| Commodity | Status | Earliest Year | Latest Year | Unit | Countries | Missing Rate | API Cost | Ready |
|---|---|---:|---:|---|---|---|---|---|
| Coal | 🟡 | TBD | TBD | TBD | TBD | TBD | TBD | No |
| Gold | 🟡 | TBD | TBD | TBD | TBD | TBD | TBD | No |
| Nickel | 🟡 | TBD | TBD | TBD | TBD | TBD | TBD | No |
| Copper | 🟡 | TBD | TBD | TBD | TBD | TBD | TBD | No |

### 4.3 Global Reserves / Resources

| Commodity | Status | Earliest Year | Latest Year | Unit | Coverage | Ready |
|---|---|---:|---:|---|---|---|
| Coal | 🟡 | TBD | TBD | TBD | TBD | No |
| Gold | 🟡 | TBD | TBD | TBD | TBD | No |
| Nickel | 🟡 | TBD | TBD | TBD | TBD | No |
| Copper | 🟡 | TBD | TBD | TBD | TBD | No |

### 4.4 Global Trade

| Commodity | Status | Earliest | Latest | Export Unit | Import Unit | Country Coverage | Ready |
|---|---|---:|---:|---|---|---|---|
| Coal | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Gold | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Nickel | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Copper | 🟡 | TBD | TBD | TBD | TBD | TBD | No |

### 4.5 Indonesia Production

| Commodity | Status | Earliest | Latest | Frequency | Unit | Missing Rate | Ready |
|---|---|---|---|---|---|---|---|
| Coal | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Gold | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Nickel | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Copper | 🟡 | TBD | TBD | TBD | TBD | TBD | No |

### 4.6 Export Destinations

| Commodity | Status | Earliest | Latest | Frequency | Country Coverage | Value/Volume | Ready |
|---|---|---|---|---|---|---|---|
| Coal | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Gold | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Nickel | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Copper | 🟡 | TBD | TBD | TBD | TBD | TBD | No |

---

## 5. Sectors Audit — Company Layer

### 5.1 Mining Company Universe

| Commodity | Status | Company Count | IDX Mapping Quality | Missing Tickers | Ready |
|---|---|---:|---|---|---|
| Coal | 🟡 | TBD | TBD | TBD | No |
| Gold | 🟡 | TBD | TBD | TBD | No |
| Nickel | 🟡 | TBD | TBD | TBD | No |
| Copper | 🟡 | TBD | TBD | TBD | No |

### 5.2 Company Production and Sales

For each company validate:

| Field | Required |
|---|---|
| company_id | Yes |
| ticker | Yes |
| commodity | Yes |
| year | Yes |
| production_volume | Yes |
| production_unit | Yes |
| sales_volume | Yes |
| sales_unit | Yes |
| resource | If available |
| reserve | If available |

Questions:
- Is production commodity-specific?
- Are units consistent across years?
- Are multi-commodity companies separated correctly?
- Are production and sales volumes comparable?
- Is history long enough for stability analysis?

### 5.3 Company Resources / Reserves

| Company | Commodity | Earliest | Latest | Unit | Missing Years | Ready |
|---|---|---:|---:|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | No |

### 5.4 Sales Destinations

Validate:
- company coverage,
- years,
- countries,
- revenue value,
- sales volume,
- unit/currency,
- whether total denominator is known.

Minimum requirement for concentration:
- sufficient destination breakdown,
- reliable total.

### 5.5 Mining Sites

Validate:
- site ID,
- company mapping,
- commodity,
- location,
- production,
- reserves/resources,
- history.

Needed for:
- site count,
- site concentration,
- operational diversification.

### 5.6 Licenses

Validate:
- company mapping,
- commodity,
- license status,
- issue date,
- expiry,
- location,
- missingness.

Initially treat license metrics as context unless coverage proves strong enough for scoring.

### 5.7 Company Financials

Validate:
- revenue,
- net income,
- assets,
- equity,
- debt,
- cash,
- ROE,
- ROA,
- DER,
- PE,
- PB,
- market cap.

For each:
- frequency,
- history,
- unit/currency,
- missing rate,
- restatement behavior if visible.

### 5.8 Revenue Segment Data

Questions:
- Which companies have segment data?
- Which years?
- Is commodity-level revenue identifiable?
- Is taxonomy stable?
- Can commodity revenue share be computed?

Fallback:
- production dependency,
- sales dependency,
- commodity classification,
- reduced confidence.

---

## 6. External Source Audit

### 6.1 World Bank

Candidate metrics:
- China GDP growth,
- India GDP growth,
- global GDP,
- manufacturing/industry indicators.

| Metric | Status | Indicator Code | Earliest | Latest | Frequency | Unit | Ready |
|---|---|---|---|---|---|---|---|
| China GDP Growth | 🟡 | TBD | TBD | TBD | Annual | % | No |
| India GDP Growth | 🟡 | TBD | TBD | TBD | Annual | % | No |
| Global GDP Growth | 🟡 | TBD | TBD | TBD | Annual | % | No |
| China Manufacturing/Industry | 🟡 | TBD | TBD | TBD | TBD | TBD | No |

### 6.2 FRED

Candidate metrics:
- broad USD index,
- real yields,
- Treasury yields,
- CPI/inflation,
- natural-gas price if used.

| Metric | Status | Series ID | Earliest | Latest | Frequency | Unit | Ready |
|---|---|---|---|---|---|---|---|
| USD Strength | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Real Yield | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Treasury Yield | 🟡 | TBD | TBD | TBD | Daily | % | No |
| US Inflation | 🟡 | TBD | TBD | TBD | Monthly | % | No |
| Natural Gas Price | 🟡 | TBD | TBD | TBD | TBD | TBD | No |

### 6.3 UN Comtrade

Candidate metrics:
- China coal imports,
- India coal imports,
- China nickel imports,
- China copper imports.

| Metric | Status | HS Code | Reporter | Partner | Earliest | Latest | Frequency | Unit | Ready |
|---|---|---|---|---|---|---|---|---|---|
| China Coal Imports | 🟡 | TBD | China | World | TBD | TBD | TBD | TBD | No |
| India Coal Imports | 🟡 | TBD | India | World | TBD | TBD | TBD | TBD | No |
| China Nickel Imports | 🟡 | TBD | China | World | TBD | TBD | TBD | TBD | No |
| China Copper Imports | 🟡 | TBD | China | World | TBD | TBD | TBD | TBD | No |

Important:
- validate HS-code version,
- validate whether value or quantity is more useful,
- avoid mixing ores, concentrates, refined products, and downstream products without explicit classification.

### 6.4 EIA

Candidate metrics:
- coal consumption,
- electricity demand,
- natural-gas prices,
- renewable generation.

| Metric | Status | Series/API Route | Geography | Earliest | Latest | Frequency | Ready |
|---|---|---|---|---|---|---|---|
| Coal Consumption | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Electricity Demand | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Natural Gas Price | 🟡 | TBD | TBD | TBD | TBD | TBD | No |
| Renewable Generation | 🟡 | TBD | TBD | TBD | TBD | TBD | No |

### 6.5 IEA

Candidate metrics:
- EV sales,
- battery demand,
- battery chemistry,
- grid investment,
- renewable capacity.

| Metric | Status | Dataset | Earliest | Latest | Frequency | Access | Ready |
|---|---|---|---|---|---|---|---|
| EV Sales | 🟡 | TBD | TBD | TBD | Annual? | Validate | No |
| Battery Demand | 🟡 | TBD | TBD | TBD | Annual? | Validate | No |
| Battery Chemistry | 🟡 | TBD | TBD | TBD | Annual? | Validate | No |
| Grid Investment | 🟡 | TBD | TBD | TBD | Annual? | Validate | No |
| Renewable Capacity | 🟡 | TBD | TBD | TBD | Annual? | Validate | No |

---

## 7. High-Priority Data Gaps

| Gap | Commodity | Priority | Candidate Source | Blocking MVP? |
|---|---|---|---|---|
| Stainless-steel production | Nickel | High | external industry data | No |
| Copper inventory | Copper | High | exchange/market source | No |
| Central-bank gold purchases | Gold | Medium | WGC/IMF | No |
| Detailed coal demand | Coal | Medium | EIA/Comtrade | No |
| Battery chemistry | Nickel | Medium | IEA | No |
| Grid investment | Copper | Medium | IEA/external | No |
| Geopolitical risk | All | Low | GDELT/index | No |

No unresolved gap should block the MVP unless it is promoted to a core scoring requirement.

---

## 8. Historical Depth Requirements

Minimum suggested thresholds:

### Descriptive Metrics
At least 3 observations where meaningful.

### Growth / Stability
Prefer at least 5 annual observations.

### Correlation / Regression
Prefer at least 30 aligned observations.

### Rolling Regression
Prefer enough observations for:
- a meaningful estimation window,
- multiple rolling windows,
- out-of-sample validation.

If history is insufficient, downgrade the method rather than forcing a model.

---

## 9. Frequency Alignment Rules

Avoid mixing raw daily/monthly/annual data directly.

Candidate hierarchy:

- daily → monthly aggregation where necessary,
- monthly → monthly,
- quarterly → quarterly,
- annual → annual.

Annual supply data should not be naively forward-filled and treated as monthly new information without an explicit methodology.

---

## 10. Unit Normalization Rules

For every metric retain:

- original value,
- original unit,
- normalized value,
- normalized unit,
- conversion method.

Examples:
- tonnes vs kilotonnes,
- USD vs IDR,
- millions vs absolute units.

No silent conversion.

---

## 11. Missing-Data Rules

Do not:
- convert missing to zero,
- interpolate structural data by default,
- forward-fill indefinitely.

Allowed only when documented:
- short-gap interpolation for suitable time series,
- nearest-period alignment,
- proxy substitution.

Any proxy must lower confidence.

---

## 12. API-Cost Audit

Because Sectors credits are limited, record:

- endpoint cost,
- number of companies,
- number of periods,
- number of commodities,
- expected refresh frequency.

Estimate total:
- initial backfill cost,
- demo refresh cost,
- daily development cost.

Use caching and local snapshots wherever allowed.

---

## 13. Definition of Analytics-Ready

A metric is `analytics_ready = Yes` only if:

1. source is confirmed,
2. endpoint is confirmed,
3. unit is known,
4. frequency is known,
5. historical depth is sufficient,
6. missingness is acceptable or handled,
7. transformation is defined,
8. license/use is acceptable,
9. source can be reproduced.

---

## 14. Audit Workflow

```text
Metric from Data Dictionary
→ Find Endpoint
→ Fetch Real Sample
→ Validate Schema
→ Check History
→ Check Missingness
→ Normalize Units
→ Estimate API Cost
→ Mark Confidence
→ Mark Analytics Ready
```

---

## 15. Definition of Done

The audit is complete enough for quant modeling when:

- all core commodity metrics are resolved,
- all core company metrics are resolved,
- historical depth is known,
- units are known,
- missingness is quantified,
- unresolved gaps have fallbacks,
- expected API cost is known,
- every core metric has an analytics-ready status.
