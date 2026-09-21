
"""
Company resilience calculation logic.
Resilience bukan kebalikan exposure - dimensi terpisah.
"""


def calculate_resilience_score(
    reserve_coverage: float = None,
    debt_to_equity: float = None,
    ebitda_margin: float = None,
    sales_diversification_hhi: float = None,
    allow_partial: bool = False,
) -> tuple[float | None, str]:
    """
    Calculate preliminary resilience score.

    Returns: (score, status_message)

    Note: Bobot & threshold final menunggu backtest.
    If ``allow_partial`` is True, a score is produced from the available
    components and scaled to the 0-100 range so the demo can surface
    partial evidence.
    """
    components = []

    # Reserve coverage (0-25 points)
    if reserve_coverage is not None:
        if reserve_coverage >= 10:
            components.append(25)
        elif reserve_coverage >= 5:
            components.append(15)
        else:
            components.append(5)

    # Leverage (0-25 points, inverse relationship)
    if debt_to_equity is not None:
        if debt_to_equity < 0.5:
            components.append(25)
        elif debt_to_equity < 1.5:
            components.append(15)
        else:
            components.append(5)

    # Profitability (0-25 points)
    if ebitda_margin is not None:
        if ebitda_margin >= 30:
            components.append(25)
        elif ebitda_margin >= 15:
            components.append(15)
        else:
            components.append(5)

    # Sales diversification (0-25 points, inverse HHI)
    if sales_diversification_hhi is not None:
        if sales_diversification_hhi < 0.25:
            components.append(25)
        elif sales_diversification_hhi < 0.50:
            components.append(15)
        else:
            components.append(5)

    if len(components) == 0:
        return (None, 'Unavailable - insufficient metrics')

    if len(components) != 4 and not allow_partial:
        return (None, 'Unavailable - insufficient metrics')

    score = sum(components)
    status = 'Pending Validation - preliminary methodology'
    if len(components) != 4:
        # Scale partial component scores to the 0-100 range.
        score = score * 4 / len(components)
        status = 'Pending Validation - preliminary methodology (partial evidence)'

    return (round(score, 2), status)
