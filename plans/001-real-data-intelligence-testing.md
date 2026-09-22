# Plan 001: Enable reproducible intelligence testing with real data

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving on. Do
> not infer API fields, units, reporting periods, or commodity mappings. If a
> required field is absent, record it as unavailable and follow the STOP
> conditions instead of substituting seed data. When finished, update this
> plan's row in `plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat b84bc97..HEAD -- backend/apps/integrations backend/apps/evidence backend/apps/intelligence backend/apps/companies backend/apps/analytics docs/data/DATA_AVAILABILITY_AUDIT.md`
>
> If an in-scope file changed, compare the current state below with the live
> code. Stop if the data contract or snapshot selection behavior has changed
> materially.

## Status

- **Priority**: P1
- **Effort**: L (2–4 focused backend days, excluding API-access delays)
- **Risk**: MED — external response contracts and metric semantics must be verified
- **Depends on**: `plans/002-connect-data-dictionary-apis.md`
- **Category**: direction, correctness, tests, docs
- **Planned at**: commit `b84bc97`, 2026-09-21

## Objective

Produce one auditable real-data vertical slice that lets the team run OreLens
intelligence without demo records influencing the result. The first slice is:

- commodities: `COAL` first;
- companies: `ADRO.JK`, `PTBA.JK`, `INCO.JK`, `ANTM.JK`, `MDKA.JK` for live
  company fundamentals, with exposure/resilience only where the source truly
  supplies the required inputs;
- existing live context: Coal price returns and China GDP growth;
- next driver target: China Coal Imports, only after HS-code, quantity unit,
  frequency, and endpoint behavior are verified.

This plan does **not** promise that Sectors contains mine production, commodity
revenue share, reserves, EBITDA margin, or destination shares. Missing data is
a valid audit result. A real partial snapshot is better than a complete fake
snapshot.

## Why this matters

The evaluation currently reports all company intelligence as `seed_demo`.
Coal is only `partial_ready`: 33 price periods and one of three candidate
drivers are ready for screening. The ingestion foundation exists, but there is
no live Sectors ingestion command and `build_company_snapshot()` still reads
seed observations and relational seed fallbacks. Without fixing both sides,
new live rows could be mixed with demo metrics and mistakenly presented as a
real intelligence test.

## Current state

### Verified baseline

Run from `backend/`:

```text
python manage.py test
→ 70 tests pass

python manage.py evaluate_intelligence --json
→ COAL: partial_ready, 33 price periods, 1/3 drivers ready
→ all emitted company/commodity snapshots: data_mode = seed_demo
```

### Relevant implementation

- `backend/apps/integrations/clients/sectors.py:4-15` — only company-report and
  subsector wrappers exist. It currently sends `Authorization: Bearer <key>`.
  Verify this against a live request: the official Sectors recipe shows the
  API key directly in the `Authorization` header, so the current prefix may be
  incorrect.
- `backend/apps/integrations/clients/base.py:23-49` — HTTP calls create a
  `RawDataLog`, redact request parameters, and convert request failures into a
  status-500 log. It does not expose response status directly to the caller.
- `backend/apps/integrations/management/commands/ingest_china_gdp.py` — current
  exemplar for response validation, atomic idempotent upsert, raw-log linkage,
  and `DataAuditItem` update. Match this structure.
- `backend/apps/evidence/models.py:14-25` — `RawDataLog.data_origin` supports
  `live_api`, `imported_file`, `derived`, and `seed_demo`.
- `backend/apps/intelligence/company_snapshot.py:39-44` — company observations
  are selected by ticker and HTTP-success evidence, but seed-origin rows are
  not excluded.
- `backend/apps/intelligence/company_snapshot.py:72-89` and `:128-160` — missing
  exposure/resilience inputs can fall back to relational seed records.
- `backend/apps/intelligence/company_snapshot.py:269-296` — peer comparison
  requires at least three companies with matching metric, date, frequency,
  unit, transformation, source, and definition.
- `backend/apps/intelligence/management/commands/evaluate_intelligence.py` —
  reproducible report entry point, but it does not yet support a real-only
  assertion mode.

Official reference used for the authentication check:
`https://docs.sectors.app/recipes/stock-investing-and-finance/01%20-%20Portfolio-Optimization`.
Do not copy example values from the recipe into OreLens data.

## Required output contract

Every normalized live observation must have:

