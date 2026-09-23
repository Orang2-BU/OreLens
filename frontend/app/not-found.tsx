import Link from 'next/link';

export default function NotFound() {
  return (
    <section className="page-message">
      <span className="eyebrow">404 / TIDAK DITEMUKAN</span>
      <h1>Halaman ini belum tersedia.</h1>
      <p>Alamat yang kamu buka tidak termasuk workspace OreLens saat ini.</p>
      <Link className="button" href="/commodities">Kembali ke komoditas</Link>
    </section>
  );
}
