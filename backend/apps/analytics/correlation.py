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
    fields = ('observation_date', 'value', 'frequency', 'unit', 'transformation')
    prices = list(NormalizedMetric.objects.filter(
        metric_name='Commodity Price', entity_type=NormalizedMetric.EntityType.COMMODITY,
        entity_id=commodity.code, raw_data_ref__status_code=200,
    ).values(*fields))
    driver_rows = list(NormalizedMetric.objects.filter(
        metric_name=driver.name, raw_data_ref__status_code=200,
        entity_type__in=[NormalizedMetric.EntityType.COMMODITY, NormalizedMetric.EntityType.MACRO],
    ).values(*fields))
    latest = NormalizedMetric.objects.filter(
        metric_name=driver.name, raw_data_ref__status_code=200,
        entity_type__in=[NormalizedMetric.EntityType.COMMODITY, NormalizedMetric.EntityType.MACRO],
    ).order_by('-observation_date', '-id').first()
    allowed_transforms = {'Return', 'Log Return', 'Pct Change', 'YoY %'}
    metadata_valid = (
        len({row['frequency'] for row in prices}) == 1
        and {row['frequency'] for row in prices} == {row['frequency'] for row in driver_rows}
        and len({row['unit'] for row in prices}) == 1 and all(row['unit'] for row in prices)
        and len({row['unit'] for row in driver_rows}) == 1 and all(row['unit'] for row in driver_rows)
        and all(row['transformation'] in allowed_transforms for row in prices + driver_rows)
    )
    price_by_date = {row['observation_date']: float(row['value']) for row in prices}
    matched_pairs = [(price_by_date[row['observation_date']], float(row['value']))
                     for row in driver_rows if row['observation_date'] in price_by_date]
    pairs = matched_pairs if metadata_valid else []
    score = pearson([pair[0] for pair in pairs], [pair[1] for pair in pairs]) if len(pairs) >= 12 else None
    driver.correlation_score = score
    driver.confidence = 'Medium' if score is not None else 'Low'
    driver.evidence = latest
    driver.save(update_fields=['correlation_score', 'confidence', 'evidence'])
    return {
        'correlation_score': score,
        'observations': len(matched_pairs),
        'confidence': driver.confidence,
        'status': 'screened' if score is not None else 'insufficient_or_incompatible_data',
    }
