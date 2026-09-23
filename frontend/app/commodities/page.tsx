import type { Metadata } from 'next';
import Link from 'next/link';
import StatePanel from '../_components/StatePanel';
import { getCommodityOverview } from '@/lib/api';
import { buildSparkline } from '@/lib/market';

export const metadata: Metadata = { title: 'Komoditas' };

const categoryLabels: Record<string, string> = {
  ENERGY: 'Energi',
  PRECIOUS_METALS: 'Logam mulia',
  INDUSTRIAL_METALS: 'Logam industri',
  BATTERY_METALS: 'Logam baterai',
};

function formatPrice(value: string) {
  return new Intl.NumberFormat('id-ID', { maximumFractionDigits: 2 }).format(Number(value));
}

function formatDate(value?: string) {
  if (!value) return 'Tanggal belum tersedia';
  return new Intl.DateTimeFormat('id-ID', { day: '2-digit', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(value));
}

function Change({ value, period }: { value: number; period: string }) {
  const direction = value > 0 ? 'Naik' : value < 0 ? 'Turun' : 'Tetap';
  const className = value > 0 ? 'positive' : value < 0 ? 'negative' : 'neutral';
  return <div className={`change ${className}`}><span>{period}</span><strong>{direction} {Math.abs(value).toLocaleString('id-ID', { maximumFractionDigits: 2 })}%</strong></div>;
}

export default async function CommoditiesPage() {
  const commodities = await getCommodityOverview();
  if (!commodities.length) return <StatePanel title="Belum ada komoditas">Jalankan ingestion atau seed data backend untuk mengisi Commodity Overview.</StatePanel>;

  return (
    <>
      <div className="eyebrow">MARKET INTELLIGENCE / COMMODITY OVERVIEW</div>
      <header className="overview-heading">
        <div><h1>Lihat pasar sebelum menilai perusahaan.</h1><p>Ringkasan harga dan tren awal untuk empat komoditas dalam cakupan MVP OreLens.</p></div>
        <div className="coverage"><span>COVERAGE</span><strong>{commodities.length}/4</strong><small>komoditas tersedia</small></div>
      </header>

      <aside className="data-notice"><strong>Demo / Pending validation</strong><p>Backend belum membedakan seed dari ingestion tervalidasi. Semua nilai di halaman ini diperlakukan sebagai data demo sampai provenance tersedia.</p></aside>

      <section className="commodity-grid" aria-label="Ringkasan komoditas">
        {commodities.map((commodity) => {
          const chronological = [...commodity.prices].reverse();
          const points = buildSparkline(chronological.map((item) => Number(item.price)));
          const latest = commodity.prices[0];
          return (
            <article className="commodity-card" key={commodity.id}>
              <header className="commodity-card-head"><div><span className="category">{categoryLabels[commodity.category] || commodity.category}</span><h2>{commodity.name}</h2><p>{commodity.code}</p></div><span className="demo-badge">DEMO</span></header>
              <div className="price"><span>{commodity.benchmark_unit}</span><strong>{formatPrice(commodity.current_price)}</strong></div>
              <div className="changes"><Change value={commodity.price_change_pct_24h} period="24 JAM" /><Change value={commodity.price_change_pct_ytd} period="YTD" /></div>
              <div className="trend">
                <div className="trend-label"><span>TREN HISTORIS</span><small>{chronological.length} observasi</small></div>
                {points ? <svg viewBox="0 0 320 80" role="img" aria-label={`Tren harga ${commodity.name} dari ${chronological.length} observasi`} preserveAspectRatio="none"><polyline points={points} /></svg> : <p className="trend-empty">{commodity.priceHistoryStatus === 'error' ? 'Riwayat gagal dimuat' : 'Riwayat belum tersedia'}</p>}
              </div>
              <footer><span>Sumber: {latest?.source || 'Belum tersedia'}</span><span>{formatDate(latest?.date || commodity.last_updated)}</span></footer>
              <Link className="card-link" href={`/commodities/${commodity.code.toLowerCase()}`}>Buka driver map</Link>
            </article>
          );
        })}
      </section>
    </>
  );
}
