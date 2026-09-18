# OreLens — Quant Methodology v0.1

Status: rancangan penelitian. Belum ada hasil statistik atau bobot terkalibrasi.

## Pertanyaan

Driver mana yang mempunyai hubungan historis cukup stabil dengan komoditas dalam regime yang berbeda? Bagaimana exposure dan resilience perusahaan diukur tanpa mencampur ukuran mentah yang tidak sebanding?

## Pipeline

1. Kumpulkan observasi aktual dengan sumber, tanggal, unit, dan lisensi.
2. Audit coverage, missingness, dan perubahan definisi series.
3. Selaraskan frekuensi dan periode; cegah look-ahead dengan hanya memakai nilai yang tersedia pada waktu analisis.
4. Terapkan transformasi yang sesuai: return, YoY, z-score, log, HHI, atau peer percentile.
5. Lakukan correlation screening sebagai eksplorasi, bukan bukti kausal.
6. Jalankan multivariate regression; periksa hubungan antar-driver dan ukuran sampel.
7. Uji rolling windows serta perbedaan regime. Catat perubahan arah dan ketidakstabilan koefisien.
8. Backtest out-of-sample terhadap baseline sederhana, dengan pemisahan waktu yang jelas.
9. Baru turunkan driver importance dan confidence. Bila performa tidak memadai, tampilkan driver sebagai konteks tanpa bobot numerik.

## Derived metrics

`HHI = Σ share_i²`; `YoY = (current - previous) / previous`; `reserve coverage = reserves / annual production`. Commodity beta mengukur hubungan historis return perusahaan terhadap return komoditas. Semua butuh validasi unit, frekuensi, dan cakupan sebelum dihitung.

## Batas klaim

Tidak ada satu bobot universal yang ditetapkan sebelum audit. Hasil regresi dan beta menjelaskan sensitivitas historis, bukan prediksi harga saham. Angka `correlation_score` dan `resilience_score` dalam seed adalah contoh, bukan hasil pipeline ini.
