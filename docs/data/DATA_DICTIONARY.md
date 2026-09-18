# OreLens Data Dictionary v0.1

## Purpose

Dokumen ini mendefinisikan metric yang akan digunakan OreLens untuk:

- Commodity Intelligence Engine
- Company Intelligence Engine
- Exposure Analysis
- Resilience Analysis
- Fundamental Analysis
- Scenario Analysis

Scope MVP commodity:

```text
Coal
Gold
Nickel
Copper
```

Prinsip utama:

```text
Literature
    ↓
Candidate Metric

Data Availability
    ↓
Usable Metric

Historical Testing
    ↓
Metric Importance

Current Market Regime
    ↓
Final OreLens Intelligence
```

Bobot belum ditentukan pada tahap ini.

---

# A. Commodity Intelligence Engine

Commodity Engine dibagi menjadi:

```text
1. Physical Supply
2. Physical Demand
3. Structural Demand
4. Macro Sensitivity
5. Event / Policy Context
```

---

# A1. Metrics Bersama untuk Semua Commodity

| Metric | Category | Definition | Primary Source | Frequency | Transformation | Expected Interpretation | Priority |
|---|---|---|---|---|---|---|---|
| Commodity Price | Market | Historical commodity price | Sectors | Monthly / available interval | Return %, rolling return | Dependent/reference variable utama | CORE |
| Global Production | Supply | Total production per country | Sectors | Annual | YoY growth | Supply growth dapat memberi pressure pada harga | CORE |
| Production Share | Supply | Share produksi global per country | Sectors | Annual | %, HHI | Concentrated supply → higher disruption sensitivity | CORE |
| Global Resources / Reserves | Supply | Resources/reserves by country | Sectors | Annual/static updates | Share %, concentration | Supply capacity jangka panjang | CORE |
| Export Value | Trade | Export commodity per country | Sectors | Annual | YoY growth | Proxy supply availability / trade activity | CORE |
| Import Value | Demand | Import commodity per country | Sectors | Annual | YoY growth | Proxy commodity demand | CORE |
| Trade Concentration | Demand | Concentration of import/export markets | Derived from Sectors | Annual | HHI | Dependence pada sedikit market | CORE |
| Indonesian Production | Supply | Production commodity Indonesia | Sectors | Annual | YoY growth | Indonesia supply contribution | CORE |
| Export Destination | Demand | Destination of Indonesian commodity exports | Sectors | Annual | country share / HHI | Country-demand dependency | CORE |
| USD Strength | Macro | Broad USD movement / dollar index | FRED | Daily/Monthly | return / rolling change | Strong USD historically pressures many USD-priced commodities | CORE |
| Global GDP Growth | Macro | Global economic growth | World Bank / IMF | Annual | YoY | Broad cyclical demand proxy | SUPPORT |
| China GDP Growth | Macro | China economic growth | World Bank | Quarterly/Annual depending source | YoY | Major demand proxy for industrial commodities | CORE for Coal/Nickel/Copper |
| China Industrial Activity | Demand | Industrial/manufacturing activity | OECD / external | Monthly | YoY / z-score | Industrial commodity demand proxy | CORE for Nickel/Copper |
| Geopolitical/Event Signal | Event | Relevant supply/trade disruptions | GDELT / news | Daily | event count / classification | Context, not direct deterministic score | OPTIONAL |

Sectors' global commodity endpoint directly provides production, production share, resources/reserves, and trade data for Coal, Gold, Nickel, Copper, and Bauxite.

---

# B. Coal Data Dictionary

## B1. Coal Supply

| Metric | Definition | Source | Frequency | Transformation | Expected Direction | MVP |
|---|---|---|---|---|---|---|
| Indonesia Coal Production | National production | Sectors | Annual | YoY % | Higher supply → downward pressure, ceteris paribus | YES |
| Global Coal Production | Global/country production | Sectors | Annual | YoY % | Higher supply → downward pressure | YES |
| Indonesia Global Production Share | Indonesia share of global supply | Sectors | Annual | % | Higher concentration increases Indonesia relevance | YES |
| Coal Reserve Share | Reserve concentration by country | Sectors | Annual | % / HHI | Higher concentration → supply concentration risk | YES |
| Coal Export Value | Country coal exports | Sectors | Annual | YoY | Higher exports → supply availability | YES |
| Production Concentration | Concentration of global production | Derived | Annual | HHI | High concentration → disruption sensitivity | YES |

