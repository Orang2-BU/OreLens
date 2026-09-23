'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';
import type { ReactNode } from 'react';

const sections = [
  { path: '/commodities', label: 'Komoditas', index: '01' },
  { path: '/companies', label: 'Perusahaan', index: '02' },
  { path: '/evidence', label: 'Evidence', index: '03' },
  { path: '/scenarios', label: 'Scenario', index: '04' },
];

function Connection() {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const controller = useRef<AbortController | null>(null);

  useEffect(() => () => controller.current?.abort(), []);

  async function check() {
    controller.current?.abort();
    controller.current = new AbortController();
    setStatus('loading');
    try {
      const response = await fetch('/api/health', { signal: controller.current.signal });
      if (!response.ok) throw new Error('API unavailable');
      setStatus('success');
    } catch (error) {
      if ((error as Error).name !== 'AbortError') setStatus('error');
    }
  }

  const messages = { idle: 'Belum diperiksa', loading: 'Memeriksa koneksi…', success: 'API dapat diakses', error: 'API belum dapat diakses' };
  return (
    <section className="connection" aria-label="Koneksi data">
      <span className="eyebrow">KONEKSI DATA</span>
      <p className={`connection-status ${status}`} role="status"><span aria-hidden="true" />{messages[status]}</p>
      {status === 'error' && <p className="connection-help">Pastikan backend Django berjalan dan API_BASE_URL sesuai.</p>}
      <button onClick={check} disabled={status === 'loading'}>{status === 'error' ? 'Coba lagi' : 'Periksa koneksi'}</button>
    </section>
  );
}

export default function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const current = sections.find((section) => pathname.startsWith(section.path));
  const main = useRef<HTMLElement | null>(null);
  const firstRender = useRef(true);

  useEffect(() => {
    if (!firstRender.current) main.current?.focus();
    firstRender.current = false;
  }, [pathname]);

  return (
    <div className="app">
      <a className="skip-link" href="#main">Lewati ke konten</a>
      <aside className="sidebar">
        <Link className="brand" href="/commodities" aria-label="OreLens beranda"><span className="brand-mark" aria-hidden="true">O</span>OreLens<span className="brand-dot">.</span></Link>
        <p className="brand-caption">Commodity & company intelligence</p>
        <nav aria-label="Navigasi utama">
          {sections.map((section) => {
            const active = pathname.startsWith(section.path);
            return <Link key={section.path} href={section.path} className={active ? 'active' : undefined} aria-current={active ? 'page' : undefined}><span className="nav-index">{section.index}</span>{section.label}</Link>;
          })}
        </nav>
        <Connection />
        <p className="sidebar-foot">Sectors Hackathon<br /><span>Research workspace</span></p>
      </aside>
      <div className="content">
        <header className="topbar"><span>OreLens / <strong>{current?.label || 'Workspace'}</strong></span><span className="badge">Preliminary intelligence</span></header>
        <main id="main" tabIndex={-1} ref={main}>{children}</main>
        <footer>OreLens <span>Komoditas. Perusahaan. Evidence.</span></footer>
      </div>
    </div>
  );
}
