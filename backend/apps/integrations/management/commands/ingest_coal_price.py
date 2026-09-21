import csv
import io
from datetime import date
from decimal import Decimal

import requests
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.commodities.models import Commodity
from apps.evidence.models import DataAuditItem, NormalizedMetric, RawDataLog


SERIES_ID = 'PCOALAUUSDA'
URL = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}'


def ingest_coal_price(rows, raw_log):
    usable = [(int((row.get('observation_date') or row.get('DATE'))[:4]), Decimal(row[SERIES_ID]))
              for row in rows if row.get(SERIES_ID) not in (None, '', '.') and (row.get('observation_date') or row.get('DATE'))]
    if len(usable) < 2:
        raise ValueError('FRED coal price series has insufficient usable observations')
    coal = Commodity.objects.get(code='COAL')
    with transaction.atomic():
        for (previous_year, previous), (year, current) in zip(usable, usable[1:]):
            if year != previous_year + 1 or previous == 0:
                continue
            annual_return = (current - previous) / previous * 100
            NormalizedMetric.objects.update_or_create(
                metric_name='Commodity Price', entity_type='Commodity', entity_id='COAL',
                commodity=coal, source='FRED/IMF', observation_date=date(year, 12, 31),
                defaults={
                    'definition': 'Annual return of IMF/FRED Global price of Coal, Australia (PCOALAUUSDA)',
                    'frequency': 'Annual', 'unit': '%', 'original_unit': 'USD/metric ton',
                    'transformation': 'Return', 'priority': 'High', 'confidence': 'High',
                    'value': annual_return, 'raw_data_ref': raw_log,
                },
            )
        years = [year for year, _ in usable]
        DataAuditItem.objects.update_or_create(
            metric='Commodity Price', source='FRED/IMF',
            defaults={
                'available': 'Yes', 'endpoint': URL,
                'earliest_date': date(min(years), 12, 31), 'latest_date': date(max(years), 12, 31),
                'frequency': 'Annual', 'unit': 'USD/metric ton; normalized to annual return %',
                'missing_values': f'{len(rows) - len(usable)}/{len(rows)}',
                'historical_depth': f'{len(usable)} annual price levels',
                'cost_rate_limit': 'Public FRED CSV; precise rate limit not verified',
                'notes': 'IMF global benchmark price distributed by FRED. Correlation uses annual returns, not price levels.',
            },
        )
    return len(usable) - 1


class Command(BaseCommand):
    help = 'Ingest annual Australian benchmark coal-price returns from FRED/IMF.'

    def handle(self, *args, **options):
        try:
            response = requests.get(URL, timeout=20)
            response.raise_for_status()
            rows = list(csv.DictReader(io.StringIO(response.text)))
        except (requests.RequestException, csv.Error) as exc:
            raise CommandError(f'FRED coal price fetch failed: {exc}') from exc
        raw_log = RawDataLog.objects.create(
            source='FRED', endpoint=URL, request_params={'series_id': SERIES_ID},
            response_payload={'series_id': SERIES_ID, 'rows': rows}, status_code=response.status_code,
        )
        try:
            count = ingest_coal_price(rows, raw_log)
        except (ValueError, KeyError, ArithmeticError) as exc:
            raise CommandError(f'Invalid FRED coal price data: {exc}') from exc
        self.stdout.write(self.style.SUCCESS(f'Coal price: {count} annual returns; upsert complete'))
