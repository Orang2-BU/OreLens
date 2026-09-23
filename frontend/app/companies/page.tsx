import type { Metadata } from 'next';
import Link from 'next/link';
import StatePanel from '../_components/StatePanel';
import { getCompanyComparison } from '@/lib/api';

export const metadata: Metadata = { title: 'Company Comparison' };

function formatNumber(value: number | string | null | undefined, maximumFractionDigits = 2) {
  if (value === null || value === undefined || value === '') return 'Unavailable';
  return Number(value).toLocaleString('id-ID', { maximumFractionDigits });
}

function formatMarketCap(value: string, currency: string) {
  const amount = Number(value);
  if (!Number.isFinite(amount)) return 'Unavailable';
  return `${currency} ${new Intl.NumberFormat('id-ID', { notation: 'compact', maximumFractionDigits: 1 }).format(amount)}`;
}

const modeLabels = { seed_demo: 'Demo seed', mixed: 'Mixed evidence', evidence_backed: 'Evidence backed' };

export default async function CompaniesPage({ searchParams }: { searchParams: Promise<{ commodity?: string }> }) {
  const { commodity = 'COAL' } = await searchParams;
  const data = await getCompanyComparison(commodity);
  if (!data) return <StatePanel title="Data perusahaan belum tersedia">Jalankan seed atau ingestion backend untuk mengisi peer group perusahaan.</StatePanel>;

  return (
    <>
      <div className="eyebrow">COMPANY INTELLIGENCE / PEER COMPARISON</div>
      <header className="company-heading">
        <div><h1>Bandingkan perusahaan dalam konteks komoditas yang sama.</h1><p>Exposure menunjukkan ketergantungan pada komoditas. Resilience menunjukkan kemampuan perusahaan menghadapi tekanan—keduanya bukan rekomendasi investasi.</p></div>
        <div className="coverage"><span>PEER GROUP</span><strong>{data.rows.length}</strong><small>perusahaan · {data.commodity.name}</small></div>
      </header>

      <nav className="commodity-switcher" aria-label="Pilih peer group komoditas">
        {data.commodities.map((item) => <Link key={item.id} href={`/companies?commodity=${item.code}`} aria-current={item.id === data.commodity.id ? 'page' : undefined}>{item.name}</Link>)}
      </nav>

      <aside className="data-notice"><strong>Demo / Pending validation</strong><p>Skor ditampilkan untuk demonstrasi metodologi. Label data mode, confidence, coverage, dan missing evidence tetap terlihat agar hasil seed tidak terbaca sebagai analisis tervalidasi.</p></aside>

      {data.rows.length ? (
        <section aria-label={`Perbandingan perusahaan ${data.commodity.name}`}>
          {data.rows.length === 1 && <p className="single-peer-note">Hanya satu perusahaan tersedia untuk peer group ini; perbandingan relatif belum dapat dilakukan.</p>}
          <div className="comparison-wrap" tabIndex={0} aria-label="Tabel dapat digulir horizontal">
            <table className="comparison-table">
              <thead><tr><th scope="col">Perusahaan</th><th scope="col">Exposure</th><th scope="col">Resilience</th><th scope="col">Fundamentals</th><th scope="col">Status data</th></tr></thead>
              <tbody>
                {data.rows.map(({ company, exposure, intelligence }) => {
                  const roe = intelligence.fundamentals.ROE;
                  const der = intelligence.fundamentals.DER;
                  const pe = intelligence.fundamentals.PE;
                  return (
                    <tr key={company.id}>
                      <th scope="row"><strong>{company.ticker}</strong><span>{company.name}</span><small>{formatMarketCap(company.market_cap, company.currency)} · {company.exchange}</small></th>
                      <td><strong className="score-value">{formatNumber(intelligence.exposure.score)}</strong><span className="score-label">/ 100 · preliminary</span><dl><div><dt>Revenue share</dt><dd>{formatNumber(exposure.revenue_share_pct)}%</dd></div><div><dt>Confidence</dt><dd>{intelligence.exposure.analysis_confidence}</dd></div></dl></td>
                      <td><strong className="score-value">{formatNumber(intelligence.resilience.uncertainty_adjusted_score)}</strong><span className="score-label">/ 100 · adjusted</span><dl><div><dt>Raw score</dt><dd>{formatNumber(intelligence.resilience.raw_score)}</dd></div><div><dt>Coverage</dt><dd>{intelligence.resilience.coverage_pct}%</dd></div><div><dt>Uncertainty</dt><dd>{intelligence.resilience.presentation.uncertainty_level}</dd></div></dl></td>
                      <td><dl><div><dt>ROE</dt><dd>{roe ? `${formatNumber(roe.value)} ${roe.unit}` : 'Unavailable'}</dd></div><div><dt>DER</dt><dd>{der ? `${formatNumber(der.value)} ${der.unit}` : 'Unavailable'}</dd></div><div><dt>PE</dt><dd>{pe ? `${formatNumber(pe.value)} ${pe.unit}` : 'Unavailable'}</dd></div></dl></td>
                      <td><span className={`mode-badge ${intelligence.data_mode}`}>{modeLabels[intelligence.data_mode]}</span><small>{intelligence.resilience.missing_components.length ? `Missing: ${intelligence.resilience.missing_components.join(', ')}` : 'No missing resilience components'}</small></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      ) : <StatePanel title={`Peer ${data.commodity.name} belum tersedia`}>Belum ada company exposure yang menghubungkan perusahaan aktif dengan komoditas ini.</StatePanel>}
    </>
  );
}
