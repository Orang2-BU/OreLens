'use client';

export default function Error({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <section className="state-panel error" role="alert">
      <span className="state-symbol" aria-hidden="true">!</span>
      <h1>Data komoditas belum dapat dimuat.</h1>
      <p>Pastikan backend Django berjalan dan konfigurasi API frontend sudah benar.</p>
      <button className="button" onClick={() => reset()}>Coba lagi</button>
    </section>
  );
}
