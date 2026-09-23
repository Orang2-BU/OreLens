import Link from 'next/link';

export default function NotFound() {
  return <section className="state-panel"><span className="state-symbol" aria-hidden="true">?</span><h1>Perusahaan tidak ditemukan.</h1><p>ID perusahaan tidak tersedia atau tidak lagi aktif dalam cakupan OreLens.</p><Link className="button" href="/companies">Kembali ke Company Comparison</Link></section>;
}
