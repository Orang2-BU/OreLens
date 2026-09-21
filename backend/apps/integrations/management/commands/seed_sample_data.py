from datetime import date, timedelta
import random
from django.core.management.base import BaseCommand
from apps.commodities.models import Commodity, CommodityPriceSeries, CommodityDriver
from apps.companies.models import Company, CompanyCommodityExposure, CompanyResilience
from apps.evidence.models import NormalizedMetric, DataAuditItem, RawDataLog
from apps.scenarios.models import Scenario, ScenarioInput, ScenarioResult


class Command(BaseCommand):
    help = 'Seed sample commodity, company, driver, evidence, and scenario data for OreLens MVP.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting OreLens database seeding...'))

        # 1. Seed Commodities
        commodities_data = [
            {
                'code': 'COAL',
                'name': 'Thermal Coal',
                'category': Commodity.Category.ENERGY,
                'description': 'Newcastle Thermal Coal benchmark (6000 kcal/kg NAR). Major export commodity for Indonesia.',
                'benchmark_unit': 'USD/mt',
                'current_price': 138.50,
                'price_change_pct_24h': 1.25,
                'price_change_pct_ytd': -8.40,
            },
            {
                'code': 'GOLD',
                'name': 'Gold',
                'category': Commodity.Category.PRECIOUS_METALS,
                'description': 'London Bullion Market spot gold price. Global safe haven asset and inflation hedge.',
                'benchmark_unit': 'USD/troy oz',
                'current_price': 2520.00,
                'price_change_pct_24h': 0.45,
                'price_change_pct_ytd': 21.80,
            },
            {
                'code': 'NICKEL',
                'name': 'Class 1 Nickel',
                'category': Commodity.Category.BATTERY_METALS,
                'description': 'LME Nickel cash settlement price. Critical input for EV batteries and stainless steel.',
                'benchmark_unit': 'USD/mt',
                'current_price': 16450.00,
                'price_change_pct_24h': -0.85,
                'price_change_pct_ytd': -5.10,
            },
            {
                'code': 'COPPER',
                'name': 'Grade A Copper',
                'category': Commodity.Category.INDUSTRIAL_METALS,
                'description': 'LME Copper cash settlement price. Bellwether for global industrial and energy transition demand.',
                'benchmark_unit': 'USD/mt',
                'current_price': 9230.00,
                'price_change_pct_24h': 0.90,
                'price_change_pct_ytd': 7.60,
            },
        ]

        commodities_map = {}
        for cdata in commodities_data:
            c, _ = Commodity.objects.update_or_create(code=cdata['code'], defaults=cdata)
            commodities_map[c.code] = c

            # Seed 30 days price history
            base_price = float(c.current_price)
            today = date.today()
            for i in range(30, -1, -1):
                obs_date = today - timedelta(days=i)
                variation = random.uniform(-0.02, 0.02)
                p_val = round(base_price * (1 + (variation * (30 - i) / 30)), 2)
                CommodityPriceSeries.objects.update_or_create(
                    commodity=c,
                    date=obs_date,
                    defaults={'price': p_val, 'source': 'World Bank Pink Sheet'}
                )

        # 2. Seed Commodity Drivers
        drivers_data = [
            # Coal Drivers
            {
                'commodity': commodities_map['COAL'],
                'name': 'China Power Generation & Thermal Plant Consumption',
                'driver_type': CommodityDriver.DriverType.DEMAND,
                'description': 'China power generation demand drives over 50% of seaborne thermal coal import volume.',
                'impact_direction': CommodityDriver.ImpactDirection.POSITIVE,
                'correlation_score': 0.74,
                'confidence': 'High',
                'source': 'UN Comtrade / EIA',
                'latest_value': '+4.2% YoY',
                'unit': 'TWh'
            },
            {
                'commodity': commodities_map['COAL'],
                'name': 'Indonesia Domestic Market Obligation (DMO) Policy',
                'driver_type': CommodityDriver.DriverType.POLICY,
                'description': 'Mandatory 25% allocation for domestic power plants restricts export supply.',
                'impact_direction': CommodityDriver.ImpactDirection.NEGATIVE,
                'correlation_score': 0.58,
                'confidence': 'High',
                'source': 'Ministry of Energy and Mineral Resources RI',
                'latest_value': '25% Cap',
                'unit': 'Percentage'
            },
            # Gold Drivers
            {
                'commodity': commodities_map['GOLD'],
                'name': 'Federal Funds Effective Rate',
                'driver_type': CommodityDriver.DriverType.MACRO,
                'description': 'Higher real interest rates increase opportunity cost of holding non-yielding bullion.',
                'impact_direction': CommodityDriver.ImpactDirection.NEGATIVE,
                'correlation_score': -0.81,
                'confidence': 'High',
                'source': 'FRED',
                'latest_value': '5.25%',
                'unit': 'Percent'
            },
            {
                'commodity': commodities_map['GOLD'],
                'name': 'Central Bank Net Buying Volumes',
                'driver_type': CommodityDriver.DriverType.DEMAND,
                'description': 'Global central bank diversification into physical gold reserves.',
                'impact_direction': CommodityDriver.ImpactDirection.POSITIVE,
                'correlation_score': 0.69,
                'confidence': 'High',
                'source': 'World Gold Council',
                'latest_value': '1,037 tonnes/yr',
                'unit': 'Metric Tonnes'
            },
            # Nickel Drivers
            {
                'commodity': commodities_map['NICKEL'],
                'name': 'Indonesian HPAL Processing Capacity Expansion',
                'driver_type': CommodityDriver.DriverType.SUPPLY,
                'description': 'Rapid commissioning of High-Pressure Acid Leach plants creating Class 2 & MHP surplus.',
                'impact_direction': CommodityDriver.ImpactDirection.NEGATIVE,
                'correlation_score': -0.76,
                'confidence': 'High',
                'source': 'Sectors / MEMR',
                'latest_value': '+120,000 mt/yr',
                'unit': 'Nickel Content mt'
            },
            # Copper Drivers
            {
                'commodity': commodities_map['COPPER'],
                'name': 'Global EV & Grid Infrastructure Spending',
                'driver_type': CommodityDriver.DriverType.DEMAND,
                'description': 'EVs require 4x more copper content than ICE vehicles; renewable grid expansion accelerates demand.',
                'impact_direction': CommodityDriver.ImpactDirection.POSITIVE,
                'correlation_score': 0.85,
                'confidence': 'High',
                'source': 'IEA / World Bank',
                'latest_value': '$680 Billion',
                'unit': 'USD'
            }
        ]

        for ddata in drivers_data:
            CommodityDriver.objects.update_or_create(
                commodity=ddata['commodity'],
                name=ddata['name'],
                defaults=ddata
            )

        # 3. Seed Companies & Exposures
        companies_data = [
            {
                'ticker': 'ADRO.JK',
                'name': 'Adaro Energy Indonesia Tbk',
                'sector': 'Energy',
                'sub_industry': 'Coal Mining',
                'market_cap': 115000000000000.00,  # IDR ~115T
                'currency': 'IDR',
                'country': 'Indonesia',
                'exchange': 'IDX',
                'description': 'Leading Indonesian integrated energy exporter with large thermal coal reserves.',
                'website': 'https://www.adaro.com',
                'exposures': [
                    {'commodity': commodities_map['COAL'], 'share': 88.0, 'vol': 65000000, 'unit': 'mt', 'cost': 52.00, 'score': 90.0}
                ],
                'resilience': {
                    'debt_to_equity': 0.28,
                    'current_ratio': 2.15,
                    'ebitda_margin': 42.5,
                    'free_cash_flow': 18500000000000.00,
                    'net_cash_position': 24000000000000.00,
                    'reserve_life_years': 14.5,
                    'resilience_score': 84.5,
                    'scoring_status': 'Pending Validation',
                    'as_of_date': date(2024, 6, 30)
                }
            },
            {
                'ticker': 'PTBA.JK',
                'name': 'Bukit Asam Tbk',
                'sector': 'Energy',
                'sub_industry': 'Coal Mining',
                'market_cap': 32000000000000.00,
                'currency': 'IDR',
                'country': 'Indonesia',
                'exchange': 'IDX',
                'description': 'State-owned Indonesian coal mining enterprise supplying PLN and international markets.',
                'website': 'https://www.ptba.co.id',
                'exposures': [
                    {'commodity': commodities_map['COAL'], 'share': 94.0, 'vol': 41000000, 'unit': 'mt', 'cost': 48.50, 'score': 95.0}
                ],
                'resilience': {
                    'debt_to_equity': 0.35,
                    'current_ratio': 1.65,
                    'ebitda_margin': 28.4,
                    'free_cash_flow': 4200000000000.00,
                    'net_cash_position': 5800000000000.00,
                    'reserve_life_years': 22.0,
                    'resilience_score': 76.0,
                    'scoring_status': 'Pending Validation',
                    'as_of_date': date(2024, 6, 30)
                }
            },
            {
                'ticker': 'MDKA.JK',
                'name': 'Merdeka Copper Gold Tbk',
                'sector': 'Basic Materials',
                'sub_industry': 'Copper & Gold Mining',
                'market_cap': 58000000000000.00,
                'currency': 'IDR',
                'country': 'Indonesia',
                'exchange': 'IDX',
                'description': 'Diversified Indonesian producer of gold, copper, and nickel via modern heap leach and smelter operations.',
                'website': 'https://www.merdekacoppergold.com',
                'exposures': [
                    {'commodity': commodities_map['GOLD'], 'share': 45.0, 'vol': 120000, 'unit': 'troy oz', 'cost': 1150.00, 'score': 65.0},
                    {'commodity': commodities_map['COPPER'], 'share': 35.0, 'vol': 18000, 'unit': 'mt', 'cost': 5800.00, 'score': 55.0},
                    {'commodity': commodities_map['NICKEL'], 'share': 20.0, 'vol': 32000, 'unit': 'mt', 'cost': 12500.00, 'score': 40.0}
                ],
                'resilience': {
                    'debt_to_equity': 0.82,
                    'current_ratio': 1.25,
                    'ebitda_margin': 24.8,
                    'free_cash_flow': -1200000000000.00,
                    'net_cash_position': -4500000000000.00,
                    'reserve_life_years': 18.0,
                    'resilience_score': 62.0,
                    'scoring_status': 'Pending Validation',
                    'as_of_date': date(2024, 6, 30)
                }
            },
            {
                'ticker': 'INCO.JK',
                'name': 'Vale Indonesia Tbk',
                'sector': 'Basic Materials',
                'sub_industry': 'Nickel Mining',
                'market_cap': 38000000000000.00,
                'currency': 'IDR',
                'country': 'Indonesia',
                'exchange': 'IDX',
                'description': 'Major pure-play nickel matte producer operating hydro-powered smelting facilities in Sulawesi.',
                'website': 'https://www.vale.com/indonesia',
                'exposures': [
                    {'commodity': commodities_map['NICKEL'], 'share': 98.0, 'vol': 70000, 'unit': 'mt matte', 'cost': 9800.00, 'score': 98.0}
                ],
                'resilience': {
                    'debt_to_equity': 0.12,
                    'current_ratio': 3.40,
                    'ebitda_margin': 35.2,
                    'free_cash_flow': 3100000000000.00,
                    'net_cash_position': 6200000000000.00,
                    'reserve_life_years': 16.0,
                    'resilience_score': 88.0,
                    'scoring_status': 'Pending Validation',
                    'as_of_date': date(2024, 6, 30)
                }
            },
            {
                'ticker': 'ANTM.JK',
                'name': 'Aneka Tambang Tbk',
                'sector': 'Basic Materials',
                'sub_industry': 'Diversified Mining',
                'market_cap': 34000000000000.00,
                'currency': 'IDR',
                'country': 'Indonesia',
                'exchange': 'IDX',
                'description': 'State-owned mining conglomerate specializing in nickel ore, ferronickel, gold refining, and bauxite.',
                'website': 'https://www.antam.com',
                'exposures': [
                    {'commodity': commodities_map['GOLD'], 'share': 58.0, 'vol': 28000, 'unit': 'kg', 'cost': 1850.00, 'score': 72.0},
                    {'commodity': commodities_map['NICKEL'], 'share': 36.0, 'vol': 22000, 'unit': 'TNi', 'cost': 11200.00, 'score': 60.0}
                ],
                'resilience': {
                    'debt_to_equity': 0.42,
                    'current_ratio': 1.85,
                    'ebitda_margin': 18.6,
                    'free_cash_flow': 2400000000000.00,
                    'net_cash_position': 3100000000000.00,
                    'reserve_life_years': 25.0,
                    'resilience_score': 74.0,
                    'scoring_status': 'Pending Validation',
                    'as_of_date': date(2024, 6, 30)
                }
            }
        ]

        for comp_data in companies_data:
            exposures = comp_data.pop('exposures')
            resilience = comp_data.pop('resilience')
            comp, _ = Company.objects.update_or_create(ticker=comp_data['ticker'], defaults=comp_data)

            for exp in exposures:
                CompanyCommodityExposure.objects.update_or_create(
                    company=comp,
                    commodity=exp['commodity'],
                    defaults={
                        'revenue_share_pct': exp['share'],
                        'production_volume': exp['vol'],
                        'production_unit': exp['unit'],
                        'cash_cost_per_unit': exp['cost'],
                        'exposure_score': exp['score']
                    }
                )

            CompanyResilience.objects.update_or_create(
                company=comp,
                defaults=resilience
            )

            # 3b. Demo company metrics. They must never impersonate live Sectors data.
            raw_log, _ = RawDataLog.objects.get_or_create(
                source=RawDataLog.SourceType.SEED_DEMO,
                endpoint=f'seed://company/report/{comp.ticker}/',
                defaults={
                    'status_code': 200,
                    'data_origin': RawDataLog.DataOrigin.SEED_DEMO,
                    'response_payload': {'ticker': comp.ticker, 'status': 'demo'},
                },
            )

            obs_date = date(2024, 6, 30)

            # Exposure metrics per commodity
            for exp in exposures:
                share = exp['share']
                hhi_val = round((share / 100) ** 2, 4)
                for m_name, m_val, m_unit in [
                    ('Commodity Revenue Share', share, '%'),
                    ('Production Dependency', share, '%'),
                    ('Sales Dependency', share, '%'),
                    ('Operational Concentration HHI', hhi_val, 'index'),
                ]:
                    NormalizedMetric.objects.update_or_create(
                        metric_name=m_name,
                        entity_type=NormalizedMetric.EntityType.COMPANY,
                        entity_id=comp.ticker,
                        commodity=exp['commodity'],
                        observation_date=obs_date,
                        defaults={
                            'definition': f"{m_name} for {comp.ticker} ({exp['commodity'].code})",
                            'source': 'Seed Demo',
                            'frequency': 'Annual',
                            'unit': m_unit,
                            'value': m_val,
                            'raw_data_ref': raw_log,
                            'confidence': NormalizedMetric.Confidence.LOW,
                            'is_proxy': False,
                        }
                    )

            # Resilience metrics (company-wide)
            company_hhi_map = {
                'ADRO.JK': 0.77,
                'PTBA.JK': 0.88,
                'INCO.JK': 0.96,
                'ANTM.JK': 0.47,
                'MDKA.JK': 0.37,
            }
            res_metrics = [
                ('Reserve Coverage', resilience['reserve_life_years'], 'years'),
                ('Reserves', 500.0, 'mt'),
                ('Annual Production', 25.0, 'mt'),
                ('DER', resilience['debt_to_equity'], 'ratio'),
                ('EBITDA Margin', resilience['ebitda_margin'], '%'),
                ('Sales Diversification HHI', company_hhi_map.get(comp.ticker, 0.50), 'index'),
            ]
            for m_name, m_val, m_unit in res_metrics:
                NormalizedMetric.objects.update_or_create(
                    metric_name=m_name,
                    entity_type=NormalizedMetric.EntityType.COMPANY,
                    entity_id=comp.ticker,
                    commodity=None,
                    observation_date=obs_date,
                    defaults={
                        'definition': f"{m_name} for {comp.ticker}",
                        'source': 'Seed Demo',
                        'frequency': 'Annual',
                        'unit': m_unit,
                        'value': m_val,
                        'raw_data_ref': raw_log,
                        'confidence': NormalizedMetric.Confidence.LOW,
                        'is_proxy': False,
                    }
                )

            # Fundamental metrics for peer comparison
            fund_data = {
                'ADRO.JK': {'Revenue Growth': 12.5, 'Net Income Growth': 8.2, 'ROE': 24.5, 'PE': 4.8, 'PB': 1.1},
                'PTBA.JK': {'Revenue Growth': 6.8, 'Net Income Growth': 4.1, 'ROE': 18.2, 'PE': 5.6, 'PB': 1.4},
                'INCO.JK': {'Revenue Growth': -3.2, 'Net Income Growth': -6.5, 'ROE': 11.4, 'PE': 14.2, 'PB': 1.2},
                'ANTM.JK': {'Revenue Growth': 8.4, 'Net Income Growth': 5.2, 'ROE': 14.6, 'PE': 12.1, 'PB': 1.6},
                'MDKA.JK': {'Revenue Growth': 14.2, 'Net Income Growth': -12.4, 'ROE': 3.2, 'PE': 42.0, 'PB': 2.1},
            }
            for m_name, m_val in fund_data.get(comp.ticker, {}).items():
                m_unit = '%' if 'Growth' in m_name or m_name == 'ROE' else 'ratio'
                NormalizedMetric.objects.update_or_create(
                    metric_name=m_name,
                    entity_type=NormalizedMetric.EntityType.COMPANY,
                    entity_id=comp.ticker,
                    commodity=None,
                    observation_date=obs_date,
                    defaults={
                        'definition': f"{m_name} for {comp.ticker}",
                        'source': 'Seed Demo',
                        'frequency': 'Annual',
                        'unit': m_unit,
                        'value': m_val,
                        'raw_data_ref': raw_log,
                        'confidence': NormalizedMetric.Confidence.LOW,
                        'is_proxy': False,
                    }
                )

        # 4. Seed Evidence Audit Items
        audit_items = [
            {
                'metric': 'Thermal Coal Newcastle Monthly Price',
                'available': DataAuditItem.Availability.YES,
                'source': 'World Bank / FRED',
                'endpoint': '/series/observations?series_id=PCOALAUUSDM',
                'earliest_date': date(1990, 1, 1),
                'latest_date': date(2024, 8, 1),
                'frequency': 'Monthly',
                'unit': 'USD/mt',
                'missing_values': '0%',
                'historical_depth': '34 years',
                'proxy_required': False,
                'cost_rate_limit': 'Free API key (120 req/min)',
                'notes': 'Newcastle 6000 kcal/kg benchmark series complete.'
            },
            {
                'metric': 'Gold Spot London AM/PM Fix',
                'available': DataAuditItem.Availability.YES,
                'source': 'FRED',
                'endpoint': '/series/observations?series_id=GOLDAMGBD228NLBM',
                'earliest_date': date(1968, 1, 1),
                'latest_date': date(2024, 9, 1),
                'frequency': 'Daily',
                'unit': 'USD/troy oz',
                'missing_values': '<0.1%',
                'historical_depth': '56 years',
                'proxy_required': False,
                'cost_rate_limit': 'Free API key',
                'notes': 'Official LBMA fixing price.'
            },
            {
                'metric': 'LME Nickel Cash Settlement',
                'available': DataAuditItem.Availability.PARTIAL,
                'source': 'World Bank / UN Comtrade Proxy',
                'endpoint': 'Commodity Pink Sheet / HS 7502',
                'earliest_date': date(2000, 1, 1),
                'latest_date': date(2024, 7, 1),
                'frequency': 'Monthly',
                'unit': 'USD/mt',
                'missing_values': '1.2%',
                'historical_depth': '24 years',
                'proxy_required': True,
                'cost_rate_limit': 'Public access',
                'notes': 'World Bank monthly average substituted for daily spot due to LME paywall.'
            },
            {
                'metric': 'Indonesian Mining Company Financial Ratios',
                'available': DataAuditItem.Availability.YES,
                'source': 'Sectors API',
                'endpoint': '/v1/company/report/{ticker}/',
                'earliest_date': date(2018, 1, 1),
                'latest_date': date(2024, 6, 30),
                'frequency': 'Quarterly',
                'unit': 'IDR / Ratio',
                'missing_values': '0%',
                'historical_depth': '6 years',
                'proxy_required': False,
                'cost_rate_limit': 'Bearer Token auth required',
                'notes': 'Full balance sheet, income statement, and ratio coverage for IDX listed entities.'
            }
        ]

        for aitem in audit_items:
            DataAuditItem.objects.update_or_create(metric=aitem['metric'], defaults=aitem)

        # 5. Seed Scenarios
        coal_scen, _ = Scenario.objects.update_or_create(
            name='China Steel & Power Demand Slump (-20% Coal Price)',
            commodity=commodities_map['COAL'],
            defaults={
                'description': 'Simulates a 20% decline in thermal coal benchmark prices caused by China power grid decarbonization and property sector weakness.',
                'status': Scenario.Status.ACTIVE,
                'created_by': 'OreLens Intelligence Engine'
            }
        )
        ScenarioInput.objects.update_or_create(
            scenario=coal_scen,
            driver_name='Newcastle Coal Benchmark Price',
            defaults={
                'original_value': '138.50 USD/mt',
                'adjusted_value': '110.80 USD/mt',
                'adjustment_pct': -20.0,
                'notes': 'Stress test applied to coal producer EBITDA margins and debt service coverage.'
            }
        )
        ScenarioResult.objects.update_or_create(
            scenario=coal_scen,
            defaults={
                'estimated_price_impact_pct': -20.0,
                'estimated_new_price': 110.80,
                'confidence_interval_lower': 102.50,
                'confidence_interval_upper': 118.00,
                'methodology': 'Revenue & EBITDA Sensitivity Matrix',
                'warnings': 'Scoring weights pending historical correlation backtesting.'
            }
        )

        self.stdout.write(self.style.SUCCESS('OreLens sample data successfully seeded!'))
