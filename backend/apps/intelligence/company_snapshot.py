
from apps.evidence.models import NormalizedMetric
from django.db.models import Q
from apps.companies.models import CompanyCommodityExposure, CompanyResilience
from apps.analytics.normalization import peer_percentile
from .exposure import calculate_exposure_score
from .resilience import calculate_resilience_score


EXPOSURE_METRICS = ('Commodity Revenue Share', 'Production Dependency', 'Sales Dependency', 'Operational Concentration HHI')
RESILIENCE_METRICS = ('Reserve Coverage', 'Reserves', 'Annual Production', 'DER', 'EBITDA Margin', 'Sales Diversification HHI')
FUNDAMENTAL_METRICS = ('Revenue Growth', 'Net Income Growth', 'ROE', 'DER', 'PE', 'PB')


def _to_float(value):
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _metric_component(latest, name):
    row = latest.get(name)
    if row is None:
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

    exposure_components = {
        name: observed(name, '%') if name != 'Operational Concentration HHI' else observed(name)
        for name in EXPOSURE_METRICS
    }
    selected = next((name for name in EXPOSURE_METRICS if exposure_components[name] is not None), None)

    # Fallback to seeded revenue share when no observed primary metric exists.
    fallback_used = False
    if exposure_components['Commodity Revenue Share'] is None:
        seed = CompanyCommodityExposure.objects.filter(company=company, commodity=commodity).first()
        if seed is not None and seed.revenue_share_pct is not None:
            exposure_components['Commodity Revenue Share'] = {
                'value': seed.revenue_share_pct,
                'unit': '%',
                'date': None,
                'source': 'CompanyCommodityExposure (seeded)',
                'confidence': 'Low',
                'is_proxy': True,
                'evidence_id': None,
            }
            fallback_used = True

    exposure_score, exposure_confidence = calculate_exposure_score(
        revenue_share_pct=_to_float(exposure_components['Commodity Revenue Share']['value']) if exposure_components['Commodity Revenue Share'] else None,
        production_dependency_pct=_to_float(exposure_components['Production Dependency']['value']) if exposure_components['Production Dependency'] else None,
        sales_dependency_pct=_to_float(exposure_components['Sales Dependency']['value']) if exposure_components['Sales Dependency'] else None,
        operational_concentration_hhi=_to_float(exposure_components['Operational Concentration HHI']['value']) if exposure_components['Operational Concentration HHI'] else None,
    )

    # Resilience inputs
    reserve_component = _metric_component(latest, 'Reserve Coverage')
    reserve_coverage = None
    if reserve_component is not None:
        reserve_coverage = _to_float(reserve_component['value'])
    else:
        reserves = _metric_component(latest, 'Reserves')
        production = _metric_component(latest, 'Annual Production')
        if reserves is not None and production is not None:
            denom = _to_float(production['value'])
            num = _to_float(reserves['value'])
            if denom and num is not None and denom != 0:
                reserve_coverage = num / denom
                reserve_component = {
                    'value': reserve_coverage,
                    'unit': 'years',
                    'date': None,
                    'source': 'Computed from Reserves / Annual Production',
                    'confidence': 'Low',
                    'is_proxy': True,
                    'evidence_id': None,
                }

    der_component = _metric_component(latest, 'DER')
    ebitda_component = _metric_component(latest, 'EBITDA Margin')
    hhi_component = _metric_component(latest, 'Sales Diversification HHI')

    debt_to_equity = _to_float(der_component['value']) if der_component is not None else None
    ebitda_margin = _to_float(ebitda_component['value']) if ebitda_component is not None else None
    sales_diversification_hhi = _to_float(hhi_component['value']) if hhi_component is not None else None

    # Fallback to seeded relational data.
    resilience_seed = CompanyResilience.objects.filter(company=company).first()
    seeded_resilience = False
    if resilience_seed is not None:
        if debt_to_equity is None:
            debt_to_equity = _to_float(resilience_seed.debt_to_equity)
        if ebitda_margin is None:
            ebitda_margin = _to_float(resilience_seed.ebitda_margin)
        if reserve_coverage is None and resilience_seed.reserve_life_years is not None:
            # Map seeded reserve life to reserve coverage only when production
            # data is available, so the value has a meaningful context.
            if 'Annual Production' in latest:
                reserve_coverage = _to_float(resilience_seed.reserve_life_years)

    def _resilience_component(value, observed_component):
        nonlocal seeded_resilience
        if value is None:
            return None
        if observed_component is not None:
            return observed_component
        # Seeded fallback
        seeded_resilience = True
        return {
            'value': value,
            'unit': '',
            'date': None,
            'source': 'CompanyResilience (seeded)',
            'confidence': 'Low',
            'is_proxy': True,
            'evidence_id': None,
        }

    resilience_components = {
        'Reserve Coverage': _resilience_component(reserve_coverage, reserve_component),
        'DER': _resilience_component(debt_to_equity, der_component),
        'EBITDA Margin': _resilience_component(ebitda_margin, ebitda_component),
        'Sales Diversification HHI': _resilience_component(sales_diversification_hhi, hhi_component),
    }

    resilience_score, resilience_status = calculate_resilience_score(
        reserve_coverage=reserve_coverage,
        debt_to_equity=debt_to_equity,
        ebitda_margin=ebitda_margin,
        sales_diversification_hhi=sales_diversification_hhi,
        allow_partial=True,
    )

    if resilience_score is not None and seeded_resilience:
        resilience_status += ' (demo fallback)'

    if resilience_score is None:
        if any(v is not None for v in (reserve_coverage, debt_to_equity, ebitda_margin, sales_diversification_hhi)):
            resilience_status = 'partial_evidence'
        else:
            resilience_status = 'unavailable'

    # Peer comparison (unchanged)
    peer_tickers = list(CompanyCommodityExposure.objects.filter(
        commodity=commodity, company__is_active=True,
    ).values_list('company__ticker', flat=True))
    peer_comparison = {}
    for name in FUNDAMENTAL_METRICS:
        own = latest.get(name)
        if own is None or own.commodity_id is not None or company.ticker not in peer_tickers:
            peer_comparison[name] = None
            continue
        rows = NormalizedMetric.objects.filter(
            metric_name=name, entity_type=NormalizedMetric.EntityType.COMPANY,
            entity_id__in=peer_tickers, commodity__isnull=True,
            observation_date=own.observation_date, frequency=own.frequency,
            unit=own.unit, transformation=own.transformation,
            source=own.source, definition=own.definition,
            raw_data_ref__status_code=200,
        ).order_by('entity_id', '-id')
        peers = {}
        for row in rows:
            peers.setdefault(row.entity_id, row)
        if len(peers) < 3 or company.ticker not in peers:
            peer_comparison[name] = None
            continue
        peer_values = [r.value for r in peers.values()]
        peer_comparison[name] = {
            'value': own.value,
            'unit': own.unit,
            'percentile_rank': peer_percentile(own.value, peer_values),
            'peer_count': len(peer_values),
            'date': own.observation_date,
            'source': own.source,
            'frequency': own.frequency,
            'interpretation': 'numeric_rank_not_quality_score',
        }

    if exposure_score is not None:
        exposure_score_status = 'Pending Validation - preliminary methodology'
        if fallback_used:
            exposure_score_status += ' (demo fallback)'
    else:
        exposure_score_status = 'unavailable'

    return {
        'exposure': {
            'status': ('provisional' if (selected or fallback_used) else 'unavailable'),
            'basis': 'Commodity Revenue Share' if fallback_used else selected,
            'observation': exposure_components['Commodity Revenue Share'] if fallback_used else (exposure_components[selected] if selected else None),
            'analysis_confidence': (
                ('Low' if fallback_used else exposure_confidence)
                if exposure_score is not None
                else (('Low' if selected != 'Commodity Revenue Share' else exposure_components[selected]['confidence']) if selected else 'Unavailable')
            ),
            'proxy_used': bool(fallback_used or (selected and selected != 'Commodity Revenue Share')),
            'components': exposure_components,
            'score': exposure_score,
            'score_status': exposure_score_status,
        },
        'resilience': {
            'status': 'partial_evidence' if any(_metric_component(latest, name) for name in RESILIENCE_METRICS) else 'unavailable',
            'components': resilience_components,
            'score': resilience_score,
            'score_status': resilience_status,
        },
        'fundamentals': {name: observed(name) for name in FUNDAMENTAL_METRICS},
        'peer_comparison': peer_comparison,
    }
