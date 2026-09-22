# Plan 002: Connect Data Dictionary APIs for raw-data testing

> **Executor instructions**: Execute this plan before Plan 001. This plan ends
> at verified raw responses and availability evidence; do not normalize fields
> into intelligence metrics here. Run every verification command. Never print,
> persist, or commit credentials. Update the status row in `plans/README.md`
> when complete.
>
> **Drift check (run first)**:
> `git diff --stat ad66fba..HEAD -- backend/apps/integrations backend/apps/evidence backend/.env.example docs/data/DATA_DICTIONARY.md docs/data/DATA_AVAILABILITY_AUDIT.md`
>
> If an in-scope client or evidence model changed, compare it with the current
> state below before editing. Treat incompatible behavior as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: M (1–2 backend days, excluding credential/access delays)
- **Risk**: MED — external endpoints and authentication can change
- **Depends on**: none
- **Category**: direction, correctness, tests, docs
- **Planned at**: commit `ad66fba`, 2026-09-22

## Why this matters

The Data Dictionary names several providers, but only World Bank and one FRED
download path have produced verified raw data in the current project. Sectors,
UN Comtrade, and EIA clients exist without a reproducible raw connectivity
gate. A single safe probe command is needed so backend developers can verify
credentials, HTTP status, response shape, date coverage, and missingness before
building normalizers or changing intelligence logic.

## Target provider matrix

These five providers are the implementation scope because clients already
exist in `backend/apps/integrations/clients/`:

| Provider | Data Dictionary role | Safe probe target | Current state |
|---|---|---|---|
| Sectors | Company profile, fundamentals, operations, commodity data | `ADRO.JK` company report | Client exists; auth format needs live verification |
| World Bank | China/global macro indicators | China GDP growth, short bounded window | Client and live ingest already work |
| FRED | Coal price, USD, yields, inflation | Existing coal series `PCOALAUUSDA` | Client exists; API-key path lacks raw probe gate |
| UN Comtrade | Coal/nickel/copper imports | China coal imports, one annual period | Client uses preview route; reporter/flow/partner semantics unverified |
| EIA | Coal demand, electricity, gas, renewables | One documented coal/gas series and short window | Client route is a placeholder until verified |

IEA, OECD, GDELT, WGC, IMF, and other “external” sources remain discovery
items. They do not have clients in the repo and are not required for this raw
connectivity milestone. Record their access/license status, but do not create
new clients until a concrete MVP metric and permitted endpoint are approved.

## Current state

- `backend/apps/integrations/clients/base.py:23-49` performs GET requests,
  returns decoded data, and writes `RawDataLog`. It catches all request errors
  and represents them as status 500. Request parameters are sanitized; headers
  are not persisted.
- `backend/apps/integrations/clients/sectors.py:4-15` exposes company report and
  company-list calls, currently using a Bearer-prefixed authorization header.
- `backend/apps/integrations/clients/worldbank.py` exposes country indicators
  without credentials.
- `backend/apps/integrations/clients/fred.py` sends its API key as a request
  parameter; `BaseApiClient._sanitize_params()` must redact it in logs.
- `backend/apps/integrations/clients/un_comtrade.py` uses
  `/preview/C/A/HS` with reporter, commodity code, and period, but does not
  explicitly pin trade flow, partner, quantity field, or HS revision.
- `backend/apps/integrations/clients/eia.py` calls `/coal/data`; this route must
  be checked against current official documentation before being treated as
  valid.
- `backend/apps/evidence/models.py` already supports raw source, endpoint,
  sanitized parameters, response payload, status, fetch time, and
  `data_origin=live_api`. Do not add another evidence model for this task.
- Existing test convention is in `backend/apps/integrations/tests.py`, using
  Django `TestCase` and mocked/constructed payloads without consuming API
  credits.

## Required raw-probe contract

Add one management command:

```text
python manage.py probe_raw_sources --source <sectors|world_bank|fred|un_comtrade|eia|all>
```

Optional source-specific arguments may include `--ticker`, `--start`,
`--end`, and `--period`, but every default must request a small bounded sample.
Do not add a job framework or generic provider registry outside this command.

For every source, the command must:

1. reject missing or placeholder credentials before the request when the
   provider requires a key;
2. make exactly one bounded probe request by default;
3. create one `RawDataLog` with `data_origin=live_api`;
4. print provider, sanitized endpoint, HTTP status, payload type, top-level
   keys, row count, first/last observed period when detectable, null count, and
   response byte size;
5. never print the full payload unless a developer inspects the stored log;
6. exit non-zero for transport errors, unauthorized access, non-JSON responses
   where JSON is expected, or an unexpected response shape;
7. allow one failed provider under `--source all` to be reported alongside the
   others, then exit non-zero after the complete summary;
8. not create `NormalizedMetric` rows.

## Commands you will need

Run from `backend/`.

