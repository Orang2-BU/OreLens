"""
Normalization utilities untuk metric transformation.
Implementasi sesuai Data Dictionary v0.1.
"""


def calculate_yoy_growth(current: float, previous: float) -> float:
    """
    YoY Growth = (Current - Previous) / Previous

    Returns: growth rate as decimal (e.g., 0.05 for 5% growth)
    """
    if previous == 0 or previous is None:
        return None
    return (current - previous) / previous


def calculate_hhi(shares: list[float]) -> float:
    """
    Herfindahl-Hirschman Index = Σ share_i²

    Args:
        shares: list of market shares as decimals (e.g., [0.30, 0.25, 0.20, ...])

    Returns: HHI value between 0 and 1 (1 = complete concentration)
    """
    if not shares:
        return None
    return sum(s ** 2 for s in shares)


def calculate_reserve_coverage(reserves: float, annual_production: float) -> float:
    """
    Reserve Coverage = Reserves / Annual Production

    Note: This is a comparative indicator, not literal mine life.

    Returns: ratio (e.g., 8.4 means 8.4x annual production)
    """
    if annual_production == 0 or annual_production is None:
        return None
    return reserves / annual_production


def peer_percentile(value: float, peer_values: list[float]) -> float:
    """
    Calculate percentile rank within peer group.

    Returns: percentile (0-100)
    """
    if not peer_values or value is None:
        return None

    sorted_peers = sorted(peer_values)
    rank = sum(1 for v in sorted_peers if v <= value)
    return (rank / len(sorted_peers)) * 100
