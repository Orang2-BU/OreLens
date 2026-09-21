# OreLens Intelligence — implementation plan

Status: tahap awal; belum ada audit data aktual atau bobot tervalidasi. Rencana ini mengikuti [MVP Scope](../product/MVP_SCOPE.md), [Data Dictionary](../data/DATA_DICTIONARY.md), [Data Availability Audit](../data/DATA_AVAILABILITY_AUDIT.md), dan [Quant Methodology](QUANT_METHODOLOGY.md).

## Tahap 1 — evidence-first read path (dimulai)

- [x] Endpoint `GET /api/v1/companies/{id}/intelligence/?commodity=COAL` (juga GOLD, NICKEL, COPPER): tampilkan company/commodity observations yang memiliki raw log HTTP sukses; skor final tetap `null` dan status `pending_data_audit`.
- [x] Filter exact `entity_id` dan `metric_name` di `/api/v1/normalized-metrics/` untuk akses evidence yang tidak bergantung pada pencarian fuzzy.
- [ ] Tandai data demo vs data aktual secara eksplisit pada record/response sebelum dipakai untuk keputusan.
- [ ] Batasi akses raw payload dan pastikan credential/parameter sensitif tidak bocor.

Selesai bila UI dapat menunjukkan sumber, tanggal, nilai, unit, transformasi, confidence, dan proxy tanpa mengklaim skor tervalidasi. Endpoint awal belum mengaitkan setiap metrik company ke komoditas tertentu; dua daftar evidence sengaja dipisahkan.

## Tahap 2 — audit dan ingest aktual (blocker scoring)

- [ ] Untuk empat komoditas, uji endpoint Sectors dan sumber eksternal dari dictionary; catat coverage, earliest/latest, frequency, unit, missingness, biaya/rate limit, lisensi di audit. Jangan gunakan seed sebagai hasil audit. Sampel live pertama: China GDP Growth (World Bank, 2015–2025), tetapi lisensi/rate limit dan metric lain belum diaudit.
- [ ] Pilih metric MVP yang benar-benar tersedia; catat proxy dan alasan bila tidak tersedia.
- [x] Implementasikan ingest satu metric dari respons live: `python manage.py ingest_china_gdp` → raw log → validasi country/indicator → observasi annual `%` → `NormalizedMetric` dengan referensi raw; upsert idempotent. Audit parsial tercatat, belum `analytics_ready`.
- [ ] Tambahkan cek freshness, duplikasi, nilai hilang, dan perbedaan unit. Perluas per metric hanya setelah satu jalur terbukti.

Selesai bila observasi nyata dapat ditelusuri sampai response sumber dan audit mendukung klaim coverage-nya.

## Tahap 3 — company/commodity intelligence

- [x] Read path exposure per komoditas: hanya observasi ber-provenance dan terhubung ke komoditas; revenue share diprioritaskan, production/sales dependency diberi label proxy dan confidence analisis Low. Missing tetap `null`. `calculate_exposure_score` sekarang dijalankan di atas evidence/seed; skor diberi status "Pending Validation - preliminary methodology" dan fallback seed diberi label demo.
- [x] Read path resilience terpisah: komponen reserve coverage, leverage (DER), profitability (EBITDA Margin), dan diversification (Sales Diversification HHI) ditampilkan bila ada evidence; missing tetap `null`. `calculate_resilience_score` dijalankan secara parsial bila komponen tersedia; skor diberi status "Pending Validation - preliminary methodology (partial evidence)" atau `unavailable`, dan fallback seed diberi label demo.
- [x] Resilience response menyertakan `coverage_pct`, jumlah komponen tersedia/wajib, dan `missing_components`; score parsial tidak boleh ditampilkan tanpa coverage/status tersebut.
- [x] Driver map per commodity memakai metric supply/demand/macro dari dictionary dan hanya menampilkan observasi ber-provenance; kategori event/policy kualitatif. Semua `importance` null dan status hipotesis, bukan hasil korelasi seed.
- [x] Snapshot fundamental per perusahaan dari metric Revenue Growth, Net Income Growth, ROE, DER, PE, PB ber-provenance; missing `null`.
- [x] Peer rank kandidat memakai company universe per commodity dan hanya muncul bila ≥3 perusahaan punya metric, periode, frekuensi, unit, dan transformasi yang sama. Rank numerik bukan kualitas investasi; validitas peer group/data sumber masih perlu audit.

