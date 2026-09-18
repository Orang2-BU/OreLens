# OreLens Data Dictionary v0.1

## Purpose

Dokumen ini mendefinisikan metric untuk Commodity Intelligence, Company Intelligence, Exposure Analysis, Resilience Analysis, Fundamental Analysis, dan Scenario Analysis.

Scope MVP: **Coal, Gold, Nickel, Copper**. Bobot belum ditentukan.

```text
Literature → Candidate Metric → Data Availability → Usable Metric
→ Historical Testing → Metric Importance → Current Market Regime
→ Final OreLens Intelligence
```

## A. Commodity Intelligence Engine

Commodity Engine mencakup Physical Supply, Physical Demand, Structural Demand, Macro Sensitivity, dan Event/Policy Context.

### Shared metrics

| Metric | Category | Source | Frequency | Transformation | Priority |
|---|---|---|---|---|---|
| Commodity Price | Market | Sectors | Monthly/available | Return, rolling return | CORE |
| Global Production | Supply | Sectors | Annual | YoY growth | CORE |
| Production Share | Supply | Sectors | Annual | Share, HHI | CORE |
| Global Resources/Reserves | Supply | Sectors | Annual/static | Share, concentration | CORE |
| Export Value | Trade | Sectors | Annual | YoY growth | CORE |
| Import Value | Demand | Sectors | Annual | YoY growth | CORE |
| Trade Concentration | Demand | Derived | Annual | HHI | CORE |
| Indonesian Production | Supply | Sectors | Annual | YoY growth | CORE |
| Export Destination | Demand | Sectors | Annual | Country share, HHI | CORE |
| USD Strength | Macro | FRED | Daily/monthly | Return, rolling change | CORE |
| Global GDP Growth | Macro | World Bank/IMF | Annual | YoY | SUPPORT |
| China GDP Growth | Macro | World Bank | Quarterly/annual | YoY | CORE for Coal/Nickel/Copper |
| China Industrial Activity | Demand | OECD/external | Monthly | YoY, z-score | CORE for Nickel/Copper |
| Geopolitical/Event Signal | Event | GDELT/news | Daily | Count, classification | OPTIONAL |

Sectors menjadi sumber utama production, production share, resources/reserves, dan trade data.

## B. Commodity-specific metrics

### Coal

Supply: Indonesia production, global production, Indonesia production share, coal reserve share, coal export value, production concentration.

Demand: China imports, India imports, China GDP, India GDP, electricity demand, coal consumption.

Structural/substitution: Natural gas price, renewable generation, energy transition trend.

Source: Sectors, UN Comtrade, World Bank, EIA/FRED, dan IEA. Energy transition trend bersifat optional.

### Gold

Supply: Global production, Indonesia production, global reserves, production concentration.

Financial demand/macro: Real interest rate, US Treasury yield, USD strength, US inflation, central bank gold demand, investment demand, geopolitical risk.

Source: Sectors, FRED, WGC/IMF/ECB, dan GDELT. Central bank demand, investment demand, dan geopolitical risk bersifat support/optional.

### Nickel

Supply: Indonesia production, global production, Indonesia production share, reserves, export value, production concentration.

Physical demand: China imports, China industrial activity, China GDP, stainless steel demand proxy.

Structural demand: EV battery demand, EV sales, battery chemistry share.

Source: Sectors, UN Comtrade, World Bank, OECD/external, dan IEA. Stainless steel production adalah high-priority data gap; battery chemistry share bersifat support.

### Copper

Supply: Global production, Indonesia production, reserves, production concentration, export value, inventory.

Demand: China imports, China industrial activity, China GDP, global manufacturing activity.

Structural demand: Grid investment, EV deployment, renewable capacity.

Inventory adalah high-priority data gap. Grid investment dan renewable capacity masih support/optional.

## C. World Bank macro metrics

| Metric | Commodity | Country | Priority |
|---|---|---|---|
| GDP Growth | Coal/Nickel/Copper | China | YES |
| GDP Growth | Coal | India | YES |
| Industrial Value Added | Nickel/Copper | China | SUPPORT |
| Manufacturing Value Added | Nickel/Copper | China | SUPPORT |
| Inflation | All | US/China | SUPPORT |

Indicator IDs dikunci setelah backend memverifikasi kode indikator yang benar.

## D. Company Intelligence Engine

Sectors menjadi sumber utama company list/detail, performance, financials, mining sites, production, resources/reserves, trade, dan sales destination.

### Company identity and operations

Commodity type, production volume, sales volume, production growth, sales growth, resources, reserves, reserve coverage, mining site count, site production concentration, license status, dan license expiry.

### Company commodity exposure

