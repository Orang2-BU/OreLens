import { enrichDrivers } from './drivers.js';
import { buildCompanyPeers, pickCommodity } from './company.js';

export type Commodity = {
  id: number;
  code: string;
  name: string;
  category: string;
  description: string;
  benchmark_unit: string;
  current_price: string;
  price_change_pct_24h: number;
  price_change_pct_ytd: number;
  last_updated: string;
};

export type PriceObservation = {
  id: number;
  commodity: number;
  commodity_code: string;
  date: string;
  price: string;
  source: string;
};

export type DriverObservation = {
  value: string;
  unit: string;
  date: string;
  source: string;
  confidence: string;
  is_proxy: boolean;
  evidence_id: number;
};

export type DriverMapItem = {
  category: string;
  metric: string;
  status: 'observed_context' | 'unavailable';
  latest: DriverObservation | null;
  importance: number | null;
  correlation_score: number | null;
  correlation_confidence: string | null;
  validation: { observations?: number; stable?: boolean; metadata_valid?: boolean };
  direction?: string;
  description?: string;
};

type DriverMap = {
  commodity: string;
  status: 'preliminary_correlation' | 'hypotheses_not_validated';
  drivers: DriverMapItem[];
  event_policy: { status: 'qualitative_only'; importance: null };
};

type PersistedDriver = {
  name: string;
  description: string;
  impact_direction: 'POSITIVE' | 'NEGATIVE' | 'MIXED';
};

export type QuantReadiness = {
  status: 'ready' | 'partial_ready' | 'blocked';
  price_periods: number;
  minimum_periods: number;
  ready_drivers_count: number;
  total_drivers_count: number;
  vintage_status: string;
  note: string;
};

type Page<T> = { count: number; results: T[] };

export type Company = {
  id: number;
  ticker: string;
  name: string;
  sector: string;
  sub_industry: string;
  market_cap: string;
  currency: string;
  exchange: string;
};

type CompanyExposure = {
  company: number;
  commodity: number;
  commodity_code: string;
  revenue_share_pct: number | null;
};

type IntelligenceObservation = {
  value: number | string;
  unit: string;
  source: string;
  confidence: string;
  evidence_id: number | null;
};

export type CompanyIntelligence = {
  data_mode: 'seed_demo' | 'mixed' | 'evidence_backed';
  exposure: {
    score: number | null;
    score_status: string;
    analysis_confidence: string;
    observation: IntelligenceObservation | null;
  };
  resilience: {
    raw_score: number | null;
    uncertainty_adjusted_score: number | null;
    score_status: string;
    coverage_pct: number;
    missing_components: string[];
    presentation: { uncertainty_level: string; warning: string | null };
  };
  fundamentals: Record<string, IntelligenceObservation | null>;
};

const API_BASE_URL = process.env.API_BASE_URL || 'http://127.0.0.1:8000/api/v1/';

export async function fetchApi<T>(path: string): Promise<T> {
  const url = new URL(path.replace(/^\/+/, ''), API_BASE_URL.replace(/\/?$/, '/'));
  const response = await fetch(url, { cache: 'no-store', headers: { Accept: 'application/json' } });
  if (!response.ok) throw new Error(`Django API gagal merespons (HTTP ${response.status}).`);
  return response.json() as Promise<T>;
}

export async function getCommodityOverview() {
  const page = await fetchApi<Page<Commodity>>('commodities/');
  return Promise.all(page.results.map(async (commodity) => {
    try {
      const prices = await fetchApi<Page<PriceObservation>>(`commodity-prices/?commodity=${commodity.id}`);
      return { ...commodity, prices: prices.results, priceHistoryStatus: 'ready' as const };
    } catch {
      return { ...commodity, prices: [], priceHistoryStatus: 'error' as const };
    }
  }));
}

export async function getCommodityDriverMap(code: string) {
  const commodityPage = await fetchApi<Page<Commodity>>('commodities/');
  const commodity = commodityPage.results.find((item) => item.code === code.toUpperCase());
  if (!commodity) return null;

  const [map, prices, persisted, readiness] = await Promise.all([
    fetchApi<DriverMap>(`commodities/${commodity.id}/intelligence/`),
    fetchApi<Page<PriceObservation>>(`commodity-prices/?commodity=${commodity.id}`),
    fetchApi<Page<PersistedDriver>>(`commodity-drivers/?commodity=${commodity.id}`),
    fetchApi<QuantReadiness>(`commodities/${commodity.id}/quant-readiness/`),
  ]);
  return {
    commodity,
    commodities: commodityPage.results,
    prices: prices.results,
    readiness,
    map: {
      ...map,
      drivers: enrichDrivers(map.drivers, persisted.results),
    },
  };
}

export async function getCompanyComparison(code: string) {
  const [commodityPage, companyPage, exposurePage] = await Promise.all([
    fetchApi<Page<Commodity>>('commodities/'),
    fetchApi<Page<Company>>('companies/'),
    fetchApi<Page<CompanyExposure>>('company-exposures/'),
  ]);
  const commodity = pickCommodity(commodityPage.results, code);
  if (!commodity) return null;

  const peers = buildCompanyPeers(companyPage.results, exposurePage.results, commodity.id);
  const rows = await Promise.all(peers.map(async ({ company, exposure }) => ({
    company,
    exposure,
    intelligence: await fetchApi<CompanyIntelligence>(`companies/${company.id}/intelligence/?commodity=${commodity.code}`),
  })));
  return { commodity, commodities: commodityPage.results, rows };
}