| Field | Requirement |
|---|---|
| `raw_data_ref` | Non-null `RawDataLog` with HTTP 200 |
| `raw_data_ref.data_origin` | `live_api` for API responses |
| `source` | Exact provider name, never `Seed Demo` |
| `entity_type` / `entity_id` | Exact OreLens entity and ticker/code |
| `commodity` | Set only for genuinely commodity-specific company metrics |
| `observation_date` | Reporting-period date, not fetch date |
| `frequency`, `unit`, `original_unit` | Explicit and source-verified |
| `transformation` | `None`, `YoY %`, or another existing supported value |
| `confidence` | Based on evidence quality; never automatically `High` |
| `is_proxy` | True whenever the source field is only an approximation |
| `proxy_description` | Required when `is_proxy=true` |

The same provider response must be safe to ingest repeatedly without creating
duplicate normalized observations.

## Commands you will need

Run all commands from `backend/` unless stated otherwise.

| Purpose | Command | Expected on success |
|---|---|---|
| Environment check | `python manage.py check` | exit 0, no issues |
| Migration drift | `python manage.py makemigrations --check` | `No changes detected` |
| Unit/integration tests | `python manage.py test` | all tests pass |
| Live company audit | `python manage.py audit_sectors_company --tickers ADRO.JK PTBA.JK INCO.JK ANTM.JK MDKA.JK` | per-ticker HTTP/schema summary, no secret output |
| Live company ingest | `python manage.py ingest_sectors_company --tickers ADRO.JK PTBA.JK INCO.JK ANTM.JK MDKA.JK` | idempotent upsert summary |
| Coal driver ingest | `python manage.py ingest_china_coal_imports` | observation/missing-count summary, or an explicit audited blocker |
| Correlation screen | `python manage.py screen_driver_correlations --commodity COAL` | no crash; persisted result or explicit insufficient-data status |
| Real-only evaluation | `python manage.py evaluate_intelligence --json --real-only` | valid JSON; no company component has `seed_demo` origin |

The three new command names above are the required operator interface. Keep
them as thin management commands; do not introduce a job framework.

## Scope

### In scope

- `backend/apps/integrations/clients/base.py`
- `backend/apps/integrations/clients/sectors.py`
- `backend/apps/integrations/clients/un_comtrade.py`
- new commands under `backend/apps/integrations/management/commands/`
- `backend/apps/integrations/tests.py`
- `backend/apps/intelligence/company_snapshot.py`
- `backend/apps/intelligence/management/commands/evaluate_intelligence.py`
- `backend/apps/intelligence/tests.py`
- `backend/apps/companies/views.py` only if an explicit demo-mode query option
  is needed at the API boundary
- evidence models/migrations only if the existing fields cannot represent a
  verified requirement
- `docs/data/DATA_AVAILABILITY_AUDIT.md`
- `docs/intelligence/IMPLEMENTATION_PLAN.md`
- a generated test report under `docs/intelligence/`

### Out of scope

- final exposure/resilience weights;
- regression, beta, price forecasts, or investment recommendations;
- PostgreSQL, queues, schedulers, caching, or new dependencies;
- all-four-commodity ingestion before the Coal slice passes;
- scraping websites or inventing values when an API field is absent;
- committing `.env`, API keys, complete sensitive headers, or raw credentials;
- changing frontend code.

## Git workflow

- Branch: `feat/backend-real-intelligence-data`
- Use the repository's conventional commit style, for example:
  `feat: ingest audited Sectors company metrics`
- Keep the credential/schema audit, ingestion, seed isolation, and acceptance
  report as reviewable logical commits.
- Do not push or open a pull request unless instructed by the operator.

## Tasks

### BE-REAL-01 — Establish credential and live-contract gates

1. Require a non-placeholder `SECTORS_API_KEY` for live Sectors commands.
   Missing credentials must raise `CommandError` before making a request.
2. Verify the accepted `Authorization` header format with one live request.
   Update `SectorsClient` only from observed HTTP behavior or current official
   documentation; never log the header.
3. Add `audit_sectors_company`. It must fetch the five pilot tickers, create
   normal `RawDataLog` records with `data_origin=live_api`, and print only:
   ticker, endpoint, HTTP status, top-level field names, reporting periods,
   null counts, and candidate metric mappings. Do not print the API key or the
   complete payload.
4. Record response availability, endpoint, dates, frequency, units, missing
   rate, and unresolved semantics in `DataAuditItem` and
   `docs/data/DATA_AVAILABILITY_AUDIT.md`.

**Verify**:

```powershell
python manage.py audit_sectors_company --tickers ADRO.JK
python manage.py shell -c "from apps.evidence.models import RawDataLog; x=RawDataLog.objects.filter(source='Sectors').first(); print(x.status_code, x.data_origin, 'authorization' in str(x.request_params).lower())"
```

Expected: HTTP 200 for valid access; `live_api`; `False`. If access is denied,
the command exits non-zero with a concise status and the plan stops before
normalization.

