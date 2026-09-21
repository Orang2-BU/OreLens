from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.commodities.models import Commodity
from apps.evidence.models import DataAuditItem, NormalizedMetric, RawDataLog
from apps.integrations.clients.worldbank import WorldBankClient


METRIC = 'Indonesia Coal Production'
ENDPOINT = '/country/IDN/indicator/EG.ELC.COAL.ZS'
DATE_RANGE = '2000:2024'


def ingest_coal_production(payload, raw_log):
    if not isinstance(payload, list) or len(payload) != 2 or not isinstance(payload[1], list):
        raise ValueError('Unexpected World Bank response shape')
    rows = payload[1]
    if not rows or any(row.get('indicator', {}).get('id') != 'EG.ELC.COAL.ZS' or row.get('countryiso3code') != 'IDN' for row in rows):
        raise ValueError('World Bank indicator/country mismatch or empty response')
    missing = sum(row.get('value') is None for row in rows)
    usable = [row for row in rows if row.get('value') is not None]
    if not usable:
        raise ValueError('No usable World Bank observations')
    coal = Commodity.objects.get(code='COAL')
    with transaction.atomic():
        for row in usable:
            observed = date(int(row['date']), 12, 31)
            NormalizedMetric.objects.update_or_create(
                metric_name=METRIC, entity_type=NormalizedMetric.EntityType.COMMODITY,
                entity_id='COAL', commodity=coal, source='World Bank', observation_date=observed,
                defaults={
                    'definition': 'Coal production (% of total), World Bank indicator EG.ELC.COAL.ZS',
                    'frequency': 'Annual', 'unit': '% of total', 'original_unit': '%',
                    'transformation': 'None', 'priority': 'High', 'confidence': 'Medium',
                    'value': Decimal(str(row['value'])), 'raw_data_ref': raw_log,
                },
            )
        years = sorted(int(row['date']) for row in usable)
        DataAuditItem.objects.update_or_create(
            metric=METRIC, source='World Bank',
            defaults={
                'available': 'Yes', 'endpoint': ENDPOINT,
                'earliest_date': date(years[0], 12, 31), 'latest_date': date(years[-1], 12, 31),
                'frequency': 'Annual', 'unit': '% of total',
                'missing_values': f'{missing}/{len(rows)} ({missing / len(rows):.1%})',
                'historical_depth': f'{len(usable)} annual observations in {DATE_RANGE}',
                'cost_rate_limit': 'Not verified',
                'notes': 'Live API response; license/rate limit and analytics readiness pending verification. '
                         'Commodity context for thermal coal (COAL), not validated for scoring.',
            },
        )
    return len(usable), missing


class Command(BaseCommand):
    help = 'Ingest audited Indonesia coal production observations from World Bank (2000-2024).'

    def handle(self, *args, **options):
        payload = WorldBankClient().get_country_indicator('IDN', 'EG.ELC.COAL.ZS', DATE_RANGE)
        raw_log = RawDataLog.objects.filter(source='World Bank', endpoint=ENDPOINT).first()
        if not raw_log or raw_log.status_code != 200:
            raise CommandError('World Bank request failed; no metrics written')
        try:
            count, missing = ingest_coal_production(payload, raw_log)
        except (ValueError, TypeError, KeyError) as exc:
            raise CommandError(f'Invalid World Bank data: {exc}') from exc
        self.stdout.write(self.style.SUCCESS(f'Coal Production: {count} observations, {missing} missing; upsert complete'))
