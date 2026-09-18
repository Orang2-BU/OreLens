# OreLens — API Architecture

## Alur data target

```text
Sectors / World Bank / FRED / UN Comtrade / EIA
    → fetch + raw response log
    → validation dan normalisasi
    → metric teramati + unit/periode/confidence/proxy
    → commodity/company intelligence
    → Django REST API
    → frontend
```

Urutan sumber dan metric mengikuti [Data Dictionary](DATA_DICTIONARY.md). Raw response harus ditautkan ke normalized observation; kegagalan fetch, status HTTP, dan waktu pembaruan perlu terlihat dalam audit. Cache boleh ditambahkan bila rate limit atau biaya nyata membutuhkannya; kebijakan TTL belum diputuskan.

## Sumber dan status

| Provider | Client di repo | Audit endpoint/coverage |
|---|---|---|
| Sectors | `integrations/clients/sectors.py` | Belum |
| World Bank | `worldbank.py` | Belum |
| FRED | `fred.py` | Belum |
| UN Comtrade | `un_comtrade.py` | Belum |
| EIA | `eia.py` | Belum |
| IEA/OECD/eksternal lain | Belum ada client | Belum |

Client saat ini membungkus request HTTP dan mencoba menyimpan `RawDataLog`. Belum ada job ingest, mapping metric per provider, normalizer, retry/caching, atau verifikasi response API. Credential provider hanya disimpan di backend. Sebelum raw log ditampilkan, parameter sensitif harus disaring dan endpoint perlu pembatasan akses.

## Kontrak backend → frontend yang tersedia

Base path: `/api/v1/`. Endpoint berikut berbentuk read-only dan mengembalikan detail object atau list berhalaman `{ count, next, previous, results }` (default 50).

| Resource | Endpoint | Filter yang tersedia |
|---|---|---|
| Commodity | `commodities/` | `category`, `is_active`; search code/name |
| Price | `commodity-prices/` | `commodity`, `source` |
| Driver | `commodity-drivers/` | `commodity`, `driver_type`, `impact_direction` |
| Company | `companies/` | `sector`, `sub_industry`, `country`, `exchange`; search ticker/name |
| Exposure | `company-exposures/` | `company`, `commodity` |
| Resilience | `company-resilience/` | Belum ada filter `company` |
| Normalized metric | `normalized-metrics/` | `entity_type`, `source`, `priority`, `confidence`, `is_proxy`; search metric/entity |
| Audit item | `data-audit/` | `available`, `source`, `proxy_required` |
| Scenario | `scenarios/` | `commodity`, `status`; detail memuat inputs/result |
| Scenario input/result | `scenario-inputs/`, `scenario-results/` | Input dapat difilter `scenario`; result belum |

`raw-data-logs/` juga ada, tetapi raw payload tidak menjadi kontrak UI publik sebelum sanitasi dan kontrol akses. Detail ID tersedia pada setiap resource. Schema aktual dapat dibuka di `/api/schema/`.

## Gap kontrak yang perlu diselesaikan

- Filter resilience per company dan exact `entity_id`/`metric_name` pada evidence sudah tersedia. Endpoint `companies/{id}/intelligence/?commodity=CODE` menampilkan evidence company dan commodity terpisah dengan status `pending_data_audit`; skor tetap `null` sampai audit dan validasi. Ini bukan klaim keterkaitan kausal antar-observasi.
- Driver map evidence-first tersedia di `commodities/{id}/intelligence/`; relasi persisted `CommodityDriver` ke normalized metric belum ada dan correlation seed tidak digunakan. Snapshot exposure di `companies/{id}/intelligence/?commodity=CODE` memakai `NormalizedMetric.commodity` dan hanya raw log HTTP 200. `commodities/{id}/quant-readiness/` menampilkan gate cakupan, sedangkan `POST commodities/{id}/scenario-preview/` hanya mengubah asumsi driver secara aritmetis; belum ada audit seluruh sumber atau skor/sensitivitas harga tervalidasi.
- Penanda data demo vs data aktual pada response.
- Endpoint submit/run scenario setelah metodologi dan validasi input disepakati.
- Aturan keamanan raw logs, auth, rate limit, dan cache. Semuanya belum dapat dianggap selesai hanya karena modelnya ada.

Untuk data availability aktual, lihat [audit](DATA_AVAILABILITY_AUDIT.md). Jangan isi angka coverage berdasarkan seed demo.
