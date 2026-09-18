from apps.evidence.models import NormalizedMetric
from django.db.models import Q


EXPOSURE_METRICS = ('Commodity Revenue Share', 'Production Dependency', 'Sales Dependency')
RESILIENCE_METRICS = ('Reserve Coverage', 'Production Stability', 'Site Diversification', 'Sales Diversification', 'DER', 'ROE')
FUNDAMENTAL_METRICS = ('Revenue Growth', 'Net Income Growth', 'ROE', 'DER', 'PE', 'PB')


def build_company_snapshot(company, commodity):
    observations = NormalizedMetric.objects.filter(
        entity_type=NormalizedMetric.EntityType.COMPANY,
        entity_id=company.ticker,
        raw_data_ref__status_code=200,
    ).filter(Q(commodity=commodity) | Q(commodity__isnull=True)).order_by('-observation_date', '-id')
    latest = {}
    for row in observations:
        if row.metric_name in EXPOSURE_METRICS and row.commodity_id != commodity.id:
            continue
        latest.setdefault(row.metric_name, row)

    def observed(name, unit=None):
        row = latest.get(name)
        if row is None or (unit and row.unit != unit):
            return None
        if unit == '%' and not 0 <= row.value <= 100:
            return None
        return {
            'value': row.value,
            'unit': row.unit,
            'date': row.observation_date,
            'source': row.source,
            'confidence': row.confidence,
            'is_proxy': row.is_proxy,
            'evidence_id': row.id,
        }

    exposure = {name: observed(name, '%') for name in EXPOSURE_METRICS}
    selected = next((name for name in EXPOSURE_METRICS if exposure[name] is not None), None)
    return {
        'exposure': {
            'status': 'provisional' if selected else 'unavailable',
            'basis': selected,
            'observation': exposure[selected] if selected else None,
            'analysis_confidence': ('Low' if selected != 'Commodity Revenue Share' else exposure[selected]['confidence']) if selected else 'Unavailable',
            'proxy_used': bool(selected and selected != 'Commodity Revenue Share'),
            'components': exposure,
            'score': None,
        },
        'resilience': {
            'status': 'partial_evidence' if any(observed(name) for name in RESILIENCE_METRICS) else 'unavailable',
            'components': {name: observed(name) for name in RESILIENCE_METRICS},
            'score': None,
        },
        'fundamentals': {name: observed(name) for name in FUNDAMENTAL_METRICS},
    }
