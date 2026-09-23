import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import StatePanel from '../_components/StatePanel';

const placeholders = {
  companies: { label: 'Perusahaan', title: 'Pahami eksposur perusahaan.', description: 'Bandingkan perusahaan melalui eksposur komoditas dan ketahanan finansial.', scope: 'Profil · Perbandingan · Exposure · Resilience', next: 'Daftar dan detail perusahaan akan diimplementasikan pada tahap frontend berikutnya.' },
  evidence: { label: 'Evidence', title: 'Kenali dasar setiap analisis.', description: 'Telusuri definisi metric, sumber, tanggal observasi, dan kualitas data.', scope: 'Sumber · Confidence · Proxy · Audit', next: 'Penelusuran evidence akan dihubungkan setelah tampilan company dan driver tersedia.' },
  scenarios: { label: 'Scenario', title: 'Eksplorasi perubahan asumsi.', description: 'Pelajari bagaimana perubahan driver dapat memengaruhi analisis komoditas.', scope: 'Asumsi · Input · Metodologi', next: 'Scenario UI tetap menunggu endpoint dan metode yang siap digunakan frontend.' },
} as const;

type Section = keyof typeof placeholders;

export async function generateMetadata({ params }: { params: Promise<{ section: string }> }): Promise<Metadata> {
  const { section } = await params;
  return { title: placeholders[section as Section]?.label || 'Halaman tidak ditemukan' };
}

export default async function PlaceholderPage({ params }: { params: Promise<{ section: string }> }) {
  const { section } = await params;
  const content = placeholders[section as Section];
  if (!content) notFound();

  return (
    <>
      <div className="eyebrow">WORKSPACE / {content.label.toUpperCase()}</div>
      <header className="page-heading"><h1>{content.title}</h1><p>{content.description}</p></header>
      <div className="scope"><span>CAKUPAN MVP</span><p>{content.scope}</p></div>
      <StatePanel title="Ruang analisis sedang disiapkan">{content.next}</StatePanel>
      <aside className="note"><strong>Transparansi data</strong><p>Data aktual dan scoring masih dalam tahap validasi. Belum ada hasil analisis yang ditampilkan di workspace ini.</p></aside>
    </>
  );
}
