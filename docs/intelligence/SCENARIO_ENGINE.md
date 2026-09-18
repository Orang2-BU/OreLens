# OreLens — Scenario Engine

## Tujuan

Pengguna mengubah asumsi driver komoditas dan melihat bagaimana analisis yang tervalidasi merespons. Scenario adalah analisis sensitivitas bersyarat, bukan prediksi harga saham.

## Input dan output

Input minimum: commodity, driver/metric, nilai awal, nilai penyesuaian, besar perubahan, unit, dan periode. Hanya driver yang punya definisi dan evidence boleh dijadikan input. Rentang nilai yang diperbolehkan harus disepakati berdasarkan data historis setelah audit.

Output yang ditargetkan: perubahan analisis, asumsi/metodologi, confidence, warning, dan evidence yang digunakan. Jika model belum tervalidasi, hasil diberi label preliminary atau tidak ditampilkan sebagai hasil numerik.

## Kondisi repo

Model `Scenario`, `ScenarioInput`, dan `ScenarioResult` beserta endpoint baca sudah ada. Field hasil saat ini berisi estimated price impact, estimated new price, confidence interval, methodology, dan warnings. Nilai seed hanyalah contoh; tidak ada endpoint untuk membuat/menjalankan scenario baru atau engine yang menghitung dampak dari input.

## Kriteria sebelum interaksi aktif

Data audit dan metodologi sensitivity tervalidasi, kontrak API input/output disepakati, validasi input tersedia, dan user dapat melihat sumber serta batasan hasil. UI mengikuti [UI Flow](../product/UI_FLOW.md).