### BE-REAL-02 — Lock the observed Sectors response contract in tests

1. Save a **minimal redacted fixture** containing only fields needed for
   normalization. Remove unrelated payload sections and all credentials.
2. Write parser tests before the ingest command. Cover:
   - valid payload;
   - missing optional metric;
   - null value;
   - wrong ticker;
   - changed/missing required key;
   - unknown unit or period;
   - idempotent repeated ingest.
3. Map only source-confirmed fields to names already consumed by
   `company_snapshot.py`: `Revenue Growth`, `Net Income Growth`, `ROE`, `DER`,
   `PE`, `PB`, plus exposure/resilience metrics only if their exact semantics
   exist in the live payload.
4. Do not map `revenue_estimate` to revenue growth, commodity revenue share, or
   production dependency. Similar names are not equivalent metrics.

**Verify**: `python manage.py test apps.integrations` → all existing and new
tests pass without network access.

### BE-REAL-03 — Implement idempotent live company ingestion

1. Add `ingest_sectors_company --tickers ...` using the tested parser.
2. Follow the transaction/upsert pattern in `ingest_china_gdp.py`.
3. Attach every `NormalizedMetric` to the exact successful `RawDataLog`.
4. Use the source reporting period for `observation_date`. If only a current
   snapshot is supplied, record its actual as-of date and do not label it
   annual history.
5. Emit counts per ticker: inserted/updated, skipped-null, unsupported fields,
   and failed tickers. One failed ticker must not silently look successful.
6. Running the command twice must leave identical normalized-row counts.

**Verify**:

```powershell
python manage.py ingest_sectors_company --tickers ADRO.JK PTBA.JK INCO.JK ANTM.JK MDKA.JK
python manage.py shell -c "from apps.evidence.models import NormalizedMetric; q=NormalizedMetric.objects.filter(entity_type='Company',raw_data_ref__data_origin='live_api'); print(q.count(), sorted(q.values_list('entity_id',flat=True).distinct()))"
python manage.py ingest_sectors_company --tickers ADRO.JK PTBA.JK INCO.JK ANTM.JK MDKA.JK
```

Expected: the first query returns a non-zero count and only requested tickers;
the second ingest reports updates/no changes without increasing unique metric
rows.

### BE-REAL-04 — Prevent demo contamination in real-data mode

1. Add an explicit mode to `build_company_snapshot`, defaulting to production
   behavior that excludes `raw_data_ref.data_origin=seed_demo` and disables
   `CompanyCommodityExposure`/`CompanyResilience` seed fallbacks.
2. Preserve demo behavior only behind an explicit opt-in such as
   `include_demo=True`. If exposed over HTTP, accept only a strict boolean query
   value and document it as demo-only.
3. Ensure `data_mode` is computed from the components actually returned.
   Fundamentals alone must not claim that exposure/resilience is
   evidence-backed.
4. Add a top-level coverage summary to evaluation output:
   live component count, imported component count, demo component count,
   missing component count, and evidence IDs.
5. Add `--real-only` to `evaluate_intelligence`. It must exit non-zero when any
   emitted intelligence component is `seed_demo`, when an evidence ID is
   missing, or when the referenced raw log is not HTTP 200.

**Verify**:

```powershell
python manage.py test apps.intelligence apps.companies
python manage.py evaluate_intelligence --json --real-only
```

Expected: tests pass; evaluation is valid JSON and either passes with no demo
components or fails explicitly with a machine-readable list of blockers. It
must never silently fall back to seed.

### BE-REAL-05 — Add the next real Coal driver without semantic shortcuts

1. Audit UN Comtrade for `China Coal Imports` before writing normalization.
   Verify reporter China, partner World, flow imports, HS revision/code, product
   scope, quantity field, unit, period, pagination, rate limit, and missingness.
2. Use coal HS code `2701` only if the live response and chosen HS revision
   confirm that it represents the intended coal scope. Do not mix quantity and
   trade value; prefer a stable physical quantity for the demand hypothesis.
3. Add `ingest_china_coal_imports` with raw-log linkage, idempotent normalized
   rows, `DataAuditItem`, and parser tests. Normalize to annual `YoY %` only
   after at least two comparable annual levels exist.
4. Run correlation screening. A Low/null result is acceptable; never promote
   importance merely because data was ingested.

**Verify**:

```powershell
python manage.py ingest_china_coal_imports
python manage.py screen_driver_correlations --commodity COAL
python manage.py shell -c "from apps.evidence.models import NormalizedMetric; q=NormalizedMetric.objects.filter(metric_name='China Coal Imports',entity_id='COAL',raw_data_ref__data_origin='live_api'); print(q.count(), list(q.values_list('unit','frequency','transformation').distinct()))"
```

