"""
Company resilience calculation logic.
Resilience bukan kebalikan exposure - dimensi terpisah.
"""


def calculate_resilience_score(
    reserve_coverage: float = None,
    debt_to_equity: float = None,
    ebitda_margin: float = None,
    sales_diversification_hhi: float = None,
) -> tuple[float | None, str]:
    """
    Calculate preliminary resilience score.

    Returns: (score, status_message)

    Note: Bobot & threshold final menunggu backtest.
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

    if len(components) != 4:
        return (None, 'Unavailable - insufficient metrics')

    score = sum(components)
    status = 'Pending Validation - preliminary methodology'

    return (round(score, 2), status)
