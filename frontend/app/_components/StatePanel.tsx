import type { ReactNode } from 'react';

export default function StatePanel({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="state-panel" role="status">
      <span className="state-symbol" aria-hidden="true">—</span>
      <h2>{title}</h2>
      <p>{children}</p>
    </section>
  );
}
