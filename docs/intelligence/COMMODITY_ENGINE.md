# OreLens — Commodity Engine

## Tujuan

Jelaskan lingkungan setiap komoditas melalui supply, physical demand, structural demand, macro, dan event/policy. [Data Dictionary](../data/DATA_DICTIONARY.md) adalah daftar metric; dokumen ini menjelaskan bagaimana membacanya. Tidak ada bobot driver final pada v0.1.

| Commodity | Supply | Demand utama | Structural/macro |
|---|---|---|---|
| Coal | Produksi dan konsentrasi Indonesia/global | Impor China/India, konsumsi, listrik | Gas, energi terbarukan, USD, GDP |
| Gold | Produksi dan cadangan | Financial demand, central bank/investor flows | Real rate, Treasury yield, USD, inflasi, risiko geopolitik |
| Nickel | Produksi Indonesia/global, reserves | Impor China, industri, stainless steel | EV/battery demand dan chemistry |
| Copper | Produksi, reserves, inventory | Impor China, aktivitas manufaktur | Grid, EV, energi terbarukan |

## Cara kerja yang direncanakan

1. Ambil series aktual dan catat sumber, unit, frekuensi, periode, serta missing values.
2. Bedakan arah hubungan ekonomi yang dihipotesiskan dari hubungan yang teruji. Misalnya naiknya produksi *dapat* menekan harga, tetapi bukan kepastian.
3. Selaraskan frekuensi sebelum melakukan correlation/regression. Jangan menjadikan event/news sebagai score deterministik.
4. Sajikan driver dengan evidence dan confidence. Jika metric hanya proxy, tampilkan label proxy.
5. Turunkan driver importance dari pipeline di [Quant Methodology](QUANT_METHODOLOGY.md), bukan nilai contoh seed.

Model `CommodityDriver` saat ini menyimpan jenis, arah, confidence, dan correlation_score. Seed mengisi angka contoh. Belum ada engine perhitungan driver importance atau data historis yang diaudit.
