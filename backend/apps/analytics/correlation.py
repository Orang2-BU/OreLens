from math import sqrt

from apps.commodities.models import CommodityDriver
from apps.evidence.models import NormalizedMetric


def pearson(xs, ys):
    if len(xs) < 2 or len(xs) != len(ys):
        return None
    x_mean, y_mean = sum(xs) / len(xs), sum(ys) / len(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    x_var = sum((x - x_mean) ** 2 for x in xs)
    y_var = sum((y - y_mean) ** 2 for y in ys)
    if not x_var or not y_var:
        return None
    return round(numerator / sqrt(x_var * y_var), 6)


def screen_driver(commodity, driver):
    prices = NormalizedMetric.objects.filter(
        metric_name='Commodity Price', entity_type=NormalizedMetric.EntityType.COMMODITY,
        entity_id=commodity.code, raw_data_ref__status_code=200,
    ).values('observation_date', 'value')
    driver_rows = NormalizedMetric.objects.filter(
        metric_name=driver.name, raw_data_ref__status_code=200,
        entity_type__in=[NormalizedMetric.EntityType.COMMODITY, NormalizedMetric.EntityType.MACRO],
    ).values('observation_date', 'value')
    latest = NormalizedMetric.objects.filter(
        metric_name=driver.name, raw_data_ref__status_code=200,
        entity_type__in=[NormalizedMetric.EntityType.COMMODITY, NormalizedMetric.EntityType.MACRO],
    ).order_by('-observation_date', '-id').first()
    price_by_date = {row['observation_date']: float(row['value']) for row in prices}
    pairs = [(price_by_date[row['observation_date']], float(row['value']))
             for row in driver_rows if row['observation_date'] in price_by_date]
    score = pearson([pair[0] for pair in pairs], [pair[1] for pair in pairs])
    driver.correlation_score = score
    driver.confidence = 'Medium' if len(pairs) >= 12 and score is not None else 'Low'
    driver.evidence = latest
    driver.save(update_fields=['correlation_score', 'confidence', 'evidence'])
    return {'correlation_score': score, 'observations': len(pairs), 'confidence': driver.confidence}