## B2. Coal Demand

| Metric | Definition | Source | Frequency | Transformation | Expected Direction | MVP |
|---|---|---|---|---|---|---|
| China Coal Imports | Coal import demand China | UN Comtrade | Monthly/Annual | YoY | Higher imports → demand support | YES |
| India Coal Imports | Coal import demand India | UN Comtrade | Monthly/Annual | YoY | Higher imports → demand support | YES |
| China GDP | China economic activity | World Bank | Annual | YoY | Higher activity generally supportive | YES |
| India GDP | India economic activity | World Bank | Annual | YoY | Higher activity generally supportive | SUPPORT |
| Electricity Demand | Power demand | EIA / external | Monthly/Annual | YoY | Higher electricity demand can support coal demand | YES |
| Coal Consumption | Actual coal consumption | EIA / external | Annual/Monthly depending geography | YoY | Direct demand proxy | YES |

## B3. Coal Structural / Substitution

| Metric | Definition | Source | Frequency | Transformation | Expected Direction | MVP |
|---|---|---|---|---|---|---|
| Natural Gas Price | Competing fuel price | EIA / FRED | Daily/Monthly | return | Higher gas price may support coal substitution | YES |
| Renewable Generation | Renewable electricity output | EIA / external | Monthly/Annual | YoY/share | Higher renewable share may reduce coal demand | SUPPORT |
| Energy Transition Trend | Long-term energy mix change | IEA | Annual | trend | Structural headwind/support context | OPTIONAL |

---

# C. Gold Data Dictionary

Gold membutuhkan framework berbeda karena demand finansial lebih penting dibanding industrial demand.

## C1. Gold Supply

| Metric | Definition | Source | Frequency | Transformation | Expected Direction | MVP |
|---|---|---|---|---|---|---|
| Global Gold Production | Mine production | Sectors | Annual | YoY | Higher supply → potential downward pressure | YES |
| Indonesia Gold Production | Indonesian production | Sectors | Annual | YoY | Local supply context | YES |
| Global Gold Reserves | Reserve distribution | Sectors | Annual | share / HHI | Long-term supply structure | YES |
| Production Concentration | Global mine concentration | Derived | Annual | HHI | Supply disruption sensitivity | YES |

## C2. Gold Financial Demand / Macro

| Metric | Definition | Source | Frequency | Transformation | Expected Direction | MVP |
|---|---|---|---|---|---|---|
| Real Interest Rate | Inflation-adjusted yield | FRED | Daily/Monthly | level / Δ | Higher real yield historically negative for gold | YES |
| US Treasury Yield | Nominal yield | FRED | Daily | Δ / rolling avg | Higher yields generally opportunity-cost headwind | YES |
| USD Strength | Broad dollar strength | FRED | Daily/Monthly | return | Stronger USD generally negative pressure | YES |
| US Inflation | CPI/inflation | FRED | Monthly | YoY | Inflation can increase gold demand depending regime | YES |
| Central Bank Gold Demand | Central-bank purchases | WGC/IMF/ECB | Monthly/Quarterly | net purchases | Higher purchases → demand support | SUPPORT |
| Investment Demand | ETF/investor flows | WGC / external | Monthly | flows | Higher flows → demand support | OPTIONAL |
| Geopolitical Risk | Crisis/conflict context | GDELT / external index | Daily/Monthly | z-score | Can increase safe-haven demand | OPTIONAL |

FRED provides programmatic historical economic time series and supports retrieving complete observations; API access requires a free key.

---

# D. Nickel Data Dictionary

## D1. Nickel Supply

| Metric | Definition | Source | Frequency | Transformation | Expected Direction | MVP |
|---|---|---|---|---|---|---|
| Indonesia Nickel Production | Indonesia mine output | Sectors | Annual | YoY | Higher production → supply pressure | YES |
| Global Nickel Production | Country/global production | Sectors | Annual | YoY | Higher supply → downward pressure | YES |
| Indonesia Production Share | Global nickel supply share | Sectors | Annual | % | Indicates Indonesia market power/supply concentration | YES |
| Nickel Reserves | Global reserve distribution | Sectors | Annual | share / HHI | Long-term supply capacity | YES |
| Nickel Export Value | Export activity | Sectors | Annual | YoY | Supply/trade proxy | YES |
| Production Concentration | Country concentration | Derived | Annual | HHI | High concentration → policy/disruption sensitivity | YES |

