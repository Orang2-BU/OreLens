# OreLens Backend Implementation Plans

Generated with the `improve` skill and updated on 2026-09-22. Execute plans in the order
listed below. Read a plan fully before editing code and update its status when
the work is complete.

## Execution order and status

| Plan | Title | Priority | Effort | Depends on | Status |
|---|---|---|---|---|---|
| 002 | Connect Data Dictionary APIs for raw-data testing | P1 | M | — | TODO |
| 001 | Enable reproducible intelligence testing with real data | P1 | L | 002 | TODO |

Status values: `TODO`, `IN PROGRESS`, `DONE`, `BLOCKED: <reason>`, or
`REJECTED: <reason>`.

## Dependency notes

Plan 002 runs first because provider authentication, endpoint validity, and
raw response shapes must be known before Plan 001 maps them into intelligence
metrics.

Plan 001 is intentionally one end-to-end backend handoff. Do not split its
ingest and seed-isolation work: an ingest that still lets demo records win the
snapshot would produce a misleading “real-data” test.

## Findings considered and rejected

- Final scoring weights: rejected for this plan because real coverage and
  historical validation are still incomplete.
- All four commodities at once: rejected for the first live-data milestone;
  Coal plus the five existing issuers gives a smaller reproducible vertical
  slice. Extend only after its acceptance gates pass.
- Synthetic replacement for unavailable Sectors fields: rejected because it
  would reproduce the provenance problem fixed in commit `b84bc97`.