| Purpose | Command | Expected on success |
|---|---|---|
| Baseline | `python manage.py check` | no issues |
| Offline tests | `python manage.py test apps.integrations apps.evidence` | all pass; no network calls |
| All raw probes | `python manage.py probe_raw_sources --source all` | five-source summary; exit 0 only when all configured sources pass |
| Inspect latest logs | `python manage.py shell -c "from apps.evidence.models import RawDataLog; print(list(RawDataLog.objects.exclude(source='Seed Demo').values_list('source','status_code','data_origin')[:10]))"` | tested providers show expected HTTP status and `live_api` |
| Ensure no normalization | `python manage.py shell -c "from apps.evidence.models import NormalizedMetric; print(NormalizedMetric.objects.count())"` | count unchanged before versus after raw probes |
| Full regression | `python manage.py test` | all tests pass |

Before running live probes, copy `.env.example` to `.env` and supply required
keys locally. Never commit `.env`.

## Scope

### In scope

- `backend/apps/integrations/clients/base.py`
- the five existing client files under `backend/apps/integrations/clients/`
- new `backend/apps/integrations/management/commands/probe_raw_sources.py`
- `backend/apps/integrations/tests.py`, or one focused test module in that app
- minimal redacted response fixtures under the integrations app, only when a
  fixture is clearer than an inline test payload
- `backend/.env.example` for variable names only
- `docs/data/DATA_AVAILABILITY_AUDIT.md`
- `docs/intelligence/IMPLEMENTATION_PLAN.md`

### Out of scope

- normalized metrics, scoring, correlation, and scenario runs;
- retry queues, schedulers, caching, async clients, or new dependencies;
- frontend controls for API probes;
- bulk historical downloads;
- clients for IEA/OECD/GDELT/WGC/IMF before access and licensing are approved;
- exposing raw payloads through a new public endpoint;
- model migrations unless a verified provider cannot be represented by the
  existing evidence fields.

## Git workflow

- Branch: `feat/raw-api-probes`
- Match existing conventional commits, for example:
  `feat: add raw provider connectivity probes`
- Keep client corrections, probe command/tests, and audit documentation as
  separate logical commits.
- Do not push or open a pull request unless instructed.

## Tasks

### API-RAW-01 — Make the shared HTTP path testable and fail clearly

1. Keep `BaseApiClient` as the single request/logging path.
2. Use `requests.RequestException` rather than a blanket exception for
   transport handling; preserve a raw log for failed requests without hiding
   programming errors.
3. Ensure all credential-like request parameters remain redacted
   case-insensitively. Never add headers to `request_params` or output.
4. Give the probe command access to HTTP status and its exact created log
   without issuing a second request. Prefer the smallest compatible change to
   `_get`; do not introduce a response-wrapper class unless a simple return or
   latest-log lookup cannot be made reliable.
5. Keep existing client callers working.

**Verify**: mocked tests cover HTTP 200 JSON, HTTP 401 JSON, timeout, malformed
JSON, redacted query keys, and one raw log per request.

### API-RAW-02 — Verify Sectors raw access

1. Reject a missing/placeholder `SECTORS_API_KEY`.
2. Probe the company-report endpoint with `ADRO.JK` by default.
3. Verify the authorization-header format from current official documentation
   and one live response. Do not log or print the header.
4. Validate only envelope-level facts at this stage: JSON type, ticker/company
   identity when present, top-level sections, and as-of/reporting periods.
5. Record credit/rate-limit headers only if they are non-sensitive and actually
   returned.

**Verify**:

```powershell
python manage.py probe_raw_sources --source sectors --ticker ADRO.JK
```

Expected: one Sectors `RawDataLog`, HTTP 200, `live_api`, structural summary,
and no credential text in console or `request_params`.

### API-RAW-03 — Verify World Bank and FRED raw access

1. World Bank probe: China GDP growth indicator with a short explicit date
   range. Validate its two-part JSON envelope and indicator/country identity.
2. FRED probe: `PCOALAUUSDA` through the existing API client. Require a real
   `FRED_API_KEY`, validate series identity and observations, and confirm the
   key is stored only as `***REDACTED***` in `request_params`.
3. Compare structural output with the already working ingest commands, but do
   not invoke normalization.

**Verify**:

```powershell
python manage.py probe_raw_sources --source world_bank
python manage.py probe_raw_sources --source fred
```

Expected: one successful live raw log per command and zero new normalized
metrics.

### API-RAW-04 — Verify UN Comtrade semantics before ingestion

1. Require `UN_COMTRADE_API_KEY` only if the selected current endpoint requires
   it; document whether preview and production endpoints differ.
2. Probe one annual China import period for coal with reporter China, partner
   World, import flow, HS classification/revision, and code `2701` explicitly
   represented in the request or verified response.
3. Report available quantity/value fields and units. Do not choose a canonical
   metric in this plan.
4. Fail if response identity does not match reporter, flow, period, and product
   requested.

**Verify**:

```powershell
python manage.py probe_raw_sources --source un_comtrade --period 2024
```

Expected: traceable raw response with verified request identity, or an explicit
non-zero blocker naming the mismatched/missing field.