## D2. Nickel Physical Demand

| Metric | Definition | Source | Frequency | Transformation | Expected Direction | MVP |
|---|---|---|---|---|---|---|
| China Nickel Imports | China nickel import demand | UN Comtrade | Monthly/Annual | YoY | Higher imports → demand support | YES |
| China Industrial Activity | Industry/manufacturing proxy | OECD / external | Monthly | YoY / z-score | Higher activity → demand support | YES |
| China GDP | Broad China demand context | World Bank | Annual | YoY | Higher growth → demand support | YES |
| Stainless Steel Demand Proxy | Stainless steel production/output | external source | Monthly/Annual | YoY | Higher production → nickel demand support | HIGH PRIORITY GAP |

## D3. Nickel Structural Demand

| Metric | Definition | Source | Frequency | Transformation | Expected Direction | MVP |
|---|---|---|---|---|---|---|
| EV Battery Demand | Battery deployment/demand | IEA | Annual | YoY | Higher battery demand can support nickel demand | YES |
| EV Sales | Global/China EV sales | IEA | Annual | YoY | Structural battery-demand proxy | YES |
| Battery Chemistry Share | NMC/NCA vs LFP | IEA / external | Annual | market share | Higher nickel-bearing chemistry → nickel demand support | SUPPORT |

IEA's Global EV data provides downloadable historical/projected EV and battery-demand data, with its current dataset licensed CC BY 4.0.

---

# E. Copper Data Dictionary

## E1. Copper Supply

| Metric | Definition | Source | Frequency | Transformation | Expected Direction | MVP |
|---|---|---|---|---|---|---|
| Global Copper Production | Mine production | Sectors | Annual | YoY | Higher supply → downward pressure | YES |
| Indonesia Copper Production | Indonesia mine production | Sectors | Annual | YoY | Local supply contribution | YES |
| Copper Reserves | Reserve distribution | Sectors | Annual | share | Long-run capacity | YES |
| Production Concentration | Country production concentration | Derived | Annual | HHI | Supply disruption sensitivity | YES |
| Copper Export Value | Export activity | Sectors | Annual | YoY | Trade/supply proxy | YES |
| Inventory | Exchange/refined copper inventory | external | Daily/Weekly | Δ / days supply | Rising inventory usually demand/supply imbalance signal | HIGH PRIORITY GAP |

## E2. Copper Demand

| Metric | Definition | Source | Frequency | Transformation | Expected Direction | MVP |
|---|---|---|---|---|---|---|
| China Copper Imports | Copper import demand China | UN Comtrade | Monthly/Annual | YoY | Higher imports → demand support | YES |
| China Industrial Activity | Industrial production/manufacturing | OECD / external | Monthly | YoY | Higher activity → copper demand support | YES |
| China GDP | Economic growth | World Bank | Annual | YoY | Higher growth generally supportive | YES |
| Global Manufacturing Activity | Global industrial cycle | external/OECD | Monthly | index / Δ | Higher manufacturing → demand support | SUPPORT |

## E3. Copper Structural Demand

| Metric | Definition | Source | Frequency | Transformation | Expected Direction | MVP |
|---|---|---|---|---|---|---|
| Grid Investment | Electricity network expansion | IEA / external | Annual | YoY | Higher investment → copper demand support | SUPPORT |
| EV Deployment | EV deployment | IEA | Annual | YoY | Electrification demand proxy | SUPPORT |
| Renewable Capacity | Renewable installations | IEA / external | Annual | YoY | Structural copper demand | OPTIONAL |

---

# F. World Bank Macro Metrics

World Bank Indicators API gives programmatic access to almost 16,000 series, many with more than 50 years of history, and does not require authentication.

Candidate metrics:

