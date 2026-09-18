# OreLens — MVP Scope

## Masuk MVP

- Empat komoditas: Coal, Gold, Nickel, Copper.
- Backend Django/DRF, schema normalized metric, raw data provenance, dan client Sectors, World Bank, FRED, UN Comtrade, EIA.
- Audit ketersediaan data aktual untuk metric prioritas [Data Dictionary](../data/DATA_DICTIONARY.md).
- Tujuh view dalam [UI Flow](UI_FLOW.md), awalnya boleh memakai demo/mock data yang diberi label.
- Exposure dan resilience ditampilkan terpisah dengan confidence dan evidence.
- Scenario eksploratif dengan input yang jelas dan hasil yang berstatus preliminary selama model belum tervalidasi.

## Dapat berjalan paralel

Frontend dapat membangun view dengan mock data sambil backend mengambil sample API nyata dan mengisi audit. API yang dapat dibaca sekarang tercatat di [API Architecture](../data/API_ARCHITECTURE.md).

## Ditunda sampai data historis memadai

Correlation screening, regression, rolling analysis, regime comparison, historical weighting, backtest, final scoring weights, dan final decision logic. Gap Phase 2 seperti commodity beta, inventory, dan detailed policy events tidak memblokir MVP.

## Implementasi saat ini

- Ada: model dan endpoint baca Django, admin, client dasar, command seed demo, fondasi frontend React/Vite (FE-01).
- Belum ada: frontend view analisis, ingest dan normalisasi data nyata yang teruji, audit aktual, quant pipeline, serta perhitungan scenario baru.
- Target arsitektur PostgreSQL, DuckDB/Parquet, dan Next.js/TypeScript belum diimplementasikan. SQLite dan React/Vite dipakai sekarang; migrasi tidak menjadi prasyarat untuk validasi MVP.
