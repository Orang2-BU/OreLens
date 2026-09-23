import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import StatePanel from '../../_components/StatePanel';
import { getCommodityDriverMap } from '@/lib/api';
import { buildSparkline } from '@/lib/market';

export const metadata: Metadata = { title: 'Commodity Driver Map' };

const categoryLabels: Record<string, string> = { supply: 'Supply', demand: 'Demand', macro: 'Macro' };
const directionLabels: Record<string, string> = { POSITIVE: 'Positif', NEGATIVE: 'Negatif', MIXED: 'Campuran' };
const readinessLabels = { ready: 'Ready', partial_ready: 'Partial ready', blocked: 'Blocked' };

function formatDate(value: string) {
  return new Intl.DateTimeFormat('id-ID', { day: '2-digit', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(value));
}

function formatValue(value: string) {
  return Number(value).toLocaleString('id-ID', { maximumFractionDigits: 4 });
}

export default async function CommodityDriverPage({ params }: { params: Promise<{ code: string }> }) {
  const { code } = await params;
  const data = await getCommodityDriverMap(code);
  if (!data) notFound();

  const chronological = [...data.prices].reverse();
  const points = buildSparkline(chronological.map((item) => Number(item.price)));
  const observedCount = data.map.drivers.filter((driver) => driver.latest).length;

  return (
    <>
      <Link className="back-link" href="/commodities">Kembali ke Commodity Overview</Link>
      <div className="eyebrow">MARKET INTELLIGENCE / DRIVER MAP</div>
      <header className="driver-heading">
        <div><span className="category">{data.commodity.category.replaceAll('_', ' ')}</span><h1>{data.commodity.name}</h1><p>Pisahkan konteks yang sudah punya evidence dari hipotesis yang belum tervalidasi sebelum membaca hubungan antar-driver.</p></div>
        <span className="validation-badge">Hypotheses not validated</span>
      </header>

      <nav className="commodity-switcher" aria-label="Pilih komoditas">
        {data.commodities.map((commodity) => <Link key={commodity.id} href={`/commodities/${commodity.code.toLowerCase()}`} aria-current={commodity.id === data.commodity.id ? 'page' : undefined}>{commodity.name}</Link>)}
      </nav>

      <section className="driver-summary" aria-label="Ringkasan driver map">
        <article className="summary-panel price-context">
          <header><span>PRICE CONTEXT</span><strong>{data.commodity.benchmark_unit} {Number(data.commodity.current_price).toLocaleString('id-ID', { maximumFractionDigits: 2 })}</strong></header>
          {points ? <svg viewBox="0 0 320 80" role="img" aria-label={`Tren harga ${data.commodity.name} dari ${chronological.length} observasi`} preserveAspectRatio="none"><polyline points={points} /></svg> : <p>Riwayat harga belum tersedia.</p>}
          <small>{chronological.length} observasi terbaru dari endpoint harga</small>
        </article>
        <article className="summary-panel readiness-panel">
          <span>QUANT READINESS</span>
          <strong className={`readiness ${data.readiness.status}`}>{readinessLabels[data.readiness.status]}</strong>
          <dl><div><dt>Price periods</dt><dd>{data.readiness.price_periods}/{data.readiness.minimum_periods}</dd></div><div><dt>Driver ready</dt><dd>{data.readiness.ready_drivers_count}/{data.readiness.total_drivers_count}</dd></div><div><dt>Vintage</dt><dd>{data.readiness.vintage_status}</dd></div></dl>
        </article>
        <article className="summary-panel evidence-panel">
          <span>EVIDENCE COVERAGE</span>
          <strong>{observedCount}/{data.map.drivers.length}</strong>
          <p>driver memiliki normalized observation yang dapat ditelusuri.</p>
        </article>
      </section>

      <aside className="data-notice"><strong>Preliminary intelligence</strong><p>Direction adalah hipotesis ekonomi. Correlation dan importance hanya ditampilkan sebagai konteks validasi, bukan prediksi harga atau rekomendasi investasi.</p></aside>

      {data.map.drivers.length ? (
        <section className="driver-grid" aria-label={`Driver ${data.commodity.name}`}>
          {data.map.drivers.map((driver) => (
            <article className={`driver-card ${driver.status}`} key={driver.metric}>
              <header><span className="driver-category">{categoryLabels[driver.category] || driver.category}</span><span className="driver-status">{driver.status === 'observed_context' ? 'Observed context' : 'Unavailable'}</span></header>
              <h2>{driver.metric}</h2>
              <p className="driver-description">{driver.description || 'Driver hypothesis dari Data Dictionary; deskripsi persistence belum tersedia.'}</p>

              {driver.latest ? (
                <div className="driver-observation">
                  <span>LATEST OBSERVATION</span>
                  <strong>{formatValue(driver.latest.value)} <small>{driver.latest.unit}</small></strong>
                  <p>{driver.latest.source} · {formatDate(driver.latest.date)}</p>
                  <div className="evidence-tags"><span>Confidence: {driver.latest.confidence}</span><span>{driver.latest.is_proxy ? 'Proxy' : 'Direct metric'}</span><span>Evidence #{driver.latest.evidence_id}</span></div>
                </div>
              ) : <div className="driver-unavailable"><strong>Evidence belum tersedia</strong><p>Tidak ada normalized observation dengan raw log HTTP 200.</p></div>}

              <dl className="driver-metadata">
                <div><dt>Arah hipotesis</dt><dd>{driver.direction ? directionLabels[driver.direction] : 'Belum ditetapkan'}</dd></div>
                <div><dt>Correlation</dt><dd>{driver.correlation_score === null ? 'Belum dihitung' : `${driver.correlation_score.toFixed(3)} (${driver.correlation_confidence || 'No confidence'})`}</dd></div>
                <div><dt>Importance</dt><dd>{driver.importance === null ? 'Pending validation' : driver.importance.toFixed(3)}</dd></div>
                <div><dt>Validation</dt><dd>{driver.validation.observations === undefined ? 'Belum dijalankan' : `${driver.validation.observations} observasi · ${driver.validation.stable ? 'Stabil' : 'Belum stabil'}`}</dd></div>
              </dl>
            </article>
          ))}
        </section>
      ) : <StatePanel title="Driver belum tersedia">Data Dictionary belum memiliki driver hypothesis untuk komoditas ini.</StatePanel>}

      <aside className="event-policy"><div><span>EVENT / POLICY</span><strong>Qualitative only</strong></div><p>Event dan kebijakan belum diberi bobot numerik. Importance tetap kosong sampai metodologi dan evidence tervalidasi.</p></aside>
    </>
  );
}
