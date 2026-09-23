import type { Metadata } from 'next';
import AppShell from './_components/AppShell';
import './globals.css';

export const metadata: Metadata = {
  title: { default: 'OreLens', template: '%s | OreLens' },
  description: 'Workspace intelligence komoditas dan perusahaan tambang Indonesia.',
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="id">
      <body><AppShell>{children}</AppShell></body>
    </html>
  );
}
