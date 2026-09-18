# OreLens — Company Engine

## Tujuan

Hubungkan kondisi komoditas dengan operasi dan ketahanan perusahaan. Empat lapisan analisis: operations, exposure, resilience, fundamentals. Nilai per lapisan harus dapat dilacak ke [Data Dictionary](../data/DATA_DICTIONARY.md).

## Exposure

Exposure dihitung per komoditas, bukan satu skor generik untuk semua komoditas. Kandidat utama: revenue share, production dependency, sales dependency, geographic destination concentration, dan site concentration. Jika revenue share tidak tersedia, gunakan production/sales dependency dan classification dengan confidence yang lebih rendah; jangan gunakan nol.

## Resilience

Resilience berdiri sendiri dari exposure. Reserve coverage, stabilitas produksi, diversifikasi site/penjualan, profitability, leverage, license context, dan likuiditas menjadi kandidat. Reserve coverage bukan prediksi literal umur tambang.

## Fundamentals dan peers

Bandingkan revenue/growth, net income, ROE/margin, DER, PE/PB, serta data operasi hanya dalam peer group komoditas yang masuk akal. Peer percentile dipilih setelah coverage data aktual dipastikan. Tampilkan sumber, periode, dan confidence sebelum menyajikan skor gabungan.

## Status implementasi

Endpoint `companies/{id}/intelligence/?commodity=CODE` kini menyajikan snapshot evidence-first: exposure per komoditas (revenue share lalu proxy production/sales), komponen resilience, dan fundamental. `NormalizedMetric.commodity` membedakan metric perusahaan yang spesifik komoditas; metric umum boleh tanpa commodity. Hanya observasi dengan raw log HTTP 200 yang masuk snapshot. Nilai, unit, tanggal, sumber, confidence, proxy, dan evidence ID tampil; missing tetap null. Production/sales dependency adalah proxy ber-confidence analisis Low. Semua score gabungan tetap null. Seed pada model legacy masih contoh dan tidak digunakan snapshot. Driver map berbasis data aktual, peer comparison, beta, serta bobot tervalidasi belum ada.
