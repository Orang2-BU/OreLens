# OreLens Intelligence — Dummy Data Integration Test Report

Date: 2026-09-21  
Environment: Django test runner, SQLite in-memory test database  
Command:

```text
python manage.py test apps.intelligence apps.analytics.tests_correlation apps.commodities apps.scenarios -v 2
```

## Executive result

The improved intelligence flow passed **30/30 tests**. The test database was created in memory and destroyed after the run, so dummy records did not modify the development database.

```text
Ran 30 tests in 0.557s
OK
System check identified no issues
```

The full backend suite previously passed **60/60 tests** after the same improvement set.

## Dummy data used

### Company intelligence

Company: `ADRO.JK`  
Commodity: `COAL`  
Evidence source: dummy `RawDataLog` with HTTP status `200` and source `Sectors`.

Complete evidence scenario:

| Metric | Dummy value | Unit | Role |
|---|---:|---|---|
| Commodity Revenue Share | 80 | `%` | Exposure |
| Production Dependency | 60 | `%` | Exposure proxy |
| Sales Dependency | 70 | `%` | Exposure proxy |
| Operational Concentration HHI | 0.4 | index | Exposure adjustment |
| Reserve Coverage | 12 | years | Resilience |
| DER | 0.3 | ratio | Resilience |
| EBITDA Margin | 35 | `%` | Resilience |
| Sales Diversification HHI | 0.2 | index | Resilience |

Expected result:

- Exposure score: `80.0`, based on direct revenue share.
- Exposure status: `Pending Validation - preliminary methodology`.
- Resilience score: `100.0` using all four provisional components.
- Resilience status: preliminary, not validated.
- Every observed component contains `evidence_id` and source metadata.

### Partial resilience scenario

Only two resilience inputs were supplied:

- Reserve Coverage: `12 years`.
- EBITDA Margin: `35%`.

Expected result:

- Provisional score remains available: `100.0` after scaling available component points to the four-component range.
- Status contains `partial evidence`.
- Missing DER and Sales Diversification HHI are not converted to zero.

### Seed fallback scenario

No normalized revenue-share evidence was supplied. The dummy company had legacy relational fields:

- `CompanyCommodityExposure.revenue_share_pct = 85`.
- `CompanyResilience.debt_to_equity = 0.3`.
- `CompanyResilience.ebitda_margin = 35`.
- `CompanyResilience.reserve_life_years = 12`.

Expected result:

- Exposure score: `85.0`.
- Exposure status contains `demo fallback`.
- Source is labeled `CompanyCommodityExposure (seeded)`.
- `is_proxy = true` and `evidence_id = null`.
- Seed data is therefore distinguishable from audited evidence.

## Driver map and correlation tests

The tests created dummy `Commodity Price` and `Coal Supply` normalized observations with matching dates and an HTTP-success raw log.

Results:

- Pearson helper for `[1, 2, 3]` and `[2, 4, 6]`: `1.0`.
- Three matched untransformed observations are rejected for screening: `correlation_score = null`, confidence `Low`.
- Twelve aligned, consistently annual, transformed observations produced `correlation_score = 1.0` and confidence `Medium`.
- The calculated driver stored a reference to the latest `NormalizedMetric` through `CommodityDriver.evidence`.
- Driver map does not use seed correlation values as evidence.

The driver map test also verified that:

- observed macro context is shown as `observed_context`;
- missing supply/demand evidence is shown as `unavailable`;
- `importance` remains `null` when no persisted correlation exists;
- no unsupported causal claim is produced.

## Quant readiness tests

The dummy data first contained 12 price and driver records, but six records used `Annual` frequency and six used `Monthly` frequency.

Result:

- Gate status: `blocked`.
- Reason: fewer than 12 observations had a consistent frequency.

After normalizing all records to `Annual`:

- Gate status changed to `ready_for_screening`.

This confirms the gate checks aligned periods/frequency rather than only counting raw rows.

## Scenario run test

Endpoint tested:

```text
POST /api/v1/scenarios/{id}/run/
```

Dummy request:

```json
{
  "metric_name": "China GDP Growth",
  "shock_pct": 10
}
```

The metric had a normalized value of `5%`, unit `%`, a successful raw log, and a valid evidence reference.

Results:

- HTTP response: `200`.
- One `ScenarioInput` was persisted.
- One `ScenarioResult` was persisted or updated.
- Adjusted driver value: `5.5%`.
- No validated regression coefficient was available, so estimated price impact and estimated new price were `null`.
- Methodology: `Arithmetic preview`.
- Warning explicitly stated that price impact was not estimated.
- Scenario notes contained the `NormalizedMetric` ID and `RawDataLog` ID.

This confirms the fallback is explainable and does not present arithmetic adjustment as a price forecast.

## Test groups passed

| Area | Tests | Result |
|---|---:|---|
| Exposure functions | 5 | Passed |
| Resilience functions | 7 | Passed |
| Company snapshot | 3 | Passed |
| Correlation screening | 2 | Passed |
| Commodity intelligence and quant gate | 7 | Passed |
| Scenario API | 6 | Passed |
| Total targeted run | **30** | **Passed** |

## Findings and remaining limitations

1. The scoring functions now produce demo-ready provisional numbers, but they are not historically calibrated.
2. Partial resilience scoring is useful for UI/demo coverage, but the scaled score can look stronger than the evidence base; the status label must remain visible in the frontend.
3. Correlation confidence is correctly kept Low below 12 matched observations.
4. A driver can be persisted and linked to evidence, but a correlation is only meaningful after price and driver units/frequencies are validated.
5. Scenario run does not convert correlation into price sensitivity. Price-impact fields remain null until a validated coefficient exists; beta, volatility-based shock limits, confidence intervals, vintage dates, regression, and out-of-sample backtesting remain pending.
6. The coal production ingest is explicitly a World Bank electricity-from-coal proxy, not physical coal production. It must remain labeled as a proxy in UI and audit outputs.

## Conclusion

The improved OreLens intelligence path is technically functional with dummy data:

```text
raw evidence
  → normalized metric
  → company snapshot / driver map
  → provisional score or correlation
  → explainable scenario result
```

The next production-quality step is not to increase the score complexity. It is to ingest enough audited commodity price and driver history for each commodity, then validate units, release dates, correlation stability, and out-of-sample behavior before presenting any score as validated.
