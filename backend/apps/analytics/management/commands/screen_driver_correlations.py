from django.core.management.base import BaseCommand

from apps.analytics.correlation import screen_driver
from apps.commodities.models import Commodity, CommodityDriver
from apps.intelligence.commodity_snapshot import DRIVERS


class Command(BaseCommand):
    help = 'Screen evidence-backed commodity driver correlations and persist preliminary values.'

    def add_arguments(self, parser):
        parser.add_argument('--commodity', dest='commodity_code')

    def handle(self, *args, **options):
        commodities = Commodity.objects.filter(code=options['commodity_code']) if options['commodity_code'] else Commodity.objects.all()
        for commodity in commodities:
            defined = {name: category for category, name, _, _ in DRIVERS.get(commodity.code, [])}
            for name, category in defined.items():
                driver, _ = CommodityDriver.objects.get_or_create(
                    commodity=commodity, name=name,
                    defaults={'driver_type': category.upper(), 'description': f'{category} driver from Data Dictionary', 'source': 'NormalizedMetric'},
                )
                result = screen_driver(commodity, driver)
                self.stdout.write(f'{commodity.code}/{driver.name}: {result}')