| Metric | Transformation | Role | MVP |
|---|---|---|---|
| Commodity Revenue Share | Percentage | Exposure | Yes if available |
| Production Dependency | Percentage | Exposure | YES |
| Sales Dependency | Percentage | Exposure | YES |
| Geographic Sales Concentration | HHI | Exposure/resilience | YES |
| Top Destination Share | Percentage | Exposure | YES |
| Operational Concentration | HHI | Exposure | YES |
| Commodity Beta | Regression beta | Historical sensitivity | SUPPORT |

Jika Commodity Revenue Share tidak tersedia, gunakan Production Dependency, Sales Dependency, dan company commodity classification dengan confidence lebih rendah. Missing value tidak boleh diubah menjadi nol.

### Company fundamentals

Revenue, revenue growth, net income, net income growth, ROE, ROA, net margin, DER, debt/assets, PE, PB, dan market cap. Revenue, growth, profitability, leverage, PE, dan PB adalah MVP; ROA, debt/assets, dan market cap bersifat support.

## E. Resilience metrics

Resilience bukan inverse dari exposure. Kandidatnya adalah reserve coverage, production stability, site diversification, sales diversification, revenue growth, profitability, leverage, license context, commodity diversification, liquidity, dan cash position.

## F. Derived metrics

```text
HHI = Σ share_i²
Reserve Coverage = Company Reserves / Annual Production
YoY Growth = (Current - Previous) / Previous
Company Return_t = α + β Commodity Return_t + ε
```

HHI digunakan untuk production, destination, site, dan country supply concentration. Reserve coverage adalah indikator komparatif, bukan literal mine life. Commodity beta menunjukkan historical sensitivity, bukan forecast.

## G. Transformation dan peer rules

Gunakan YoY %, rolling return, z-score, peer percentile, HHI, log transform, dan standardized beta sesuai kebutuhan metric.

Jangan membandingkan metric mentah antar-komoditas yang tidak sebanding. Gunakan peer group terpisah untuk Coal, Gold, Nickel, dan Copper. Exposure multi-komoditas dihitung terpisah per komoditas.

## H. Data confidence

```text
HIGH        Direct structured data
MEDIUM      Derived from complete structured data
LOW         Proxy or partial coverage
UNAVAILABLE Insufficient data
```

Missing tidak boleh disamakan dengan zero.

## I. Data source priority

1. Sectors — core mining dan company data.
2. World Bank, FRED, UN Comtrade, EIA, IEA — macro dan demand context.
3. Derived OreLens metrics.
4. GDELT atau sumber event context lain.

## J. MVP metric priority

### Must have — commodity

Commodity price, production, production growth, production share, resources/reserves, trade, import/export demand, USD, dan major consumer GDP/activity.

### Must have — company

Production, sales, reserves, reserve coverage, sales destination, operational concentration, revenue, revenue growth, net income, ROE, DER, PE, dan PB.

### Phase 2

Commodity beta, battery chemistry, grid investment, geopolitical risk, central bank gold demand, inventory, dan detailed policy events.

## K. Remaining data gaps

| Metric | Commodity | Candidate source | Problem |
|---|---|---|---|
| Stainless Steel Production | Nickel | External industry data | Free reliable API perlu divalidasi |
| Copper Inventory | Copper | Exchange/market source | Free historical series perlu divalidasi |
| Central Bank Gold Purchases | Gold | WGC/IMF | Access dan frequency perlu divalidasi |
| Detailed coal demand | Coal | EIA/Comtrade/external | Series yang tepat perlu ditentukan |
| Battery Chemistry Share | Nickel | IEA | Annual dan API tidak sederhana |
| Grid Investment | Copper | IEA/external | Ekstraksi data kompleks |
| Geopolitical Risk | Gold/all | GDELT/index | Methodology perlu divalidasi |

Gap ini tidak boleh memblokir MVP.

## L. Data audit fields

```text
metric_id, metric_name, source, source_endpoint, commodity, country,
unit, frequency, earliest_date, latest_date, observation_count,
missing_count, missing_rate, last_updated, api_cost, license
```

Audit wajib diselesaikan sebelum quantitative weighting dimulai.

## M. Quant research pipeline

```text
Data Collection → Align Frequency → Missing Data Check → Transformation
→ Correlation Screening → Multivariate Regression → Rolling Regression
→ Regime Comparison → Backtest → Driver Importance
```

Dynamic weight hanya ditentukan setelah pipeline ini selesai.

## N. Definition of done

Data Dictionary siap untuk Data Availability Audit ketika metric list Coal, Gold, Nickel, dan Copper sudah dikunci; company metrics sudah dikunci; setiap metric memiliki source, frequency, unit, economic meaning, transformation, priority; dan remaining gaps terdokumentasi.

Tahap berikutnya adalah mengambil sample response dari setiap API dan mengisi earliest date, latest date, actual frequency, actual unit, missing rate, coverage, dan API cost. Scoring dilakukan setelah bentuk dataset nyata diketahui.
