from apps.evidence.models import NormalizedMetric
from apps.intelligence.commodity_snapshot import DRIVERS
from collections import Counter


def quant_readiness(commodity):
    prices = NormalizedMetric.objects.filter(
        metric_name='Commodity Price', entity_type='Commodity', entity_id=commodity.code,
        raw_data_ref__status_code=200,
        transformation__in=['Return', 'Log Return', 'Pct Change', 'YoY %'],
    ).values('observation_date', 'frequency')
    price_periods = {(row['observation_date'], row['frequency']) for row in prices}
    drivers = []
    for category, name, entity_type, entity_id in DRIVERS.get(commodity.code, []):
        rows = NormalizedMetric.objects.filter(
            metric_name=name, entity_type=entity_type, entity_id=entity_id,
            raw_data_ref__status_code=200,
            transformation__in=['Return', 'Log Return', 'Pct Change', 'YoY %'],
        )
        aligned = {(row.observation_date, row.frequency) for row in rows
                   if (row.observation_date, row.frequency) in price_periods}
        counts = Counter(frequency for _, frequency in aligned)
        consistent_periods = max(counts.values(), default=0)
        drivers.append({'metric': name, 'category': category,
                        'safe_aligned_periods': consistent_periods,
                        'status': 'ready_for_screening' if consistent_periods >= 12 else 'insufficient_history_or_vintage'})
    return {
        'commodity': commodity.code, 'price_periods': len(price_periods),
        'minimum_periods': 12, 'drivers': drivers,
        'status': 'ready_for_screening' if any(d['status'] == 'ready_for_screening' for d in drivers) else 'blocked',
        'vintage_status': 'unavailable',
        'note': 'Preliminary screening readiness only; historical publication/vintage dates are unavailable and must be resolved before backtesting.',
    }
