from apps.evidence.models import NormalizedMetric
from apps.intelligence.commodity_snapshot import DRIVERS
from collections import Counter


def quant_readiness(commodity):
    prices = NormalizedMetric.objects.filter(
        metric_name='Commodity Price', entity_type='Commodity', entity_id=commodity.code,
        raw_data_ref__status_code=200,
    ).values('observation_date', 'frequency')
    price_periods = {(row['observation_date'], row['frequency']) for row in prices}
    drivers = []
    for category, name, entity_type, entity_id in DRIVERS.get(commodity.code, []):
        rows = NormalizedMetric.objects.filter(
            metric_name=name, entity_type=entity_type, entity_id=entity_id,
            raw_data_ref__status_code=200,
        ).select_related('raw_data_ref')
        aligned = {(row.observation_date, row.frequency) for row in rows
                   if (row.observation_date, row.frequency) in price_periods
                   and row.raw_data_ref.fetched_at.date() <= row.observation_date}
        counts = Counter(frequency for _, frequency in aligned)
        consistent_periods = max(counts.values(), default=0)
        drivers.append({'metric': name, 'category': category,
                        'safe_aligned_periods': consistent_periods,
                        'status': 'ready_for_screening' if consistent_periods >= 12 else 'insufficient_history_or_vintage'})
    return {
        'commodity': commodity.code, 'price_periods': len(price_periods),
        'minimum_periods': 12, 'drivers': drivers,
        'status': 'ready_for_screening' if any(d['status'] == 'ready_for_screening' for d in drivers) else 'blocked',
        'note': 'Screening readiness only; publication/vintage dates, unit consistency, license and out-of-sample tests still require review.',
    }