| Metric | Commodity | Country | Source | Frequency | MVP |
|---|---|---|---|---|---|
| GDP Growth | Coal/Nickel/Copper | China | World Bank | Annual | YES |
| GDP Growth | Coal | India | World Bank | Annual | YES |
| Industrial Value Added | Nickel/Copper | China | World Bank | Annual | SUPPORT |
| Manufacturing Value Added | Nickel/Copper | China | World Bank | Annual | SUPPORT |
| Inflation | All | US / China | World Bank/FRED | Annual/Monthly | SUPPORT |

World Bank metric IDs should be locked only after backend verifies the exact indicator code being used.

---

# G. Company Intelligence Engine

Company Engine applies across Coal, Gold, Nickel, and Copper.

Sectors v2 exposes mining company endpoints including company list/detail, company performance, company financials, mining sites, production, resources/reserves, trade and sales destination.

---

# G1. Company Identity & Operations

| Metric | Definition | Source | Frequency | Transformation | Role |
|---|---|---|---|---|---|
| Commodity Type | Company's mining commodity | Sectors | Static/update | categorical | Company universe |
| Production Volume | Company production | Sectors | Annual | YoY | Exposure + Operations |
| Sales Volume | Company sales output | Sectors | Annual | YoY | Exposure |
| Production Growth | Production trend | Derived | Annual | YoY | Operational health |
| Sales Growth | Sales volume trend | Derived | Annual | YoY | Operational health |
| Resources | Company resources | Sectors | Annual | raw/normalized | Resilience |
| Reserves | Company reserves | Sectors | Annual | raw/normalized | Resilience |
| Reserve Coverage | Reserve / annual production | Derived | Annual | ratio | Resilience |
| Mining Site Count | Number of operating sites | Sectors | Update-based | count | Diversification |
| Site Production Concentration | Production distribution across sites | Derived | Annual | HHI | Operational concentration |
| License Status | Mining permit status | Sectors | Update-based | categorical | Operational context |
| License Expiry | Permit expiry profile | Sectors | Update-based | years remaining | Operational context |

---

# G2. Company Commodity Exposure

| Metric | Definition | Source | Frequency | Transformation | Role | MVP |
|---|---|---|---|---|---|---|
| Commodity Revenue Share | Revenue attributable to commodity / total revenue | Sectors Segment Data | Annual | % | Exposure | YES if available |
| Production Dependency | Commodity production / total mining production | Sectors | Annual | % | Exposure | YES |
| Sales Dependency | Commodity sales / total commodity sales | Sectors | Annual | % | Exposure | YES |
| Geographic Sales Concentration | Sales concentration by destination | Sectors | Annual | HHI | Exposure / Resilience | YES |
| Top Destination Share | Largest country share | Sectors | Annual | % | Exposure | YES |
| Operational Concentration | Production concentration across mining sites | Derived | Annual | HHI | Exposure | YES |
| Commodity Beta | Historical company-return sensitivity to commodity price | Sectors stock + commodity price | Monthly | regression beta | Historical sensitivity | SUPPORT |

Revenue segment coverage must be checked per listed company because segment data is only available for companies/years included in Sectors' segment dataset.

Fallback rule:

```text
If Commodity Revenue Share unavailable:

do NOT set value = 0.

Use:
Production Dependency
+
Sales Dependency
+
Company commodity classification

and reduce confidence level.
```

---

# G3. Company Fundamental Profile

| Metric | Category | Definition | Source | Frequency | Transformation | MVP |
|---|---|---|---|---|---|---|
| Revenue | Growth | Company revenue | Sectors | Quarterly/Annual | YoY | YES |
| Revenue Growth | Growth | Growth in revenue | Derived | Quarterly/Annual | YoY | YES |
| Net Income | Growth | Net profit | Sectors | Quarterly/Annual | YoY | YES |
| Net Income Growth | Growth | Profit growth | Derived | Quarterly/Annual | YoY | YES |
| ROE | Profitability | Net income / equity | Sectors | Quarterly/Annual | percentile | YES |
| ROA | Profitability | Net income / assets | Sectors | Quarterly/Annual | percentile | SUPPORT |
| Net Margin | Profitability | Net income / revenue | Derived/Sectors | Quarterly/Annual | % | YES |
| DER | Leverage | Debt / equity | Sectors | Quarterly/Annual | percentile | YES |
| Debt / Asset | Leverage | Debt/assets | Sectors | Quarterly/Annual | % | SUPPORT |
| PE | Valuation | Price / earnings | Sectors | Current/periodic | peer percentile | YES |
| PB | Valuation | Price / book | Sectors | Current/periodic | peer percentile | YES |
| Market Cap | Market | Company valuation size | Sectors | Daily/current | log / percentile | SUPPORT |

