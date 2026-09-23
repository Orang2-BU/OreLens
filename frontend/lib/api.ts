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

type Page<T> = { count: number; results: T[] };

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
