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

Model saat ini menyimpan company, commodity exposure, dan resilience; endpoint baca tersedia. Seed memuat nilai exposure/resilience contoh dan `scoring_status = Pending Validation`. Belum ada perhitungan berbasis data audited atau company beta. Kontrak yang dibutuhkan frontend ada di [API Architecture](../data/API_ARCHITECTURE.md).
