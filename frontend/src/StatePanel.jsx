import React from 'react';

export default function StatePanel({ kind = 'empty', title, children, onRetry }) {
  return (
    <section className={`state-panel ${kind}`} role={kind === 'error' ? 'alert' : 'status'} aria-busy={kind === 'loading'}>
      <span className="state-symbol" aria-hidden="true">{kind === 'loading' ? '…' : kind === 'error' ? '!' : '—'}</span>
      <h2>{title}</h2>
      <p>{children}</p>
      {onRetry && <button className="button" onClick={onRetry}>Coba lagi</button>}
    </section>
  );
}
