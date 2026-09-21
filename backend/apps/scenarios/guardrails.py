from apps.evidence.models import NormalizedMetric


def percentile(values, percentile):
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def historical_shock_bounds(metric_name, entity_type, entity_id):
    history = NormalizedMetric.objects.filter(
        metric_name=metric_name, entity_type=entity_type, entity_id=entity_id,
        raw_data_ref__status_code=200,
    ).select_related('raw_data_ref').order_by('observation_date', 'id')
    latest = history.last()
    if latest is None:
        return [], None
    history = list(history.filter(
        frequency=latest.frequency, unit=latest.unit, transformation=latest.transformation,
    ))
    changes = [
        (float(current.value) - float(previous.value)) / abs(float(previous.value)) * 100
        for previous, current in zip(history, history[1:]) if previous.value != 0
    ]
    if len(changes) < 12:
        return history, None
    return history, (percentile(changes, .05), percentile(changes, .95))