Expected: traceable observations with one consistent unit/frequency/
transformation, or an explicit audited blocker. No seed rows satisfy this
gate.

### BE-REAL-06 — Produce the real-data intelligence test report

Create `docs/intelligence/REAL_DATA_INTELLIGENCE_TEST_REPORT.md` from command
output. Include:

- execution date and git commit;
- commands run;
- provider endpoints without credentials;
- tickers/commodities tested;
- live observation counts and periods;
- missing/proxy metrics;
- snapshot `data_mode`, component coverage, evidence IDs, and score labels;
- Coal quant-readiness and correlation result;
- scenario guardrail result, if the chosen live driver has enough history;
- failures/blockers and the next concrete data source required.

Do not copy full raw API payloads into the report. Do not call a partial score
validated.

**Verify**:

```powershell
python manage.py evaluate_intelligence --json --real-only
git grep -n "Seed Demo\|seed_demo" -- docs/intelligence/REAL_DATA_INTELLIGENCE_TEST_REPORT.md
```

Expected: real-only evaluation passes or reports named blockers; grep returns
no match in claimed real results (it may appear only in a clearly labeled
baseline/comparison section).

## Test plan

Use Django `TestCase` and mocked client responses; tests must not consume live
API credits.

- `backend/apps/integrations/tests.py`
  - Sectors auth header never appears in `RawDataLog`.
  - Each supported live field maps to the exact metric/unit/date.
  - Unknown shapes fail before writing normalized metrics.
  - Nulls are skipped and counted.
  - Repeated ingest is idempotent.
  - UN Comtrade product/reporter/flow/unit mismatch fails closed.
- `backend/apps/intelligence/tests.py`
  - default/real mode excludes normalized seed rows and relational fallbacks;
  - explicit demo mode keeps the current demo behavior;
  - mixed live and seed records cannot cause seed to win in real mode;
  - real partial inputs remain partial and list missing components.
- management-command tests
  - `--real-only` succeeds for fully traceable returned components;
  - `--real-only` exits non-zero and names seed/missing-evidence blockers.

Final verification:

```powershell
python manage.py makemigrations --check
python manage.py check
python manage.py test
```

Expected: no migration drift, no system-check issues, and all tests pass.

## Done criteria

- [ ] Live credential failure is explicit; no key/header is persisted or printed.
- [ ] Sectors response contract is captured by a minimal redacted fixture and parser tests.
- [ ] Five pilot tickers can be audited; supported metrics ingest idempotently.
- [ ] Every returned real metric has source, period, unit, transformation, evidence ID, and `live_api` origin.
- [ ] Real/default snapshot mode excludes all seed observations and relational fallbacks.
- [ ] Missing exposure/resilience fields remain unavailable instead of being synthesized.
- [ ] `evaluate_intelligence --json --real-only` is a reproducible pass/fail gate.
- [ ] China Coal Imports is either traceably ingested or documented as a precise audited blocker.
- [ ] Coal screening runs without converting correlation into a causal or forecast claim.
- [ ] `REAL_DATA_INTELLIGENCE_TEST_REPORT.md` records actual results and limitations.
- [ ] `python manage.py test` passes.
- [ ] No unplanned dependency, queue, scheduler, or frontend change is introduced.
- [ ] `plans/README.md` status is updated.

## STOP conditions

Stop and report instead of improvising if:

- `SECTORS_API_KEY` or the required UN Comtrade access is unavailable;
- the official/live Sectors authorization contract conflicts with both the
  current client and the referenced recipe;
- a response does not expose an unambiguous ticker, reporting period, unit, or
  metric meaning;
- exposure/resilience would require mapping an estimate or generic company
  value to a commodity-specific metric;
- real company data requires scraping or manually transcribing values not
  supplied and reviewed by the operator;
- HS-code/product revision cannot be pinned for China Coal Imports;
- a model migration becomes necessary only to accommodate speculative future
  providers;
- any verification fails twice after a reasonable correction;
- completing a task requires modifying an out-of-scope file.

## Maintenance notes

- The current `data_origin` is attached to `RawDataLog`, so reviewers must
  confirm each normalized row points to the exact response that produced it.
- If a provider later supplies revised/restated periods, define a revision
  policy before overwriting historical observations; the current upsert key
  does not preserve vintages.
- Extend to Gold, Nickel, and Copper only by repeating the same audit → fixture
  → parser → ingest → real-only evaluation sequence.
- The next plan after this one should cover publication vintages and
  out-of-sample validation, not more scoring complexity.
