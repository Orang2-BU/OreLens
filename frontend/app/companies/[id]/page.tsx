import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import StatePanel from '../../_components/StatePanel';
import { getCompanyDetail, type IntelligenceObservation } from '@/lib/api';

export const metadata: Metadata = { title: 'Company Detail' };

function formatNumber(value: number | string | null | undefined, maximumFractionDigits = 2) {
  if (value === null || value === undefined || value === '') return 'Unavailable';
  return Number(value).toLocaleString('id-ID', { maximumFractionDigits });
}

function formatDate(value: string | null) {
  if (!value) return 'Periode unavailable';
  return new Intl.DateTimeFormat('id-ID', { day: '2-digit', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(value));
}

function MetricList({ metrics }: { metrics: Record<string, IntelligenceObservation | null> }) {
  return (
    <div className="metric-list">
      {Object.entries(metrics).map(([name, observation]) => (
        <article className={`metric-row ${observation ? '' : 'unavailable'}`} key={name}>
          <div><h3>{name}</h3>{observation ? <p>{observation.source} · {formatDate(observation.date)}</p> : <p>Belum ada normalized observation.</p>}</div>
          <div className="metric-value">{observation ? <><strong>{formatNumber(observation.value)}</strong><span>{observation.unit || 'unitless'}</span></> : <strong>Unavailable</strong>}</div>
          <div className="metric-evidence">{observation ? <><span>Confidence: {observation.confidence}</span><span>{observation.is_proxy ? 'Proxy metric' : 'Direct metric'}</span><span>{observation.evidence_id ? `Evidence #${observation.evidence_id}` : 'No evidence ID'}</span></> : <span>Missing, bukan nol</span>}</div>
        </article>
      ))}
    </div>
  );
}

const modeLabels = { seed_demo: 'Demo seed', mixed: 'Mixed evidence', evidence_backed: 'Evidence backed' };

export default async function CompanyDetailPage({ params, searchParams }: { params: Promise<{ id: string }>; searchParams: Promise<{ commodity?: string }> }) {
  const [{ id }, { commodity = 'COAL' }] = await Promise.all([params, searchParams]);
  const data = await getCompanyDetail(id, commodity);
  if (!data) notFound();
  if (!data.commodity || !data.intelligence) return <StatePanel title="Exposure perusahaan belum tersedia">Perusahaan ini belum terhubung ke komoditas dalam cakupan OreLens.</StatePanel>;

  const activeExposure = data.exposures.find((item) => item.commodity === data.commodity?.id);
  const intelligence = data.intelligence;

  return (
    <>
      <Link className="back-link" href={`/companies?commodity=${data.commodity.code}`}>Kembali ke Company Comparison</Link>
      <div className="eyebrow">COMPANY INTELLIGENCE / DETAIL</div>
      <header className="company-detail-heading">
        <div><span className="category">{data.company.exchange} · {data.company.sub_industry}</span><h1>{data.company.ticker}</h1><h2>{data.company.name}</h2><p>{data.company.description || 'Profil perusahaan belum tersedia.'}</p></div>
        <dl className="company-profile"><div><dt>Market cap</dt><dd>{data.company.currency} {formatNumber(data.company.market_cap, 0)}</dd></div><div><dt>Country</dt><dd>{data.company.country}</dd></div><div><dt>Commodity</dt><dd>{data.commodity.name}</dd></div></dl>
      </header>

      <nav className="company-exposure-switcher" aria-label="Pilih exposure komoditas">
        {data.commodities.map((item) => {
          const exposure = data.exposures.find((row) => row.commodity === item.id);
          return <Link key={item.id} href={`/companies/${data.company.id}?commodity=${item.code}`} aria-current={item.id === data.commodity?.id ? 'page' : undefined}><span>{item.name}</span><strong>{exposure?.revenue_share_pct === null || exposure?.revenue_share_pct === undefined ? 'Unavailable' : `${formatNumber(exposure.revenue_share_pct)}% revenue`}</strong></Link>;
        })}
      </nav>

      <aside className="data-notice"><strong>{modeLabels[intelligence.data_mode]} / Pending validation</strong><p>{intelligence.resilience.presentation.warning || 'Skor masih preliminary dan wajib dibaca bersama komponen serta evidence.'}</p></aside>

      <section className="score-overview" aria-label="Ringkasan exposure dan resilience">
        <article className="score-panel"><span>EXPOSURE · {data.commodity.name}</span><strong>{formatNumber(intelligence.exposure.score)}</strong><small>/ 100 · preliminary</small><dl><div><dt>Basis</dt><dd>{intelligence.exposure.basis || 'Unavailable'}</dd></div><div><dt>Revenue share</dt><dd>{activeExposure?.revenue_share_pct === null || activeExposure?.revenue_share_pct === undefined ? 'Unavailable' : `${formatNumber(activeExposure.revenue_share_pct)}%`}</dd></div><div><dt>Confidence</dt><dd>{intelligence.exposure.analysis_confidence}</dd></div><div><dt>Method</dt><dd>{intelligence.exposure.proxy_used ? 'Proxy used' : 'Direct metric'}</dd></div></dl></article>
        <article className="score-panel"><span>RESILIENCE</span><strong>{formatNumber(intelligence.resilience.uncertainty_adjusted_score)}</strong><small>/ 100 · uncertainty adjusted</small><dl><div><dt>Raw score</dt><dd>{formatNumber(intelligence.resilience.raw_score)}</dd></div><div><dt>Coverage</dt><dd>{intelligence.resilience.coverage_pct}%</dd></div><div><dt>Uncertainty</dt><dd>{intelligence.resilience.presentation.uncertainty_level}</dd></div><div><dt>Missing</dt><dd>{intelligence.resilience.missing_components.join(', ') || 'None'}</dd></div></dl></article>
      </section>

      <section className="breakdown-grid">
        <div><header className="section-heading"><span>01</span><div><h2>Exposure breakdown</h2><p>Komponen yang menjelaskan ketergantungan perusahaan pada {data.commodity.name}.</p></div></header><MetricList metrics={intelligence.exposure.components} /></div>
        <div><header className="section-heading"><span>02</span><div><h2>Resilience breakdown</h2><p>Komponen daya tahan; nilai missing tetap dipisahkan dari skor nol.</p></div></header><MetricList metrics={intelligence.resilience.components} /></div>
      </section>

      <section className="fundamentals-section"><header className="section-heading"><span>03</span><div><h2>Fundamentals</h2><p>Metric umum perusahaan dengan sumber, periode, confidence, dan evidence ID.</p></div></header><MetricList metrics={intelligence.fundamentals} /></section>
    </>
  );
}
