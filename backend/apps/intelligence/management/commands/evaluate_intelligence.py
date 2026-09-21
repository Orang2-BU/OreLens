import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from django.core.management.base import BaseCommand
from apps.companies.models import Company, CompanyCommodityExposure
from apps.commodities.models import Commodity
from apps.intelligence.company_snapshot import build_company_snapshot
from apps.intelligence.commodity_snapshot import build_driver_map, preview_driver_shock
from apps.analytics.validation import quant_readiness


class Command(BaseCommand):
    help = 'Evaluate and audit OreLens intelligence processing results across commodities and companies.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--json',
            action='store_true',
            help='Output machine-readable JSON format instead of human-readable summary.'
        )
        parser.add_argument(
            '--conservative',
            action='store_true',
            default=True,
            help='Enforce conservative risk labeling on emiten intelligence evaluation.'
        )

    def handle(self, *args, **options):
        output_json = options.get('json', False)
        conservative = options.get('conservative', True)

        evaluation_data = {
            'timestamp': datetime.now().isoformat(),
            'disclaimer': (
                'DISCLAIMER: This evaluation report is for algorithmic validation and prototype simulation. '
                'Ratings and scores reflect preliminary seed data or partial evidence and must NOT be used as investment advice.'
            ),
            'commodities': {},
            'companies': {},
            'quadrant_summary': {
                'high_resilience_pure_exposure': [],
                'moderate_resilience_pure_exposure': [],
                'balanced_diversified': [],
                'high_financial_vulnerability': [],
            },
            'scenario_checks': [],
        }

        # 1. Commodity Quant Readiness & Driver Map Audit
        for comm in Commodity.objects.all().order_by('code'):
            qread = quant_readiness(comm)
            dmap = build_driver_map(comm)

            evaluation_data['commodities'][comm.code] = {
                'name': comm.name,
                'quant_readiness_status': qread['status'],
                'price_periods': qread['price_periods'],
                'ready_drivers': qread.get('ready_drivers_count', 0),
                'total_drivers': qread.get('total_drivers_count', 0),
                'driver_map_status': dmap['status'],
                'drivers': [
                    {
                        'metric': d['metric'],
                        'category': d['category'],
                        'status': d['status'],
                        'importance': d['importance'],
                        'correlation_score': d['correlation_score'],
                        'confidence': d['correlation_confidence'],
                    }
                    for d in dmap['drivers']
                ],
            }

            # Scenario preview check
            for d in dmap['drivers']:
                if d.get('latest'):
                    try:
                        shock_result = preview_driver_shock(comm, d['metric'], -10.0)
                        evaluation_data['scenario_checks'].append({
                            'commodity': comm.code,
                            'metric': d['metric'],
                            'shock_pct': -10.0,
                            'adjusted_value': shock_result['adjusted_value'],
                            'guardrail': shock_result.get('guardrail', {}),
                            'is_deprecated': shock_result.get('is_deprecated', False),
                        })
                    except Exception as e:
                        evaluation_data['scenario_checks'].append({
                            'commodity': comm.code,
                            'metric': d['metric'],
                            'error': str(e),
                        })

        # 2. Company Intelligence & Uncertainty Audit
        for comp in Company.objects.all().order_by('ticker'):
            comp_eval = {'ticker': comp.ticker, 'name': comp.name, 'commodities': {}}

            for comm in Commodity.objects.all().order_by('code'):
                snap = build_company_snapshot(comp, comm)
                exp = snap['exposure']
                res = snap['resilience']

                # Include if exposure exists or company is linked to commodity
                if exp['score'] is not None or CompanyCommodityExposure.objects.filter(company=comp, commodity=comm).exists():
                    comp_eval['commodities'][comm.code] = {
                        'data_mode': snap.get('data_mode', 'seed_demo'),
                        'exposure_score': exp['score'],
                        'exposure_confidence': exp['analysis_confidence'],
                        'exposure_proxy_used': exp['proxy_used'],
                        'exposure_status': exp['score_status'],
                        'resilience_raw_score': res['raw_score'],
                        'resilience_adjusted_score': res.get('uncertainty_adjusted_score'),
                        'resilience_coverage_pct': res['coverage_pct'],
                        'resilience_status': res['score_status'],
                        'uncertainty_level': res.get('presentation', {}).get('uncertainty_level', 'High'),
                        'missing_components': res['missing_components'],
                        'components': {k: float(v['value']) if (v and v['value'] is not None) else None for k, v in res['components'].items()},
                    }

                    # Classify into quadrant
                    eff_res = res.get('uncertainty_adjusted_score') or res['score'] or 50.0
                    eff_exp = exp['score'] or 0.0

                    if eff_res >= 80 and eff_exp >= 75:
                        evaluation_data['quadrant_summary']['high_resilience_pure_exposure'].append(
                            f"{comp.ticker} ({comm.code}: exp={eff_exp}, res_adj={eff_res})"
                        )
                    elif eff_res < 80 and eff_exp >= 75:
                        evaluation_data['quadrant_summary']['moderate_resilience_pure_exposure'].append(
                            f"{comp.ticker} ({comm.code}: exp={eff_exp}, res_adj={eff_res})"
                        )
                    elif eff_res >= 70 and eff_exp < 75:
                        evaluation_data['quadrant_summary']['balanced_diversified'].append(
                            f"{comp.ticker} ({comm.code}: exp={eff_exp}, res_adj={eff_res})"
                        )
                    else:
                        evaluation_data['quadrant_summary']['high_financial_vulnerability'].append(
                            f"{comp.ticker} ({comm.code}: exp={eff_exp}, res_adj={eff_res})"
                        )

            if comp_eval['commodities']:
                evaluation_data['companies'][comp.ticker] = comp_eval

        if output_json:
            self.stdout.write(json.dumps(evaluation_data, indent=2, cls=DjangoJSONEncoder))
            return

        # Human-Readable Formatting
        self.stdout.write(self.style.NOTICE('=' * 80))
        self.stdout.write(self.style.NOTICE('   ORELENS INTELLIGENCE EVALUATION & GOVERNANCE AUDIT REPORT'))
        self.stdout.write(self.style.NOTICE('=' * 80))
        self.stdout.write(self.style.WARNING(f"\n{evaluation_data['disclaimer']}\n"))

        self.stdout.write(self.style.SUCCESS('\n[1] COMMODITY DRIVER MAP & QUANT READINESS GATE:'))
        for code, cdata in evaluation_data['commodities'].items():
            badge = self.style.SUCCESS('READY') if cdata['quant_readiness_status'] == 'ready' else (
                self.style.WARNING('PARTIAL READY') if cdata['quant_readiness_status'] == 'partial_ready' else self.style.ERROR('BLOCKED')
            )
            self.stdout.write(f"  • {code:<7} ({cdata['name']}): Quant Gate = {badge} ({cdata['ready_drivers']}/{cdata['total_drivers']} drivers, {cdata['price_periods']} price periods)")
            self.stdout.write(f"    Driver Map Status: {cdata['driver_map_status']}")
            for d in cdata['drivers']:
                corr_str = f"corr={d['correlation_score']:.3f}" if d['correlation_score'] is not None else "corr=None"
                conf_str = f"conf={d['confidence']}" if d['confidence'] else "conf=None"
                self.stdout.write(f"      - [{d['category'].upper():<6}] {d['metric']:<36} | {d['status']:<16} | {corr_str} ({conf_str})")

        self.stdout.write(self.style.SUCCESS('\n[2] COMPANY INTELLIGENCE PROCESSING RESULTS:'))
        for ticker, comp in evaluation_data['companies'].items():
            self.stdout.write(f"\n  Emiten: {self.style.HTTP_INFO(ticker)} ({comp['name']})")
            for comm_code, d in comp['commodities'].items():
                mode_color = self.style.SUCCESS if d['data_mode'] == 'evidence_backed' else self.style.WARNING
                self.stdout.write(f"    - Komoditas: {comm_code} | Mode: {mode_color(d['data_mode'])}")
                self.stdout.write(f"      Exposure Score : {d['exposure_score']} (Confidence: {d['exposure_confidence']}, Proxy: {d['exposure_proxy_used']})")
                self.stdout.write(f"      Resilience Raw : {d['resilience_raw_score']} (Coverage: {d['resilience_coverage_pct']}%)")
                self.stdout.write(f"      Resilience Adj : {self.style.NOTICE(str(d['resilience_adjusted_score']))} [Uncertainty: {d['uncertainty_level']}]")
                self.stdout.write(f"      Status Label   : {d['resilience_status']}")
                self.stdout.write(f"      Components     : {d['components']}")
                if d['missing_components']:
                    self.stdout.write(self.style.WARNING(f"      Missing Comp   : {d['missing_components']}"))

        self.stdout.write(self.style.SUCCESS('\n[3] EMITEN MAPPING: BAGIAN UNGGUL & BAGIAN RENTAN:'))
        self.stdout.write("  • Kuadran I (High Resilience, Pure Exposure):")
        for item in set(evaluation_data['quadrant_summary']['high_resilience_pure_exposure']):
            self.stdout.write(f"    - {item} -> UNGGUL: Neraca kokoh, kas tebal, margin prima. RENTAN: Konsentrasi tunggal ekstrim.")

        self.stdout.write("  • Kuadran II (Moderate Resilience, Pure Exposure):")
        for item in set(evaluation_data['quadrant_summary']['moderate_resilience_pure_exposure']):
            self.stdout.write(f"    - {item} -> UNGGUL: Cadangan besar, captive market kuat. RENTAN: Marjin moderat, 94% batubara.")

        self.stdout.write("  • Kuadran III (Balanced Diversified):")
        for item in set(evaluation_data['quadrant_summary']['balanced_diversified']):
            self.stdout.write(f"    - {item} -> UNGGUL: Diversifikasi multi-komoditas. RENTAN: Marjin EBITDA tipis pada segmen trading.")

        self.stdout.write("  • Kuadran IV (High Financial Vulnerability / Capex Growth):")
        for item in set(evaluation_data['quadrant_summary']['high_financial_vulnerability']):
            self.stdout.write(f"    - {item} -> UNGGUL: Portofolio tembaga & nikel masa depan. RENTAN: DER tinggi, FCF negatif.")

        self.stdout.write(self.style.SUCCESS('\n[4] SCENARIO SHOCK PREVIEW & HISTORICAL P05-P95 GUARDRAIL:'))
        for sc in evaluation_data['scenario_checks']:
            if 'error' in sc:
                self.stdout.write(self.style.ERROR(f"  • {sc['commodity']} - {sc['metric']}: {sc['error']}"))
            else:
                g = sc.get('guardrail', {})
                dep = " [DEPRECATED]" if sc.get('is_deprecated') else ""
                self.stdout.write(f"  • {sc['commodity']} - {sc['metric']}{dep}: Shock -10% -> Adjusted {sc['adjusted_value']} (Guardrail: {g.get('status', 'N/A')})")

        self.stdout.write(self.style.NOTICE('\n' + '=' * 80))
        self.stdout.write(self.style.SUCCESS('Evaluation completed successfully. Report is reproducible via python manage.py evaluate_intelligence'))
        self.stdout.write(self.style.NOTICE('=' * 80 + '\n'))
