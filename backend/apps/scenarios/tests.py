from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.commodities.models import Commodity
from apps.scenarios.models import Scenario, ScenarioInput, ScenarioResult
from apps.evidence.models import RawDataLog, NormalizedMetric


class ScenarioApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.commodity = Commodity.objects.create(
            code='COAL',
            name='Thermal Coal',
            category=Commodity.Category.ENERGY,
            benchmark_unit='USD/mt',
            current_price=138.50
        )
        self.scenario = Scenario.objects.create(
            name='China Demand +15% Scenario',
            description='What-if China thermal coal imports increase 15% YoY',
            commodity=self.commodity,
            status='Active'
        )
        self.scenario_input = ScenarioInput.objects.create(
            scenario=self.scenario,
            driver_name='China Coal Imports',
            original_value='450 million tons',
            adjusted_value='517.5 million tons',
            adjustment_pct=15.0,
            notes='Assumption: stable supply, no policy change'
        )
        self.scenario_result = ScenarioResult.objects.create(
            scenario=self.scenario,
            estimated_price_impact_pct=8.5,
            estimated_new_price=150.25,
            confidence_interval_lower=145.00,
            confidence_interval_upper=155.00,
            methodology='Sensitivity Analysis (Preliminary)',
            warnings='Model not validated. Result is illustrative only.'
        )

    def test_list_scenarios(self):
        response = self.client.get('/api/v1/scenarios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_scenario_detail(self):
        response = self.client.get(f'/api/v1/scenarios/{self.scenario.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'China Demand +15% Scenario')

    def test_list_scenario_inputs(self):
        response = self.client.get('/api/v1/scenario-inputs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_inputs_by_scenario(self):
        response = self.client.get(f'/api/v1/scenario-inputs/?scenario={self.scenario.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_scenario_results(self):
        response = self.client.get('/api/v1/scenario-results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_run_scenario_persists_evidence_backed_arithmetic_result(self):
        log = RawDataLog.objects.create(source='World Bank', endpoint='/gdp', status_code=200)
        metric = NormalizedMetric.objects.create(metric_name='China GDP Growth', definition='GDP growth',
            entity_type='Macro', entity_id='CHN', source='World Bank', frequency='Annual', unit='%',
            observation_date='2025-12-31', value=5, raw_data_ref=log)
        response = self.client.post(f'/api/v1/scenarios/{self.scenario.id}/run/',
            {'metric_name': 'China GDP Growth', 'shock_pct': 10}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ScenarioInput.objects.filter(scenario=self.scenario).count(), 1)
        result = ScenarioResult.objects.get(scenario=self.scenario)
        self.assertIsNone(result.estimated_price_impact_pct)
        self.assertIsNone(result.estimated_new_price)
        self.assertIn('Arithmetic preview', result.methodology)
        self.assertIn(str(metric.id), result.warnings + self.scenario.inputs.first().notes)
