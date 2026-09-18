"""
Tests untuk analytics normalization functions.
"""
from django.test import TestCase
from .normalization import (
    calculate_yoy_growth,
    calculate_hhi,
    calculate_reserve_coverage,
    peer_percentile
)


class NormalizationTests(TestCase):

    def test_yoy_growth_positive(self):
        result = calculate_yoy_growth(110, 100)
        self.assertAlmostEqual(result, 0.10)

    def test_yoy_growth_negative(self):
        result = calculate_yoy_growth(90, 100)
        self.assertAlmostEqual(result, -0.10)

    def test_yoy_growth_zero_previous(self):
        result = calculate_yoy_growth(100, 0)
        self.assertIsNone(result)

    def test_hhi_concentrated(self):
        # One player dominates: 80%, 10%, 10%
        result = calculate_hhi([0.80, 0.10, 0.10])
        self.assertAlmostEqual(result, 0.66, places=2)

    def test_hhi_diversified(self):
        # Four equal players: 25% each
        result = calculate_hhi([0.25, 0.25, 0.25, 0.25])
        self.assertEqual(result, 0.25)

    def test_hhi_empty(self):
        result = calculate_hhi([])
        self.assertIsNone(result)

    def test_reserve_coverage(self):
        result = calculate_reserve_coverage(840, 100)
        self.assertAlmostEqual(result, 8.4)

    def test_reserve_coverage_zero_production(self):
        result = calculate_reserve_coverage(1000, 0)
        self.assertIsNone(result)

    def test_peer_percentile_median(self):
        # value 50 is median in [10, 30, 50, 70, 90]
        result = peer_percentile(50, [10, 30, 50, 70, 90])
        self.assertEqual(result, 60.0)

    def test_peer_percentile_highest(self):
        result = peer_percentile(100, [10, 30, 50, 70])
        self.assertEqual(result, 100.0)

    def test_peer_percentile_lowest(self):
        result = peer_percentile(5, [10, 30, 50, 70])
        self.assertEqual(result, 0.0)
