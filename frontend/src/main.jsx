import React, { useEffect, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Link, NavLink, Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { apiGet } from './api.js';
import StatePanel from './StatePanel.jsx';
import './styles.css';

const sections = [
  { path: '/commodities', label: 'Komoditas', index: '01', title: 'Mulai dari komoditas.', description: 'Telusuri pasar, pahami penggeraknya, lalu lihat perusahaan yang terhubung.', scope: 'Coal · Gold · Nickel · Copper', next: 'Commodity Overview dan Driver Map akan tersedia pada tahap berikutnya.' },
  { path: '/companies', label: 'Perusahaan', index: '02', title: 'Pahami eksposur perusahaan.', description: 'Bandingkan perusahaan melalui eksposur komoditas dan ketahanan finansial.', scope: 'Profil · Perbandingan · Exposure · Resilience', next: 'Daftar, perbandingan, dan detail perusahaan belum diimplementasikan.' },
  { path: '/evidence', label: 'Evidence', index: '03', title: 'Kenali dasar setiap analisis.', description: 'Telusuri definisi metric, sumber, tanggal observasi, dan kualitas data.', scope: 'Sumber · Confidence · Proxy · Audit', next: 'Penelusuran evidence akan dihubungkan setelah data dan relasinya tersedia.' },
  { path: '/scenarios', label: 'Scenario', index: '04', title: 'Eksplorasi perubahan asumsi.', description: 'Pelajari bagaimana perubahan driver dapat memengaruhi analisis komoditas.', scope: 'Asumsi · Input · Metodologi', next: 'Scenario UI belum tersedia. Perhitungan menunggu engine dan metodologi yang tervalidasi.' },
];

function Workspace({ section }) {
  return <>
    <div className="eyebrow">WORKSPACE / {section.label.toUpperCase()}</div>
    <header className="page-heading"><h1>{section.title}</h1><p>{section.description}</p></header>
    <div className="scope"><span>CAKUPAN MVP</span><p>{section.scope}</p></div>
    <StatePanel title="Ruang analisis sedang disiapkan">{section.next}</StatePanel>
    <aside className="note"><strong>Transparansi data</strong><p>Data aktual dan scoring masih dalam tahap validasi. Belum ada hasil analisis yang ditampilkan di workspace ini.</p></aside>
  </>;
}

function Connection() {
  const [status, setStatus] = useState('idle');
  const controller = useRef(null);
  useEffect(() => () => controller.current?.abort(), []);
  async function check() {
    controller.current?.abort();
    controller.current = new AbortController();
    setStatus('loading');
    try {
      await apiGet('commodities/', { signal: controller.current.signal });
      setStatus('success');
    } catch (error) {
      if (error.name !== 'AbortError') setStatus('error');
    }
  }
  return <section className="connection" aria-label="Koneksi data">
    <span className="eyebrow">KONEKSI DATA</span>
    <p className={`connection-status ${status}`} role="status"><span aria-hidden="true" />{({ idle: 'Belum diperiksa', loading: 'Memeriksa koneksi…', success: 'API dapat diakses', error: 'API belum dapat diakses' })[status]}</p>
    {status === 'error' && <p className="connection-help">Pastikan backend berjalan dan alamat API sudah sesuai.</p>}
    <button onClick={check} disabled={status === 'loading'}>{status === 'error' ? 'Coba lagi' : 'Periksa koneksi'}</button>
  </section>;
}

function App() {
  const location = useLocation();
  const main = useRef(null);
  const firstRender = useRef(true);
  const current = sections.find(s => s.path === location.pathname);
  useEffect(() => {
    document.title = `${current?.label || 'Halaman tidak ditemukan'} | OreLens`;
    if (!firstRender.current) main.current?.focus();
    firstRender.current = false;
  }, [location.pathname, current]);
  return <div className="app">
    <a className="skip-link" href="#main">Lewati ke konten</a>
    <aside className="sidebar">
      <Link className="brand" to="/commodities" aria-label="OreLens beranda"><span className="brand-mark" aria-hidden="true">O</span>OreLens<span className="brand-dot">.</span></Link>
      <p className="brand-caption">Commodity & company intelligence</p>
      <nav aria-label="Navigasi utama">{sections.map(s => <NavLink key={s.path} to={s.path}><span className="nav-index">{s.index}</span>{s.label}</NavLink>)}</nav>
      <Connection />
      <p className="sidebar-foot">Sectors Hackathon<br /><span>Research workspace</span></p>
    </aside>
    <div className="content">
      <header className="topbar"><span>OreLens / <strong>{current?.label || '404'}</strong></span><span className="badge">Tahap pengembangan</span></header>
      <main id="main" tabIndex={-1} ref={main}>
        <Routes>
          <Route path="/" element={<Navigate to="/commodities" replace />} />
          {sections.map(s => <Route key={s.path} path={s.path} element={<Workspace section={s} />} />)}
          <Route path="*" element={<><h1>Halaman tidak ditemukan.</h1><p>Alamat ini belum tersedia di OreLens.</p><Link className="button" to="/commodities">Kembali ke komoditas</Link></>} />
        </Routes>
      </main>
      <footer>OreLens <span>Komoditas. Perusahaan. Evidence.</span></footer>
    </div>
  </div>;
}

createRoot(document.getElementById('root')).render(<React.StrictMode><BrowserRouter><App /></BrowserRouter></React.StrictMode>);
