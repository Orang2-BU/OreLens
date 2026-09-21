from apps.evidence.models import NormalizedMetric
from apps.commodities.models import CommodityDriver


# Hypotheses from DATA_DICTIONARY.md, not statistically validated driver weights.
DRIVERS = {
    'COAL': [('supply', 'Indonesia Coal Production', 'Commodity', 'COAL'),
             ('demand', 'China Coal Imports', 'Commodity', 'COAL'),
             ('macro', 'China GDP Growth', 'Macro', 'CHN')],
    'GOLD': [('supply', 'Global Gold Production', 'Commodity', 'GOLD'),
             ('demand', 'Central Bank Gold Demand', 'Commodity', 'GOLD'),
             ('macro', 'Real Interest Rate', 'Macro', 'USA')],
    'NICKEL': [('supply', 'Indonesia Nickel Production', 'Commodity', 'NICKEL'),
               ('demand', 'China Nickel Imports', 'Commodity', 'NICKEL'),
               ('macro', 'China GDP Growth', 'Macro', 'CHN')],
    'COPPER': [('supply', 'Global Copper Production', 'Commodity', 'COPPER'),
               ('demand', 'China Copper Imports', 'Commodity', 'COPPER'),
               ('macro', 'China GDP Growth', 'Macro', 'CHN')],
}


def build_driver_map(commodity):
    drivers = []
    for category, name, entity_type, entity_id in DRIVERS.get(commodity.code, []):
        row = NormalizedMetric.objects.filter(
            metric_name=name, entity_type=entity_type, entity_id=entity_id,
            raw_data_ref__status_code=200,
        ).order_by('-observation_date', '-id').first()
        persisted = CommodityDriver.objects.filter(commodity=commodity, name=name).first()
        drivers.append({
            'category': category, 'metric': name,
            'status': 'observed_context' if row else 'unavailable',
            'latest': ({'value': row.value, 'unit': row.unit, 'date': row.observation_date,
                        'source': row.source, 'confidence': row.confidence,
                        'is_proxy': row.is_proxy, 'evidence_id': row.id} if row else None),
            'importance': abs(persisted.correlation_score) if persisted and persisted.correlation_score is not None and persisted.confidence != 'Low' else None,
            'correlation_score': persisted.correlation_score if persisted else None,
            'correlation_confidence': persisted.confidence if persisted else None,
            'validation': persisted.validation_details if persisted else {},
        })
    has_valid_correlation = any(
        item['correlation_score'] is not None
        and item.get('correlation_confidence') != 'Low'
        and abs(item['correlation_score']) >= 0.10
        for item in drivers
    )
    return {
        'status': 'preliminary_correlation' if has_valid_correlation else 'hypotheses_not_validated',
        'drivers': drivers,
        'event_policy': {'status': 'qualitative_only', 'importance': None}
    }


def preview_driver_shock(commodity, metric_name, shock_pct):
    import math

    if isinstance(shock_pct, bool) or not isinstance(shock_pct, (int, float)) or not math.isfinite(shock_pct):
        raise ValueError('shock_pct must be a finite number')
    if shock_pct < -100:
        raise ValueError('shock_pct cannot be below -100%')
    driver = next((item for item in build_driver_map(commodity)['drivers']
                   if item['metric'] == metric_name and item['latest']), None)
    if driver is None:
        raise ValueError('Metric has no traceable observation for this commodity')
    observed = driver['latest']
    baseline = float(observed['value'])
    adjusted = baseline * (1 + shock_pct / 100)
    if not math.isfinite(adjusted):
        raise ValueError('Adjusted value is outside supported range')

    # Use the same relative-change distribution as a persisted scenario run.
    from apps.scenarios.guardrails import historical_shock_bounds
    driver_spec = next(item for item in DRIVERS[commodity.code] if item[1] == metric_name)
    _, _, entity_type, entity_id = driver_spec
    _, shock_bounds = historical_shock_bounds(metric_name, entity_type, entity_id)

    guardrail = {
        'status': 'uncalibrated_bounds',
        'p05': None,
        'p95': None,
        'warning': 'Insufficient historical observations (< 12) to compute empirical P05-P95 bounds.'
    }
    if shock_bounds is not None:
        p05, p95 = (round(value, 2) for value in shock_bounds)
        is_outside = shock_pct < p05 or shock_pct > p95
        guardrail = {
            'status': 'outside_historical_range' if is_outside else 'within_historical_range',
            'p05': p05,
            'p95': p95,
            'warning': (
                f"Shock ({shock_pct}%) is outside historical P05-P95 range ({p05}% to {p95}%). Extreme tail shock assumption."
                if is_outside else None
            )
        }

    return {
        'metric': metric_name,
        'baseline': observed,
        'shock_pct': shock_pct,
        'adjusted_value': round(adjusted, 4),
        'status': 'arithmetic_preview_only',
        'estimated_price_impact_pct': None,
        'guardrail': guardrail,
        'is_deprecated': True,
        'deprecation_notice': 'This endpoint provides arithmetic preview only. Use /api/v1/scenarios/{id}/run/ for audited scenario modeling.',
        'warning': 'Mechanical change to driver assumption; no calibrated price sensitivity or forecast.',
    }
