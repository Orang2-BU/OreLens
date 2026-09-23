# OreLens — UI Flow

## Alur utama

```text
Commodity Overview → Commodity Driver Map → Company Comparison
→ Company Detail / Exposure & Resilience → Evidence View → Scenario UI
```

Navigasi global tersedia di `/commodities`, `/companies`, `/evidence`, dan `/scenarios`. FE-02 sampai FE-05 mengimplementasikan alur commodity dan company; FE-06 mengimplementasikan Evidence View di `/evidence` dan deep link `/evidence?metric_id={id}`. Scenario masih placeholder.

| View | Tujuan dan isi minimum | Endpoint terkait |
|---|---|---|
| Commodity Overview | Empat komoditas; harga, unit, perubahan, tanggal data, status demo/aktual | `commodities/` |
| Commodity Driver Map | Driver supply/demand/structural/macro/event, arah, confidence, evidence; seri harga | `commodity-drivers/`, `commodity-prices/` |
| Company Comparison | Pilih peer group komoditas sama; lihat exposure, uncertainty-adjusted resilience, fundamentals ringkas, coverage, dan status evidence secara terpisah | `companies/`, `company-exposures/`, `companies/{id}/intelligence/` |
| Company Detail | Identitas, exposure per komoditas, score preliminary, fundamentals, breakdown resilience, missing data, dan evidence ID | `companies/{id}/`, `company-exposures/`, `companies/{id}/intelligence/` |
| Exposure/Resilience breakdown | Nilai, definisi, periode, unit, source, confidence; missing tetap missing | Endpoint exposure/resilience dan normalized metric |
| Evidence View | Filter metric/entity/confidence; jejak normalized metric → metadata raw source → availability audit; raw payload tidak dirender | `normalized-metrics/`, `raw-data-logs/`, `data-audit/` |
| Scenario UI | Input asumsi, perubahan, metodologi, result/warnings; status preliminary | `scenarios/` untuk membaca saja |

## State wajib

Semua view menampilkan loading, error dengan retry, kosong, dan unavailable secara berbeda. Nilai demo dan score pending validation harus diberi label dekat angka. Jangan memakai nol untuk missing. Grafik harga perlu urutan tanggal dan pagination yang benar.

## Batas interaksi saat ini

Backend belum menyediakan scenario run baru; form dapat dirancang, tetapi tombol menghitung hanya diaktifkan setelah endpoint dan metode tersedia. Evidence belum selalu dapat dilink langsung dari driver karena relasi metric belum ada. UX tidak boleh menampilkan hasil seed sebagai analisis terverifikasi.

## Kriteria selesai frontend MVP

Alur dari commodity ke driver, perusahaan, evidence, dan scenario dapat dinavigasi di desktop dan mobile; keyboard navigation jelas; setiap nilai punya konteks data; error tidak menyamar sebagai daftar kosong. FE-01 hanya menyelesaikan fondasi layout, navigasi, dan state component.
