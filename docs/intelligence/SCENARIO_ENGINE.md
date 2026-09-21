# OreLens — Scenario Engine

## Tujuan

Pengguna mengubah asumsi driver komoditas dan melihat bagaimana analisis yang tervalidasi merespons. Scenario adalah analisis sensitivitas bersyarat, bukan prediksi harga saham.

## Input dan output

Input minimum: commodity, driver/metric, nilai awal, nilai penyesuaian, besar perubahan, unit, dan periode. Hanya driver yang punya definisi dan evidence boleh dijadikan input. Rentang nilai yang diperbolehkan harus disepakati berdasarkan data historis setelah audit.

Output yang ditargetkan: perubahan analisis, asumsi/metodologi, confidence, warning, dan evidence yang digunakan. Jika model belum tervalidasi, hasil diberi label preliminary atau tidak ditampilkan sebagai hasil numerik.

## Kondisi repo

Model `Scenario`, `ScenarioInput`, dan `ScenarioResult` beserta endpoint baca sudah ada. Field hasil saat ini berisi estimated price impact, estimated new price, confidence interval, methodology, dan warnings. Nilai seed hanyalah contoh; tidak ada endpoint untuk membuat/menjalankan scenario baru atau engine yang menghitung dampak dari input.

`POST /api/v1/commodities/{id}/scenario-preview/` dengan JSON `{"metric_name":"China GDP Growth","shock_pct":10}` kini memberi preview aritmetis pada driver yang punya evidence: `adjusted_value = baseline × (1 + shock_pct/100)`. Respons selalu `estimated_price_impact_pct: null` dan tidak menyimpan run. Ini bukan sensitivitas harga, forecast, atau validasi model.

`POST /api/v1/scenarios/{id}/run/` menyimpan input dan result setelah memvalidasi driver yang diizinkan, evidence HTTP 200, dan shock -100% sampai 100%. Jika `CommodityDriver.correlation_score` tersedia, result memakai sensitivitas preliminary `correlation × shock`; jika belum, price impact disimpan sebagai 0 dengan methodology `Arithmetic preview` dan warning bahwa dampak harga tidak diestimasi. Semua output menyertakan referensi `NormalizedMetric` dan `RawDataLog` pada catatan input. Ini belum memakai beta, volatilitas historis, confidence interval, atau vintage-aware backtest.

## Kriteria sebelum interaksi aktif

Data audit dan metodologi sensitivity tervalidasi, kontrak API input/output disepakati, validasi input tersedia, dan user dapat melihat sumber serta batasan hasil. UI mengikuti [UI Flow](../product/UI_FLOW.md).
