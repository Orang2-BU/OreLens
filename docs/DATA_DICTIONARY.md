# OreLens — Data Dictionary v0.1

This is the approved data-definition boundary from the product discussion. Exact metric rows and values must be filled from the data audit; they are not invented here.

## Common fields for every metric

Each metric should record:

- Name
- Definition
- Source
- Frequency
- Unit
- Transformation
- Priority
- Confidence

## Planned data sources

| Source | Intended use |
|---|---|
| Sectors | Primary sector and commodity data |
| World Bank | Macro and commodity context |
| FRED | Economic and financial time series |
| UN Comtrade | Trade and physical-demand context |
| EIA | Energy data, especially coal and related indicators |

## Initial commodity scope

- Coal
- Gold
- Nickel
- Copper

## Data rules

- Preserve raw responses before normalization.
- Normalize sources into a common internal schema.
- Record units and frequency explicitly.
- Mark proxy metrics instead of silently substituting them.
- Keep confidence and source evidence with the metric.
