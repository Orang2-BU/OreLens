# OreLens — Data Availability Audit v0.1

This audit validates whether the approved metrics can be obtained from real APIs before the scoring engine is finalized.

## Required fields

For each metric, record:

| Field | Description |
|---|---|
| Metric | Metric being checked |
| Available | Yes, no, or partial |
| Source | API or dataset |
| Endpoint | Exact endpoint used |
| Earliest date | First available observation |
| Latest date | Most recent observation |
| Frequency | Daily, monthly, quarterly, etc. |
| Unit | Original and normalized unit |
| Missing values | Count or rate |
| Historical depth | Usable history length |
| Proxy required | Whether a proxy is needed |
| Cost/rate limit | Access and request constraints |
| Notes | Caveats and transformation details |

## Initial audit scope

Start with sample data for Coal, Gold, Nickel, and Copper, then expand to every approved metric in the full dictionary.

## Decision rule

Do not finalize weights or decision logic until this audit and the historical-data collection are complete enough to support correlation screening, regression, rolling analysis, regime comparison, historical weighting, and backtesting.
