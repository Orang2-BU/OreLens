"""
Company commodity exposure calculation logic.
Sesuai Company Engine & Data Dictionary.
"""


def calculate_exposure_score(
    revenue_share_pct: float = None,
    production_dependency_pct: float = None,
    sales_dependency_pct: float = None,
    operational_concentration_hhi: float = None,
) -> tuple[float | None, str]:
    """
    Calculate preliminary exposure score.

    Returns: (score, confidence_level)

    Note: Bobot final menunggu historical validation.
    Fallback rule: jika revenue_share unavailable, gunakan production/sales dependency.
    """
    if revenue_share_pct is not None:
        # High confidence: direct revenue data
        base_score = revenue_share_pct
        confidence = 'High'
    elif production_dependency_pct is not None and sales_dependency_pct is not None:
        # Medium confidence: operational proxy
        base_score = (production_dependency_pct + sales_dependency_pct) / 2
        confidence = 'Medium'
    elif production_dependency_pct is not None:
        # Low confidence: single metric proxy
        base_score = production_dependency_pct
        confidence = 'Low'
    else:
        return (None, 'Unavailable')

    # Adjust for operational concentration if available
    if operational_concentration_hhi is not None and operational_concentration_hhi > 0.5:
        # High operational concentration increases exposure risk
        base_score = min(100, base_score * 1.1)

    return (round(base_score, 2), confidence)