Sectors' company dataset exposes sortable metrics including market cap, revenue, earnings, PB and PE.

---

# H. Company Resilience Metrics

Resilience is **not** the inverse of exposure.

A company can be:

```text
High Exposure
+
High Resilience
```

or:

```text
High Exposure
+
Low Resilience
```

Candidate Resilience Metrics:

| Metric | Why it matters | Calculation | MVP |
|---|---|---|---|
| Reserve Coverage | Ability to sustain production | reserves / production | YES |
| Production Stability | Operational consistency | volatility of production growth | YES |
| Site Diversification | Reduces single-site dependency | site HHI / count | YES |
| Sales Diversification | Reduces destination dependency | destination HHI | YES |
| Revenue Growth | Business momentum | YoY revenue | YES |
| Profitability | Ability to absorb commodity pressure | ROE / margin | YES |
| Leverage | Debt vulnerability | DER | YES |
| License Context | Operational continuity | status/expiry | YES |
| Commodity Diversification | Dependence on one commodity | commodity shares | SUPPORT |
| Liquidity / Cash Position | Ability to withstand downturn | cash/debt/current metrics | SUPPORT |

---

# I. Derived Metrics

These metrics are calculated internally by OreLens.

## I1. HHI Concentration

Used for:

```text
Production concentration
Sales destination concentration
Site concentration
Country supply concentration
```

Formula:

```text
HHI = Σ share_i²
```

Interpretation:

```text
Low HHI
→ diversified

High HHI
→ concentrated
```

---

## I2. Reserve Coverage

```text
Reserve Coverage =
Company Reserves
/
Annual Production
```

Important:

This is **not** literal mine life.

It is used only as a standardized comparative indicator.

---

## I3. Growth Metrics

```text
YoY Growth =
(Current - Previous)
/
Previous
```

Applicable to:

```text
Production
Sales
Revenue
Net Income
Imports
Exports
Commodity Demand
```

---

## I4. Commodity Beta

Historical relationship:

```text
Company Return_t =
α
+
β Commodity Return_t
+
ε
```

Output:

```text
β Commodity
```

Interpretation:

```text
Higher β
→ historically greater price sensitivity
```

This is historical sensitivity, **not a forecast**.

---

# J. Transformation Rules

OreLens should avoid comparing raw values directly across companies.

Preferred normalization:

```text
Peer Percentile
```

Example:

```text
Company Reserve Coverage:
8.4

Coal peer percentile:
82nd
```

This becomes more meaningful than comparing raw reserve values across commodities.

Other candidate transforms:

| Transformation | Use |
|---|---|
| YoY % | growth metrics |
| Rolling return | commodity prices |
| Z-score | anomaly/current regime |
| Percentile | company comparison |
| HHI | concentration |
| Log transform | highly skewed metrics |
| Standardized β | historical driver importance |

---

# K. Peer Group Rule

Never compare raw mining metrics across unrelated commodities.

```text
Coal company
→ Coal peers

Gold company
→ Gold peers

Nickel company
→ Nickel peers

Copper company
→ Copper peers
```

For companies exposed to multiple OreLens commodities:

```text
calculate commodity-specific exposure separately.
```

Example:

```text
Company X

Gold Exposure
72

Copper Exposure
48
```

Do not prematurely combine them into one generic exposure score.

---

# L. Data Confidence

Every metric should carry a confidence state.

```text
HIGH
Direct structured data

MEDIUM
Derived from complete structured data

LOW
Proxy / partial coverage

UNAVAILABLE
Insufficient data
```

Example:

```text
Commodity Revenue Dependency
Unavailable

Production Dependency
High Confidence
```

Never:

```text
missing = zero
```

---

# M. Data Source Priority

OreLens data hierarchy:

```text
1. Sectors
   Core mining + company data

2. Official international APIs
   World Bank
   FRED
   UN Comtrade
   EIA
   IEA

3. Derived OreLens Metrics

4. News/Event Context
   GDELT / other contextual data
```

