export default function Loading() {
  return (
    <section aria-label="Memuat ringkasan komoditas" aria-busy="true">
      <div className="eyebrow">MARKET INTELLIGENCE</div>
      <div className="skeleton skeleton-title" />
      <div className="commodity-grid">
        {[0, 1, 2, 3].map((item) => <div className="commodity-card skeleton-card" key={item} />)}
      </div>
    </section>
  );
}