Selesai bila setiap insight memiliki input, periode, sumber, confidence, status proxy, dan alasan saat unavailable.

## Tahap 4 — quant validation dan skenario

- [x] Gate kesiapan quant per commodity memeriksa seri harga/driver ber-provenance, periode+frekuensi yang sama, minimal 12 pasangan, dan tanggal fetch driver tidak melewati periode target. Di DB lokal empat commodity berstatus `blocked`; ini belum membuktikan bebas look-ahead karena tanggal publikasi/vintage belum tersedia.
- [x] Correlation screening Pearson tersedia melalui `python manage.py screen_driver_correlations [--commodity CODE]`; membutuhkan minimal 12 pasangan bertanggal sama, frekuensi konsisten, unit non-kosong/konsisten, transformasi return/YoY yang diizinkan, dan non-zero variance. Data yang tidak memenuhi syarat menghapus score menjadi null/Low.
- [x] Coal price benchmark FRED/IMF (`PCOALAUUSDA`) di-ingest menjadi 33 annual returns (1993–2025); China GDP Growth diperluas menjadi 34 annual YoY observations (1992–2025). Coal/China GDP kini memiliki 33 aligned periods.
- [x] Screening menyimpan rolling 12-period correlations dan temporal 70/30 train/test correlation. Hubungan harus `|r| >= 0.1`, konsisten tanda pada ≥70% rolling windows, dan tidak berbalik arah di train/test untuk mendapat confidence Medium.
- [ ] Publication/vintage history belum tersedia; regression, regime checks, dan out-of-sample backtest terhadap baseline belum boleh diklaim selesai.
- [ ] Physical Indonesia coal production dan China coal imports masih blocked: belum ada endpoint/key yang terverifikasi pada environment ini.
- [ ] Hanya rilis driver importance/bobot numerik tervalidasi bila stabilitas dan cakupan memadai; nilai saat ini tetap preliminary.
- [x] Preview skenario deterministik (`POST /api/v1/commodities/{id}/scenario-preview/`) menghitung perubahan aritmetis satu driver teramati dari `metric_name` dan `shock_pct`; baseline/evidence/warning terlihat, dampak harga null. Tidak menyimpan scenario run.
- [x] `POST /api/v1/scenarios/{id}/run/` memvalidasi driver/evidence dan range shock serta menyimpan input/result. Correlation tidak diperlakukan sebagai coefficient; tanpa regression coefficient tervalidasi, `estimated_price_impact_pct` dan `estimated_new_price` selalu null.
- [x] P2 scenario safety: minimal 12 historical changes; shock dibatasi percentile 5–95; run metadata menyimpan model version, evidence/raw-log IDs, observation window, coefficient source, confidence, correlation context, dan coverage.
- [x] Provenance guard: `RawDataLog.data_origin` membedakan `live_api`, imported, derived, dan `seed_demo`. Seed company metrics direklasifikasi sebagai `Seed Demo`/Low confidence dan snapshot tidak boleh menerbitkannya sebagai `evidence_backed`.
- [x] Preview dan scenario run memakai distribusi perubahan historis relatif yang sama untuk guardrail P05–P95.
- [x] Status run eksplisit tersedia: `arithmetic_preview`, `preliminary_sensitivity`, `validated_sensitivity`. Engine saat ini hanya menerbitkan arithmetic preview dan membersihkan stale price impact/confidence interval saat rerun.
- [ ] Skenario sensitivitas production-ready baru boleh dijalankan setelah koefisien, volatilitas historis, unit, dan rentang input divalidasi.

Selesai bila metodologi, sampel, baseline, dan hasil uji bisa direproduksi. Bobot final dan forecast tidak termasuk tahap awal.