Sectors remains the core data provider.

External sources enrich macro/demand context.

---

# N. MVP Metric Priority

## Must Have — Commodity

```text
Commodity Price
Production
Production Growth
Production Share
Resources / Reserves
Trade
Import / Export Demand
USD
Major Consumer GDP / Activity
```

## Must Have — Company

```text
Production
Sales
Reserves
Reserve Coverage
Sales Destination
Operational Concentration
Revenue
Revenue Growth
Net Income
ROE
DER
PE
PB
```

## Phase 2

```text
Commodity Beta
Battery Chemistry
Grid Investment
Geopolitical Risk
Central Bank Gold Demand
Inventory
Detailed Policy Events
```

---

# O. Remaining Data Gaps

Current high-priority gaps requiring validation:

| Metric | Commodity | Candidate Source | Problem |
|---|---|---|---|
| Stainless Steel Production | Nickel | external industry data | Need free reliable API |
| Copper Inventory | Copper | exchange/market source | Need free reliable history |
| Central Bank Gold Purchases | Gold | WGC/IMF | Access/update frequency |
| India/China detailed coal demand | Coal | EIA/Comtrade/external | Need exact series |
| Battery Chemistry Share | Nickel | IEA | likely annual, not API-friendly |
| Grid Investment | Copper | IEA/external | annual / data extraction complexity |
| Geopolitical Risk | Gold/all | GDELT/index | methodology needs validation |

These gaps should **not block MVP**.

---

# P. Data Audit Fields

Backend should record this metadata for every series:

```text
metric_id
metric_name
source
source_endpoint
commodity
country
unit
frequency
earliest_date
latest_date
observation_count
missing_count
missing_rate
last_updated
api_cost
license
```

Example:

```text
metric_id:
nickel_indonesia_production

source:
Sectors

frequency:
annual

unit:
ton

earliest_date:
TBD

latest_date:
2025

missing_rate:
TBD
```

This audit must be completed before quantitative weighting begins.

---

# Q. Quant Research Pipeline

After Data Dictionary and Data Audit are complete:

```text
DATA COLLECTION
      ↓
ALIGN FREQUENCY
      ↓
MISSING DATA CHECK
      ↓
TRANSFORMATION
      ↓
CORRELATION SCREENING
      ↓
MULTIVARIATE REGRESSION
      ↓
ROLLING REGRESSION
      ↓
REGIME COMPARISON
      ↓
BACKTEST
      ↓
DRIVER IMPORTANCE
```

Only after this pipeline do we assign dynamic weight.

---

# R. Final OreLens Model

```text
                         ORELENS

                 COMMODITY ENGINE
                         │
     ┌──────────────┬────┴────┬──────────────┐
     ↓              ↓         ↓              ↓
   Supply        Demand     Macro      Structural Demand
     │              │         │              │
     └──────────────┴────┬────┴──────────────┘
                         ↓
                Commodity Environment
                         │
                         │
                         ↓
                  COMPANY ENGINE
                         │
      ┌──────────────┬───┴─────┬─────────────┐
      ↓              ↓         ↓             ↓
 Operations       Exposure  Resilience   Fundamentals
      │              │         │             │
      └──────────────┴────┬────┴─────────────┘
                          ↓
                 Company Intelligence
                          │
             ┌────────────┴────────────┐
             ↓                         ↓
      Historical Sensitivity      Scenario Engine
             │                         │
             └────────────┬────────────┘
                          ↓
                   OreLens Analysis
                          ↓
                     Evidence
```

---

# Definition of Done — Data Dictionary v0.1

Data Dictionary dianggap siap untuk tahap selanjutnya jika:

```text
Coal     → metric list locked
Gold     → metric list locked
Nickel   → metric list locked
Copper   → metric list locked

Company metrics locked

Every metric has:
source
frequency
unit
economic meaning
transformation
priority

Remaining gaps explicitly documented
```

Setelah itu tahap berikutnya adalah **Data Availability Audit**, bukan scoring.

Backend akan mengambil sample response dari masing-masing API dan kita isi:

```text
earliest date
latest date
actual frequency
actual unit
missing rate
coverage
API cost
```

Setelah kita tahu bentuk real dataset-nya, baru Quant mulai menentukan model historis dan bobot.
