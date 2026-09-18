# OreLens — Product Requirements

## Ringkasan

OreLens adalah workspace commodity dan company intelligence untuk Sectors Hackathon. Pengguna menelusuri driver komoditas, melihat hubungan dengan perusahaan, memeriksa exposure dan resilience, lalu membaca evidence dan scenario. Target pengguna MVP: analis, investor, atau juri yang ingin memahami hubungan tersebut; persona dan kebutuhan riset pengguna masih perlu divalidasi.

## Masalah dan tujuan

Data komoditas, operasi perusahaan, dan kondisi finansial tersebar di beberapa sumber. OreLens menyatukannya dalam alur yang bisa ditelusuri hingga metric, tanggal, unit, dan sumber. Keberhasilan MVP berarti pengguna dapat menyelesaikan alur ini untuk Coal, Gold, Nickel, dan Copper tanpa menganggap angka demo sebagai hasil riset.

## Alur utama

1. Pilih komoditas dan lihat harga serta konteks datanya.
2. Baca driver supply, demand, structural demand, macro, dan event/policy.
3. Lihat perusahaan terkait dan bandingkan exposure serta resilience dalam peer group komoditas yang sama.
4. Buka detail perusahaan dan telusuri evidence metric.
5. Eksplorasi scenario beserta asumsi, status metodologi, dan keterbatasannya.

## Fitur MVP

Commodity Overview, Commodity Driver Map, Company Comparison, Company Detail, Exposure/Resilience breakdown, Evidence View, dan Scenario UI. Rincian halaman ada di [UI Flow](UI_FLOW.md).

## Batasan produk

- Exposure dan resilience adalah dimensi berbeda. Perusahaan dapat memiliki keduanya tinggi.
- Metric hilang ditampilkan sebagai tidak tersedia, tidak diubah menjadi nol.
- Nilai demo diberi label demo; korelasi dan bobot awal tidak dipresentasikan sebagai hasil validasi.
- Scenario menjelaskan sensitivitas atas asumsi. OreLens tidak memberikan prediksi harga saham.
- Final scoring dan decision logic menunggu data audit dan backtest.

## Kriteria penerimaan

Pengguna dapat berpindah dari komoditas ke driver, perusahaan, evidence, dan scenario; setiap angka yang ditampilkan mempunyai unit, periode, sumber, serta status confidence bila tersedia. Halaman harus menangani loading, kosong, error, dan data yang belum tervalidasi.