### API-RAW-05 — Replace the EIA placeholder with one verified probe route

1. Use current official EIA API documentation to select one Data Dictionary
   candidate: coal consumption, electricity demand, natural-gas price, or
   renewable generation.
2. Require `EIA_API_KEY` and use a short date range plus explicit frequency,
   facets, and data columns as required by that endpoint.
3. Replace `/coal/data` only after the live route returns the expected series.
4. Validate response metadata, frequency, units, and row count. Do not map it
   to an OreLens metric yet.

**Verify**:

```powershell
python manage.py probe_raw_sources --source eia
```

Expected: one bounded HTTP-200 raw response with identified frequency/unit, or
an explicit audit blocker. A generic 404/empty response is not success.

### API-RAW-06 — Add one offline contract test per provider

For each provider, add the smallest redacted payload that proves envelope and
identity validation. Mock `requests.get`; no test may use the network or a
real credential.

Required cases:

- all five happy-path response shapes;
- unauthorized response;
- timeout;
- malformed JSON;
- wrong indicator/ticker/reporter/product/series identity;
- sanitization for query-string keys;
- `--source all` reports every source and exits non-zero when one fails;
- no probe creates a `NormalizedMetric`.

**Verify**: `python manage.py test apps.integrations apps.evidence` → all pass.

### API-RAW-07 — Update the availability matrix from actual probes

Update `docs/data/DATA_AVAILABILITY_AUDIT.md` with one table containing:

| Field | Required value |
|---|---|
| provider | Exact provider |
| checked_at | UTC timestamp/date |
| endpoint | Sanitized route |
| credential_required | Yes/No, never the key |
| HTTP status | Actual status |
| response shape | Object/list and relevant top-level keys |
| earliest/latest sample | From the bounded response |
| frequency/unit | Observed or `unverified` |
| rows/nulls | Actual sample counts |
| rate limit/cost/license | Observed/documented or `unverified` |
| raw log ID | Exact `RawDataLog` reference |
| verdict | `connected`, `blocked`, or `connected_not_mapped` |

Also list IEA, OECD, GDELT, WGC, IMF, and other external candidates as
`discovery_only` unless an approved API contract and license were verified.
Do not call a source analytics-ready merely because HTTP 200 was returned.

**Verify**:

```powershell
python manage.py probe_raw_sources --source all
git diff --check
```

Expected: command summary matches the audit table; Markdown has no whitespace
errors and contains no credential values or complete raw payloads.

## Test plan

- Extend the existing integration test style; mock at `requests.get` so the
  shared client and logging path are exercised.
- Assert database effects: exactly one `RawDataLog`, correct source/status/
  origin, sanitized parameters, and zero `NormalizedMetric` writes.
- Test the management command with `call_command` and captured stdout/stderr.
- Use one test per failure class rather than duplicating each failure for all
  providers; provider-specific identity mismatches still need one test each.

Final verification:

```powershell
python manage.py makemigrations --check
python manage.py check
python manage.py test
```

Expected: no migration drift, no system-check issues, and all tests pass.

## Done criteria

- [ ] One command probes each of the five existing providers independently or together.
- [ ] Every probe is bounded and creates exactly one traceable `live_api` raw log.
- [ ] Required credentials fail before requests when absent or placeholder.
- [ ] No credential/header value appears in console, committed fixtures, or raw-log parameters.
- [ ] World Bank and FRED response identities match the requested indicator/series.
- [ ] Sectors authentication and company-report shape are verified live.
- [ ] UN Comtrade reporter/partner/flow/product/period are explicit and verified.
- [ ] EIA uses one documented working route instead of the placeholder route.
- [ ] Probe commands create zero normalized metrics.
- [ ] Offline tests cover all provider envelopes and shared failure handling.
- [ ] Availability Audit records actual results and distinguishes connectivity from analytics readiness.
- [ ] IEA/OECD/GDELT/WGC/IMF remain discovery-only until approved.
- [ ] Full Django test suite passes and `plans/README.md` is updated.

## STOP conditions

Stop and report instead of improvising if:

- a required credential is unavailable;
- current official documentation cannot establish an endpoint/auth contract;
- live response identity conflicts with the requested ticker, indicator,
  series, reporter, partner, flow, product, or period;
- provider terms do not permit storing raw responses;
- a full raw payload contains sensitive/user-specific data not represented in
  the current evidence policy;
- success would require an unbounded/bulk request;
- a new dependency, model, queue, scheduler, or public raw-data endpoint seems
  necessary;
- verification fails twice after a reasonable correction;
- an out-of-scope file must be changed.

## Maintenance notes

- Raw connectivity proves transport and response shape, not metric semantics or
  analytical quality. Plan 001 owns normalization and real-only intelligence.
- Keep probe defaults small because provider credits and payload sizes vary.
- If provider schemas change, update their single identity validator and
  redacted fixture before changing any downstream ingest.
- Add a new provider only when the Data Dictionary names a concrete metric and
  the team has verified endpoint access, storage rights, and unit semantics.

