# Dokumentasi OreLens

OreLens menghubungkan lingkungan komoditas dengan exposure, resilience, fundamentals, evidence, dan scenario perusahaan tambang. Dokumen ini dibagi menurut kebutuhan tim. "Target" adalah keputusan produk/arsitektur; "tersedia" berarti ada implementasi di repo; "menunggu audit" berarti belum dibuktikan dengan data API nyata.

## Product

- [PRD](product/PRD.md) — tujuan, pengguna, alur, dan kriteria keberhasilan.
- [MVP Scope](product/MVP_SCOPE.md) — batas pekerjaan dan yang ditunda.
- [UI Flow](product/UI_FLOW.md) — halaman, navigasi, dan state.

## Data dan API

- [Data Dictionary](data/DATA_DICTIONARY.md) — naskah metric lengkap v0.1 dari Product/Quant.
- [Data Availability Audit](data/DATA_AVAILABILITY_AUDIT.md) — template; **hasil audit aktual belum tersedia**.
- [API Architecture](data/API_ARCHITECTURE.md) — sumber, alur data, kontrak API saat ini, dan gap.
- [Technical Architecture](data/TECHNICAL_ARCHITECTURE.md) — keputusan stack dan pembagian storage.

## Intelligence

- [Commodity Engine](intelligence/COMMODITY_ENGINE.md) — drivers per komoditas.
- [Company Engine](intelligence/COMPANY_ENGINE.md) — exposure, resilience, dan fundamentals.
- [Quant Methodology](intelligence/QUANT_METHODOLOGY.md) — riset historis sebelum weighting.
- [Scenario Engine](intelligence/SCENARIO_ENGINE.md) — input, output, dan batasan.

## Research dan submission

- [Research References](research/RESEARCH_REFERENCES.md) — register sumber yang masih perlu diverifikasi.
- [Hackathon Submission](research/HACKATHON_SUBMISSION.md) — checklist kerja; aturan resmi belum dilampirkan.

## Kondisi repo saat ini

Backend Django/DRF memiliki model, migration, endpoint baca, client sumber data dasar, dan seed demo. Frontend Next.js memiliki app shell FE-01, Commodity Overview FE-02, Commodity Driver Map FE-03, Company Comparison FE-04, Company Detail FE-05, dan Evidence View FE-06; scenario masih placeholder. Seed berisi nilai contoh, termasuk histori harga yang dibuat acak; nilainya bukan hasil audit. Scoring, pipeline normalisasi historis, dan scenario engine belum tervalidasi. PostgreSQL serta DuckDB/Parquet masih menjadi target lanjutan dari implementasi SQLite saat ini.
