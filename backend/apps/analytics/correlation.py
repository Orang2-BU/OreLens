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
    matched = sorted((row['observation_date'], price_by_date[row['observation_date']], float(row['value']))
                     for row in driver_rows if row['observation_date'] in price_by_date)
    pairs = [(price, value) for _, price, value in matched] if metadata_valid else []
    score = pearson([pair[0] for pair in pairs], [pair[1] for pair in pairs]) if len(pairs) >= 12 else None
    rolling = [pearson([pair[0] for pair in pairs[i:i + 12]], [pair[1] for pair in pairs[i:i + 12]])
               for i in range(len(pairs) - 11)]
    split = int(len(pairs) * .7)
    train = pearson([pair[0] for pair in pairs[:split]], [pair[1] for pair in pairs[:split]]) if split >= 3 else None
    test = pearson([pair[0] for pair in pairs[split:]], [pair[1] for pair in pairs[split:]]) if len(pairs) - split >= 3 else None
    rolling_valid = [value for value in rolling if value is not None]
    same_sign_ratio = (sum(1 for value in rolling_valid if score is not None and value * score >= 0) / len(rolling_valid)) if rolling_valid else 0
    stable = bool(score is not None and train is not None and test is not None
                  and abs(score) >= .1 and same_sign_ratio >= .7
                  and score * train >= 0 and score * test >= 0
                  and abs(score - train) <= .5 and abs(score - test) <= .5)
    details = {
        'observations': len(matched), 'window': 12,
        'rolling_correlations': rolling, 'train_correlation': train,
        'test_correlation': test, 'split_index': split,
        'same_sign_ratio': round(same_sign_ratio, 4),
        'stable': stable, 'metadata_valid': metadata_valid,
    }
    driver.correlation_score = score
    driver.confidence = 'Medium' if stable else 'Low'
    driver.evidence = latest
    driver.validation_details = details
    driver.save(update_fields=['correlation_score', 'confidence', 'evidence', 'validation_details'])
    return {
        'correlation_score': score,
        'observations': len(matched),
        'confidence': driver.confidence,
        'status': 'stable' if stable else ('negligible_or_unstable' if score is not None else 'insufficient_or_incompatible_data'),
        'validation': details,
    }
