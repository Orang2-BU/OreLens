'use client';

export default function Error({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return <section className="state-panel error" role="alert"><span className="state-symbol" aria-hidden="true">!</span><h1>Evidence belum dapat dimuat.</h1><p>Pastikan backend berjalan dan endpoint normalized metric, raw log, serta data audit dapat diakses.</p><button className="button" onClick={() => reset()}>Coba lagi</button></section>;
}
