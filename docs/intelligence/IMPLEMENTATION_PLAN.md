# OreLens Intelligence — implementation plan

Status: tahap awal; belum ada audit data aktual atau bobot tervalidasi. Rencana ini mengikuti [MVP Scope](../product/MVP_SCOPE.md), [Data Dictionary](../data/DATA_DICTIONARY.md), [Data Availability Audit](../data/DATA_AVAILABILITY_AUDIT.md), dan [Quant Methodology](QUANT_METHODOLOGY.md).

## Tahap 1 — evidence-first read path (dimulai)

- [x] Endpoint `GET /api/v1/companies/{id}/intelligence/?commodity=COAL` (juga GOLD, NICKEL, COPPER): tampilkan company/commodity observations yang memiliki raw log HTTP sukses; skor final tetap `null` dan status `pending_data_audit`.
- [x] Filter exact `entity_id` dan `metric_name` di `/api/v1/normalized-metrics/` untuk akses evidence yang tidak bergantung pada pencarian fuzzy.
- [ ] Tandai data demo vs data aktual secara eksplisit pada record/response sebelum dipakai untuk keputusan.
- [ ] Batasi akses raw payload dan pastikan credential/parameter sensitif tidak bocor.

Selesai bila UI dapat menunjukkan sumber, tanggal, nilai, unit, transformasi, confidence, dan proxy tanpa mengklaim skor tervalidasi. Endpoint awal belum mengaitkan setiap metrik company ke komoditas tertentu; dua daftar evidence sengaja dipisahkan.

## Tahap 2 — audit dan ingest aktual (blocker scoring)

- [ ] Untuk empat komoditas, uji endpoint Sectors dan sumber eksternal dari dictionary; catat coverage, earliest/latest, frequency, unit, missingness, biaya/rate limit, lisensi di audit. Jangan gunakan seed sebagai hasil audit.
- [ ] Pilih metric MVP yang benar-benar tersedia; catat proxy dan alasan bila tidak tersedia.
- [ ] Implementasikan ingest satu metric yang sudah diaudit: raw log → validasi → normalisasi unit/periode → `NormalizedMetric` dengan referensi raw; idempotent untuk run ulang.
- [ ] Tambahkan cek freshness, duplikasi, nilai hilang, dan perbedaan unit. Perluas per metric hanya setelah satu jalur terbukti.

Selesai bila observasi nyata dapat ditelusuri sampai response sumber dan audit mendukung klaim coverage-nya.

## Tahap 3 — company/commodity intelligence

- [ ] Exposure per komoditas: revenue share bila tersedia; proxy production/sales diberi confidence lebih rendah. Missing tetap `null`, bukan nol.
- [ ] Resilience terpisah: reserve coverage, stabilitas produksi, diversifikasi, leverage, profitabilitas; tampilkan komponen dan evidence, jangan gunakan angka seed sebagai score final.
- [ ] Commodity driver map: supply, demand, macro, event/policy dengan arah sebagai hipotesis sampai diuji.
- [ ] Fundamental comparison dalam peer group yang valid, dengan periode dan unit yang sebanding.

Selesai bila setiap insight memiliki input, periode, sumber, confidence, status proxy, dan alasan saat unavailable.

## Tahap 4 — quant validation dan skenario

- [ ] Selaraskan series dan cegah look-ahead; lakukan correlation screening, regression, rolling/regime checks, dan backtest out-of-sample terhadap baseline sederhana.
- [ ] Hanya rilis driver importance/bobot numerik bila stabilitas dan cakupan memadai; jika gagal, sajikan sebagai konteks kualitatif.
- [ ] Jalankan skenario deterministik berbasis input terstruktur, tampilkan asumsi dan sensitivitas; tidak mengklaim prediksi harga saham.

Selesai bila metodologi, sampel, baseline, dan hasil uji bisa direproduksi. Bobot final dan forecast tidak termasuk tahap awal.
