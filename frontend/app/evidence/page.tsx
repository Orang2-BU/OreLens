import type { Metadata } from 'next';
import Link from 'next/link';
import StatePanel from '../_components/StatePanel';
import { getEvidenceView, type EvidenceFilters, type RawDataLog } from '@/lib/api';
import { buildEvidenceQuery } from '@/lib/evidence.js';

export const metadata: Metadata = { title: 'Evidence' };

function formatDate(value: string | null) {
  if (!value) return 'Unavailable';
  return new Intl.DateTimeFormat('id-ID', { day: '2-digit', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(value));
}

function pageHref(filters: EvidenceFilters, page: number) {
  const query = buildEvidenceQuery({ ...filters, page: String(page) });
  return `/evidence${query ? `?${query}` : ''}`;
}

const originLabels: Record<RawDataLog['data_origin'], string> = { live_api: 'Live API', imported_file: 'Imported file', derived: 'Derived', seed_demo: 'Seed demo' };

export default async function EvidencePage({ searchParams }: { searchParams: Promise<{ entity_type?: string; confidence?: string; search?: string; page?: string; metric_id?: string }> }) {
  const params = await searchParams;
  const filters: EvidenceFilters = { entityType: params.entity_type, confidence: params.confidence, search: params.search, page: params.page, metricId: params.metric_id };
  const data = await getEvidenceView(filters);
  const page = Math.max(1, Number.parseInt(params.page || '1', 10) || 1);
  const auditsByMetric = new Map(data.audits.results.map((item) => [item.metric, item]));
  const originCounts = data.metrics.results.reduce<Record<string, number>>((counts, metric) => {
    const origin = metric.raw_data_ref ? data.rawLogs[metric.raw_data_ref]?.data_origin || 'unlinked' : 'unlinked';
    counts[origin] = (counts[origin] || 0) + 1;
    return counts;
  }, {});

  return (
    <>
      <div className="eyebrow">DATA INTELLIGENCE / EVIDENCE VIEW</div>
      <header className="evidence-heading"><div><h1>Telusuri setiap angka sampai ke sumbernya.</h1><p>Normalized metric, transformasi, raw fetch metadata, dan data availability audit disajikan dalam satu jejak yang dapat diperiksa.</p></div><div className="coverage"><span>OBSERVATIONS</span><strong>{data.metrics.count}</strong><small>{data.selectedMetricId ? 'evidence dipilih' : 'hasil sesuai filter'}</small></div></header>

      <aside className="data-notice"><strong>Metadata only</strong><p>Raw response payload dan request parameters tidak ditampilkan. Status HTTP 200 atau origin Live API tidak otomatis berarti metric sudah tervalidasi.</p></aside>

      <form className="evidence-filters" method="get">
        <label><span>Cari metric / entity</span><input type="search" name="search" defaultValue={params.search || ''} placeholder="Contoh: Revenue Growth" /></label>
        <label><span>Entity</span><select name="entity_type" defaultValue={params.entity_type || ''}><option value="">Semua entity</option><option>Commodity</option><option>Company</option><option>Macro</option></select></label>
        <label><span>Confidence</span><select name="confidence" defaultValue={params.confidence || ''}><option value="">Semua confidence</option><option>High</option><option>Medium</option><option>Low</option></select></label>
        <button className="button" type="submit">Terapkan filter</button>
        <Link className="filter-reset" href="/evidence">Reset</Link>
      </form>

      <section className="evidence-summary" aria-label="Ringkasan evidence yang tampil">
        <div><span>LIVE API</span><strong>{originCounts.live_api || 0}</strong></div><div><span>SEED DEMO</span><strong>{originCounts.seed_demo || 0}</strong></div><div><span>DERIVED / IMPORTED</span><strong>{(originCounts.derived || 0) + (originCounts.imported_file || 0)}</strong></div><div><span>UNLINKED</span><strong>{originCounts.unlinked || 0}</strong></div><div><span>AUDIT ITEMS</span><strong>{data.audits.count}</strong></div>
      </section>

      {data.selectedMetricId && <div className="selected-evidence"><span>Menampilkan Evidence #{data.selectedMetricId}</span><Link href="/evidence">Lihat semua evidence</Link></div>}

      {data.metrics.results.length ? <section className="evidence-list" aria-label="Daftar normalized metric">
        {data.metrics.results.map((metric) => {
          const raw = metric.raw_data_ref ? data.rawLogs[metric.raw_data_ref] : undefined;
          const audit = auditsByMetric.get(metric.metric_name);
          return <article className="evidence-card" key={metric.id}>
            <header><div><span className="evidence-id">EVIDENCE #{metric.id}</span><h2>{metric.metric_name}</h2><p>{metric.definition}</p></div><div className="evidence-reading"><strong>{Number(metric.value).toLocaleString('id-ID', { maximumFractionDigits: 4 })}</strong><span>{metric.unit}</span></div></header>
            <div className="provenance-chain">
              <section><span>01 · NORMALIZED</span><dl><div><dt>Entity</dt><dd>{metric.entity_type} · {metric.entity_id}</dd></div><div><dt>Period</dt><dd>{formatDate(metric.observation_date)} · {metric.frequency}</dd></div><div><dt>Transform</dt><dd>{metric.transformation}</dd></div><div><dt>Original unit</dt><dd>{metric.original_unit || metric.unit}</dd></div></dl><div className="evidence-tags"><span>Confidence: {metric.confidence}</span><span>Priority: {metric.priority}</span><span>{metric.is_proxy ? 'Proxy metric' : 'Direct metric'}</span></div></section>
              <section><span>02 · RAW SOURCE</span>{raw ? <><dl><div><dt>Source</dt><dd>{raw.source}</dd></div><div><dt>Origin</dt><dd>{originLabels[raw.data_origin]}</dd></div><div><dt>HTTP</dt><dd>{raw.status_code}</dd></div><div><dt>Fetched</dt><dd>{formatDate(raw.fetched_at)}</dd></div></dl><p className="endpoint">{raw.endpoint}</p></> : <p className="trace-missing">Raw log metadata tidak tersedia pada halaman ini.</p>}</section>
              <section><span>03 · AVAILABILITY AUDIT</span>{audit ? <><dl><div><dt>Status</dt><dd>{audit.available}</dd></div><div><dt>Coverage</dt><dd>{formatDate(audit.earliest_date)} – {formatDate(audit.latest_date)}</dd></div><div><dt>Missing</dt><dd>{audit.missing_values}</dd></div><div><dt>Depth</dt><dd>{audit.historical_depth}</dd></div></dl><div className="evidence-tags"><span>{audit.proxy_required ? 'Proxy required' : 'Direct source target'}</span><span>{audit.source}</span></div></> : <p className="trace-missing">Audit item belum tersedia untuk metric ini.</p>}</section>
            </div>
          </article>;
        })}
      </section> : <StatePanel title="Evidence tidak ditemukan">Ubah filter atau pastikan normalized metric sudah tersedia dari pipeline backend.</StatePanel>}

      {!data.selectedMetricId && (data.metrics.previous || data.metrics.next) && <nav className="evidence-pagination" aria-label="Pagination evidence"><span>Halaman {page}</span>{data.metrics.previous ? <Link href={pageHref(filters, page - 1)}>Sebelumnya</Link> : <span />}{data.metrics.next && <Link href={pageHref(filters, page + 1)}>Berikutnya</Link>}</nav>}
    </>
  );
}
